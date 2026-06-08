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

context.RAW_PROMPTS["code-demo-es"] = "[NOMBRE O URL] [MODULO]";
elements.set("code-demo-es", { textContent: "PREVIEW ALTERADO" });
elements.set("code-fw-es", { textContent: "FW ALTERADO" });
context.RAW_PROMPTS["code-fw-es"] = "Framework [NOMBRE O URL]";
const originalGetCurrentLanguage = context.getCurrentLanguage;
context.getCurrentLanguage = () => "es";

let copied = "";
context.doCopy = text => { copied = text; };
context.showUnresolvedWarning = () => {};
const button = { dataset: {}, classList: { contains() { return false; } } };
context.copyPromptLang("demo", "es", button);
assert(copied.includes("org/<repo>&$1 módulo/ñ"));
assert(!copied.includes("PREVIEW ALTERADO"));

const checkbox = { dataset: { pid: "demo" } };
context.getSelected = () => [checkbox];
context.copySelected(button);
assert(copied.includes("org/<repo>&$1 módulo/ñ"));
assert(!copied.includes("PREVIEW ALTERADO"));

const preview = { textContent: "" };
elements.set("code-demo-es", preview);
context.updateContextualVariablePanel = () => {};
context.updateLivePreview();
assert.strictEqual(preview.textContent, "org/<repo>&$1 módulo/ñ");

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

console.log("runtime variable tests: ok");
