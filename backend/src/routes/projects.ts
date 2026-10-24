import { Router } from "express";
import { requireAuth } from "../auth/middleware.ts";
import { pool } from "../db.ts";

export const projectsRouter = Router();
projectsRouter.use(requireAuth);

interface ProjectRow {
  id: string;
  name: string;
  is_default: boolean;
  vars: Record<string, unknown>;
}

// RLS equivalente: "cada quien ve y edita solo lo suyo"
// (using/with check: auth.uid() = user_id) -- ver supabase/schema.sql.
// Cada query de este archivo filtra o fuerza user_id = req.session.userId
// explicitamente, nunca confia en un user_id que venga en el body.

projectsRouter.get("/", async (req, res) => {
  const { rows } = await pool.query<ProjectRow>(
    "select id, name, is_default, vars from projects where user_id = $1",
    [req.session!.userId],
  );
  res.json({ data: rows });
});

// Equivalente a client.from('projects').insert(rows).select() -- usado
// solo en la importacion inicial de proyectos que vivian en localStorage
// antes de iniciar sesion (ver pushLocalProjectsToCloud en build.py).
// Postgres genera el id; nunca se acepta uno del cliente aqui.
projectsRouter.post("/", async (req, res) => {
  const rows = Array.isArray(req.body?.rows) ? req.body.rows : [];
  if (rows.length === 0) {
    res.json({ data: [] });
    return;
  }

  const inserted: ProjectRow[] = [];
  for (const row of rows) {
    const { rows: result } = await pool.query<ProjectRow>(
      `insert into projects (user_id, name, is_default, vars)
       values ($1, $2, $3, $4)
       returning id, name, is_default, vars`,
      [req.session!.userId, String(row.name), Boolean(row.isDefault), row.vars ?? {}],
    );
    inserted.push(result[0]!);
  }
  res.json({ data: inserted });
});

// Equivalente a client.from('projects').upsert(rows) -- usado en cada
// alta/edicion normal (pushProjectsUpdateToCloud). El cliente SI manda un
// id propio (generado con crypto.randomUUID() al crear el proyecto), asi
// que esto es un insert-or-update real por id, no un insert con id
// generado por la base.
projectsRouter.put("/", async (req, res) => {
  const rows = Array.isArray(req.body?.rows) ? req.body.rows : [];
  for (const row of rows) {
    if (!row.id) continue;
    // La clausula WHERE del ON CONFLICT replica la politica RLS "with
    // check (auth.uid() = user_id)": si el id ya existe y pertenece a
    // OTRO usuario, el UPDATE se salta (0 filas), igual que RLS lo haria
    // -- sin lanzar error, para no romper el fire-and-forget del cliente.
    await pool.query(
      `insert into projects (id, user_id, name, is_default, vars, updated_at)
       values ($1, $2, $3, $4, $5, now())
       on conflict (id) do update set
         name = excluded.name,
         is_default = excluded.is_default,
         vars = excluded.vars,
         updated_at = now()
       where projects.user_id = $2`,
      [row.id, req.session!.userId, String(row.name), Boolean(row.isDefault), row.vars ?? {}],
    );
  }
  res.status(204).end();
});

projectsRouter.delete("/:id", async (req, res) => {
  await pool.query("delete from projects where id = $1 and user_id = $2", [
    req.params.id,
    req.session!.userId,
  ]);
  res.status(204).end();
});
