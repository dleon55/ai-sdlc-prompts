// Réplica server-side de resolvePrompt()/TOKEN_REGISTRY del sitio
// (build.py, funciones resolvePrompt/getTokenField/replaceToken/
// parseAdditionalVars/findUnresolvedPlaceholders) -- misma semántica de
// sustitución de placeholders [ALIAS]/{{ALIAS}}, para que un agente que
// use resolve_prompt obtenga exactamente el mismo texto que copiaría un
// humano desde el navegador con las mismas variables.

// Debe reflejar el mismo set que build.py/extract_vars.py: placeholders de
// formato, no campos a llenar desde variables de proyecto.
const PLACEHOLDER_IGNORE = [
  "N", "X", "Y", "Z", "ADR-NNN", "NNN", "YYYYMMDD",
  "SÍ / NO", "SÍ/NO", "YES / NO", "YES/NO",
];

function escapeRegExp(token) {
  return token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function replaceToken(text, token, value) {
  const escaped = escapeRegExp(token);
  text = text.replace(new RegExp("\\[" + escaped + "\\]", "g"), () => value);
  return text.replace(new RegExp("\\{\\{" + escaped + "\\}\\}", "g"), () => value);
}

function getTokenField(token, registry) {
  for (const field of Object.keys(registry)) {
    if (registry[field].aliases.includes(token)) return field;
  }
  return null;
}

export function parseAdditionalVars(raw) {
  const result = {};
  (raw || "").split(/\r?\n/).forEach((line) => {
    const idx = line.indexOf("=");
    if (idx < 1) return;
    const token = line.slice(0, idx).trim().replace(/^\[|\]$/g, "").replace(/^\{\{|\}\}$/g, "");
    const value = line.slice(idx + 1).trim();
    if (token && value) result[token] = value;
  });
  return result;
}

export function findUnresolvedPlaceholders(text, registry) {
  const found = [];
  const rx = /\[([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ0-9_ /.,#()-]{1,80})\]|\{\{([A-Z][A-Z0-9_]{1,60})\}\}/g;
  let match;
  while ((match = rx.exec(text)) !== null) {
    const token = (match[1] || match[2] || "").trim();
    if (!PLACEHOLDER_IGNORE.includes(token) && !found.includes(token)) found.push(token);
  }
  // Alias registrados que empiezan en minúscula (p.ej. "[ej. Python + ...]")
  // no los captura el regex, que exige mayúscula inicial -- buscarlos
  // explícitamente para no dejar placeholders sin aviso.
  Object.keys(registry).forEach((field) => {
    (registry[field].aliases || []).forEach((alias) => {
      if (/^[A-ZÁÉÍÓÚÑ]/.test(alias)) return;
      if (found.includes(alias)) return;
      if (text.includes("[" + alias + "]") || text.includes("{{" + alias + "}}")) {
        found.push(alias);
      }
    });
  });
  return found;
}

/**
 * @param {string} template - texto crudo del prompt (o del framework), con placeholders intactos
 * @param {object} registry - token_registry de prompts-full.json
 * @param {object} values - { [campo_canonico]: valor } (ver claves en token_registry), más 'adicionales' opcional
 * @returns {{ text: string, unresolvedRequired: string[], unresolvedOptional: string[] }}
 */
export function resolvePrompt(template, registry, values) {
  let text = template || "";
  const v = values || {};
  Object.keys(registry).forEach((field) => {
    const val = (v[field] || "").toString().trim();
    if (!val) return;
    (registry[field].aliases || []).forEach((token) => {
      text = replaceToken(text, token, val);
    });
  });
  const additional = parseAdditionalVars(v.adicionales);
  Object.keys(additional).forEach((token) => {
    text = replaceToken(text, token, additional[token]);
  });
  const unresolved = findUnresolvedPlaceholders(text, registry);
  return {
    text,
    unresolvedRequired: unresolved.filter((token) => {
      const field = getTokenField(token, registry);
      return field && registry[field].required;
    }),
    unresolvedOptional: unresolved.filter((token) => {
      const field = getTokenField(token, registry);
      return !field || !registry[field].required;
    }),
  };
}
