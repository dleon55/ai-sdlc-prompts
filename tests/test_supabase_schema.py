#!/usr/bin/env python3
"""
tests/test_supabase_schema.py — Contrato de supabase/schema.sql

Bloquea que un futuro cambio a supabase/schema.sql rompa en silencio una
de las garantías de las que depende el código de sincronización en la
nube (ver AUTENTICACIÓN en build.py y docs/auth-setup.md).
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SCHEMA = (PROJECT_ROOT / "supabase" / "schema.sql").read_text(encoding="utf-8")


def test_id_column_has_default_so_client_side_import_can_omit_it():
    """pushLocalProjectsToCloud() (build.py) inserta filas sin `id` al
    importar los proyectos locales de un usuario que inicia sesión por
    primera vez -- espera que Postgres lo genere. Sin este default, ese
    insert falla con violación de NOT NULL en `id` (primary key)."""
    assert "gen_random_uuid()" in SCHEMA, (
        "Falta 'default gen_random_uuid()' en la columna id -- rompe la "
        "importación inicial de proyectos locales al iniciar sesión"
    )


def test_user_id_is_not_null_and_references_auth_users():
    assert "references auth.users(id)" in SCHEMA
    assert "user_id" in SCHEMA and "not null" in SCHEMA


def test_row_level_security_is_enabled():
    assert "enable row level security" in SCHEMA


def test_policy_restricts_both_read_and_write_to_own_rows():
    """using() controla lecturas/updates/deletes, with check() controla
    inserts/updates -- sin ambas, el anon key público (seguro de exponer
    solo porque RLS existe) expondría o permitiría modificar filas ajenas."""
    assert "using (auth.uid() = user_id)" in SCHEMA
    assert "with check (auth.uid() = user_id)" in SCHEMA
