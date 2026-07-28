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
