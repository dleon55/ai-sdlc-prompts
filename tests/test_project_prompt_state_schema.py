#!/usr/bin/env python3
"""
tests/test_project_prompt_state_schema.py — Contrato de regresión para
supabase/project_prompt_state.sql

Riesgo central: esta tabla no tiene columna user_id propia -- la propiedad
se verifica indirectamente vía projects.user_id. Si la política RLS no
filtrara correctamente por esa relación, cualquier usuario autenticado
podría leer o escribir el estado (progreso, personalización, resultados de
IA) de un proyecto ajeno usando el anon key público.
"""
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SCHEMA = (PROJECT_ROOT / "supabase" / "project_prompt_state.sql").read_text(encoding="utf-8")


def _policies_on_table(table):
    pattern = re.compile(
        r"create policy\s+\"[^\"]*\"\s+on\s+" + re.escape(table) + r"\s+for\s+(\w+)",
        re.IGNORECASE,
    )
    return [m.group(1).lower() for m in pattern.finditer(SCHEMA)]


def test_project_prompt_state_has_rls_enabled():
    assert "alter table project_prompt_state enable row level security" in SCHEMA


def test_project_prompt_state_has_no_user_id_column():
    """La propiedad se verifica vía projects.user_id, no con una columna
    user_id propia -- si alguien agregara una columna user_id aquí sin
    actualizar la política, sería fácil introducir una ruta de bypass."""
    create_table_match = re.search(
        r"create table if not exists project_prompt_state\s*\(([\s\S]*?)\);",
        SCHEMA,
        re.IGNORECASE,
    )
    assert create_table_match, "No se encontró la definición de la tabla"
    columns_block = create_table_match.group(1)
    assert not re.search(r"\buser_id\b", columns_block, re.IGNORECASE), (
        "project_prompt_state no debe tener columna user_id propia -- "
        "la propiedad se verifica indirectamente vía projects.user_id"
    )


def test_project_prompt_state_policy_checks_ownership_via_projects():
    """La política debe verificar auth.uid() = projects.user_id a través de
    una subconsulta a projects -- sin esto, RLS estaría habilitado pero sin
    ninguna restricción real de propiedad."""
    policy_match = re.search(
        r'create policy\s+"[^"]*"\s+on\s+project_prompt_state\s+for\s+all'
        r"[\s\S]*?;",
        SCHEMA,
        re.IGNORECASE,
    )
    assert policy_match, "No se encontró la política RLS de project_prompt_state"
    body = policy_match.group(0).lower()
    assert "from projects" in body, "la política no consulta la tabla projects"
    assert "projects.user_id = auth.uid()" in body, (
        "la política no verifica auth.uid() contra projects.user_id"
    )
    assert "projects.id = project_prompt_state.project_id" in body, (
        "la política no vincula project_prompt_state.project_id con projects.id"
    )


def test_project_prompt_state_policy_covers_all_operations():
    """A diferencia de subscriptions (solo lectura de cliente), aquí SÍ debe
    permitirse escritura -- el usuario dueño del proyecto necesita poder
    marcar progreso, guardar personalizaciones y pegar resultados de IA."""
    policies = _policies_on_table("project_prompt_state")
    assert policies == ["all"], f"Se esperaba solo ['all'], se encontró {policies}"


def test_project_prompt_state_has_composite_primary_key():
    assert re.search(
        r"primary key\s*\(\s*project_id\s*,\s*prompt_id\s*\)", SCHEMA, re.IGNORECASE
    ), "falta la llave primaria compuesta (project_id, prompt_id)"


def test_project_prompt_state_references_projects_with_cascade_delete():
    """Si se borra un proyecto, su estado por-prompt debe borrarse con él --
    de lo contrario quedarían filas huérfanas sin dueño verificable."""
    assert re.search(
        r"references\s+projects\s*\(\s*id\s*\)\s+on\s+delete\s+cascade",
        SCHEMA,
        re.IGNORECASE,
    ), "project_id debe referenciar projects(id) con ON DELETE CASCADE"


def test_project_prompt_state_has_expected_columns():
    for column in ("used_at", "custom_additions", "ai_output", "updated_at"):
        assert re.search(r"\b" + column + r"\b", SCHEMA), f"falta la columna {column}"
