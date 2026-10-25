// Fase 2: el backend acepta el access_token de Supabase. Estas pruebas
// firman tokens con una clave ES256 propia (la misma forma que Supabase)
// y comprueban que solo se acepta el token correcto: emisor, audiencia,
// algoritmo, rol e identidad de GitHub.
import test from "node:test";
import assert from "node:assert/strict";
import type { AddressInfo } from "node:net";
import { SignJWT, createLocalJWKSet, exportJWK, generateKeyPair } from "jose";
import express from "express";
import { usarClavesDePrueba, verificarTokenSupabase } from "../src/auth/supabase.ts";

const ISS = "https://proyecto-de-prueba.supabase.co/auth/v1";
const { privateKey, publicKey } = await generateKeyPair("ES256");
const jwk = { ...(await exportJWK(publicKey)), kid: "clave-prueba", alg: "ES256", use: "sig" };
usarClavesDePrueba(createLocalJWKSet({ keys: [jwk] }), ISS);

const USER_ID = "33333333-3333-3333-3333-333333333333";

async function firmar(opciones: {
  iss?: string; aud?: string; role?: string; exp?: string; clave?: CryptoKey; meta?: Record<string, unknown>; sub?: string;
} = {}): Promise<string> {
  return new SignJWT({
    role: opciones.role ?? "authenticated",
    email: "persona@example.com",
    user_metadata: opciones.meta ?? { provider_id: "424242", user_name: "persona-github" },
  })
    .setProtectedHeader({ alg: "ES256", kid: "clave-prueba" })
    .setSubject(opciones.sub ?? USER_ID)
    .setIssuer(opciones.iss ?? ISS)
    .setAudience(opciones.aud ?? "authenticated")
    .setIssuedAt()
    .setExpirationTime(opciones.exp ?? "1h")
    .sign(opciones.clave ?? privateKey);
}

test("acepta un access_token valido y devuelve la identidad de GitHub", async () => {
  assert.deepEqual(await verificarTokenSupabase(await firmar()), {
    userId: USER_ID,
    githubId: "424242",
    githubLogin: "persona-github",
    email: "persona@example.com",
  });
});

test("rechaza tokens que no son del proyecto, vencidos o sin identidad de GitHub", async () => {
  const otra = (await generateKeyPair("ES256")).privateKey;
  const casos: Array<[string, Promise<string>]> = [
    ["firmado con otra clave", firmar({ clave: otra })],
    ["otro emisor", firmar({ iss: "https://otro.supabase.co/auth/v1" })],
    ["otra audiencia", firmar({ aud: "anon" })],
    ["rol anonimo", firmar({ role: "anon" })],
    ["vencido", firmar({ exp: "-1m" })],
    ["sin provider_id", firmar({ meta: { user_name: "x" } })],
    ["sin login", firmar({ meta: { provider_id: "1" } })],
  ];
  for (const [nombre, token] of casos) {
    assert.equal(await verificarTokenSupabase(await token), null, nombre);
  }
  assert.equal(await verificarTokenSupabase("no-es-un-jwt"), null, "basura");
  // HS256 con cualquier secreto: el algoritmo esta fijado a ES256.
  const hs = await new SignJWT({ role: "authenticated", user_metadata: { provider_id: "1", user_name: "x" } })
    .setProtectedHeader({ alg: "HS256" }).setSubject(USER_ID).setIssuer(ISS).setAudience("authenticated")
    .setExpirationTime("1h").sign(new TextEncoder().encode("secreto-cualquiera-de-32-bytes!!"));
  assert.equal(await verificarTokenSupabase(hs), null, "HS256");
});

test("con base: el Bearer de Supabase crea la fila en users y autoriza /api/projects", { skip: !process.env.DATABASE_URL }, async () => {
  const { pool } = await import("../src/db.ts");
  const { projectsRouter } = await import("../src/routes/projects.ts");
  const { manejadorDeErrores } = await import("../src/asincrono.ts");
  const { aplicarEsquema } = await import("./esquema.ts");
  await aplicarEsquema(pool);
  const sub = "44444444-4444-4444-4444-444444444444";
  await pool.query("delete from users where id = $1 or github_id = $2", [sub, "515151"]);

  const app = express();
  app.use(express.json());
  app.use("/api/projects", projectsRouter);
  app.use(manejadorDeErrores);
  const server = app.listen(0, "127.0.0.1");
  await new Promise<void>((r) => server.once("listening", () => r()));
  const url = `http://127.0.0.1:${(server.address() as AddressInfo).port}/api/projects`;
  try {
    const token = await firmar({ sub, meta: { provider_id: "515151", user_name: "nueva-en-supabase" } });

    const sinToken = await fetch(url);
    assert.equal(sinToken.status, 401);

    const r = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
    assert.equal(r.status, 200);
    assert.deepEqual(await r.json(), { data: [] });

    const { rows } = await pool.query("select github_id, github_login from users where id = $1", [sub]);
    assert.deepEqual(rows, [{ github_id: "515151", github_login: "nueva-en-supabase" }]);

    const crear = await fetch(url, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({ rows: [{ name: "Proyecto F2", isDefault: true, vars: { a: 1 } }] }),
    });
    assert.equal(crear.status, 200);
    const { data } = await crear.json() as { data: Array<{ name: string; is_default: boolean }> };
    assert.equal(data[0]!.name, "Proyecto F2");
    assert.equal(data[0]!.is_default, true);
  } finally {
    await new Promise<void>((r) => server.close(() => r()));
    await pool.query("delete from users where id = $1", [sub]);
    await pool.end();
  }
});
