-- AI-SDLC Pro -- esquema del backend propio (Fase 1 de
-- docs/PLAN_MIGRACION_SUPABASE_A_LOCAL.md).
--
-- Portado de supabase/schema.sql, supabase/trial_gate.sql,
-- supabase/subscriptions.sql y supabase/prompt_copy_stats.sql.
--
-- Diferencia deliberada frente al original: SIN Row Level Security ni
-- funciones `security definer`. La autorizacion que alla vivia en
-- politicas RLS ahora vive en el codigo de cada ruta del backend
-- (backend/src/routes/*.ts) -- cada ruta replica exactamente la misma
-- regla que su politica equivalente (ver comentarios "RLS equivalente"
-- en cada ruta). gen_random_uuid() es nativo desde Postgres 13, no
-- requiere ninguna extension.

-- ───────────────────────── users ─────────────────────────
-- Reemplaza auth.users (gestionada por GoTrue en Supabase, no por SQL
-- propio). Unico proveedor: GitHub OAuth -- ver backend/src/auth/github.ts.
create table if not exists users (
  id          uuid primary key default gen_random_uuid(),
  github_id   text not null unique,
  github_login text not null,
  email       text,
  created_at  timestamptz not null default now()
);

-- ───────────────────────── projects ─────────────────────────
create table if not exists projects (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references users(id) on delete cascade,
  name        text not null,
  is_default  boolean not null default false,
  vars        jsonb not null default '{}'::jsonb,
  updated_at  timestamptz not null default now()
);

create index if not exists projects_user_id_idx on projects(user_id);

-- ───────────────────────── project_prompt_state ─────────────────────────
create table if not exists project_prompt_state (
  project_id       uuid not null references projects(id) on delete cascade,
  prompt_id        text not null,
  used_at          timestamptz,
  custom_additions text,
  ai_output        text,
  updated_at       timestamptz not null default now(),
  primary key (project_id, prompt_id)
);

-- ───────────────────────── user_trial ─────────────────────────
create table if not exists user_trial (
  user_id          uuid primary key references users(id) on delete cascade,
  trial_started_at timestamptz not null default now(),
  trial_expires_at timestamptz not null default (now() + interval '1 week'),
  renewed_count    int not null default 0
);

-- Trigger: crea la fila de prueba al registrarse (equivalente a
-- on_auth_user_created_trial, pero disparado aqui por la propia insercion
-- en `users`, no por auth.users).
create or replace function create_user_trial()
returns trigger
language plpgsql
as $$
begin
  insert into user_trial (user_id) values (new.id)
  on conflict (user_id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_user_created_trial on users;
create trigger on_user_created_trial
  after insert on users
  for each row execute function create_user_trial();

-- ───────────────────────── feedback ─────────────────────────
create table if not exists feedback (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references users(id) on delete cascade,
  rating      int not null check (rating >= 1 and rating <= 5),
  comments    text,
  created_at  timestamptz not null default now()
);

-- ───────────────────────── subscriptions ─────────────────────────
create table if not exists subscriptions (
  user_id                uuid primary key references users(id) on delete cascade,
  paddle_subscription_id text not null,
  paddle_customer_id     text not null,
  status                 text not null,
  current_period_end     timestamptz,
  last_event_occurred_at timestamptz,
  created_at             timestamptz not null default now(),
  updated_at             timestamptz not null default now()
);

create index if not exists subscriptions_paddle_subscription_id_idx
  on subscriptions (paddle_subscription_id);

-- ───────────────────────── paddle_webhook_events ─────────────────────────
create table if not exists paddle_webhook_events (
  event_id     text primary key,
  event_type   text not null,
  occurred_at  timestamptz,
  received_at  timestamptz not null default now(),
  processed_at timestamptz
);

-- ───────────────────────── prompt_copy_stats ─────────────────────────
create table if not exists prompt_copy_stats (
  prompt_id  text primary key,
  copy_count int not null default 0,
  updated_at timestamptz not null default now()
);

-- Nota: anon_usage / check_anon_usage() NO se portan -- confirmado como
-- codigo muerto en la revision del plan (build.py no los llama desde el
-- rediseño del muro Free/Pro, issue #7). Ver
-- docs/PLAN_MIGRACION_SUPABASE_A_LOCAL.md §2.2.

-- ───────────────────────── apply_paddle_subscription_event ─────────────────────────
-- Portada SIN CAMBIOS DE LOGICA desde supabase/subscriptions.sql. Alla
-- era `security definer` porque el cliente (anon key) nunca debia poder
-- llamarla directamente -- aqui no hace falta ese mecanismo: la unica via
-- de invocacion es el propio backend (backend/src/routes/webhooks/paddle.ts),
-- con su propia conexion de base de datos, nunca expuesta al cliente.
create or replace function apply_paddle_subscription_event(
  p_event_id text,
  p_event_type text,
  p_occurred_at timestamptz,
  p_user_id uuid,
  p_subscription_id text,
  p_customer_id text,
  p_status text,
  p_current_period_end timestamptz
)
returns boolean
language plpgsql
as $$
declare
  already_processed timestamptz;
  affected integer;
begin
  insert into paddle_webhook_events (event_id, event_type, occurred_at)
  values (p_event_id, p_event_type, p_occurred_at)
  on conflict (event_id) do nothing;

  select processed_at into already_processed
  from paddle_webhook_events
  where event_id = p_event_id
  for update;

  if already_processed is not null then
    return false;
  end if;

  if p_event_type like 'subscription.%' then
    if p_subscription_id is null then
      raise exception 'subscription event is missing subscription id';
    end if;

    if p_user_id is not null then
      insert into subscriptions (
        user_id, paddle_subscription_id, paddle_customer_id, status,
        current_period_end, last_event_occurred_at, updated_at
      ) values (
        p_user_id, p_subscription_id, p_customer_id, p_status,
        p_current_period_end, p_occurred_at, now()
      )
      on conflict (user_id) do update set
        paddle_subscription_id = excluded.paddle_subscription_id,
        paddle_customer_id = excluded.paddle_customer_id,
        status = excluded.status,
        current_period_end = excluded.current_period_end,
        last_event_occurred_at = excluded.last_event_occurred_at,
        updated_at = excluded.updated_at
      where subscriptions.last_event_occurred_at is null
        or subscriptions.last_event_occurred_at <= excluded.last_event_occurred_at;
    else
      update subscriptions set
        status = p_status,
        current_period_end = p_current_period_end,
        last_event_occurred_at = p_occurred_at,
        updated_at = now()
      where paddle_subscription_id = p_subscription_id
        and (
          last_event_occurred_at is null
          or last_event_occurred_at <= p_occurred_at
        );

      get diagnostics affected = row_count;

      -- 0 filas actualizadas significa dos cosas MUY distintas, y hay que
      -- separarlas o el modo de fallo es el peor posible:
      --
      --   (a) la suscripcion ya existe pero su ultimo evento es mas
      --       reciente -> descarte intencional por orden. Todo bien.
      --   (b) no existe ninguna fila con ese paddle_subscription_id ->
      --       este evento no trae user_id y no hay como ligarlo a nadie.
      --
      -- En el caso (b) NO se puede marcar el evento como procesado: si se
      -- marcara, la funcion devolveria 200, Paddle dejaria de reintentar,
      -- el cliente se quedaria sin el acceso que pago, y ni siquiera un
      -- replay manual lo arreglaria (el evento ya contaria como hecho).
      -- Ademas el tablero se veria sano, sin ninguna señal del problema.
      --
      -- Paddle no garantiza el orden de entrega, asi que un
      -- subscription.updated puede llegar antes que el created que si
      -- trae el user_id. Fallar aqui hace que el endpoint responda 500 y
      -- Paddle reintente hasta que ese created llegue. Si nunca llega, el
      -- evento queda visible en la cola de fallidos de Paddle en vez de
      -- desaparecer en silencio.
      if affected = 0 and not exists (
        select 1 from subscriptions
        where paddle_subscription_id = p_subscription_id
      ) then
        raise exception
          'no local subscription for % and event % carries no user_id; '
          'failing so Paddle retries until the creating event arrives',
          p_subscription_id, p_event_id;
      end if;
    end if;
  end if;

  update paddle_webhook_events
  set processed_at = now()
  where event_id = p_event_id;

  return true;
end;
$$;
