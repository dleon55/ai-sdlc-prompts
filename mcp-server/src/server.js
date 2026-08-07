import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import {
  listPrompts,
  getPrompt,
  getFramework,
  getTokenRegistry,
} from "./dataStore.js";
import { resolvePrompt } from "./resolvePrompt.js";
import { operatingContractBlock } from "./operatingContract.js";

const LANG = z.enum(["es", "en"]).optional().describe("Idioma de salida (es/en). Por defecto: es.");

function textResult(value) {
  return { content: [{ type: "text", text: JSON.stringify(value, null, 2) }] };
}

function errorResult(message) {
  return { content: [{ type: "text", text: JSON.stringify({ error: message }, null, 2) }], isError: true };
}

function promptSummary(p, lang) {
  return {
    id: p.id,
    section: p.section,
    title: p.title[lang] || p.title.es,
    expected_risk_tags: p.contract?.es?.expected_risk_tags || [],
    permitted_autonomy_tags: p.contract?.es?.permitted_autonomy_tags || [],
  };
}

export function createServer() {
  const server = new McpServer({
    name: "ai-sdlc-prompts",
    version: "1.0.0",
    websiteUrl: "https://github.com/dleon55/ai-sdlc-prompts",
  });

  server.registerTool(
    "list_prompts",
    {
      title: "Listar prompts",
      description:
        "Lista los prompts de la biblioteca AI-SDLC Pro, con filtro opcional por sección (00-17), riesgo esperado (low/medium/high/variable), autonomía permitida (A0-A3) y texto libre (busca en título y descripción).",
      inputSchema: {
        section: z.string().optional().describe("Código de sección, ej. '07', '16'."),
        risk: z.enum(["low", "medium", "high", "variable"]).optional(),
        autonomy: z.enum(["A0", "A1", "A2", "A3"]).optional(),
        query: z.string().optional().describe("Texto libre a buscar en título/descripción."),
        lang: LANG,
      },
    },
    async ({ section, risk, autonomy, query, lang }) => {
      const l = lang || "es";
      const results = listPrompts({ section, risk, autonomy, query }).map((p) => promptSummary(p, l));
      return textResult({ count: results.length, prompts: results });
    }
  );

  server.registerTool(
    "get_prompt",
    {
      title: "Obtener prompt",
      description:
        "Devuelve el detalle completo de un prompt por id: título, descripción, texto crudo del prompt (con placeholders [ASI] sin resolver), fórmulas de uso, contrato editorial y siguiente(s) prompt(s) recomendado(s).",
      inputSchema: {
        id: z.string().describe("Id del prompt, ej. '07-06-pruebas-performance-carga'."),
        lang: LANG,
      },
    },
    async ({ id, lang }) => {
      const p = getPrompt(id);
      if (!p) return errorResult(`Prompt no encontrado: ${id}`);
      const l = lang || "es";
      return textResult({
        id: p.id,
        section: p.section,
        title: p.title[l] || p.title.es,
        description: p.description[l] || p.description.es,
        template: p.template[l] || p.template.es,
        formulas: p.formulas[l] || p.formulas.es,
        contract: p.contract[l] || p.contract.es,
        recommended_next_prompt_ids: p.recommended_next_prompt_ids,
      });
    }
  );

  server.registerTool(
    "resolve_prompt",
    {
      title: "Resolver prompt con variables",
      description:
        "Sustituye los placeholders del prompt (y opcionalmente del preámbulo del framework) con las variables provistas -- misma sustitución que hace el sitio. Las claves de 'variables' son los campos canónicos (repositorio, referencia, rama_actual, rama_destino, ambiente, componentes, modulo, stack, tipo_proyecto, metodologia, agentes, autonomia, entrada, objetivo, responsable, workspace, compliance, documentos, profundidad, adicionales), no los alias en mayúsculas del texto. Devuelve el texto resuelto y los placeholders obligatorios/opcionales que quedaron sin resolver.",
      inputSchema: {
        id: z.string().describe("Id del prompt a resolver."),
        lang: LANG,
        variables: z.record(z.string(), z.string()).optional().describe("Campo canónico -> valor."),
        prepend_framework: z.boolean().optional().describe("Antepone el preámbulo obligatorio del framework (default: true)."),
        append_contract: z.boolean().optional().describe("Anexa el contrato de operación del prompt -- techo de autonomía, herramientas permitidas, criterios de detención y evidencia mínima (default: true). Desactivarlo entrega el prompt sin sus límites."),
      },
    },
    async ({ id, lang, variables, prepend_framework, append_contract }) => {
      const p = getPrompt(id);
      if (!p) return errorResult(`Prompt no encontrado: ${id}`);
      const l = lang || "es";
      const registry = getTokenRegistry();
      const values = variables || {};
      const promptResolved = resolvePrompt(p.template[l] || p.template.es, registry, values);

      let text = promptResolved.text;
      let unresolvedRequired = promptResolved.unresolvedRequired;
      let unresolvedOptional = promptResolved.unresolvedOptional;

      const shouldPrependFramework = prepend_framework !== false;
      if (shouldPrependFramework) {
        const framework = getFramework();
        const fwResolved = resolvePrompt(framework.preamble[l] || framework.preamble.es, registry, values);
        text = fwResolved.text + "\n\n---\n\n" + text;
        unresolvedRequired = [...fwResolved.unresolvedRequired, ...unresolvedRequired];
        unresolvedOptional = [...fwResolved.unresolvedOptional, ...unresolvedOptional];
      }

      // El contrato va al final, igual que en el sitio. Sin esto, un agente
      // que consume la biblioteca por MCP recibiria el prompt sin ninguno de
      // sus limites -- y por MCP el agente suele ejecutar, no solo redactar.
      const contractBlock = append_contract === false
        ? ""
        : operatingContractBlock(p.contract[l] || p.contract.es, l);
      if (contractBlock) text = text + "\n\n---\n\n" + contractBlock;

      return textResult({
        id: p.id,
        text,
        unresolved_required: unresolvedRequired,
        unresolved_optional: unresolvedOptional,
        contract_included: Boolean(contractBlock),
      });
    }
  );

  server.registerTool(
    "get_framework",
    {
      title: "Obtener framework",
      description:
        "Devuelve el preámbulo obligatorio del framework AI-SDLC (principio operativo que se antepone a cualquier prompt de la biblioteca).",
      inputSchema: { lang: LANG },
    },
    async ({ lang }) => {
      const l = lang || "es";
      const framework = getFramework();
      return textResult({ text: framework.preamble[l] || framework.preamble.es });
    }
  );

  server.registerTool(
    "recommend_next",
    {
      title: "Siguiente prompt recomendado",
      description: "Devuelve el/los prompt(s) que el contrato editorial recomienda usar después de uno dado.",
      inputSchema: {
        id: z.string().describe("Id del prompt actual."),
        lang: LANG,
      },
    },
    async ({ id, lang }) => {
      const p = getPrompt(id);
      if (!p) return errorResult(`Prompt no encontrado: ${id}`);
      const l = lang || "es";
      const next = (p.recommended_next_prompt_ids || [])
        .map((nid) => getPrompt(nid))
        .filter(Boolean)
        .map((np) => promptSummary(np, l));
      return textResult({ id: p.id, recommended_next: next });
    }
  );

  return server;
}
