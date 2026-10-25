import test from "node:test";
import assert from "node:assert/strict";
import { rutaDeVuelta } from "../src/auth/volver.ts";

test("acepta rutas relativas del propio sitio", () => {
  for (const ruta of ["/", "/precios.html", "/app", "/precios.html?plan=anual", "/a/b-c_d.e~f"]) {
    assert.equal(rutaDeVuelta(ruta), ruta);
  }
});

test("rechaza todo lo que lleve a otro dominio o no sea texto", () => {
  const malas: unknown[] = [
    "https://malicioso.example", "//malicioso.example", "/\\malicioso.example", "\\\\malicioso.example",
    "javascript:alert(1)", "precios.html", "", " /precios.html", "/precios\nhtml", "/" + "a".repeat(250),
    undefined, null, 42, ["/precios.html"],
  ];
  for (const valor of malas) assert.equal(rutaDeVuelta(valor), "/", String(valor));
});

test("/api/auth/login guarda state y vuelta segura; el callback exige el state", async () => {
  process.env.GITHUB_OAUTH_CLIENT_ID = "id-de-prueba";
  process.env.GITHUB_OAUTH_CLIENT_SECRET = "secreto-de-prueba";
  process.env.PUBLIC_BASE_URL = "https://sitio.example";
  const express = (await import("express")).default;
  const { authRouter } = await import("../src/routes/auth.ts");
  const { manejadorDeErrores } = await import("../src/asincrono.ts");
  const app = express();
  app.use("/api/auth", authRouter);
  app.use(manejadorDeErrores);
  const server = app.listen(0, "127.0.0.1");
  await new Promise<void>((r) => server.once("listening", () => r()));
  const base = `http://127.0.0.1:${(server.address() as import("node:net").AddressInfo).port}/api/auth`;
  try {
    const r = await fetch(`${base}/login?volver=/precios.html`, { redirect: "manual" });
    assert.equal(r.status, 302);
    assert.match(r.headers.get("location") ?? "", /^https:\/\/github\.com\/login\/oauth\/authorize\?/);
    const cookies = r.headers.getSetCookie();
    assert.ok(cookies.some((c) => /^ai_sdlc_oauth_state=[0-9a-f]{48};.*HttpOnly/i.test(c)));
    assert.ok(cookies.some((c) => c.startsWith("ai_sdlc_oauth_volver=%2Fprecios.html;")));

    const mala = await fetch(`${base}/login?volver=https://malicioso.example`, { redirect: "manual" });
    assert.ok(mala.headers.getSetCookie().some((c) => c.startsWith("ai_sdlc_oauth_volver=%2F;")));

    const sinState = await fetch(`${base}/callback?code=x&state=y`, { redirect: "manual" });
    assert.equal(sinState.status, 401);
  } finally {
    await new Promise<void>((r) => server.close(() => r()));
  }
});
