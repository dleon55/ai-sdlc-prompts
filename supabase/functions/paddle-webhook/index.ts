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

Deno.serve(async (req) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  const rawBody = await req.text();
  const signatureHeader = req.headers.get("Paddle-Signature") ?? "";
  const parts = Object.fromEntries(
    signatureHeader.split(";").map((p) => p.split("=") as [string, string]),
  );
  const ts = parts["ts"];
  const h1 = parts["h1"];

  if (!ts || !h1 || !PADDLE_WEBHOOK_SECRET) {
    return new Response("Missing signature", { status: 401 });
  }

  const expected = await hmacHex(PADDLE_WEBHOOK_SECRET, `${ts}:${rawBody}`);
  if (!timingSafeEqual(expected, h1)) {
    return new Response("Invalid signature", { status: 401 });
  }

  let payload: any;
  try {
    payload = JSON.parse(rawBody);
  } catch {
    return new Response("Invalid JSON", { status: 400 });
  }

  const eventType: string = payload.event_type ?? "";
  const data = payload.data ?? {};

  if (!eventType.startsWith("subscription.")) {
    // Otros eventos (transaction.*, etc.) no son relevantes para el gate.
    return new Response("Ignored", { status: 200 });
  }

  const userId: string | undefined = data.custom_data?.user_id;
  const paddleSubscriptionId: string | undefined = data.id;
  const paddleCustomerId: string | undefined = data.customer_id;
  const status: string = ACTIVE_STATUSES.has(data.status) ? "active" : (data.status ?? "unknown");
  const currentPeriodEnd: string | null = data.current_billing_period?.ends_at ?? null;

  if (!paddleSubscriptionId) {
    return new Response("Missing subscription id", { status: 400 });
  }

  if (userId) {
    // subscription.created siempre trae el custom_data que mandamos en el
    // checkout -- este es el único punto donde correlacionamos la
    // suscripción de Paddle con el usuario real de Supabase.
    const { error } = await supabase.from("subscriptions").upsert({
      user_id: userId,
      paddle_subscription_id: paddleSubscriptionId,
      paddle_customer_id: paddleCustomerId,
      status,
      current_period_end: currentPeriodEnd,
      updated_at: new Date().toISOString(),
    });
    if (error) {
      console.error("upsert por user_id fallo:", error);
      return new Response("DB error", { status: 500 });
    }
  } else {
    // subscription.updated/canceled no siempre repiten custom_data --
    // actualizamos por paddle_subscription_id, que ya vinculamos antes.
    const { error } = await supabase
      .from("subscriptions")
      .update({
        status,
        current_period_end: currentPeriodEnd,
        updated_at: new Date().toISOString(),
      })
      .eq("paddle_subscription_id", paddleSubscriptionId);
    if (error) {
      console.error("update por paddle_subscription_id fallo:", error);
      return new Response("DB error", { status: 500 });
    }
  }

  return new Response("OK", { status: 200 });
});
