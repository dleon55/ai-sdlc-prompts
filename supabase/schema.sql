-- AI-SDLC Pro — esquema de registro de usuarios (Supabase)
--
-- Ejecutar una sola vez en el SQL Editor del proyecto de Supabase que crees
-- siguiendo docs/auth-setup.md. Espeja la forma exacta que ya usan los
-- proyectos guardados en localStorage (id, name, isDefault, vars) para que
-- el frontend no necesite remapear campos entre la caché local y la nube.
--
-- La política de seguridad a nivel de fila (RLS) es la única barrera real:
-- el anon key que se embebe en el HTML es público por diseño (ver
-- docs/auth-setup.md), así que sin RLS cualquier visitante podría leer o
-- escribir los proyectos de cualquier otro usuario.

create table if not exists projects (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references auth.users(id) on delete cascade,
  name        text not null,
  is_default  boolean not null default false,
  vars        jsonb not null default '{}'::jsonb,
  updated_at  timestamptz not null default now()
);

create index if not exists projects_user_id_idx on projects(user_id);

alter table projects enable row level security;

-- Cada usuario solo puede ver, crear, editar o borrar sus propios proyectos.
-- auth.uid() lo resuelve Supabase a partir de la sesión autenticada -- no
-- es un valor que el cliente pueda falsificar.
create policy "cada quien ve y edita solo lo suyo"
  on projects for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
