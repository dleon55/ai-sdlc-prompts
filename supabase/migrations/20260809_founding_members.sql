-- Programa Fundador — tracking de cohorte y contador público (decisión
-- 2026-08-09, ver docs/STRATEGY.md "Decisiones registradas" y
-- docs/marketing/early-adopters-program.md).
--
-- Contexto: el "precio congelado" NO se implementa aquí porque es el
-- comportamiento por defecto de Paddle Billing — cambiar un precio solo
-- afecta suscripciones nuevas; las activas siguen cobrándose al monto con
-- el que se crearon salvo migración explícita vía API, que simplemente
-- nunca se hará para la cohorte fundadora. Lo único que faltaba era:
--
--   1. Saber el ORDEN de llegada (quiénes son los primeros 50) — columna
--      created_at, fijada al primer insert y nunca pisada por el upsert
--      del webhook (el ON CONFLICT de apply_paddle_subscription_event no
--      la toca).
--   2. Un contador real para el banner "quedan N de 50" de /precios —
--      RPC founding_spots_left(), que expone SOLO el agregado (jamás
--      filas ni columnas de usuarios). El copy exige dato real de
--      Supabase, no un número inventado.
--
-- Ejecutar una sola vez en el SQL Editor, en instalaciones que ya corrieron
-- supabase/subscriptions.sql. Las instalaciones nuevas no la necesitan: el
-- script base ya incluye ambas piezas.
--
-- Nota deliberada: las filas existentes antes de esta migración reciben
-- created_at = now() al aplicarla. Es aceptable porque el piloto aún no
-- tiene volumen de suscripciones; si existiera alguna, su orden real puede
-- reconstruirse desde paddle_webhook_events.occurred_at.

alter table subscriptions
  add column if not exists created_at timestamptz not null default now();

comment on column subscriptions.created_at is
  'Primer alta de la suscripción (orden de llegada de la cohorte fundadora). '
  'El upsert del webhook no la actualiza: queda fijada al primer insert.';

-- Un lugar fundador se CONSUME al crearse la suscripción y no se libera si
-- después se cancela: liberar lugares haría el contador reversible (subiría
-- y bajaría en público) y permitiría "reciclar" la promesa de por vida, que
-- está condicionada a suscripción activa sin interrupción.
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
