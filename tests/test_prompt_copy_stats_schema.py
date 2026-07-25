#!/usr/bin/env python3
"""
tests/test_prompt_copy_stats_schema.py — Contrato de regresión para
supabase/prompt_copy_stats.sql

Mismo patrón de seguridad ya auditado en supabase/trial_gate.sql (ver 04-01
§3.D y §5): la tabla no debe tener ninguna política RLS de cliente -- todo
acceso de escritura pasa por track_prompt_copy() (security definer). Si se
abriera una política de cliente, cualquiera podría inflar o manipular el
indicador de "prompts más copiados" que alimentará la decisión de la Fase 2
(issue #7) directamente desde la consola del navegador.
"""
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SCHEMA = (PROJECT_ROOT / "supabase" / "prompt_copy_stats.sql").read_text(encoding="utf-8")


def _policies_on_table(table):
    pattern = re.compile(
        r"create policy\s+\"[^\"]*\"\s+on\s+" + re.escape(table) + r"\s+for\s+(\w+)",
        re.IGNORECASE,
    )
    return [m.group(1).lower() for m in pattern.finditer(SCHEMA)]


def test_prompt_copy_stats_has_rls_enabled():
    assert "alter table prompt_copy_stats enable row level security" in SCHEMA, (
        "Falta 'enable row level security' en prompt_copy_stats"
    )


def test_prompt_copy_stats_has_zero_client_policies():
    """Igual que anon_usage en trial_gate.sql: ninguna política de cliente,
    todo acceso pasa por track_prompt_copy()."""
    policies = _policies_on_table("prompt_copy_stats")
    assert not policies, (
        f"prompt_copy_stats no debería tener políticas de cliente, se encontró {policies}"
    )


def test_track_prompt_copy_is_security_definer():
    fn_pattern = re.compile(
        r"create (or replace )?function track_prompt_copy\s*\([^)]*\)"
        r"[\s\S]*?security definer",
        re.IGNORECASE,
    )
    assert fn_pattern.search(SCHEMA), "track_prompt_copy no está marcada 'security definer'"


def test_track_prompt_copy_grants_are_scoped_to_correct_roles():
    """Se llama tanto en sesión anónima como autenticada -- ambos roles
    necesitan grant, a diferencia de check_anon_usage/check_trial_status
    que son exclusivos de un solo rol cada una."""
    assert "grant execute on function track_prompt_copy(text[]) to anon;" in SCHEMA
    assert "grant execute on function track_prompt_copy(text[]) to authenticated;" in SCHEMA


def test_track_prompt_copy_upserts_instead_of_blind_insert():
    """Debe incrementar el contador existente (upsert), no fallar o
    duplicar filas al copiar el mismo prompt más de una vez."""
    match = re.search(
        r"create (or replace )?function track_prompt_copy\([^)]*\)"
        r"[\s\S]*?\$\$;",
        SCHEMA,
        re.IGNORECASE,
    )
    assert match, "No se encontró el cuerpo de track_prompt_copy()"
    body = match.group(0).lower()
    assert "on conflict (prompt_id) do update" in body


def test_track_prompt_copy_has_no_client_controlled_limit_param():
    """Mismo patrón de riesgo ya corregido en check_anon_usage: la firma no
    debe aceptar ningún parámetro que controle un límite o comportamiento
    sensible -- solo el arreglo de ids a incrementar."""
    match = re.search(
        r"create (?:or replace )?function track_prompt_copy\(([^)]*)\)",
        SCHEMA,
        re.IGNORECASE,
    )
    assert match, "No se encontró la firma de track_prompt_copy()"
    params = match.group(1).lower()
    assert params.strip() == "p_prompt_ids text[]", (
        f"la firma de track_prompt_copy debe ser exactamente (p_prompt_ids text[]), se encontró ({params})"
    )
