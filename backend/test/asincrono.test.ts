// Express 4 no atrapa los rechazos de un manejador `async`: sin
// src/asincrono.ts, un fallo de base de datos terminaba el proceso. Estas
// pruebas fijan el comportamiento corregido y vigilan que ninguna ruta
// nueva se registre sin envolver.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import type { AddressInfo } from "node:net";
import express from "express";
import { asincrono, manejadorDeErrores } from "../src/asincrono.ts";

async function servir(app: express.Express): Promise<{ url: string; cerrar: () => Promise<void> }> {
  const server = app.listen(0, "127.0.0.1");
  await new Promise<void>((resolve) => server.once("listening", () => resolve()));
  const { port } = server.address() as AddressInfo;
  return {
    url: `http://127.0.0.1:${port}`,
    cerrar: () => new Promise<void>((resolve) => server.close(() => resolve())),
  };
}

test("un rechazo en un manejador responde 500 y el servidor sigue vivo", async () => {
  const sinManejar: unknown[] = [];
  const alRechazo = (razon: unknown) => sinManejar.push(razon);
  process.on("unhandledRejection", alRechazo);

  const app = express();
  app.get("/falla", asincrono(async () => {
    throw new Error("la base de datos no responde");
  }));
  app.get("/ok", (_req, res) => {
    res.json({ ok: true });
  });
  app.use(manejadorDeErrores);
  const { url, cerrar } = await servir(app);
  try {
    const r = await fetch(`${url}/falla`);
    assert.equal(r.status, 500);
    assert.deepEqual(await r.json(), { error: "Error interno" });

    const r2 = await fetch(`${url}/ok`);
    assert.equal(r2.status, 200);
    assert.deepEqual(sinManejar, []);
  } finally {
    await cerrar();
    process.off("unhandledRejection", alRechazo);
  }
});

test("si la respuesta ya empezo, se delega en Express sin intentar otro 500", async () => {
  const app = express();
  app.get("/a-medias", asincrono(async (_req, res) => {
    res.status(200).write("parcial");
    throw new Error("fallo a mitad de la respuesta");
  }));
  app.use(manejadorDeErrores);
  const { url, cerrar } = await servir(app);
  try {
    const r = await fetch(`${url}/a-medias`);
    assert.equal(r.status, 200);
    await r.text().catch(() => undefined);
  } finally {
    await cerrar();
  }
});

test("ruta real: /api/health con la base caida responde 500 y no tumba el proceso", async () => {
  // Puerto 1 en loopback: nada escucha ahi, la consulta falla con ECONNREFUSED.
  // node --test corre cada archivo en su propio proceso, asi que esto no
  // afecta a las pruebas de integracion.
  process.env.DATABASE_URL = "postgres://nadie:nada@127.0.0.1:1/inexistente";
  const { publicRouter } = await import("../src/routes/public.ts");
  const { pool } = await import("../src/db.ts");

  const app = express();
  app.use("/api", publicRouter);
  app.use(manejadorDeErrores);
  const { url, cerrar } = await servir(app);
  try {
    const r = await fetch(`${url}/api/health`);
    assert.equal(r.status, 500);
    const r2 = await fetch(`${url}/api/founding/spots-left`);
    assert.equal(r2.status, 500, "el proceso sigue atendiendo despues del primer fallo");
  } finally {
    await cerrar();
    await pool.end();
  }
});

test("toda ruta o middleware async del backend esta envuelto con asincrono()", () => {
  const raiz = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "src");
  const archivos: string[] = [];
  const recorrer = (dir: string) => {
    for (const nombre of readdirSync(dir)) {
      const ruta = path.join(dir, nombre);
      if (statSync(ruta).isDirectory()) recorrer(ruta);
      else if (ruta.endsWith(".ts")) archivos.push(ruta);
    }
  };
  recorrer(raiz);

  const registro = /\b\w+\.(get|post|put|patch|delete|use|all)\(/;
  const problemas: string[] = [];
  for (const archivo of archivos) {
    readFileSync(archivo, "utf8").split("\n").forEach((linea, i) => {
      const donde = `${path.relative(raiz, archivo)}:${i + 1}`;
      if (registro.test(linea) && /\basync\b/.test(linea) && !/asincrono\(async\b/.test(linea)) {
        problemas.push(`${donde}: ${linea.trim()}`);
      }
      // Un middleware (req, res, next) exportado como `async function` tambien
      // rechazaria sin manejar; las funciones auxiliares como readSession no cuentan.
      if (archivo.includes(`${path.sep}auth${path.sep}`) && /^export async function \w+\([^)]*\bnext\b/.test(linea)) {
        problemas.push(`${donde}: ${linea.trim()}`);
      }
    });
  }
  assert.deepEqual(problemas, [], `Registrar con asincrono(async (req, res) => ...):\n${problemas.join("\n")}`);
});
