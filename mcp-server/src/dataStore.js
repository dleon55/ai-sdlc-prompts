import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_FILE = path.join(__dirname, "..", "data", "prompts-full.json");

let cached = null;

// prompts-full.json es generado por build.py (python build.py, repo raíz) --
// no se edita a mano. Se cachea en memoria porque el proceso del servidor
// MCP vive mientras dura la sesión del cliente (stdio), no por request.
function loadData() {
  if (cached) return cached;
  const raw = readFileSync(DATA_FILE, "utf-8");
  cached = JSON.parse(raw);
  return cached;
}

export function getFramework() {
  return loadData().framework;
}

export function getTokenRegistry() {
  return loadData().token_registry;
}

export function listPrompts({ section, risk, autonomy, query } = {}) {
  const data = loadData();
  const q = (query || "").toLowerCase().trim();
  return data.prompts.filter((p) => {
    if (section && p.section !== section) return false;
    if (risk) {
      const tags = p.contract?.es?.expected_risk_tags || [];
      if (!tags.includes(risk)) return false;
    }
    if (autonomy) {
      const tags = p.contract?.es?.permitted_autonomy_tags || [];
      if (!tags.includes(autonomy)) return false;
    }
    if (q) {
      const haystack = [
        p.title?.es, p.title?.en,
        p.description?.es, p.description?.en,
      ].filter(Boolean).join(" ").toLowerCase();
      if (!haystack.includes(q)) return false;
    }
    return true;
  });
}

export function getPrompt(id) {
  const data = loadData();
  return data.prompts.find((p) => p.id === id) || null;
}

export function getAllPromptIds() {
  return loadData().prompts.map((p) => p.id);
}
