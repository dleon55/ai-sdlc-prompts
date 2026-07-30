// Supabase Edge Function — recibe los webhooks de Paddle Billing y
// actualiza la tabla `subscriptions` (ver supabase/subscriptions.sql).
//
// Desplegada automáticamente por .github/workflows/deploy.yml en cada push
// a main (job deploy-supabase-function). Requiere el secreto
// PADDLE_WEBHOOK_SECRET configurado en Supabase (Project Settings > Edge
// Functions > Secrets, o `supabase secrets set`) -- NUNCA en el repo.
// SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY los inyecta Supabase
// automáticamente en el runtime de toda Edge Function, no hay que
// configurarlos aparte.
//
// Verificación de firma: Paddle manda el header `Paddle-Signature` con el
// formato `ts=<unix_timestamp>;h1=<hmac_hex>`. El HMAC-SHA256 se calcula
// sobre el string `${ts}:${raw_body}` (el body TAL CUAL llegó, antes de
// parsear JSON -- si se re-serializa el JSON el hash no coincide). Sin
// verificar esto, cualquiera podría mandar un POST falso diciendo "ya
// pagué" y auto-otorgarse acceso ilimitado.
//
// Supuesto a validar contra la documentación real de Paddle (no verificado
// en runtime todavía, ver docs/paddle-integration.md): el nombre exacto de
// los campos `event_type`, `data.custom_data.user_id`,
// `data.current_billing_period.ends_at` puede variar ligeramente; probar
// primero con el botón "Send test event" del dashboard de Paddle antes de
// conectar el checkout real.

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const PADDLE_WEBHOOK_SECRET = Deno.env.get("PADDLE_WEBHOOK_SECRET") ?? "";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);

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

  let payload: any;
  try {
    payload = JSON.parse(rawBody);
  } catch {
    return new Response("Invalid JSON", { status: 400 });
  }

  const eventType: string = payload.event_type ?? "";
  const eventId: string = payload.event_id ?? "";
  const data = payload.data ?? {};
  const occurredAt: string = payload.occurred_at ?? "";

  if (!eventId || !occurredAt || Number.isNaN(Date.parse(occurredAt))) {
    return new Response("Missing or invalid event metadata", { status: 400 });
  }

  const userId: string | undefined = data.custom_data?.user_id;
  const paddleSubscriptionId: string | undefined = data.id;
  const paddleCustomerId: string | undefined = data.customer_id;
  const status: string = ACTIVE_STATUSES.has(data.status) ? "active" : (data.status ?? "unknown");
  const currentPeriodEnd: string | null = data.current_billing_period?.ends_at ?? null;

  if (eventType.startsWith("subscription.") && !paddleSubscriptionId) {
    return new Response("Missing subscription id", { status: 400 });
  }

  const { data: applied, error } = await supabase.rpc("apply_paddle_subscription_event", {
    p_event_id: eventId,
    p_event_type: eventType,
    p_occurred_at: occurredAt,
    p_user_id: userId ?? null,
    p_subscription_id: paddleSubscriptionId ?? null,
    p_customer_id: paddleCustomerId ?? null,
    p_status: status,
    p_current_period_end: currentPeriodEnd,
  });
  if (error) {
    console.error("webhook event transaction failed:", error);
    return new Response("DB error", { status: 500 });
  }

  return new Response(applied ? "OK" : "Already processed", { status: 200 });
});
