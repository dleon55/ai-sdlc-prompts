import { test } from "node:test";
import assert from "node:assert/strict";
import { listPrompts, getPrompt, getFramework, getTokenRegistry, getAllPromptIds } from "../src/dataStore.js";

test("getAllPromptIds returns the full catalog", () => {
  const ids = getAllPromptIds();
  assert.ok(ids.length >= 92, `expected at least 92 prompts, got ${ids.length}`);
  assert.ok(new Set(ids).size === ids.length, "ids must be unique");
});

test("getPrompt returns full detail for a known id", () => {
  const p = getPrompt("00-C-01-issue-para-agente-ia");
  assert.ok(p, "prompt should exist");
  assert.equal(p.section, "00");
  assert.ok(p.template.es.includes("Objetivo:"));
  assert.ok(p.recommended_next_prompt_ids.includes("00-C-02-plan-mode-multiagente"));
});

test("getPrompt returns null for unknown id", () => {
  assert.equal(getPrompt("no-existe-este-id"), null);
});

test("listPrompts filters by section", () => {
  const results = listPrompts({ section: "16" });
  assert.equal(results.length, 5);
  assert.ok(results.every((p) => p.section === "16"));
});

test("listPrompts filters by risk tag", () => {
  const results = listPrompts({ risk: "high" });
  assert.ok(results.length > 0);
  assert.ok(results.every((p) => (p.contract?.es?.expected_risk_tags || []).includes("high")));
});

test("listPrompts filters by autonomy tag", () => {
  const results = listPrompts({ autonomy: "A3" });
  assert.ok(results.length > 0);
  assert.ok(results.every((p) => (p.contract?.es?.permitted_autonomy_tags || []).includes("A3")));
});

test("listPrompts filters by free-text query", () => {
  const results = listPrompts({ query: "capacity planning" });
  assert.ok(results.some((p) => p.id === "11-10-capacity-planning"));
});

test("getFramework returns bilingual preamble", () => {
  const fw = getFramework();
  assert.ok(fw.preamble.es.length > 100);
  assert.ok(fw.preamble.en.length > 100);
});

test("getTokenRegistry has expected shape", () => {
  const registry = getTokenRegistry();
  assert.ok(registry.repositorio);
  assert.equal(registry.repositorio.required, true);
  assert.equal(registry.repositorio.scope, "project");
  assert.ok(Array.isArray(registry.repositorio.aliases));
  assert.ok(registry.repositorio.aliases.length > 0);
});
