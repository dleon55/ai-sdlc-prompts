-- AI-SDLC Pro — conteo de copias por prompt (indicador para el administrador)
--
-- Ejecutar una sola vez en el SQL Editor del proyecto de Supabase, después de
-- supabase/trial_gate.sql. Alimenta el criterio de activación de la Fase 2
-- (issue #7: gate Free/Pro por prompt) con datos reales de uso, en vez de
-- decidir a ciegas qué prompts serían "gratis" y cuáles "Pro".
--
-- Mismo patrón de seguridad ya auditado en trial_gate.sql (ver riesgos #1-3
-- corregidos ahí): RLS habilitado, CERO políticas de cliente -- todo acceso
-- de escritura pasa por track_prompt_copy() (security definer), sin
-- parámetros que controlen ningún límite ni comportamiento sensible.

-- ───────────────────── prompt_copy_stats ─────────────────────
-- Un contador por prompt_id. Solo lo escribe track_prompt_copy().
create table if not exists prompt_copy_stats (
  prompt_id  text primary key,
  copy_count int not null default 0,
  updated_at timestamptz not null default now()
);

alter table prompt_copy_stats enable row level security;
-- Sin políticas: ni anon ni authenticated pueden leer/escribir esta tabla
-- directamente. El administrador la consulta desde el SQL Editor con su
-- propio acceso de servicio, no desde el cliente.

-- ───────────────────── track_prompt_copy() ─────────────────────
-- Incrementa el contador de cada prompt_id copiado. Se llama desde el mismo
-- choke point que el gate (copyResolvedText() en build.py), después de que
-- la copia al portapapeles ya fue exitosa -- nunca antes, nunca bloqueante.
-- Ejecutable por anon y authenticated (se copia en ambos estados de sesión).
--
-- Riesgo aceptado y declarado (ver diseño 04-01 §3.D): no se valida que
-- p_prompt_ids corresponda a ids reales de la biblioteca -- el peor caso es
-- una fila con un id inventado en una tabla de solo lectura administrativa,
-- no una vulnerabilidad de acceso ni de integridad de negocio como las de
-- trial_gate.sql. No se sobre-diseña una validación para un riesgo bajo.
create or replace function track_prompt_copy(p_prompt_ids text[])
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  pid text;
begin
  if p_prompt_ids is null then
    return;
  end if;

  foreach pid in array p_prompt_ids
  loop
    if pid is not null and length(trim(pid)) > 0 then
      insert into prompt_copy_stats (prompt_id, copy_count, updated_at)
      values (pid, 1, now())
      on conflict (prompt_id) do update
        set copy_count = prompt_copy_stats.copy_count + 1,
            updated_at = now();
    end if;
  end loop;
end;
$$;

grant execute on function track_prompt_copy(text[]) to anon;
grant execute on function track_prompt_copy(text[]) to authenticated;
