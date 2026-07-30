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
