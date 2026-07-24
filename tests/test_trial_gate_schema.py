#!/usr/bin/env python3
"""
tests/test_trial_gate_schema.py — Contrato de regresión para supabase/trial_gate.sql

Regla de seguridad central del diseño (04-01 riesgo #1): user_trial no debe
tener ninguna política RLS que permita a un usuario editar directamente su
propia fila. Si la tuviera, cualquiera podría extender su propia prueba
indefinidamente desde la consola del navegador con el anon key público --
la única vía de escritura sobre trial_expires_at deben ser las funciones
security definer (el trigger de creación y submit_feedback_and_renew()).
"""
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SCHEMA = (PROJECT_ROOT / "supabase" / "trial_gate.sql").read_text(encoding="utf-8")


def _policies_on_table(table):
    """Extrae los bloques 'create policy ... on <table> ...' del SQL."""
    pattern = re.compile(
        r"create policy\s+\"[^\"]*\"\s+on\s+" + re.escape(table) + r"\s+for\s+(\w+)",
        re.IGNORECASE,
    )
    return [m.group(1).lower() for m in pattern.finditer(SCHEMA)]


def test_user_trial_has_no_update_or_insert_policy_for_client():
    """Negativo a propósito: NO debe existir 'for update' ni 'for insert' ni
    'for all' sobre user_trial -- solo 'select' es aceptable."""
    policies = _policies_on_table("user_trial")
    assert policies, "user_trial no tiene ninguna política RLS -- revisar RLS habilitado"
    forbidden = {"update", "insert", "delete", "all"}
    found_forbidden = forbidden.intersection(policies)
    assert not found_forbidden, (
        f"user_trial tiene política(s) de {found_forbidden} para el cliente -- "
        "esto permitiría a un usuario auto-extender su propia prueba (ver "
        "diseño 04-01, riesgo #1). Solo debe existir una política 'for select'."
    )
    assert policies == ["select"], f"Se esperaba solo ['select'], se encontró {policies}"


def test_feedback_has_no_update_or_delete_policy():
    """El historial de feedback debe ser inmutable: insert + select, nunca
    update/delete, para preservar la integridad del log."""
    policies = _policies_on_table("feedback")
    assert set(policies) == {"insert", "select"}, (
        f"feedback debe permitir solo insert+select, se encontró {policies}"
    )


def test_all_new_tables_have_rls_enabled():
    for table in ("anon_usage", "user_trial", "feedback"):
        assert f"alter table {table} enable row level security" in SCHEMA, (
            f"Falta 'enable row level security' en la tabla {table}"
        )


def test_anon_usage_has_zero_client_policies():
    """anon_usage no debe tener NINGUNA política -- todo acceso pasa por
    check_anon_usage() (security definer), nunca directo desde el cliente."""
    policies = _policies_on_table("anon_usage")
    assert not policies, (
        f"anon_usage no debería tener políticas de cliente, se encontró {policies}"
    )


def test_write_functions_are_security_definer():
    for fn in ("check_anon_usage", "check_trial_status", "submit_feedback_and_renew", "create_user_trial"):
        fn_pattern = re.compile(
            r"create (or replace )?function " + re.escape(fn) + r"\s*\([^)]*\)"
            r"[\s\S]*?security definer",
            re.IGNORECASE,
        )
        assert fn_pattern.search(SCHEMA), f"La función {fn} no está marcada 'security definer'"


def test_trial_renewal_uses_one_month_interval():
    """Documenta explícitamente la decisión de diseño: 1 mes calendario de
    Postgres, no 30 días fijos (04-01 §2)."""
    assert "interval '1 month'" in SCHEMA


def test_grants_are_scoped_to_the_correct_role():
    assert "grant execute on function check_anon_usage(int) to anon;" in SCHEMA
    assert "grant execute on function check_trial_status() to authenticated;" in SCHEMA
    assert "grant execute on function submit_feedback_and_renew(int, text) to authenticated;" in SCHEMA
