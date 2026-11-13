import { Router } from "express";
import type { Pool, PoolClient } from "pg";
import { requireAuth } from "../auth/middleware.ts";
import { pool, withTransaction } from "../db.ts";
import { asincrono } from "../asincrono.ts";

export const trialRouter = Router();
trialRouter.use(requireAuth);

// ───────────────────────── Politica de la prueba ─────────────────────────
// Una prueba de 7 dias + TRIAL_MAX_RENEWALS renovaciones con feedback (por
// omision 1: dos semanas en total). Antes no habia tope y cualquier usuario
// renovaba cada semana para siempre con una estrella (spec E1, 13-nov-2026).
//
// TRIAL_GRACE_UNTIL: hasta esa fecha, quien ya agoto las renovaciones puede
// renovar UNA vez mas (cortesia para los usuarios que ya tenian la prueba
// cuando entro el tope, para que no la pierdan de golpe). Fecha AAAA-MM-DD
// = fin de ese dia en hora del centro de Mexico (UTC-6, sin horario de
// verano desde 2022). Vacio, "off" o "none" la desactiva.
export const DEFAULT_MAX_RENEWALS = 1;
export const DEFAULT_GRACE_UNTIL = "2026-11-30";
// Solo se renueva si la prueba ya vencio o vence en menos de esto: evita
// "renovar por adelantado" y acumular semanas.
export const RENEWAL_WINDOW_HOURS = 48;

export interface TrialPolicy {
  maxRenewals: number;
  graceUntil: Date | null;
}

export function parseMaxRenewals(raw: string | undefined): number {
  if (raw === undefined || raw.trim() === "") return DEFAULT_MAX_RENEWALS;
  if (!/^\d{1,4}$/.test(raw.trim())) {
    console.warn(`TRIAL_MAX_RENEWALS invalido (${JSON.stringify(raw)}); se usa ${DEFAULT_MAX_RENEWALS}`);
    return DEFAULT_MAX_RENEWALS;
  }
  return Number(raw.trim());
}

export function parseGraceUntil(raw: string | undefined): Date | null {
  const valor = raw === undefined ? DEFAULT_GRACE_UNTIL : raw.trim();
  if (valor === "" || /^(off|none|no)$/i.test(valor)) return null;
  const iso = /^\d{4}-\d{2}-\d{2}$/.test(valor) ? `${valor}T23:59:59.999-06:00` : valor;
  const fecha = new Date(iso);
  if (Number.isNaN(fecha.getTime())) {
    console.warn(`TRIAL_GRACE_UNTIL invalido (${JSON.stringify(raw)}); se usa ${DEFAULT_GRACE_UNTIL}`);
    return parseGraceUntil(DEFAULT_GRACE_UNTIL);
  }
  return fecha;
}

export function trialPolicyFromEnv(env: NodeJS.ProcessEnv = process.env): TrialPolicy {
  return {
    maxRenewals: parseMaxRenewals(env.TRIAL_MAX_RENEWALS),
    graceUntil: parseGraceUntil(env.TRIAL_GRACE_UNTIL),
  };
}

const politica = trialPolicyFromEnv();

// Renovaciones que le quedan al usuario. Es una pista para la UI (decide si
// el muro ofrece renovar o pasar a Pro); la regla real es el UPDATE de
// renewTrialWithFeedback().
export function renewalsLeft(
  renewedCount: number,
  courtesyUsed: boolean,
  policy: TrialPolicy,
  now: Date = new Date(),
): number {
  const base = Math.max(0, policy.maxRenewals - renewedCount);
  const cortesia = !courtesyUsed && policy.graceUntil !== null && now < policy.graceUntil ? 1 : 0;
  return base + cortesia;
}

interface TrialStatus {
  active: boolean;
  expires_at: string | null;
  no_trial_row: boolean;
  subscribed: boolean;
  // null con suscripcion activa: no aplica.
  renewals_left: number | null;
  max_renewals: number;
}

async function tieneSuscripcionActiva(db: Pool | PoolClient, userId: string) {
  const { rows } = await db.query<{ status: string; current_period_end: string | null }>(
    "select status, current_period_end from subscriptions where user_id = $1",
    [userId],
  );
  return rows.length > 0 && rows[0]!.status === "active" ? rows[0]! : null;
}

// Estado de la prueba: revisa primero si hay una suscripcion de pago activa (acceso ilimitado sin
// importar la prueba), y solo si no la hay cae al estado de user_trial,
// autocreando la fila si falta (una fila ausente nunca debe leerse como
// "prueba vencida").
export async function checkTrialStatus(userId: string, policy: TrialPolicy = politica): Promise<TrialStatus> {
  const sub = await tieneSuscripcionActiva(pool, userId);
  if (sub) {
    return {
      active: true,
      expires_at: sub.current_period_end,
      no_trial_row: false,
      subscribed: true,
      renewals_left: null,
      max_renewals: policy.maxRenewals,
    };
  }

  const { rows } = await pool.query<{
    trial_expires_at: string;
    renewed_count: number;
    courtesy_renewal_at: string | null;
  }>(
    `insert into user_trial (user_id) values ($1)
     on conflict (user_id) do update set user_id = excluded.user_id
     returning trial_expires_at, renewed_count, courtesy_renewal_at`,
    [userId],
  );
  const fila = rows[0]!;

  return {
    active: new Date(fila.trial_expires_at).getTime() > Date.now(),
    expires_at: fila.trial_expires_at,
    no_trial_row: false,
    subscribed: false,
    renewals_left: renewalsLeft(fila.renewed_count, fila.courtesy_renewal_at !== null, policy),
    max_renewals: policy.maxRenewals,
  };
}

export type RenewalResult =
  | { renewed: true; new_expires_at: string; renewals_left: number; courtesy: boolean }
  | {
      renewed: false;
      reason: "renewal_limit" | "trial_active" | "subscribed";
      renewals_used: number;
      max: number;
      expires_at?: string;
    };

// Guarda el feedback SIEMPRE (vale aunque no renueve) y renueva 1 semana si:
// no hay suscripcion activa, la prueba vencio o vence en <= 48 h, y quedan
// renovaciones (o la de cortesia sigue disponible). Todo en una transaccion,
// y la condicion va en el WHERE del UPDATE: con dos peticiones simultaneas
// la segunda espera el bloqueo de la fila, reevalua el WHERE contra la fila
// ya renovada y no renueva otra vez.
export async function renewTrialWithFeedback(
  userId: string,
  rating: number,
  comments: string | null,
  policy: TrialPolicy = politica,
): Promise<RenewalResult> {
  return withTransaction(async (client) => {
    await client.query("insert into feedback (user_id, rating, comments) values ($1, $2, $3)", [
      userId,
      rating,
      comments,
    ]);
    await client.query("insert into user_trial (user_id) values ($1) on conflict (user_id) do nothing", [userId]);

    if (await tieneSuscripcionActiva(client, userId)) {
      const { rows } = await client.query<{ renewed_count: number }>(
        "select renewed_count from user_trial where user_id = $1",
        [userId],
      );
      return {
        renewed: false,
        reason: "subscribed",
        renewals_used: rows[0]!.renewed_count,
        max: policy.maxRenewals,
      };
    }

    const graceIso = policy.graceUntil ? policy.graceUntil.toISOString() : null;
    const condicionCupo = `(renewed_count < $2
         or ($3::timestamptz is not null and now() < $3::timestamptz and courtesy_renewal_at is null))`;
    const ventana = `trial_expires_at < now() + interval '${RENEWAL_WINDOW_HOURS} hours'`;

    const { rows } = await client.query<{
      trial_expires_at: string;
      renewed_count: number;
      courtesy_renewal_at: string | null;
      fue_cortesia: boolean;
    }>(
      `update user_trial set
         trial_expires_at = now() + interval '1 week',
         renewed_count = renewed_count + 1,
         courtesy_renewal_at = case when renewed_count >= $2 then now() else courtesy_renewal_at end
       where user_id = $1 and ${ventana} and ${condicionCupo}
       returning trial_expires_at, renewed_count, courtesy_renewal_at,
                 (courtesy_renewal_at is not null and renewed_count - 1 >= $2) as fue_cortesia`,
      [userId, policy.maxRenewals, graceIso],
    );
    if (rows.length > 0) {
      const fila = rows[0]!;
      return {
        renewed: true,
        new_expires_at: fila.trial_expires_at,
        renewals_left: renewalsLeft(fila.renewed_count, fila.courtesy_renewal_at !== null, policy),
        courtesy: fila.fue_cortesia,
      };
    }

    const { rows: actual } = await client.query<{
      trial_expires_at: string;
      renewed_count: number;
      con_cupo: boolean;
    }>(
      `select trial_expires_at, renewed_count, ${condicionCupo} as con_cupo
       from user_trial where user_id = $1`,
      [userId, policy.maxRenewals, graceIso],
    );
    const fila = actual[0]!;
    return {
      renewed: false,
      reason: fila.con_cupo ? "trial_active" : "renewal_limit",
      renewals_used: fila.renewed_count,
      max: policy.maxRenewals,
      expires_at: fila.trial_expires_at,
    };
  });
}

trialRouter.get("/status", asincrono(async (req, res) => {
  res.json(await checkTrialStatus(req.session!.userId));
}));

trialRouter.post("/feedback", asincrono(async (req, res) => {
  const rating = Number(req.body?.rating);
  const comments = typeof req.body?.comments === "string" ? req.body.comments : null;
  if (!Number.isInteger(rating) || rating < 1 || rating > 5) {
    res.status(400).json({ error: "rating debe ser un entero entre 1 y 5" });
    return;
  }

  const resultado = await renewTrialWithFeedback(req.session!.userId, rating, comments);
  res.status(resultado.renewed ? 200 : 409).json(resultado);
}));
