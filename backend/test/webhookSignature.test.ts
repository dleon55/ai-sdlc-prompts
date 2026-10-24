// Prueba la verificacion de firma HMAC del webhook de Paddle de forma
// aislada (sin servidor HTTP ni base de datos) -- el mismo calculo que
// hoy hace que un POST falso sin la firma correcta no pueda
// auto-otorgarse acceso pagado.
import test from "node:test";
import assert from "node:assert/strict";
import { hmacHex, timingSafeEqual } from "../src/routes/webhooks/paddle.ts";

test("hmacHex es determinista para el mismo secreto y mensaje", async () => {
  const a = await hmacHex("secreto", "123:{}");
  const b = await hmacHex("secreto", "123:{}");
  assert.equal(a, b);
});

test("hmacHex cambia si el mensaje cambia", async () => {
  const a = await hmacHex("secreto", "123:{}");
  const b = await hmacHex("secreto", "124:{}");
  assert.notEqual(a, b);
});

test("timingSafeEqual compara correctamente", () => {
  assert.equal(timingSafeEqual("abc", "abc"), true);
  assert.equal(timingSafeEqual("abc", "abd"), false);
  assert.equal(timingSafeEqual("abc", "ab"), false);
});
