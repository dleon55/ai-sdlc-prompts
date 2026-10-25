import { Router } from "express";
import { pool } from "../db.ts";
import { asincrono } from "../asincrono.ts";

// Rutas sin autenticacion -- equivalentes a las funciones RPC otorgadas a
// `anon` (y tambien a `authenticated`) en supabase/prompt_copy_stats.sql y
// supabase/subscriptions.sql. Ninguna de las dos expone datos de usuarios
// individuales.
export const publicRouter = Router();

// Puerto de track_prompt_copy(text[]) -- incrementa el contador de cada
// prompt_id copiado. Sin validar que los ids sean reales (mismo riesgo
// aceptado y declarado en el original: en el peor caso, una fila con un
// id inventado en una tabla de solo lectura administrativa).
publicRouter.post("/prompt-stats/track", asincrono(async (req, res) => {
  const promptIds = Array.isArray(req.body?.promptIds) ? req.body.promptIds : [];
  for (const rawId of promptIds) {
    const promptId = typeof rawId === "string" ? rawId.trim() : "";
    if (!promptId) continue;
    await pool.query(
      `insert into prompt_copy_stats (prompt_id, copy_count, updated_at)
       values ($1, 1, now())
       on conflict (prompt_id) do update set
         copy_count = prompt_copy_stats.copy_count + 1,
         updated_at = now()`,
      [promptId],
    );
  }
  res.status(204).end();
}));

// Puerto de founding_spots_left() -- expone UNICAMENTE el agregado (nunca
// filas ni columnas de usuarios). Un lugar se consume al crearse la
// suscripcion y no se libera al cancelar (ver supabase/subscriptions.sql
// para la justificacion: evita "reciclar" una promesa condicionada a
// suscripcion activa sin interrupcion).
const FOUNDING_TOTAL = 50;

publicRouter.get("/founding/spots-left", asincrono(async (_req, res) => {
  const { rows } = await pool.query<{ count: string }>("select count(*)::int as count from subscriptions");
  const used = Number(rows[0]!.count);
  res.json({ total: FOUNDING_TOTAL, left: Math.max(0, FOUNDING_TOTAL - used) });
}));

publicRouter.get("/health", asincrono(async (_req, res) => {
  await pool.query("select 1");
  res.json({ ok: true });
}));
