-- AI-SDLC Pro — estado por (proyecto, prompt): progreso, personalización,
-- resultados de IA
--
-- Ejecutar una sola vez en el SQL Editor del proyecto de Supabase, después
-- de supabase/schema.sql (requiere que la tabla `projects` ya exista).
--
-- Fase 0 del diseño acotado discutido en los issues #137 (personalización),
-- #138 (modo guiado), #139 (checklist de progreso) y #140 (guardado de
-- resultados de IA) -- las cuatro features comparten la misma necesidad de
-- datos indexados por (proyecto, prompt), algo que `projects.vars` no tiene
-- hoy (solo guarda variables por proyecto, no por prompt).
--
-- Tabla separada en vez de extender `projects.vars`: evita que cada sync de
-- variables (alta frecuencia, en cada edición) tenga que serializar/
-- deserializar también resultados de IA potencialmente grandes; permite
-- leer/escribir el estado de un solo prompt sin reescribir todo el
-- proyecto.
--
-- RLS por relación indirecta: no hay columna `user_id` en esta tabla --
-- la política verifica la propiedad a través de `projects.user_id` (mismo
-- patrón indirecto que ya usa el flujo de suscripciones para verificar
-- acceso vía una tabla relacionada). El anon key embebido en el HTML es
-- público por diseño, así que sin RLS cualquier visitante podría leer o
-- escribir el estado de cualquier proyecto ajeno.

create table if not exists project_prompt_state (
  project_id       uuid not null references projects(id) on delete cascade,
  prompt_id        text not null,
  used_at          timestamptz,               -- #139: no nulo si el prompt ya se usó en este proyecto
  custom_additions text,                       -- #137: texto anexado al prompt resuelto al copiar (nunca sustituye el cuerpo canónico)
  ai_output        text,                       -- #140: resultado pegado manualmente por el usuario; la herramienta nunca llama a un modelo de IA
  updated_at       timestamptz not null default now(),
  primary key (project_id, prompt_id)
);
-- Sin índice adicional en `project_id`: la llave primaria compuesta
-- (project_id, prompt_id) ya cubre eficientemente los filtros por
-- project_id solo, al ser la columna líder del índice de la PK.

alter table project_prompt_state enable row level security;

-- Cada usuario solo puede ver o editar el estado de prompts que pertenecen
-- a SUS PROPIOS proyectos -- se verifica indirectamente porque esta tabla
-- no tiene user_id propio, solo project_id.
create policy "cada quien ve y edita solo el estado de sus propios proyectos"
  on project_prompt_state for all
  using (
    exists (
      select 1 from projects
      where projects.id = project_prompt_state.project_id
        and projects.user_id = auth.uid()
    )
  )
  with check (
    exists (
      select 1 from projects
      where projects.id = project_prompt_state.project_id
        and projects.user_id = auth.uid()
    )
  );
