const assert = require("assert");
const fs = require("fs");
const vm = require("vm");
const path = require("path");

const root = path.resolve(__dirname, "..", "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const source = scripts.find(script => script.includes("var TOKEN_REGISTRY"));
assert(source, "No se encontró el script principal generado");

const storage = new Map();
const elements = new Map();
const document = {
  documentElement: { lang: "es", setAttribute() {} },
  body: {
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    appendChild() {},
    removeChild() {},
  },
  addEventListener() {},
  querySelectorAll() { return []; },
  querySelector() { return null; },
  getElementById(id) { return elements.get(id) || null; },
  createElement() {
    return {
      style: {},
      classList: { add() {}, remove() {}, contains() { return false; } },
      focus() {},
      select() {},
      appendChild() {},
    };
  },
  execCommand() { return true; },
};
const context = {
  console,
  document,
  navigator: { language: "es-MX", clipboard: { writeText: async () => {} } },
  localStorage: {
    getItem(key) { return storage.has(key) ? storage.get(key) : null; },
    setItem(key, value) { storage.set(key, String(value)); },
  },
  window: {
    confirm: () => true, // confirmDeleteProject() lo requiere; siempre confirma en las pruebas
    location: { pathname: "/", search: "", hash: "" },
    history: { replaceState() {}, pushState() {} },
    addEventListener() {},
  },
  setTimeout(fn) { fn(); },
  clearTimeout() {},
};
vm.createContext(context);
vm.runInContext(source, context);

function setValues(values) {
  context.getVarValues = () => Object.assign({}, context.EMPTY_VARS, values);
}

setValues({
  repositorio: "org/<repo>&$1",
  referencia: "#1034\nsegunda línea",
  modulo: "módulo/ñ",
  workspace: "apps\\admin",
  compliance: "ISO 27001",
});

const template = [
  "[NOMBRE O URL]",
  "[PEGAR]",
  "[MODULO]",
  "[WORKSPACE/SUBPROYECTO]",
  "[ESTÁNDAR/COMPLIANCE]",
].join("|");
const resolved = context.resolvePrompt(template);
assert.strictEqual(
  resolved.text,
  "org/<repo>&$1|#1034\nsegunda línea|módulo/ñ|apps\\admin|ISO 27001"
);
assert.deepStrictEqual(Array.from(resolved.unresolvedRequired), []);

// Regresión: bug real corregido de doble sustitución cruzada. Antes,
// resolvePrompt() sustituía campo por campo con .replace() encadenado,
// reescaneando el texto YA sustituido en cada paso -- si el valor de un
// campo contenía literalmente el placeholder de OTRO campo procesado
// después, ese texto recién insertado se volvía a sustituir. Aquí
// "repositorio" contiene literalmente "[MODULO]" y "modulo" se procesa
// después en VAR_MAP -- el valor de repositorio debe quedar intacto.
const valuesBeforeRegressionChecks = {
  repositorio: "org/<repo>&$1",
  referencia: "#1034\nsegunda línea",
  modulo: "módulo/ñ",
  workspace: "apps\\admin",
  compliance: "ISO 27001",
};
setValues({ repositorio: "mi-repo [MODULO]", modulo: "auth-service" });
const crossField = context.resolvePrompt("[NOMBRE O URL] | [MODULO]");
assert.strictEqual(
  crossField.text,
  "mi-repo [MODULO] | auth-service",
  "el valor de un campo no debe volver a sustituirse aunque contenga el placeholder literal de otro campo"
);

// Regresión: bug real corregido de falso bloqueo de "placeholder sin
// resolver". Antes, si un campo REQUERIDO se llenaba con un valor
// idéntico a su propio token (ej. entrada = "[ENTRADA PRINCIPAL]"), el
// texto sustituido seguía conteniendo ese literal y el escaneo posterior
// lo marcaba como no resuelto pese a que el campo sí tenía un valor.
setValues({ entrada: "[ENTRADA PRINCIPAL]" });
const selfLiteral = context.resolvePrompt("Entrada: [ENTRADA PRINCIPAL]");
assert.strictEqual(selfLiteral.text, "Entrada: [ENTRADA PRINCIPAL]");
assert.deepStrictEqual(
  Array.from(selfLiteral.unresolvedRequired),
  [],
  "un campo requerido con valor propio no debe marcarse como sin resolver aunque su valor coincida con su placeholder"
);
setValues(valuesBeforeRegressionChecks); // restaura el estado que usan las aserciones siguientes

// PLACEHOLDER_IGNORE debe reflejar extract_vars.py IGNORED: [SÍ / NO] es un
// placeholder de formato (usado en 00-C-01, 00-C-02, 09-04-promotion-checklist),
// no un campo a llenar — no debe disparar la advertencia de "captura manual".
const formatPlaceholder = context.resolvePrompt("permisos definidos: [SÍ / NO]");
assert.deepStrictEqual(Array.from(formatPlaceholder.unresolvedRequired), []);
assert.deepStrictEqual(Array.from(formatPlaceholder.unresolvedOptional), []);

// El texto de los prompts se pide con fetch a prompts-text.<lang>.json
// (issue #202), y en esta VM no hay fetch. Este harness inyecta los textos
// directamente en RAW_PROMPTS -- que es exactamente el estado en el que
// queda el navegador despues de cargarlos --, asi que se marcan como ya
// cargados. Sin esto, copySelected intentaria descargarlos y reventaria por
// el entorno de prueba, no por el codigo que se quiere probar.
context._textosCargados = { es: true, en: true };

context.RAW_PROMPTS["code-demo-es"] = "[NOMBRE O URL] [MODULO]";
elements.set("code-demo-es", { textContent: "PREVIEW ALTERADO" });
elements.set("code-fw-es", { textContent: "FW ALTERADO" });
context.RAW_PROMPTS["code-fw-es"] = "Framework [NOMBRE O URL]";
const originalGetCurrentLanguage = context.getCurrentLanguage;
context.getCurrentLanguage = () => "es";

// A partir de aquí el flujo corre dentro de un IIFE async: desde el muro de
// registro/prueba/feedback (ver docs/trial-gate-setup.md), copyPromptLang()/
// copySelected() resuelven vía checkCopyGate().then(...) antes de llamar a
// doCopy() -- ya no son síncronos, así que hace falta ceder el control
// (await) para que ese microtask corra antes de leer `copied`.
(async () => {
  let copied = "";
  context.doCopy = text => { copied = text; };
  context.showUnresolvedWarning = () => {};
  const button = { dataset: {}, classList: { contains() { return false; } } };
  context.copyPromptLang("demo", "es", button);
  await Promise.resolve(); await Promise.resolve();
  assert(copied.includes("org/<repo>&$1 módulo/ñ"));
  assert(!copied.includes("PREVIEW ALTERADO"));

  const checkbox = { dataset: { pid: "demo" } };
  context.getSelected = () => [checkbox];
  context.copySelected(button);
  await Promise.resolve(); await Promise.resolve();
  assert(copied.includes("org/<repo>&$1 módulo/ñ"));
  assert(!copied.includes("PREVIEW ALTERADO"));

  const preview = { textContent: "" };
  elements.set("code-demo-es", preview);
  context.updateContextualVariablePanel = () => {};
  context.updateLivePreview();
  assert.strictEqual(preview.textContent, "org/<repo>&$1 módulo/ñ");

  // Regresión: gap real de eficiencia corregido -- updateLivePreview()
  // ahora filtra por el idioma activo (antes recorría los 228 bloques de
  // AMBOS idiomas en cada tecla). Con "es" activo, un bloque "-en" no debe
  // tocarse; el idioma activo sí debe seguir resolviéndose con normalidad.
  context.RAW_PROMPTS["code-demo-en"] = "[NAME OR URL] [MODULE]";
  const previewEn = { textContent: "SIN TOCAR" };
  elements.set("code-demo-en", previewEn);
  const previewEsAgain = { textContent: "" };
  elements.set("code-demo-es", previewEsAgain);
  context.updateLivePreview();
  assert.strictEqual(previewEn.textContent, "SIN TOCAR", "un bloque del idioma inactivo no debe re-resolverse en cada tecla");
  assert.strictEqual(previewEsAgain.textContent, "org/<repo>&$1 módulo/ñ", "el bloque del idioma activo sí debe seguir resolviéndose");

  storage.clear();
  context.saveProjects([{
    id: "p1",
    name: "Proyecto",
    isDefault: true,
    vars: { repositorio: "org/repo" },
  }]);
  storage.set(context.LS_KEY_ACTV, "p1");
  assert.strictEqual(context.getActiveProject().vars.repositorio, "org/repo");
  assert(Object.prototype.hasOwnProperty.call(context.getActiveProject().vars, "workspace"));

  storage.set(context.I18N_KEY, "en");
  context.getCurrentLanguage = originalGetCurrentLanguage;
  assert.strictEqual(context.getCurrentLanguage(), "en");

  // escId() debe escapar comilla simple/doble, & y backslash antes de que un
  // id se inserte en onclick="fn('ID')" (auditoría de seguridad: hoy genId()
  // nunca produce estos caracteres, pero un futuro id de otro origen -ej.
  // importar un proyecto- no debe poder romper el atributo ni inyectar JS).
  assert.strictEqual(
    context.escId(`a'b"c&d${String.fromCharCode(92)}e`),
    "a\\'b&quot;c&amp;d\\\\e"
  );

  // Checklist de progreso por proyecto (issue #139) -- p1 sigue activo desde
  // el bloque anterior. computeProjectProgress() depende de PROMPT_INFO
  // (embebido en el mismo script generado), así que debe existir de verdad,
  // no un stub -- si build.py deja de emitir el campo "section" por prompt,
  // esta prueba lo detecta.
  assert(context.PROMPT_INFO && Object.keys(context.PROMPT_INFO).length > 50,
    "PROMPT_INFO no está poblado en el script generado");
  const anyPid = Object.keys(context.PROMPT_INFO).find(id => id !== "fw");
  assert(context.PROMPT_INFO[anyPid].section, `PROMPT_INFO['${anyPid}'] no trae 'section'`);

  elements.delete("proj-progress-summary"); // fuerza el camino "contenedor ausente" primero
  context.refreshProjectProgressUI(); // no debe lanzar aunque el contenedor no exista

  assert.strictEqual(context.isPromptUsedInActiveProject(anyPid), null);
  context.markPromptsUsed([anyPid, "fw"]); // "fw" nunca debe contarse
  const usedAtFirst = context.isPromptUsedInActiveProject(anyPid);
  assert(usedAtFirst, "markPromptsUsed no registró el prompt como usado");

  const progress = context.computeProjectProgress();
  assert.strictEqual(progress.totalUsed, 1);
  assert(progress.totalCount > 50);
  const secOfPid = context.PROMPT_INFO[anyPid].section;
  assert.strictEqual(progress.bySection[secOfPid].used, 1);

  // Re-copiar el mismo prompt no debe pisar la marca de tiempo de la
  // primera vez -- "usado" refleja cuándo se ejecutó por primera vez.
  context.markPromptsUsed([anyPid]);
  assert.strictEqual(context.isPromptUsedInActiveProject(anyPid), usedAtFirst);

  // Alternar manualmente debe des-marcarlo.
  context.togglePromptUsedManually(anyPid);
  assert.strictEqual(context.isPromptUsedInActiveProject(anyPid), null);
  assert.strictEqual(context.computeProjectProgress().totalUsed, 0);

  // refreshProjectProgressUI() sí debe poblar el contenedor cuando existe.
  const progressContainer = { innerHTML: "" };
  elements.set("proj-progress-summary", progressContainer);
  context.markPromptsUsed([anyPid]);
  assert(progressContainer.innerHTML.includes("proj-progress-fill"),
    "refreshProjectProgressUI() no actualizó el contenedor existente");

  // Personalización por proyecto (issue #137) -- las adiciones nunca deben
  // tocar el texto canónico ya resuelto, solo anexarse al copiar.
  const pidA = anyPid;
  const pidB = Object.keys(context.PROMPT_INFO).find(id => id !== "fw" && id !== pidA);
  assert.strictEqual(context.getPromptStateField(pidA, "customAdditions"), "");
  context.saveCustomAdditions(pidA, "  siempre usar TypeScript strict mode  ");
  assert.strictEqual(
    context.getPromptStateField(pidA, "customAdditions"),
    "  siempre usar TypeScript strict mode  "
  );

  const noExtras = context.appendCustomAdditions({ text: "TEXTO BASE", promptIds: [pidB] });
  assert.strictEqual(noExtras, "TEXTO BASE", "no debe anexar nada si el prompt no tiene adiciones guardadas");

  const withExtras = context.appendCustomAdditions({ text: "TEXTO BASE", promptIds: [pidA, pidB] });
  assert(withExtras.startsWith("TEXTO BASE"), "el texto base debe ir primero, intacto");
  assert(
    withExtras.includes("siempre usar TypeScript strict mode"),
    "debe anexar la adición personalizada del proyecto activo"
  );

  // Resultado de IA (issue #140) -- almacenamiento puro, sin invocar ningún
  // modelo; y no debe pisar customAdditions al guardarse para el mismo pid.
  context.saveAiOutput(pidA, "## Hallazgos\n- X\n- Y");
  assert.strictEqual(context.getPromptStateField(pidA, "aiOutput"), "## Hallazgos\n- X\n- Y");
  assert.strictEqual(
    context.getPromptStateField(pidA, "customAdditions"),
    "  siempre usar TypeScript strict mode  ",
    "guardar aiOutput no debe borrar customAdditions del mismo prompt"
  );

  // Regresión: togglePromptUsedManually() solo debe tocar used_at -- no
  // debe borrar customAdditions/aiOutput ya guardados para el mismo prompt
  // (bug real detectado y corregido antes de este commit: la primera
  // versión hacía `delete proj[pid]`, perdiendo todo lo demás).
  context.markPromptsUsed([pidA]);
  assert(context.isPromptUsedInActiveProject(pidA));
  context.togglePromptUsedManually(pidA); // des-marca "usado"
  assert.strictEqual(context.isPromptUsedInActiveProject(pidA), null);
  assert.strictEqual(
    context.getPromptStateField(pidA, "customAdditions"),
    "  siempre usar TypeScript strict mode  ",
    "des-marcar como usado no debe borrar customAdditions"
  );
  assert.strictEqual(
    context.getPromptStateField(pidA, "aiOutput"),
    "## Hallazgos\n- X\n- Y",
    "des-marcar como usado no debe borrar aiOutput"
  );

  // Guardar un campo vacío limpia solo ese campo, sin afectar los demás.
  context.saveAiOutput(pidA, "");
  assert.strictEqual(context.getPromptStateField(pidA, "aiOutput"), "");
  assert.strictEqual(
    context.getPromptStateField(pidA, "customAdditions"),
    "  siempre usar TypeScript strict mode  ",
    "limpiar aiOutput no debe borrar customAdditions"
  );

  // Export/import v2 (issues #137/#139/#140): promptState viaja junto con
  // las variables. Exports v1 (sin promptState) deben seguir importando
  // sin lanzar y sin crear ningún estado de progreso/personalización.
  storage.clear();
  context.saveProjects([{ id: "src", name: "Origen", isDefault: true, vars: { repositorio: "org/x" } }]);
  const exportedState = { [pidA]: { customAdditions: "adición exportada", usedAt: "2026-01-01T00:00:00.000Z" } };
  context.savePromptState({ src: exportedState });
  const addedV2 = context.importProjects({
    ai_sdlc_export_version: 2,
    projects: [{ name: "Importado v2", vars: { repositorio: "org/x" }, promptState: exportedState }],
  });
  assert.strictEqual(addedV2, 1);
  const importedProjectV2 = context.loadProjects().find(p => p.name === "Importado v2");
  assert(importedProjectV2, "el proyecto importado (v2) debe existir");
  const importedStateV2 = context.loadPromptState()[importedProjectV2.id];
  assert.strictEqual(importedStateV2[pidA].customAdditions, "adición exportada");

  const addedV1 = context.importProjects({
    ai_sdlc_export_version: 1,
    projects: [{ name: "Importado v1", vars: { repositorio: "org/y" } }], // sin promptState, como un export viejo
  });
  assert.strictEqual(addedV1, 1, "un export v1 sin promptState debe seguir importándose sin lanzar");
  const importedProjectV1 = context.loadProjects().find(p => p.name === "Importado v1");
  assert.strictEqual(context.loadPromptState()[importedProjectV1.id], undefined);

  // Modo guiado (issue #138) -- reactiva el proyecto "p1" ya usado en el
  // bloque de progreso para tener un estado limpio y conocido.
  storage.clear();
  context.saveProjects([{ id: "p1", name: "Proyecto", isDefault: true, vars: { repositorio: "org/repo" } }]);
  storage.set(context.LS_KEY_ACTV, "p1");

  const guidedSeq = context.getGuidedSequence();
  assert(guidedSeq.length > 50, "getGuidedSequence() debe cubrir prácticamente toda la biblioteca");
  assert(!guidedSeq.includes("fw"), "'fw' no es un paso de la ruta guiada");
  // El orden debe coincidir exactamente con el de PROMPT_INFO (mismo orden
  // curado en que build.py genera las secciones) -- no un orden distinto
  // derivado de otra fuente.
  // guidedSeq es un Array del realm interno de la vm (getGuidedSequence()
  // corre dentro del script cargado en vm.createContext) -- deepStrictEqual
  // compararía prototipos de Array de dos realms distintos y fallaría
  // aunque el contenido sea idéntico; JSON.stringify evita ese falso
  // negativo comparando solo los valores.
  assert.strictEqual(
    JSON.stringify(guidedSeq),
    JSON.stringify(Object.keys(context.PROMPT_INFO).filter(id => id !== "fw"))
  );

  assert.strictEqual(context.getGuidedPosition(), 0, "posición inicial debe ser 0 sin nada guardado");
  context.guidedGoTo(3);
  assert.strictEqual(context.getGuidedPosition(), 3);
  context.guidedNext();
  assert.strictEqual(context.getGuidedPosition(), 4);
  context.guidedPrev();
  context.guidedPrev();
  assert.strictEqual(context.getGuidedPosition(), 2);

  // No debe salirse de los límites de la secuencia en ningún sentido.
  context.guidedGoTo(-5);
  assert.strictEqual(context.getGuidedPosition(), 0);
  context.guidedGoTo(guidedSeq.length + 50);
  assert.strictEqual(context.getGuidedPosition(), guidedSeq.length - 1);

  // guidedJumpToFirstUnused() debe encontrar el primer prompt no usado.
  context.guidedGoTo(0);
  context.markPromptsUsed([guidedSeq[0], guidedSeq[1]]);
  context.guidedJumpToFirstUnused();
  assert.strictEqual(context.getGuidedPosition(), 2, "debe saltar al primer prompt aún no usado (índice 2)");

  // renderGuidedStep() no debe lanzar sin los contenedores en el DOM...
  elements.delete("guided-body");
  elements.delete("guided-prev-btn");
  elements.delete("guided-next-btn");
  context.renderGuidedStep(0);

  // ...y sí debe poblar el body y deshabilitar "Anterior" en el primer paso.
  const guidedBody = { innerHTML: "", appendChild(node) { this.children = (this.children || []); this.children.push(node); } };
  const prevBtn = { disabled: false };
  const nextBtn = { disabled: false };
  elements.set("guided-body", guidedBody);
  elements.set("guided-prev-btn", prevBtn);
  elements.set("guided-next-btn", nextBtn);
  context.renderGuidedStep(0);
  assert.strictEqual(prevBtn.disabled, true, "en el primer paso, 'Anterior' debe estar deshabilitado");
  assert.strictEqual(nextBtn.disabled, false);
  assert(guidedBody.children && guidedBody.children.length >= 3, "debe agregar overall/step/title al body");

  context.renderGuidedStep(guidedSeq.length - 1);
  assert.strictEqual(nextBtn.disabled, true, "en el último paso, 'Siguiente' debe estar deshabilitado");

  // Regresión: bug real corregido (auditoría de UX -- cambio entre
  // proyectos). Al borrar el proyecto ACTIVO, el panel de variables (el
  // DOM) seguía mostrando los valores del proyecto recién eliminado -- si
  // el usuario editaba cualquier campo después, syncProjectFromPanel()
  // leía esos valores obsoletos y sobrescribía el proyecto sobreviviente.
  storage.clear();
  context.saveProjects([
    { id: "alpha", name: "Alpha", isDefault: true, vars: Object.assign({}, context.EMPTY_VARS, { repositorio: "org/alpha" }) },
    { id: "beta", name: "Beta", isDefault: false, vars: Object.assign({}, context.EMPTY_VARS, { repositorio: "org/beta" }) },
  ]);
  storage.set(context.LS_KEY_ACTV, "beta");
  const repoInput = { value: "", multiple: false };
  elements.set("vf-repositorio", repoInput);
  context.syncPanelToProject();
  assert.strictEqual(repoInput.value, "org/beta", "el panel debe reflejar el proyecto activo (Beta) antes de borrar");

  context.confirmDeleteProject("beta", "Beta");
  assert.strictEqual(context.getActiveProject().id, "alpha", "tras borrar el proyecto activo, Alpha debe quedar activo");
  assert.strictEqual(
    repoInput.value,
    "org/alpha",
    "el panel de variables debe resincronizarse al proyecto sobreviviente tras borrar el activo"
  );

  // Si el panel NO se hubiera resincronizado, este siguiente "editar campo"
  // habría sobrescrito Alpha con el valor obsoleto de Beta -- confirma que
  // Alpha queda con el valor recién editado, intacto.
  repoInput.value = "org/alpha-editado";
  context.syncProjectFromPanel();
  assert.strictEqual(context.getActiveProject().vars.repositorio, "org/alpha-editado");

  // ═══════════ Gate de plataforma (issue #7, Opción B) ═══════════
  // El repositorio es público, así que copiar prompts ya NO se gatea (ver
  // copyResolvedText()); lo que sí se gatea es crear un 2do proyecto o más,
  // y guardar personalización/resultados de IA -- ver checkProFeatureGate().
  // isSupabaseConfigured()/getSupabaseClient() se sobreescriben aquí (mismo
  // patrón ya usado para getCurrentLanguage) porque el build local no trae
  // SUPABASE_URL/SUPABASE_ANON_KEY configurados -- sin esto,
  // checkProFeatureGate() haría fail-open en su primera línea y ninguna
  // rama de bloqueo sería alcanzable en esta prueba.
  context.isSupabaseConfigured = () => true;
  storage.clear();
  context.saveProjects([{ id: "p1", name: "Proyecto", isDefault: true, vars: Object.assign({}, context.EMPTY_VARS) }]);
  storage.set(context.LS_KEY_ACTV, "p1");

  // Anónimo: el gate rechaza sin necesidad de ningún RPC (el límite de "1
  // proyecto gratis" se decide con loadProjects().length, no con IPs).
  context._authStateResolved = true;
  context._sbUser = null;
  const anonGate = await context.checkProFeatureGate();
  // anonGate viene del realm interno de la vm -- deepStrictEqual fallaría
  // por prototipos de Object distintos aunque el contenido sea idéntico
  // (mismo problema documentado para Array más abajo con getGuidedSequence()).
  assert.strictEqual(JSON.stringify(anonGate), JSON.stringify({ allowed: false, reason: "anon_project_limit" }));

  // Fail-open mientras el estado de auth aún no se resuelve (ver bug real
  // corregido documentado en checkProFeatureGate()).
  context._authStateResolved = false;
  const pendingGate = await context.checkProFeatureGate();
  assert.strictEqual(pendingGate.allowed, true, "debe fallar abierto mientras _authStateResolved es false");
  context._authStateResolved = true;

  // Con sesión: check_trial_status() decide -- activo permite, vencido
  // bloquea con reason 'trial_expired'.
  context._sbUser = { id: "fake-user" };
  context.getSupabaseClient = () => ({
    rpc: (name) => name === "check_trial_status"
      ? Promise.resolve({ data: { active: true }, error: null })
      : Promise.resolve({ data: null, error: null }),
  });
  const activeTrialGate = await context.checkProFeatureGate();
  assert.strictEqual(JSON.stringify(activeTrialGate), JSON.stringify({ allowed: true }));

  context.getSupabaseClient = () => ({
    rpc: (name) => name === "check_trial_status"
      ? Promise.resolve({ data: { active: false }, error: null })
      : Promise.resolve({ data: null, error: null }),
  });
  const expiredTrialGate = await context.checkProFeatureGate();
  assert.strictEqual(JSON.stringify(expiredTrialGate), JSON.stringify({ allowed: false, reason: "trial_expired" }));

  // requestNewProject(): el primer proyecto (lista vacía) siempre es
  // gratis, sin pasar por el gate en absoluto.
  storage.clear();
  let onSuccessCalled = false;
  context.requestNewProject(() => { onSuccessCalled = true; });
  assert.strictEqual(context.loadProjects().length, 1, "el primer proyecto debe crearse sin gate");
  assert.strictEqual(onSuccessCalled, true);

  // 2do proyecto, anónimo -- el gate bloquea y NO se crea.
  // requestNewProject() es fire-and-forget (igual que copyResolvedText()),
  // así que se cede el control con microtasks en vez de un await directo.
  context._sbUser = null;
  onSuccessCalled = false;
  context.requestNewProject(() => { onSuccessCalled = true; });
  // 3 flushes: requestNewProject().then(...) encadena sobre la promesa que
  // ya devuelve checkProFeatureGate() (rpc -> .then() -> .then()).
  await Promise.resolve(); await Promise.resolve(); await Promise.resolve();
  assert.strictEqual(context.loadProjects().length, 1, "no debe crearse un 2do proyecto sin sesión");
  assert.strictEqual(onSuccessCalled, false);

  // 2do proyecto, con sesión y prueba activa -- el gate permite.
  context._sbUser = { id: "fake-user" };
  context.getSupabaseClient = () => ({
    rpc: (name) => name === "check_trial_status"
      ? Promise.resolve({ data: { active: true }, error: null })
      : Promise.resolve({ data: null, error: null }),
  });
  context.requestNewProject(() => { onSuccessCalled = true; });
  await Promise.resolve(); await Promise.resolve(); await Promise.resolve();
  assert.strictEqual(context.loadProjects().length, 2, "el 2do proyecto sí debe crearse con prueba activa");
  assert.strictEqual(onSuccessCalled, true);

  // Copiar prompts NUNCA pasa por este gate, ni siquiera en el estado más
  // restrictivo (anónimo, gate rechazando) -- regresión clave del rediseño.
  context._sbUser = null;
  context.getSupabaseClient = () => ({
    rpc: () => Promise.resolve({ data: { allowed: false }, error: null }),
  });
  let copiedDespiteBlockedGate = "";
  context.doCopy = text => { copiedDespiteBlockedGate = text; };
  context.showUnresolvedWarning = () => {};
  context.copyPromptLang("demo", "es", { dataset: {}, classList: { contains: () => false } });
  await Promise.resolve(); await Promise.resolve();
  assert(copiedDespiteBlockedGate.length > 0, "copiar debe funcionar siempre, sin importar el estado del gate");
  const anyPidForCopy = Object.keys(context.PROMPT_INFO).find(id => id !== "fw");

  // saveGatedPromptField(): vaciar un campo siempre se permite sin gate;
  // guardar contenido no vacío pasa por el gate y revierte el textarea si
  // se bloquea.
  context._sbUser = null;
  const gatedTextarea = { value: "", dataset: {} };
  let clearedValue = "sin-llamar";
  context.saveGatedPromptField(gatedTextarea, (pid, value) => { clearedValue = value; }, anyPidForCopy);
  assert.strictEqual(clearedValue, "", "vaciar el campo debe guardar directo, sin pasar por el gate");

  let savedValue = null;
  const saveFnStub = (pid, value) => { savedValue = value; };
  gatedTextarea.value = "restricción de mi organización";
  context.saveGatedPromptField(gatedTextarea, saveFnStub, anyPidForCopy);
  await Promise.resolve(); await Promise.resolve(); await Promise.resolve();
  assert.strictEqual(savedValue, null, "no debe guardarse contenido no vacío sin sesión");
  assert.strictEqual(gatedTextarea.value, "", "el textarea debe vaciarse cuando el gate bloquea");

  context._sbUser = { id: "fake-user" };
  context.getSupabaseClient = () => ({
    rpc: (name) => name === "check_trial_status"
      ? Promise.resolve({ data: { active: true }, error: null })
      : Promise.resolve({ data: null, error: null }),
  });
  gatedTextarea.value = "restricción de mi organización";
  context.saveGatedPromptField(gatedTextarea, saveFnStub, anyPidForCopy);
  await Promise.resolve(); await Promise.resolve(); await Promise.resolve();
  assert.strictEqual(savedValue, "restricción de mi organización", "sí debe guardarse con prueba activa");
  assert.strictEqual(gatedTextarea.dataset.proOk, "1", "debe marcarse como ya verificado para no repetir el RPC en cada tecla");

  console.log("runtime variable tests: ok");
})().catch(err => {
  console.error(err);
  process.exit(1);
});
