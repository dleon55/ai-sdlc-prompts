import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import { createServer } from "../src/server.js";
import { getAllPromptIds, getPrompt } from "../src/dataStore.js";

async function connectedClient() {
  const server = createServer();
  const client = new Client({ name: "test-client", version: "1.0.0" });
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await Promise.all([client.connect(clientTransport), server.connect(serverTransport)]);
  return { client, server };
}

function parseToolResult(result) {
  return JSON.parse(result.content[0].text);
}

test("lists the 5 registered tools", async () => {
  const { client } = await connectedClient();
  const { tools } = await client.listTools();
  const names = tools.map((t) => t.name).sort();
  assert.deepEqual(names, [
    "get_framework",
    "get_prompt",
    "list_prompts",
    "recommend_next",
    "resolve_prompt",
  ]);
});

test("list_prompts filters by section over MCP", async () => {
  const { client } = await connectedClient();
  const result = await client.callTool({ name: "list_prompts", arguments: { section: "17" } });
  const data = parseToolResult(result);
  const expectedCount = getAllPromptIds().filter((id) => getPrompt(id).section === "17").length;
  assert.equal(data.count, expectedCount);
  assert.ok(data.prompts.every((p) => p.section === "17"));
});

test("get_prompt returns template text in the requested language", async () => {
  const { client } = await connectedClient();
  const result = await client.callTool({
    name: "get_prompt",
    arguments: { id: "11-10-capacity-planning", lang: "en" },
  });
  const data = parseToolResult(result);
  assert.equal(data.id, "11-10-capacity-planning");
  assert.ok(data.template.toLowerCase().includes("objective"));
});

test("get_prompt reports an error for an unknown id", async () => {
  const { client } = await connectedClient();
  const result = await client.callTool({ name: "get_prompt", arguments: { id: "no-existe" } });
  assert.equal(result.isError, true);
});

test("resolve_prompt substitutes variables and prepends the framework by default", async () => {
  const { client } = await connectedClient();
  const result = await client.callTool({
    name: "resolve_prompt",
    arguments: {
      id: "00-C-01-issue-para-agente-ia",
      variables: { repositorio: "org/support-repo" },
    },
  });
  const data = parseToolResult(result);
  assert.ok(data.text.includes("org/support-repo"));
  assert.ok(data.text.includes("---"), "framework preamble should be prepended by default");
});

test("resolve_prompt can skip the framework preamble", async () => {
  const { client } = await connectedClient();
  const result = await client.callTool({
    name: "resolve_prompt",
    arguments: { id: "00-C-01-issue-para-agente-ia", prepend_framework: false },
  });
  const data = parseToolResult(result);
  assert.ok(!data.text.startsWith("Actúa como"), "should not include the framework preamble text");
});

test("get_framework returns the mandatory preamble", async () => {
  const { client } = await connectedClient();
  const result = await client.callTool({ name: "get_framework", arguments: {} });
  const data = parseToolResult(result);
  assert.ok(data.text.includes("Principal Software Engineer"));
});

test("recommend_next resolves ids to full summaries", async () => {
  const { client } = await connectedClient();
  const result = await client.callTool({
    name: "recommend_next",
    arguments: { id: "00-C-01-issue-para-agente-ia" },
  });
  const data = parseToolResult(result);
  assert.ok(data.recommended_next.some((p) => p.id === "00-C-02-plan-mode-multiagente"));
});
