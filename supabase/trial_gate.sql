-- AI-SDLC Pro — muro de registro + prueba de 1 mes + renovación por feedback
--
-- Ejecutar una sola vez en el SQL Editor del proyecto de Supabase, después de
-- supabase/schema.sql. Ver docs/trial-gate-setup.md para el paso a paso.
--
-- Regla de seguridad central de este archivo (ver diseño 04-01 §3 y riesgo #1):
-- NINGUNA de las tablas siguientes debe tener una política RLS que permita a
-- un usuario editar directamente su propia fila de `user_trial`. Si la
-- tuviera, cualquiera podría extender su propia prueba indefinidamente desde
-- la consola del navegador con el `anon key` público. La única vía de
-- escritura sobre `user_trial` son las funciones `security definer` de abajo.

-- ───────────────────────── anon_usage ─────────────────────────
-- Contador de copias por IP para visitantes sin sesión. Solo lo escribe
-- check_anon_usage() (security definer) -- ninguna política de cliente.
create table if not exists anon_usage (
  ip_address text primary key,
  use_count  int not null default 0,
  first_seen timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table anon_usage enable row level security;
-- Sin políticas: ni anon ni authenticated pueden leer/escribir esta tabla
-- directamente. Todo acceso pasa por check_anon_usage().

-- ───────────────────────── user_trial ─────────────────────────
-- Una fila por usuario registrado. trial_expires_at solo lo mueve el
-- trigger (creación) y submit_feedback_and_renew() (renovación).
create table if not exists user_trial (
  user_id          uuid primary key references auth.users(id) on delete cascade,
  trial_started_at  timestamptz not null default now(),
  trial_expires_at  timestamptz not null default (now() + interval '1 month'),
  renewed_count     int not null default 0
);

alter table user_trial enable row level security;

-- El usuario puede LEER su propia fila (para reflejar el estado en la UI),
-- pero no existe ninguna política de insert/update/delete para el cliente:
-- esa es la garantía de seguridad central de este diseño.
create policy "cada quien lee solo su propia prueba"
  on user_trial for select
  using (auth.uid() = user_id);

-- ───────────────────────── feedback ─────────────────────────
-- Historial de retroalimentación. Insert-only para el propio usuario;
-- nadie puede editar ni borrar una fila ya enviada (integridad del log).
create table if not exists feedback (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references auth.users(id) on delete cascade,
  rating      int not null check (rating >= 1 and rating <= 5),
  comments    text,
  created_at  timestamptz not null default now()
);

alter table feedback enable row level security;

create policy "cada quien inserta solo su propio feedback"
  on feedback for insert
  with check (auth.uid() = user_id);

create policy "cada quien lee solo su propio feedback"
  on feedback for select
  using (auth.uid() = user_id);
-- Sin política de update ni delete: el historial de feedback es inmutable.

-- ───────────────────── check_anon_usage() ─────────────────────
-- Identifica al visitante por su IP (cabecera que PostgREST expone en cada
-- request) e incrementa su contador. Devuelve cuántas copias le quedan.
-- Ejecutable por el rol anon.
create or replace function check_anon_usage(free_limit int default 2)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  caller_ip text;
  current_count int;
begin
  caller_ip := coalesce(
    (current_setting('request.headers', true)::json ->> 'x-forwarded-for'),
    'unknown'
  );

  insert into anon_usage (ip_address, use_count, updated_at)
  values (caller_ip, 1, now())
  on conflict (ip_address) do update
    set use_count = anon_usage.use_count + 1,
        updated_at = now()
  returning use_count into current_count;

  return jsonb_build_object(
    'remaining', greatest(free_limit - current_count, 0),
    'allowed', current_count <= free_limit
  );
end;
$$;

grant execute on function check_anon_usage(int) to anon;

-- ───────────────────── check_trial_status() ─────────────────────
-- Devuelve el estado de la prueba del usuario autenticado. Ejecutable por
-- el rol authenticated -- usa auth.uid(), nunca un id que el cliente pase.
create or replace function check_trial_status()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  row_trial user_trial%rowtype;
begin
  select * into row_trial from user_trial where user_id = auth.uid();

  if not found then
    -- No debería ocurrir si el trigger de creación funcionó, pero se
    -- declara explícitamente en vez de fallar en silencio.
    return jsonb_build_object('active', false, 'expires_at', null, 'no_trial_row', true);
  end if;

  return jsonb_build_object(
    'active', row_trial.trial_expires_at > now(),
    'expires_at', row_trial.trial_expires_at,
    'no_trial_row', false
  );
end;
$$;

grant execute on function check_trial_status() to authenticated;

-- ───────────────── submit_feedback_and_renew() ─────────────────
-- Inserta el feedback y extiende la prueba 1 mes desde ahora, en una sola
-- transacción. Ejecutable por el rol authenticated.
create or replace function submit_feedback_and_renew(p_rating int, p_comments text default null)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  new_expiry timestamptz;
begin
  insert into feedback (user_id, rating, comments)
  values (auth.uid(), p_rating, p_comments);

  update user_trial
    set trial_expires_at = now() + interval '1 month',
        renewed_count = renewed_count + 1
    where user_id = auth.uid()
    returning trial_expires_at into new_expiry;

  return jsonb_build_object('renewed', true, 'new_expires_at', new_expiry);
end;
$$;

grant execute on function submit_feedback_and_renew(int, text) to authenticated;

-- ───────────────── trigger: crear prueba al registrarse ─────────────────
-- Se dispara una sola vez, al crear la fila en auth.users -- el cliente
-- nunca puede invocar esto ni duplicar su propia prueba.
create or replace function create_user_trial()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into user_trial (user_id) values (new.id)
  on conflict (user_id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created_trial on auth.users;
create trigger on_auth_user_created_trial
  after insert on auth.users
  for each row execute function create_user_trial();
