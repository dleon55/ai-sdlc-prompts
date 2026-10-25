import { test } from "node:test";
import assert from "node:assert/strict";
import { direccionDeEscucha } from "../src/escucha.ts";

test("sin HOST escucha solo en loopback", () => {
  assert.equal(direccionDeEscucha({}), "127.0.0.1");
});

test("HOST vacio o con espacios cuenta como ausente", () => {
  assert.equal(direccionDeEscucha({ HOST: "" }), "127.0.0.1");
  assert.equal(direccionDeEscucha({ HOST: "  " }), "127.0.0.1");
});

test("HOST explicito se respeta", () => {
  assert.equal(direccionDeEscucha({ HOST: "0.0.0.0" }), "0.0.0.0");
  assert.equal(direccionDeEscucha({ HOST: "::1" }), "::1");
});
