// Endpoint propio del webhook de Paddle Billing. Portado desde
// supabase/functions/paddle-webhook/index.ts (Deno) como parte de la Fase
// 1 de docs/PLAN_MIGRACION_SUPABASE_A_LOCAL.md -- misma logica de
// verificacion de firma y los mismos criterios de aceptacion de eventos;
// unico cambio real: `supabase.rpc(...)` se vuelve una llamada SQL directa
// a la funcion `apply_paddle_subscription_event` (portada tal cual en
// backend/src/schema.sql), sin pasar por PostgREST.
//
// Verificacion de firma: Paddle manda el header `Paddle-Signature` con el
// formato `ts=<unix_timestamp>;h1=<hmac_hex>`. El HMAC-SHA256 se calcula
// sobre el string `${ts}:${raw_body}` (el body TAL CUAL llego, antes de
// parsear JSON). Sin verificar esto, cualquiera podria mandar un POST
// falso diciendo "ya pague" y auto-otorgarse acceso ilimitado.
import { Router, type Request } from "express";
import { pool } from "../../db.ts";
import { crearAlertador, mensajeDe } from "./alertas.ts";

export const paddleWebhookRouter = Router();

const alertar = crearAlertador({ webhookUrl: process.env.ALERTAS_WEBHOOK_URL ?? "" });

// Paddle reporta el estado de la suscripcion con estos valores; solo
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

export async function hmacHex(secret: string, message: string): Promise<string> {
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

export function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

interface ParametrosEvento {
  p_event_id: string;
  p_event_type: string;
  p_occurred_at: string;
  p_user_id: string | null;
  p_subscription_id: string | null;
  p_customer_id: string | null;
  p_status: string;
  p_current_period_end: string | null;
}

// req.body es un string crudo: ver backend/src/index.ts, donde esta ruta
// se monta con express.text({ type: () => true }) ANTES del parser JSON
// global, exactamente para conservar el body intacto que la firma firmo.
paddleWebhookRouter.post("/", async (req: Request, res) => {
  const PADDLE_WEBHOOK_SECRET = process.env.PADDLE_WEBHOOK_SECRET ?? "";
  const rawBody = typeof req.body === "string" ? req.body : "";

  const signatureHeader = req.headers["paddle-signature"];
  const signatureHeaderStr = Array.isArray(signatureHeader) ? signatureHeader[0] ?? "" : signatureHeader ?? "";
  const parts = signatureHeaderStr.split(";").map((part) => part.trim().split("=", 2));
  const ts = parts.find(([key]) => key === "ts")?.[1];
  const signatures = parts.filter(([key]) => key === "h1").map(([, value]) => value as string);

  if (!ts || signatures.length === 0 || !PADDLE_WEBHOOK_SECRET) {
    res.status(401).send("Missing signature");
    return;
  }

  const timestamp = Number(ts);
  const now = Math.floor(Date.now() / 1000);
  if (!Number.isInteger(timestamp) || Math.abs(now - timestamp) > MAX_SIGNATURE_AGE_SECONDS) {
    res.status(408).send("Expired signature");
    return;
  }

  const expected = await hmacHex(PADDLE_WEBHOOK_SECRET, `${ts}:${rawBody}`);
  if (!signatures.some((signature) => timingSafeEqual(expected, signature))) {
    res.status(401).send("Invalid signature");
    return;
  }

  let payload: unknown;
  try {
    payload = JSON.parse(rawBody);
  } catch {
    res.status(400).send("Invalid JSON");
    return;
  }
  if (!esObjeto(payload)) {
    res.status(400).send("Invalid JSON");
    return;
  }

  const eventType = texto(payload.event_type) ?? "";
  const eventId = texto(payload.event_id) ?? "";
  const data: Json = esObjeto(payload.data) ? payload.data : {};
  const occurredAt = texto(payload.occurred_at) ?? "";

  if (!eventId || !occurredAt || Number.isNaN(Date.parse(occurredAt))) {
    res.status(400).send("Missing or invalid event metadata");
    return;
  }

  let params: ParametrosEvento;

  if (eventType.startsWith("subscription.")) {
    const paddleSubscriptionId = texto(data.id);
    if (!paddleSubscriptionId) {
      res.status(400).send("Missing subscription id");
      return;
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
    const { rows } = await pool.query<{ applied: boolean }>(
      `select apply_paddle_subscription_event($1, $2, $3, $4, $5, $6, $7, $8) as applied`,
      [
        params.p_event_id,
        params.p_event_type,
        params.p_occurred_at,
        params.p_user_id,
        params.p_subscription_id,
        params.p_customer_id,
        params.p_status,
        params.p_current_period_end,
      ],
    );
    const applied = rows[0]?.applied ?? false;
    res.status(200).send(applied ? "OK" : "Already processed");
  } catch (error) {
    console.error("webhook event transaction failed:", error);
    await alertar({
      clave: "webhook_error",
      detalle: {
        event_id: eventId,
        event_type: eventType,
        http_status: 500,
        error_message: mensajeDe(error),
      },
    });
    res.status(500).send("DB error");
  }
});
