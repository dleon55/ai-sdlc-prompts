-- Apply this migration to existing Supabase installations before deploying
-- the hardened Paddle webhook. New installations get the same table from
-- subscriptions.sql.
create table if not exists paddle_webhook_events (
  event_id text primary key,
  event_type text not null,
  occurred_at timestamptz,
  received_at timestamptz not null default now(),
  processed_at timestamptz
);

alter table paddle_webhook_events enable row level security;

-- The service-role webhook is the sole writer. Do not add client policies.
alter table subscriptions
  add column if not exists last_event_occurred_at timestamptz;

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
