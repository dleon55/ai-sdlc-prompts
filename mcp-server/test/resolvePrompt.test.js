import { test } from "node:test";
import assert from "node:assert/strict";
import { resolvePrompt, parseAdditionalVars, findUnresolvedPlaceholders } from "../src/resolvePrompt.js";

const REGISTRY = {
  repositorio: { required: true, scope: "project", aliases: ["NOMBRE O URL", "REPO"] },
  rama_actual: { required: false, scope: "task", aliases: ["RAMA ACTUAL"] },
};

test("resolvePrompt substitutes a known alias", () => {
  const result = resolvePrompt("repo: [NOMBRE O URL]", REGISTRY, { repositorio: "org/repo" });
  assert.equal(result.text, "repo: org/repo");
  assert.deepEqual(result.unresolvedRequired, []);
});

test("resolvePrompt substitutes {{ALIAS}} tokens too", () => {
  const result = resolvePrompt("repo: {{REPO}}", REGISTRY, { repositorio: "org/repo" });
  assert.equal(result.text, "repo: org/repo");
});

test("resolvePrompt flags an unresolved required placeholder", () => {
  const result = resolvePrompt("repo: [NOMBRE O URL], rama: [RAMA ACTUAL]", REGISTRY, {});
  assert.ok(result.unresolvedRequired.includes("NOMBRE O URL"));
  assert.ok(result.unresolvedOptional.includes("RAMA ACTUAL"));
});

test("resolvePrompt ignores empty/whitespace-only values", () => {
  const result = resolvePrompt("repo: [NOMBRE O URL]", REGISTRY, { repositorio: "   " });
  assert.equal(result.text, "repo: [NOMBRE O URL]");
  assert.ok(result.unresolvedRequired.includes("NOMBRE O URL"));
});

test("resolvePrompt applies TOKEN=valor lines from 'adicionales'", () => {
  const result = resolvePrompt("custom: [MI TOKEN]", REGISTRY, { adicionales: "MI TOKEN=hola mundo" });
  assert.equal(result.text, "custom: hola mundo");
});

test("parseAdditionalVars parses multiple lines and skips malformed ones", () => {
  const parsed = parseAdditionalVars("A=1\nsin-igual\nB = 2 \n=huerfano");
  assert.deepEqual(parsed, { A: "1", B: "2" });
});

test("findUnresolvedPlaceholders ignores format placeholders like YYYYMMDD", () => {
  const found = findUnresolvedPlaceholders("fecha: [YYYYMMDD], repo: [NOMBRE O URL]", REGISTRY);
  assert.ok(!found.includes("YYYYMMDD"));
  assert.ok(found.includes("NOMBRE O URL"));
});
