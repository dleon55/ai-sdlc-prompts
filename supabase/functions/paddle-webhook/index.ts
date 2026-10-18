// Supabase Edge Function — recibe los webhooks de Paddle Billing y
// actualiza la tabla `subscriptions` (ver supabase/subscriptions.sql).
//
// Desplegada automáticamente por .github/workflows/deploy.yml en cada push
// a main (job deploy-supabase-function). Requiere el secreto
// PADDLE_WEBHOOK_SECRET configurado en Supabase (Project Settings > Edge
// Functions > Secrets, o `supabase secrets set`) -- NUNCA en el repo.
// SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY los inyecta Supabase
// automáticamente en el runtime de toda Edge Function, no hay que
// configurarlos aparte. ALERTAS_WEBHOOK_URL es opcional (ver alertas.ts).
//
// Verificación de firma: Paddle manda el header `Paddle-Signature` con el
// formato `ts=<unix_timestamp>;h1=<hmac_hex>`. El HMAC-SHA256 se calcula
// sobre el string `${ts}:${raw_body}` (el body TAL CUAL llegó, antes de
// parsear JSON -- si se re-serializa el JSON el hash no coincide). Sin
// verificar esto, cualquiera podría mandar un POST falso diciendo "ya
// pagué" y auto-otorgarse acceso ilimitado.
//
// Eventos que maneja:
//   subscription.*     -> apply_paddle_subscription_event cambia el estado
//                         de la suscripción (idempotente y ordenado por
//                         occurred_at, ver migraciones 20260730/20260731).
//   adjustment.created -> reembolsos, créditos y contracargos emitidos
//                         desde el dashboard de Paddle (issue #232, T3). Se
//                         registra en paddle_webhook_events como procesado
//                         SIN tocar subscriptions: el acceso se degrada con
//                         el subscription.canceled que Paddle emite aparte
//                         cuando el reembolso cancela la suscripción. Se
//                         avisa al operador (alerta `reembolso`) para que
//                         confirme en Paddle que la suscripción quedó como
//                         debe, porque un reembolso sin cancelación deja al
//                         cliente con acceso pagado por un cobro devuelto.
//   cualquier otro     -> se registra como procesado y se responde 200,
//                         para que Paddle no reintente eventos que no nos
//                         interesan.
//
// Supuesto a validar contra la documentación real de Paddle (no verificado
// en runtime todavía, ver docs/paddle-integration.md): el nombre exacto de
// los campos `event_type`, `data.custom_data.user_id`,
// `data.current_billing_period.ends_at` puede variar ligeramente; probar
// primero con el botón "Send test event" del dashboard de Paddle antes de
// conectar el checkout real.

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { crearAlertador, mensajeDe } from "./alertas.ts";

const PADDLE_WEBHOOK_SECRET = Deno.env.get("PADDLE_WEBHOOK_SECRET") ?? "";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);

// Una sola instancia por aislado: la deduplicación de una hora vive en su
// memoria. Solo lee la URL del destino; nunca recibe el secreto de Paddle.
const alertar = crearAlertador({ webhookUrl: Deno.env.get("ALERTAS_WEBHOOK_URL") ?? "" });

async function hmacHex(secret: string, message: string): Promise<string> {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(message));
  return Array.from(new Uint8Array(sig))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

// Paddle reporta el estado de la suscripción con estos valores; solo
// 'active' y 'trialing' cuentan como acceso pagado vigente para nuestro
// gate -- el resto (canceled, past_due, paused) cae de vuelta al muro de
// prueba gratuita normal.
const ACTIVE_STATUSES = new Set(["active", "trialing"]);
const MAX_SIGNATURE_AGE_SECONDS = 300;

type Json = Record<string, unknown>;

function esObjeto(valor: unknown): valor is Json {
  return typeof valor === "object" && valor !== null && !Array.isArray(valor);
}

function texto(valor: unknown): string | undefined {
  return typeof valor === "string" ? valor : undefined;
}

// Parámetros de apply_paddle_subscription_event. Para eventos que no son
// subscription.* la función SQL solo registra el evento y lo marca como
// procesado; los campos de suscripción van en null a propósito.
// `type` y no `interface`: el cliente de Supabase tipa los argumentos del
// RPC como Record<string, unknown>, y una interface no tiene la firma de
// índice implícita que sí tiene un alias de tipo.
type ParametrosEvento = {
  p_event_id: string;
  p_event_type: string;
  p_occurred_at: string;
  p_user_id: string | null;
  p_subscription_id: string | null;
  p_customer_id: string | null;
  p_status: string;
  p_current_period_end: string | null;
};

Deno.serve(async (req) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  const rawBody = await req.text();
  const signatureHeader = req.headers.get("Paddle-Signature") ?? "";
  const parts = signatureHeader.split(";").map((part) => part.trim().split("=", 2));
  const ts = parts.find(([key]) => key === "ts")?.[1];
  const signatures = parts.filter(([key]) => key === "h1").map(([, value]) => value);

  if (!ts || signatures.length === 0 || !PADDLE_WEBHOOK_SECRET) {
    return new Response("Missing signature", { status: 401 });
  }

  const timestamp = Number(ts);
  const now = Math.floor(Date.now() / 1000);
  if (!Number.isInteger(timestamp) || Math.abs(now - timestamp) > MAX_SIGNATURE_AGE_SECONDS) {
    return new Response("Expired signature", { status: 408 });
  }

  const expected = await hmacHex(PADDLE_WEBHOOK_SECRET, `${ts}:${rawBody}`);
  if (!signatures.some((signature) => timingSafeEqual(expected, signature))) {
    return new Response("Invalid signature", { status: 401 });
  }

  let payload: unknown;
  try {
    payload = JSON.parse(rawBody);
  } catch {
    return new Response("Invalid JSON", { status: 400 });
  }
  if (!esObjeto(payload)) {
    return new Response("Invalid JSON", { status: 400 });
  }

  const eventType = texto(payload.event_type) ?? "";
  const eventId = texto(payload.event_id) ?? "";
  const data: Json = esObjeto(payload.data) ? payload.data : {};
  const occurredAt = texto(payload.occurred_at) ?? "";

  if (!eventId || !occurredAt || Number.isNaN(Date.parse(occurredAt))) {
    return new Response("Missing or invalid event metadata", { status: 400 });
  }

  let params: ParametrosEvento;

  if (eventType.startsWith("subscription.")) {
    const paddleSubscriptionId = texto(data.id);
    if (!paddleSubscriptionId) {
      return new Response("Missing subscription id", { status: 400 });
    }
    const customData = esObjeto(data.custom_data) ? data.custom_data : {};
    const periodo = esObjeto(data.current_billing_period) ? data.current_billing_period : {};
    const estadoPaddle = texto(data.status);
    params = {
      p_event_id: eventId,
      p_event_type: eventType,
      p_occurred_at: occurredAt,
      p_user_id: texto(customData.user_id) ?? null,
      p_subscription_id: paddleSubscriptionId,
      p_customer_id: texto(data.customer_id) ?? null,
      p_status: estadoPaddle && ACTIVE_STATUSES.has(estadoPaddle) ? "active" : (estadoPaddle ?? "unknown"),
      p_current_period_end: texto(periodo.ends_at) ?? null,
    };
  } else {
    // adjustment.created y cualquier otro evento suscrito: solo registro.
    // Para un ajuste, `data.id` es el adj_… y `data.subscription_id` la
    // suscripción afectada; ninguno se usa para cambiar estado.
    params = {
      p_event_id: eventId,
      p_event_type: eventType,
      p_occurred_at: occurredAt,
      p_user_id: null,
      p_subscription_id: null,
      p_customer_id: texto(data.customer_id) ?? null,
      p_status: texto(data.action) ?? texto(data.status) ?? "n/a",
      p_current_period_end: null,
    };
  }

  if (eventType === "adjustment.created") {
    // Sin importes ni datos del cliente: el operador los ve en Paddle. Lo
    // que importa aquí es que exista un aviso con el id para buscarlo.
    const detalle = {
      event_id: eventId,
      adjustment_id: texto(data.id) ?? null,
      action: texto(data.action) ?? null,
      status: texto(data.status) ?? null,
      subscription_id: texto(data.subscription_id) ?? null,
      transaction_id: texto(data.transaction_id) ?? null,
    };
    console.log("adjustment.created recibido:", JSON.stringify(detalle));
    await alertar({ clave: "reembolso", detalle });
  }

  try {
    const { data: applied, error } = await supabase.rpc("apply_paddle_subscription_event", params);
    if (error) {
      // El objeto de error de PostgREST trae message/details/hint/code; no
      // trae credenciales. Se pasan por `alertar`, que además filtra por
      // nombre de clave cualquier cosa que parezca un secreto.
      console.error("webhook event transaction failed:", error);
      await alertar({
        clave: "webhook_error",
        detalle: {
          event_id: eventId,
          event_type: eventType,
          http_status: 500,
          error_code: texto(error.code) ?? null,
          error_message: texto(error.message) ?? null,
        },
      });
      return new Response("DB error", { status: 500 });
    }
    return new Response(applied ? "OK" : "Already processed", { status: 200 });
  } catch (error) {
    // La llamada al RPC lanzó (red, timeout, cliente): también es un 500 y
    // también merece aviso. Paddle reintentará; el operador debe saberlo.
    console.error("webhook event transaction threw:", mensajeDe(error));
    await alertar({
      clave: "webhook_error",
      detalle: {
        event_id: eventId,
        event_type: eventType,
        http_status: 500,
        error_message: mensajeDe(error),
      },
    });
    return new Response("DB error", { status: 500 });
  }
});
