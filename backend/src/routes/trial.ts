import { Router } from "express";
import { requireAuth } from "../auth/middleware.ts";
import { pool, withTransaction } from "../db.ts";
import { asincrono } from "../asincrono.ts";

export const trialRouter = Router();
trialRouter.use(requireAuth);

interface TrialStatus {
  active: boolean;
  expires_at: string | null;
  no_trial_row: boolean;
  subscribed: boolean;
}

// Puerto de check_trial_status() (supabase/subscriptions.sql) -- revisa
// primero si hay una suscripcion de pago activa (acceso ilimitado sin
// importar la prueba), y solo si no la hay cae al estado de user_trial,
// autocreando la fila si falta (mismo "auto-reparable" documentado en el
// original: una fila ausente nunca debe leerse como "prueba vencida").
export async function checkTrialStatus(userId: string): Promise<TrialStatus> {
  const { rows: subRows } = await pool.query<{ status: string; current_period_end: string | null }>(
    "select status, current_period_end from subscriptions where user_id = $1",
    [userId],
  );
  if (subRows.length > 0 && subRows[0]!.status === "active") {
    return {
      active: true,
      expires_at: subRows[0]!.current_period_end,
      no_trial_row: false,
      subscribed: true,
    };
  }

  const { rows: trialRows } = await pool.query<{ trial_expires_at: string }>(
    "select trial_expires_at from user_trial where user_id = $1",
    [userId],
  );
  let trialExpiresAt: string;
  if (trialRows.length > 0) {
    trialExpiresAt = trialRows[0]!.trial_expires_at;
  } else {
    const { rows: created } = await pool.query<{ trial_expires_at: string }>(
      `insert into user_trial (user_id) values ($1)
       on conflict (user_id) do update set user_id = excluded.user_id
       returning trial_expires_at`,
      [userId],
    );
    trialExpiresAt = created[0]!.trial_expires_at;
  }

  return {
    active: new Date(trialExpiresAt).getTime() > Date.now(),
    expires_at: trialExpiresAt,
    no_trial_row: false,
    subscribed: false,
  };
}

trialRouter.get("/status", asincrono(async (req, res) => {
  res.json(await checkTrialStatus(req.session!.userId));
}));

// Puerto de submit_feedback_and_renew() (supabase/trial_gate.sql):
// inserta el feedback y extiende la prueba 1 semana desde ahora, en una
// sola transaccion.
trialRouter.post("/feedback", asincrono(async (req, res) => {
  const rating = Number(req.body?.rating);
  const comments = typeof req.body?.comments === "string" ? req.body.comments : null;
  if (!Number.isInteger(rating) || rating < 1 || rating > 5) {
    res.status(400).json({ error: "rating debe ser un entero entre 1 y 5" });
    return;
  }

  const newExpiresAt = await withTransaction(async (client) => {
    await client.query("insert into feedback (user_id, rating, comments) values ($1, $2, $3)", [
      req.session!.userId,
      rating,
      comments,
    ]);

    const { rows } = await client.query<{ trial_expires_at: string }>(
      `insert into user_trial (user_id, trial_expires_at, renewed_count)
       values ($1, now() + interval '1 week', 1)
       on conflict (user_id) do update set
         trial_expires_at = now() + interval '1 week',
         renewed_count = user_trial.renewed_count + 1
       returning trial_expires_at`,
      [req.session!.userId],
    );
    return rows[0]!.trial_expires_at;
  });

  res.json({ renewed: true, new_expires_at: newExpiresAt });
}));
