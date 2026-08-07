// El contrato de operacion debe viajar tambien por MCP.
//
// Por que importa mas aqui que en el navegador: quien copia un prompt desde
// el sitio lo pega y lo lee. Un agente que lo pide por MCP suele EJECUTAR
// directamente. Entregarle el prompt sin su techo de autonomia ni sus
// criterios de detencion es la peor de las dos rutas para perderlos.

import test from "node:test";
import assert from "node:assert/strict";
import { operatingContractBlock } from "../src/operatingContract.js";
import { getPrompt, listPrompts } from "../src/dataStore.js";

const CAMPOS = ["permitted_autonomy", "allowed_tools", "stop_criteria", "minimum_evidence"];

test("el bloque trae los cuatro campos con su texto real", () => {
  const p = getPrompt(listPrompts({})[0].id);
  const contrato = p.contract.es;
  const bloque = operatingContractBlock(contrato, "es");

  assert.match(bloque, /^## Contrato de operación/);
  for (const campo of CAMPOS) {
    if (!contrato[campo]) continue;
    assert.ok(
      bloque.includes(contrato[campo]),
      `el campo ${campo} aparece sin su texto: un encabezado vacio no restringe nada`
    );
  }
});

test("no le ordena obedecer por encima de la tarea del usuario", () => {
  const bloque = operatingContractBlock(getPrompt(listPrompts({})[0].id).contract.es, "es");
  // Si la tarea contradice al contrato, el agente debe DECLARARLO, no elegir
  // en silencio. Ver tests/test_mcp_contract_parity.py.
  assert.doesNotMatch(bloque, /por encima de (todo|cualquier)/i);
  assert.match(bloque, /decláralo en vez de excederlas/);
});

test("el ingles esta traducido, no es español con otra etiqueta", () => {
  const p = getPrompt(listPrompts({})[0].id);
  const bloque = operatingContractBlock(p.contract.en, "en");
  assert.match(bloque, /^## Operating contract/);
  assert.ok(bloque.includes(p.contract.en.stop_criteria));
});

test("un contrato vacio no produce encabezados huerfanos", () => {
  assert.equal(operatingContractBlock(null, "es"), "");
  assert.equal(operatingContractBlock({}, "es"), "");
});

test("los 112 prompts llegan con contrato completo por MCP", () => {
  // Cobertura parcial es peor que ninguna: quien confia en que el limite
  // viaja no revisa prompt por prompt si esta vez viajo.
  const faltantes = listPrompts({})
    .map((s) => getPrompt(s.id))
    .filter((p) => {
      for (const lang of ["es", "en"]) {
        const b = operatingContractBlock(p.contract[lang], lang);
        if (!b || !b.includes("Detente") && !b.includes("Stop and ask")) return true;
      }
      return false;
    })
    .map((p) => p.id);

  assert.deepEqual(faltantes, [], `estos prompts llegarian sin contrato por MCP: ${faltantes.slice(0, 5)}`);
});
