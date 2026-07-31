-- Corrige un fallo silencioso en apply_paddle_subscription_event: un evento
-- de suscripcion que no podia ligarse a ningun usuario se marcaba como
-- procesado igual y devolvia 200.
--
-- Cadena de consecuencias que esto producia:
--   1. La Edge Function respondia 200 -> Paddle dejaba de reintentar.
--   2. La fila de subscriptions nunca se escribia -> el cliente pagaba y
--      no recibia acceso.
--   3. El evento quedaba marcado como procesado -> un replay manual
--      tampoco lo arreglaba.
--   4. El log de Paddle se veia verde. Cero señal del problema.
--
-- Se dispara cuando llega un evento subscription.* SIN custom_data.user_id
-- y todavia no existe fila local para ese paddle_subscription_id. Paddle no
-- garantiza el orden de entrega, asi que un subscription.updated puede
-- llegar antes que el subscription.created que si trae el user_id.
--
-- La correccion distingue los dos casos que hoy se ven identicos (0 filas
-- actualizadas) y solo falla en el que representa perdida de datos. Aplicar
-- despues de 20260730_paddle_webhook_idempotency.sql.

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
      -- Con user_id se puede crear la fila desde cero. Si el ON CONFLICT
      -- no actualiza nada es porque ya se proceso un evento mas reciente
      -- para ese usuario: descarte intencional, no hay perdida de datos.
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

      -- (a) 0 filas y la suscripcion SI existe -> evento viejo descartado
      --     a proposito. Continuar y marcarlo procesado.
      -- (b) 0 filas y NO existe -> no hay a quien darle el acceso. Fallar
      --     para que la Edge Function devuelva 500 y Paddle reintente
      --     hasta que llegue el evento con user_id. Si nunca llega, queda
      --     visible en la cola de fallidos de Paddle en vez de perderse.
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
