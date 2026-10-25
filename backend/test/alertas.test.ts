// Mismo comportamiento que tests/js/test_alertas_runtime.js (raiz del
// repo) pero corrido con el test runner nativo de Node sobre la copia de
// alertas.ts que vive en el backend -- confirma que portar el archivo sin
// cambios de logica no rompio nada.
import test from "node:test";
import assert from "node:assert/strict";
import { crearAlertador, limpiarDetalle } from "../src/routes/webhooks/alertas.ts";

test("limpiarDetalle filtra claves que parecen secretos", () => {
  const limpio = limpiarDetalle({
    event_id: "evt_1",
    paddle_webhook_secret: "shhh",
    Authorization: "Bearer x",
    status: "active",
  });
  assert.deepEqual(limpio, { event_id: "evt_1", status: "active" });
});

test("limpiarDetalle trunca valores largos", () => {
  const limpio = limpiarDetalle({ mensaje: "a".repeat(600) });
  assert.equal((limpio.mensaje as string).length, 501);
  assert.ok((limpio.mensaje as string).endsWith("…"));
});

test("alertar() sin webhookUrl solo loguea", async () => {
  const logs: unknown[] = [];
  const alertar = crearAlertador({ log: (msg, datos) => logs.push({ msg, datos }) });
  const resultado = await alertar({ clave: "webhook_error", detalle: { event_id: "evt_1" } });
  assert.equal(resultado, "solo_log");
  assert.equal(logs.length, 1);
});

test("alertar() deduplica la misma clave+id dentro de 1 hora", async () => {
  let ahora = 1000;
  const alertar = crearAlertador({ ahora: () => ahora, log: () => {} });
  const r1 = await alertar({ clave: "reembolso", detalle: { event_id: "evt_x" } });
  const r2 = await alertar({ clave: "reembolso", detalle: { event_id: "evt_x" } });
  assert.equal(r1, "solo_log");
  assert.equal(r2, "deduplicada");

  ahora += 60 * 60 * 1000 + 1;
  const r3 = await alertar({ clave: "reembolso", detalle: { event_id: "evt_x" } });
  assert.equal(r3, "solo_log");
});

test("alertar() nunca lanza aunque el detalle sea raro", async () => {
  const alertar = crearAlertador({ log: () => {} });
  const resultado = await alertar({ clave: "webhook_error", detalle: {} as never });
  assert.equal(resultado, "solo_log");
});

test("alertar() con webhookUrl manda POST y reporta 'enviada'", async () => {
  const llamadas: unknown[] = [];
  const fetchImpl = (async (_url: string, opts: RequestInit) => {
    llamadas.push(JSON.parse(opts.body as string));
    return new Response(null, { status: 200 });
  }) as typeof fetch;
  const alertar = crearAlertador({ webhookUrl: "https://hooks.example.com/x", fetchImpl, log: () => {} });
  const resultado = await alertar({ clave: "reembolso", detalle: { event_id: "evt_2" } });
  assert.equal(resultado, "enviada");
  assert.equal(llamadas.length, 1);
});
