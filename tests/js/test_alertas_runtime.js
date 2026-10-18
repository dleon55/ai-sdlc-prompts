// Ejecuta alertas.ts (Edge Function paddle-webhook) en Node, de verdad.
//
// No hay Deno en CI ni en local, y una alerta que no se prueba es una
// alerta que falla justo cuando hace falta. El modulo no toca Deno.* a
// proposito: recibe fetch, reloj y log por inyeccion, asi que Node lo
// ejecuta tal cual con type stripping (Node >= 22.6).
//
// Se relanza a si mismo con --experimental-strip-types si no viene ya con
// el flag, para que `node tests/js/*.js` lo corra sin cambios en CI.

const assert = require("assert");
const path = require("path");
const { pathToFileURL } = require("url");
const { spawnSync } = require("child_process");

const FLAG = "--experimental-strip-types";
if (!process.execArgv.includes(FLAG)) {
  const r = spawnSync(process.execPath, [FLAG, "--no-warnings", __filename], { stdio: "inherit" });
  process.exit(r.status === null ? 1 : r.status);
}

const modulo = pathToFileURL(
  path.resolve(__dirname, "..", "..", "supabase", "functions", "paddle-webhook", "alertas.ts"),
).href;

(async () => {
  const { crearAlertador, limpiarDetalle, VENTANA_DEDUP_MS } = await import(modulo);

  // ── 1. Sin destino configurado: solo log, nunca red ──
  {
    const logs = [];
    let llamadasFetch = 0;
    const alertar = crearAlertador({
      webhookUrl: "",
      fetchImpl: async () => { llamadasFetch++; return { ok: true, status: 200 }; },
      log: (m, d) => logs.push([m, d]),
    });
    const r = await alertar({ clave: "webhook_error", detalle: { event_id: "evt_1", http_status: 500 } });
    assert.strictEqual(r, "solo_log");
    assert.strictEqual(llamadasFetch, 0, "sin ALERTAS_WEBHOOK_URL no debe haber red");
    assert.strictEqual(logs.length, 1);
    assert.strictEqual(logs[0][0], "ALERTA webhook_error");
    assert.strictEqual(logs[0][1].producto, "ai-sdlc-pro");
    assert.strictEqual(logs[0][1].detalle.event_id, "evt_1");
  }

  // ── 2. Con destino: POST JSON con texto para Slack/Discord y campos ──
  {
    const peticiones = [];
    const alertar = crearAlertador({
      webhookUrl: "https://hooks.example/abc",
      fetchImpl: async (url, init) => { peticiones.push({ url, init }); return { ok: true, status: 200 }; },
      log: () => {},
      ahora: () => 1_000_000,
    });
    const r = await alertar({ clave: "reembolso", detalle: { event_id: "evt_2", action: "refund" } });
    assert.strictEqual(r, "enviada");
    assert.strictEqual(peticiones.length, 1);
    assert.strictEqual(peticiones[0].url, "https://hooks.example/abc");
    assert.strictEqual(peticiones[0].init.method, "POST");
    assert.strictEqual(peticiones[0].init.headers["Content-Type"], "application/json");
    const cuerpo = JSON.parse(peticiones[0].init.body);
    assert.strictEqual(cuerpo.producto, "ai-sdlc-pro");
    assert.strictEqual(cuerpo.clave, "reembolso");
    assert.deepStrictEqual(cuerpo.detalle, { event_id: "evt_2", action: "refund" });
    assert.match(cuerpo.text, /^\[ai-sdlc-pro\] reembolso — event_id=evt_2 action=refund$/);
    assert.strictEqual(cuerpo.content, cuerpo.text, "Discord lee `content`, Slack `text`");
    assert.strictEqual(cuerpo.fecha, new Date(1_000_000).toISOString());
  }

  // ── 3. Deduplicacion: misma clave+id durante 1 h ──
  {
    let t = 0;
    let envios = 0;
    const alertar = crearAlertador({
      webhookUrl: "https://hooks.example/abc",
      fetchImpl: async () => { envios++; return { ok: true, status: 200 }; },
      log: () => {},
      ahora: () => t,
    });
    assert.strictEqual(await alertar({ clave: "webhook_error", detalle: { event_id: "evt_3" } }), "enviada");
    t += 5 * 60 * 1000; // Paddle reintenta a los pocos minutos
    assert.strictEqual(await alertar({ clave: "webhook_error", detalle: { event_id: "evt_3" } }), "deduplicada");
    assert.strictEqual(envios, 1, "el reintento de Paddle no debe generar una segunda alerta");
    // Otro evento, misma clave: si se avisa.
    assert.strictEqual(await alertar({ clave: "webhook_error", detalle: { event_id: "evt_4" } }), "enviada");
    // Misma id, otra clave: tambien.
    assert.strictEqual(await alertar({ clave: "reembolso", detalle: { event_id: "evt_3" } }), "enviada");
    assert.strictEqual(envios, 3);
    // Pasada la ventana, se vuelve a avisar.
    t += VENTANA_DEDUP_MS + 1;
    assert.strictEqual(await alertar({ clave: "webhook_error", detalle: { event_id: "evt_3" } }), "enviada");
    assert.strictEqual(envios, 4);
  }

  // ── 4. Nunca lanza: red caida, respuesta no-2xx, log roto ──
  {
    const caida = crearAlertador({
      webhookUrl: "https://hooks.example/abc",
      fetchImpl: async () => { throw new Error("ECONNREFUSED"); },
      log: () => {},
    });
    assert.strictEqual(await caida({ clave: "webhook_error", detalle: { event_id: "evt_5" } }), "fallo_webhook");

    const rechazo = crearAlertador({
      webhookUrl: "https://hooks.example/abc",
      fetchImpl: async () => ({ ok: false, status: 503 }),
      log: () => {},
    });
    assert.strictEqual(await rechazo({ clave: "webhook_error", detalle: { event_id: "evt_6" } }), "fallo_webhook");

    const logRoto = crearAlertador({
      webhookUrl: "",
      log: () => { throw new Error("stdout cerrado"); },
    });
    const errores = [];
    const consoleError = console.error;
    console.error = (...a) => errores.push(a);
    try {
      const r = await logRoto({ clave: "webhook_error", detalle: { event_id: "evt_7" } });
      assert.strictEqual(r, "solo_log", "ni un log roto debe tumbar al webhook que avisa");
    } finally {
      console.error = consoleError;
    }
    assert(errores.length >= 1, "el fallo interno se reporta por console.error");
  }

  // ── 5. Nunca viajan secretos ni cuerpos enormes ──
  {
    const limpio = limpiarDetalle({
      event_id: "evt_8",
      PADDLE_WEBHOOK_SECRET: "whsec_x",
      access_token: "t",
      Authorization: "Bearer y",
      signature: "h1=z",
      service_role_key: "k",
      api_key: "a",
      mensaje: "x".repeat(600),
    });
    assert.deepStrictEqual(Object.keys(limpio).sort(), ["event_id", "mensaje"]);
    assert.strictEqual(limpio.mensaje.length, 501, "se trunca a 500 + elipsis");
    assert(limpio.mensaje.endsWith("…"));

    const peticiones = [];
    const alertar = crearAlertador({
      webhookUrl: "https://hooks.example/abc",
      fetchImpl: async (url, init) => { peticiones.push(init.body); return { ok: true, status: 200 }; },
      log: () => {},
    });
    await alertar({ clave: "webhook_error", detalle: { event_id: "evt_9", PADDLE_WEBHOOK_SECRET: "whsec_x" } });
    assert(!peticiones[0].includes("whsec_x"), "el secreto no debe salir en el POST");
  }

  console.log("runtime alertas tests: ok");
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
