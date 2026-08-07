// Contrato de operación: las restricciones que viajan CON el prompt.
//
// El sitio ya lo hace (ver operatingContractText() en build.py): quien copia
// un prompt desde prompts.lionsystems.com.mx pega tambien el techo de
// autonomia, las herramientas permitidas, los criterios de detencion y la
// evidencia minima. Sin esto, un agente que consume la biblioteca por MCP
// recibiria el mismo prompt SIN ninguno de sus limites -- que es peor que el
// caso del navegador, porque por MCP el agente suele ejecutar directamente.
//
// El texto se mantiene identico al del sitio a proposito: es el mismo
// contrato editorial y no debe decir una cosa al copiar y otra por MCP.
// tests/test_mcp_contract_parity.py falla si las dos versiones divergen.

const LABELS = {
  es: {
    permitted_autonomy: "Autonomía máxima",
    allowed_tools: "Herramientas permitidas",
    stop_criteria: "Detente y pregunta cuando",
    minimum_evidence: "Evidencia mínima de tu salida",
  },
  en: {
    permitted_autonomy: "Maximum autonomy",
    allowed_tools: "Allowed tools",
    stop_criteria: "Stop and ask when",
    minimum_evidence: "Minimum evidence in your output",
  },
};

const HEADER = {
  es:
    "## Contrato de operación\n\n" +
    "Estas restricciones vienen del contrato editorial de este prompt. " +
    // No se le ordena obedecer "por encima de todo": si la tarea contradice
    // el contrato, lo correcto es que lo declare, no que elija en silencio.
    "Si la tarea las contradice, decláralo en vez de excederlas.\n\n",
  en:
    "## Operating contract\n\n" +
    "These constraints come from this prompt's editorial contract. " +
    "If the task contradicts them, say so instead of exceeding them.\n\n",
};

const ORDER = ["permitted_autonomy", "allowed_tools", "stop_criteria", "minimum_evidence"];

/**
 * Construye el bloque Markdown del contrato de operación de un prompt.
 *
 * @param {object} contract contrato editorial ya resuelto al idioma pedido
 * @param {"es"|"en"} lang
 * @returns {string} bloque Markdown, o "" si el prompt no declara ninguno
 */
export function operatingContractBlock(contract, lang) {
  if (!contract) return "";
  const l = lang === "en" ? "en" : "es";
  const labels = LABELS[l];
  const lines = ORDER.filter((k) => contract[k]).map((k) => `- **${labels[k]}:** ${contract[k]}`);
  if (!lines.length) return "";
  return HEADER[l] + lines.join("\n");
}

export const OPERATING_CONTRACT_LABELS = LABELS;
export const OPERATING_CONTRACT_ORDER = ORDER;
