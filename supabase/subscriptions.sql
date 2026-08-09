-- AI-SDLC Pro — suscripciones de pago (Paddle Billing)
--
-- Ejecutar una sola vez en el SQL Editor del proyecto de Supabase, después de
-- supabase/trial_gate.sql.
--
-- Mismo patrón de seguridad ya auditado en trial_gate.sql: RLS habilitado,
-- el usuario solo puede LEER su propia fila (para reflejar "ya eres Pro" en
-- la UI) -- NINGUNA política de insert/update/delete para el cliente. La
-- única vía de escritura es la Supabase Edge Function que recibe los
-- webhooks de Paddle (supabase/functions/paddle-webhook/), que usa la
-- service role key y por eso no necesita (ni debe) pasar por RLS.

create table if not exists subscriptions (
  user_id             uuid primary key references auth.users(id) on delete cascade,
  paddle_subscription_id text not null,
  paddle_customer_id     text not null,
  status              text not null,
  current_period_end timestamptz,
  last_event_occurred_at timestamptz,
  -- Orden de llegada de la cohorte fundadora (Programa Fundador, decisión
  -- 2026-08-09): fijada al primer insert; el upsert del webhook no la toca.
  created_at          timestamptz not null default now(),
  updated_at          timestamptz not null default now()
);

alter table subscriptions enable row level security;

create policy "cada quien lee solo su propia suscripcion"
  on subscriptions for select
  using (auth.uid() = user_id);
-- Sin política de insert/update/delete: solo la Edge Function (service
-- role) escribe aquí. Si un cliente pudiera escribir su propia fila,
-- cualquiera podría auto-otorgarse status='active' desde la consola del
-- navegador con el anon key público -- exactamente el mismo riesgo que ya
-- se corrigió en user_trial (ver trial_gate.sql, riesgo #1).

create index if not exists subscriptions_paddle_subscription_id_idx
  on subscriptions (paddle_subscription_id);

-- Eventos aceptados desde Paddle. Esta tabla permite reconocer reintentos y
-- replays sin exponer ninguna escritura al cliente.
create table if not exists paddle_webhook_events (
  event_id      text primary key,
  event_type    text not null,
  occurred_at   timestamptz,
  received_at   timestamptz not null default now(),
  processed_at  timestamptz
);

alter table paddle_webhook_events enable row level security;
-- Sin politicas RLS: solo la Edge Function con service role registra eventos.

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
set search_path = public
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
      -- trae el user_id. Fallar aqui hace que la Edge Function responda
      -- 500 y Paddle reintente hasta que ese created llegue. Si nunca
      -- llega, el evento queda visible en la cola de fallidos de Paddle
      -- en vez de desaparecer en silencio.
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

revoke execute on function apply_paddle_subscription_event(
  text, text, timestamptz, uuid, text, text, text, timestamptz
) from public, anon, authenticated;
grant execute on function apply_paddle_subscription_event(
  text, text, timestamptz, uuid, text, text, text, timestamptz
) to service_role;
-- Índice de búsqueda: el webhook de "actualización" de Paddle no siempre
-- trae el user_id (algunos eventos solo traen el id de la suscripción de
-- Paddle) -- sin este índice, cada webhook de actualización requeriría un
-- table scan completo para encontrar a qué usuario pertenece.

-- ───────────── check_trial_status(): ahora también revisa suscripción ─────────────
-- Reemplaza la versión de trial_gate.sql (ejecutar este archivo DESPUÉS de
-- ese). Un usuario con suscripción activa de pago siempre tiene acceso
-- ilimitado, sin importar si su prueba gratuita ya venció -- se revisa la
-- suscripción primero. Ningún código del cliente cambia: sigue llamando al
-- mismo RPC check_trial_status() y esperando el mismo shape de respuesta
-- {active, expires_at}, así que este cambio no requiere tocar build.py.
create or replace function check_trial_status()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  row_trial user_trial%rowtype;
  row_sub subscriptions%rowtype;
begin
  select * into row_sub from subscriptions where user_id = auth.uid();

  if found and row_sub.status = 'active' then
    return jsonb_build_object(
      'active', true,
      'expires_at', row_sub.current_period_end,
      'no_trial_row', false,
      'subscribed', true
    );
  end if;

  select * into row_trial from user_trial where user_id = auth.uid();

  if not found then
    insert into user_trial (user_id) values (auth.uid())
    on conflict (user_id) do nothing;
    select * into row_trial from user_trial where user_id = auth.uid();
  end if;

  return jsonb_build_object(
    'active', row_trial.trial_expires_at > now(),
    'expires_at', row_trial.trial_expires_at,
    'no_trial_row', false,
    'subscribed', false
  );
end;
$$;

grant execute on function check_trial_status() to authenticated;

-- ───────────── founding_spots_left(): contador público del Programa Fundador ─────────────
-- (decisión 2026-08-09, ver docs/marketing/early-adopters-program.md). El
-- "precio congelado" en sí no requiere código: es el comportamiento por
-- defecto de Paddle Billing (un cambio de precio solo afecta suscripciones
-- nuevas). Este RPC solo alimenta el banner "quedan N de 50" de /precios
-- con dato real. Expone ÚNICAMENTE el agregado — nunca filas ni columnas de
-- usuarios — y por eso es seguro otorgarlo a anon. security definer es
-- necesario: con RLS, anon no ve ninguna fila y contaría siempre 0.
--
-- Un lugar se CONSUME al crearse la suscripción y no se libera al cancelar:
-- liberar lugares haría el contador reversible en público y permitiría
-- "reciclar" una promesa condicionada a suscripción activa sin interrupción.
create or replace function founding_spots_left()
returns jsonb
language sql
stable
security definer
set search_path = public
as $$
  select jsonb_build_object(
    'total', 50,
    'left', greatest(0, 50 - (select count(*) from subscriptions))::int
  );
$$;

revoke all on function founding_spots_left() from public;
grant execute on function founding_spots_left() to anon, authenticated;
