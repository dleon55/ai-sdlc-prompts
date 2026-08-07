// Ejecuta el JS generado de precios.html en una VM real.
//
// Por que existe: los tests de contrato de precios.html comprobaban que
// ciertas CADENAS estuvieran en el HTML ("pxPollPro" in html, etc). Eso es
// ciego a los errores en tiempo de ejecucion. Un bug real llego a
// produccion asi: pxStartCheckout usaba `anual` para elegir el precio pero
// la firma quedo sin declarar el parametro, y cada clic lanzaba
// `ReferenceError: anual is not defined`. Los dos botones de pago -- no
// solo el anual -- quedaron rotos, con el codigo intacto a la vista.
//
// index.html ya tenia test_variables_runtime.js con este enfoque; la
// pagina que cobra dinero no lo tenia.

const assert = require("assert");
const fs = require("fs");
const vm = require("vm");
const path = require("path");

const root = path.resolve(__dirname, "..", "..");
const html = fs.readFileSync(path.join(root, "precios.html"), "utf8");
const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const source = scripts.find(script => script.includes("function pxStartCheckout"));
assert(source, "No se encontro el script de checkout en precios.html");

// ── Stubs del entorno de navegador ────────────────────────────────────

const storage = new Map();
const elements = new Map();

function makeEl(id) {
  const el = {
    id,
    style: {},
    innerHTML: "",
    get innerText() { return this.innerHTML.replace(/<[^>]+>/g, ""); },
    dataset: {},
    classList: { add() {}, remove() {}, contains() { return false; } },
    focus() {}, click() {}, appendChild() {},
    setAttribute() {}, getAttribute() { return null; },
  };
  elements.set(id, el);
  return el;
}

makeEl("px-subscribe-btn");
makeEl("px-subscribe-annual-btn");
makeEl("px-sub-status");

let checkoutAbierto = null;

const context = {
  console,
  document: {
    documentElement: { lang: "es", setAttribute() {}, getAttribute: () => "es" },
    getElementById(id) { return elements.get(id) || null; },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    createElement: () => makeEl("tmp"),
    addEventListener() {},
  },
  navigator: { language: "es-MX" },
  localStorage: {
    getItem(k) { return storage.has(k) ? storage.get(k) : null; },
    setItem(k, v) { storage.set(k, String(v)); },
    removeItem(k) { storage.delete(k); },
  },
  window: {
    location: { origin: "https://prompts.lionsystems.com.mx", pathname: "/precios.html", search: "", hash: "" },
    history: { replaceState() {} },
    localStorage: null, // se completa abajo
  },
  history: { replaceState() {} },
  setTimeout(fn) { fn(); },
  // Paddle.js y el SDK de Supabase, tal como los usa la pagina.
  Paddle: {
    Environment: { set() {} },
    Initialize() {},
    Checkout: { open(cfg) { checkoutAbierto = cfg; } },
  },
  supabase: { createClient: () => stubSupabase },
  // El script hace `window.dataLayer=window.dataLayer||[]` y luego llama
  // `dataLayer.push(...)` como global. En un navegador asignar a window
  // crea ese global; dentro de una VM, window es un objeto normal y no.
  // Se declara aqui para que gtag() no reviente al cargar el script.
  dataLayer: [],
};
context.window.localStorage = context.localStorage;
context.global = context;

// Cliente de Supabase controlable por cada prueba.
let loginPedido = null;

let stubSupabase = {
  auth: {
    getSession: () => Promise.resolve({ data: { session: null } }),
    // Sin sesion, pxStartCheckout llama a pxSignIn() para autenticar en
    // sitio en vez de expulsar al visitante a la landing.
    signInWithOAuth: (opts) => { loginPedido = opts; return Promise.resolve({}); },
  },
  rpc: () => Promise.resolve({ data: null }),
};

vm.createContext(context);
vm.runInContext(source, context);

// ── Utilidades ────────────────────────────────────────────────────────

const flush = async () => { for (let i = 0; i < 8; i++) await Promise.resolve(); };

function reset() {
  checkoutAbierto = null;
  storage.clear();
  context._pxUser = null;
  context._pxYaPro = false;
  elements.get("px-subscribe-btn").style = {};
  elements.get("px-subscribe-annual-btn").style = {};
  elements.get("px-sub-status").innerHTML = "";
}

// En los PR el build corre con PADDLE_CLIENT_TOKEN=PENDIENTE_CONFIGURAR a
// proposito (cero peticiones a Paddle desde una preview), y entonces
// pxStartCheckout sale temprano con "el pago aun no esta disponible". Sin
// esta deteccion el test fallaria en cada PR por una razon falsa.
const checkoutHabilitado = context.PADDLE_CLIENT_TOKEN !== "PENDIENTE_CONFIGURAR";

(async () => {
  // ── 0. La firma declara lo que el cuerpo usa ──
  //
  // Esto se comprueba SIEMPRE, configurado o no: es el bug que llego a
  // produccion. `anual` se usaba sin declararse y cada clic lanzaba
  // ReferenceError, con los dos botones de pago rotos.
  const firma = /function pxStartCheckout\(([^)]*)\)/.exec(source);
  assert(firma, "no se encontro pxStartCheckout");
  assert(/anual/.test(firma[1]),
    "pxStartCheckout debe declarar el parametro que usa para elegir el precio");

  if (!checkoutHabilitado) {
    console.log("runtime checkout tests: ok (checkout deshabilitado, solo firma)");
    return;
  }

  // ── 1. Cada boton abre el precio que le corresponde ──
  reset();
  context._pxUser = { id: "u1" };

  context.pxStartCheckout();
  assert(checkoutAbierto, "el checkout mensual no abrio");
  const idMensual = checkoutAbierto.items[0].priceId;
  assert.strictEqual(idMensual, context.PADDLE_PRICE_ID,
    "el boton mensual debe abrir el precio mensual");
  assert.strictEqual(checkoutAbierto.customData.user_id, "u1",
    "el checkout debe enviar el user_id: sin el, el webhook no sabe a quien dar acceso");

  checkoutAbierto = null;
  context.pxStartCheckout(true);
  assert(checkoutAbierto, "el checkout anual no abrio");
  assert.strictEqual(checkoutAbierto.items[0].priceId, context.PADDLE_PRICE_ID_ANNUAL || context.PADDLE_PRICE_ID,
    "el boton anual debe abrir el precio anual cuando existe");

  // ── 2. Sin plan anual configurado, el flag cae al mensual ──
  //
  // Nunca debe abrirse un checkout con un priceId vacio.
  if (!context.PADDLE_PRICE_ID_ANNUAL) {
    checkoutAbierto = null;
    context.pxStartCheckout(true);
    assert.strictEqual(checkoutAbierto.items[0].priceId, context.PADDLE_PRICE_ID,
      "sin precio anual, el flag debe caer al mensual, no abrir un checkout vacio");
  }

  // ── 3. Un suscriptor activo no puede comprar dos veces ──
  //
  // Cobrarle de nuevo a quien ya paga es el peor resultado de esta pagina.
  // La guarda vive DENTRO de la funcion: ocultar el boton no basta, porque
  // se puede invocar desde la consola o si el DOM cambia.
  reset();
  context._pxUser = { id: "u1" };
  context.pxShowPro();

  assert.strictEqual(elements.get("px-subscribe-btn").style.display, "none",
    "pxShowPro debe ocultar el boton mensual");
  assert.strictEqual(elements.get("px-subscribe-annual-btn").style.display, "none",
    "pxShowPro debe ocultar TAMBIEN el anual: se agrego despues y quedo visible para clientes Pro");

  checkoutAbierto = null;
  context.pxStartCheckout();
  assert.strictEqual(checkoutAbierto, null, "un suscriptor activo no debe abrir el checkout mensual");
  context.pxStartCheckout(true);
  assert.strictEqual(checkoutAbierto, null, "un suscriptor activo no debe abrir el checkout anual");

  // ── 4. Sin sesion no se abre el checkout ──
  //
  // El webhook necesita custom_data.user_id para ligar el pago a alguien.
  reset();
  context._pxUser = null;
  context._pxClient = null;
  loginPedido = null;
  context.pxStartCheckout();
  assert.strictEqual(checkoutAbierto, null,
    "sin sesion no debe abrirse el checkout: el pago quedaria sin dueño");
  // Y en vez de dejar al visitante varado, se le autentica en sitio.
  assert(loginPedido, "debe iniciarse el login cuando falta sesion");
  assert.match(loginPedido.options.redirectTo, /precios\.html$/,
    "el login debe devolver a precios, no a la landing: antes el visitante " +
    "aterrizaba en otra pagina sin pista de que debia volver a pagar");

  // ── 5. El retorno del pago espera al webhook ──
  //
  // Paddle es asincrono: una sola consulta llega antes que la escritura y
  // deja al comprador viendo "Suscribirme" despues de pagar.
  reset();
  context._pxUser = { id: "u1" };
  let consultas = 0;
  stubSupabase = {
    auth: { getSession: () => Promise.resolve({ data: { session: { user: { id: "u1" } } } }) },
    rpc: () => { consultas++; return Promise.resolve({ data: { subscribed: consultas >= 3 } }); },
  };
  context._pxClient = null;
  context.window.location.search = "?checkout=success";

  context.pxInitAuth();
  await flush();

  assert(consultas >= 3, `debe reintentar hasta que el webhook escriba (consultas: ${consultas})`);
  assert.strictEqual(elements.get("px-subscribe-btn").style.display, "none",
    "tras confirmarse la suscripcion, el boton debe ocultarse");
  assert.match(elements.get("px-sub-status").innerHTML, /Pro/,
    "debe confirmarse el acceso Pro al comprador");

  // ── 6. Los tokens de OAuth no quedan en la URL ──
  //
  // Supabase los deja en el fragmento por el flujo implicito y no los
  // limpia solo. Quedaban visibles en la barra de direcciones, el
  // historial y cualquier captura compartida.
  reset();
  let urlLimpiada = null;
  context.history.replaceState = (a, b, url) => { urlLimpiada = url; };
  context.window.location.hash = "#access_token=FALSO&refresh_token=X";
  context.pxStripTokens();
  assert(urlLimpiada && !/access_token/.test(urlLimpiada),
    "el fragmento con los tokens debe borrarse de la URL");

  console.log("runtime checkout tests: ok");
})().catch(err => {
  console.error(err);
  process.exit(1);
});
