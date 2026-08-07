// Ejecuta el JS generado de index.html para comprobar que el contrato de
// operacion viaja de verdad en el texto copiado.
//
// Por que en runtime y no comprobando cadenas en el HTML: hoy mismo un bug
// llego a produccion porque los tests solo verificaban que ciertas cadenas
// estuvieran presentes. El codigo se veia intacto y el checkout estaba
// completamente roto. Aqui lo que importa no es que exista la funcion, sino
// que el texto que termina en el portapapeles contenga las restricciones.
//
// Que protege: los cuatro campos del contrato (techo de autonomia,
// herramientas permitidas, criterios de detencion, evidencia minima)
// estaban escritos al 100% en los 224 contratos y llegaban al modelo en 0%.
// Si alguien vuelve a desconectarlos, el prompt sigue copiandose bien y
// nadie lo nota: el agente simplemente deja de conocer sus limites.

const assert = require("assert");
const fs = require("fs");
const vm = require("vm");
const path = require("path");

const root = path.resolve(__dirname, "..", "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const source = scripts.find(script => script.includes("function operatingContractText"));
assert(source, "No se encontro el script con operatingContractText en index.html");

const context = {
  console,
  document: {
    documentElement: { lang: "es", setAttribute() {}, getAttribute: () => "es" },
    body: { classList: { add() {}, remove() {}, contains() { return false; } }, appendChild() {} },
    addEventListener() {},
    querySelector() { return null; },
    querySelectorAll() { return []; },
    getElementById() { return null; },
    createElement: () => ({ style: {}, classList: { add() {}, remove() {} }, appendChild() {} }),
  },
  navigator: { language: "es-MX" },
  localStorage: { getItem: () => null, setItem() {} },
  window: { location: { pathname: "/", search: "", hash: "" }, history: {}, addEventListener() {} },
  setTimeout(fn) { fn(); },
  clearTimeout() {},
};
vm.createContext(context);
vm.runInContext(source, context);

const INFO = context.PROMPT_INFO;
assert(INFO, "PROMPT_INFO no llego al navegador");

// Un prompt real cualquiera, para no depender de un id concreto que podria
// renombrarse. 'fw' es el preambulo del framework, no un prompt.
const pids = Object.keys(INFO).filter(p => p !== "fw");
const pid = pids.find(p => INFO[p].contract_es && INFO[p].contract_es.s);
assert(pid, "ningun prompt trae criterios de detencion");

context.getCurrentLanguage = () => "es";

// ── 1. Cobertura: el contrato viaja para TODOS los prompts ──
//
// Cobertura parcial es peor que ninguna: quien confia en que el limite
// viaja no revisa prompt por prompt si esta vez viajo.
const sinContrato = pids.filter(p => {
  const es = INFO[p].contract_es, en = INFO[p].contract_en;
  return !es || !en || !es.s || !en.s || !es.a || !en.a;
});
assert.strictEqual(sinContrato.length, 0,
  `estos prompts perderian su contrato al copiarse: ${sinContrato.slice(0, 5).join(", ")}`);

// ── 2. El bloque lleva los cuatro campos, con su texto real ──
const bloque = context.operatingContractText(pid, "es");
const c = INFO[pid].contract_es;
assert(/## Contrato de operación/.test(bloque), "falta el encabezado del contrato");
for (const [clave, etiqueta] of [["a", "Autonomía máxima"], ["t", "Herramientas permitidas"],
                                 ["s", "Detente y pregunta cuando"], ["e", "Evidencia mínima"]]) {
  if (!c[clave]) continue;
  assert(bloque.includes(etiqueta), `falta la etiqueta "${etiqueta}"`);
  assert(bloque.includes(c[clave]),
    `la etiqueta "${etiqueta}" esta pero sin su texto: un encabezado vacio no restringe nada`);
}

// ── 3. Ingles de verdad, no español con otra etiqueta ──
const bloqueEn = context.operatingContractText(pid, "en");
assert(/## Operating contract/.test(bloqueEn), "el bloque en ingles no esta traducido");
assert(bloqueEn.includes(INFO[pid].contract_en.s),
  "el bloque en ingles debe traer el criterio de detencion en ingles");

// ── 4. No se le ordena obedecer por encima de la tarea ──
//
// Decision deliberada: si la tarea contradice el contrato, el agente debe
// DECIRLO, no elegir en silencio. Un "obedece esto por encima de todo"
// convierte una guia editorial en un secuestro de la instruccion del
// usuario, y ademas es la clase de frase que un prompt hostil imita.
assert(!/por encima de (todo|cualquier)/i.test(bloque),
  "el contrato no debe ordenar obedecerlo por encima de la tarea del usuario");
assert(/decláralo en vez de excederlas/.test(bloque),
  "el contrato debe pedir que declare el conflicto, no que lo resuelva solo");

const base = "TEXTO DEL PROMPT";

// ── 5. Recorre la cadena REAL del boton Copiar ──
//
// Comprobar appendOperatingContracts() sola no sirve de nada: la funcion
// puede estar perfecta y no estar conectada al boton, que es precisamente
// como se pierde la gobernanza sin que nadie lo note (el prompt se sigue
// copiando bien; solo desaparecen los limites). Asi que se invoca
// copyPromptLang() y se captura lo que llega al portapapeles.
const codeId = "code-" + pid + "-es";
context.RAW_PROMPTS[codeId] = base;
context.document.getElementById = (id) => (id === codeId ? { textContent: base } : null);

let copiado = null;
context.doCopy = (texto) => { copiado = texto; };
context.copyPromptLang(pid, "es", null);

assert(copiado, "el boton Copiar no produjo texto");
assert(copiado.startsWith(base), "el prompt original no debe alterarse");
assert(copiado.includes(c.s),
  "el criterio de detencion debe llegar al portapapeles por la cadena real del boton");
assert(copiado.includes(c.a),
  "el techo de autonomia debe llegar al portapapeles");

// ── 6. Copiar una FORMULA no arrastra el contrato ──
//
// El modal copia formulas sueltas por la misma tuberia. Colgarle un
// contrato de operacion a un fragmento de una linea es ruido.
const soloFormula = context.appendOperatingContracts(base, { promptIds: [pid] });
assert.strictEqual(soloFormula, base,
  "sin withContract no debe agregarse nada: esa es la ruta de copiar formula");

// ── 7. Con varios prompts, cada contrato dice a cual pertenece ──
//
// El copiado masivo concatena prompts. Cuatro bloques identicos sin nombre
// no permiten saber que limite aplica a que fase.
const dos = [pid, pids.find(p => p !== pid && INFO[p].contract_es && INFO[p].contract_es.s)];
const multi = context.appendOperatingContracts(base, { withContract: true, promptIds: dos });
for (const p of dos) {
  assert(multi.includes(INFO[p].title_es),
    `con varios prompts, el bloque debe nombrar "${INFO[p].title_es}"`);
}

// ── 8. 'fw' no inventa un contrato ──
const conFw = context.appendOperatingContracts(base, { withContract: true, promptIds: ["fw"] });
assert.strictEqual(conFw, base,
  "el preambulo del framework no tiene contrato propio y no debe fabricarse uno");

console.log(`runtime contract tests: ok (${pids.length} prompts con contrato completo)`);
