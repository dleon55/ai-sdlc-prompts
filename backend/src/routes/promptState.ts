import { Router } from "express";
import { requireAuth } from "../auth/middleware.ts";
import { pool, withTransaction } from "../db.ts";
import { asincrono } from "../asincrono.ts";

export const promptStateRouter = Router();
promptStateRouter.use(requireAuth);

const UPSERTABLE_COLUMNS = ["used_at", "custom_additions", "ai_output"] as const;
type UpsertableColumn = (typeof UPSERTABLE_COLUMNS)[number];

interface PromptStateRow {
  project_id: string;
  prompt_id: string;
  used_at: string | null;
  custom_additions: string | null;
  ai_output: string | null;
}

// RLS equivalente a "cada quien ve y edita solo el estado de sus propios
// proyectos" (supabase/project_prompt_state.sql) -- esta tabla no tiene
// user_id propio, la propiedad se verifica indirectamente por projects.

// Espejo de pullCloudPromptState(): trae el estado de TODOS los
// proyectos del usuario en una sola consulta.
promptStateRouter.get("/", asincrono(async (req, res) => {
  const { rows } = await pool.query<PromptStateRow>(
    `select pps.project_id, pps.prompt_id, pps.used_at, pps.custom_additions, pps.ai_output
     from project_prompt_state pps
     join projects p on p.id = pps.project_id
     where p.user_id = $1`,
    [req.session!.userId],
  );
  res.json({ data: rows });
}));

// Equivalente a client.from('project_prompt_state').upsert(rows, {
// onConflict: 'project_id,prompt_id' }) -- PostgREST solo toca, tanto al
// insertar como en el ON CONFLICT, las columnas presentes en cada fila
// enviada (ver comentario en build.py junto a pushPromptStateFieldsToCloud).
// Se replica exactamente ese comportamiento de "upsert parcial de
// columnas" en vez de forzar las 3 columnas siempre.
promptStateRouter.put("/", asincrono(async (req, res) => {
  const rows = Array.isArray(req.body?.rows) ? req.body.rows : [];
  if (rows.length === 0) {
    res.status(204).end();
    return;
  }

  await withTransaction(async (client) => {
    for (const row of rows) {
      if (!row.project_id || !row.prompt_id) continue;

      const { rows: owned } = await client.query(
        "select 1 from projects where id = $1 and user_id = $2",
        [row.project_id, req.session!.userId],
      );
      if (owned.length === 0) continue; // no es tuyo -- mismo resultado que RLS: 0 filas afectadas, sin error.

      const presentColumns = UPSERTABLE_COLUMNS.filter(
        (col): col is UpsertableColumn => row[col] !== undefined,
      );
      const insertColumns = ["project_id", "prompt_id", "updated_at", ...presentColumns];
      const insertValues = [row.project_id, row.prompt_id, new Date().toISOString(), ...presentColumns.map((col) => row[col])];
      const placeholders = insertValues.map((_, i) => `$${i + 1}`);
      const updateSet = ["updated_at = excluded.updated_at", ...presentColumns.map((col) => `${col} = excluded.${col}`)];

      await client.query(
        `insert into project_prompt_state (${insertColumns.join(", ")})
         values (${placeholders.join(", ")})
         on conflict (project_id, prompt_id) do update set ${updateSet.join(", ")}`,
        insertValues,
      );
    }
  });

  res.status(204).end();
}));
