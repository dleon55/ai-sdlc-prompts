from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
BUILD_SOURCE = (PROJECT_ROOT / "build.py").read_text(encoding="utf-8")
PROMPTS_DIR = PROJECT_ROOT / "ai_sdlc_pro_prompts"

CANONICAL_FIELDS = {
    "repositorio",
    "referencia",
    "rama_actual",
    "rama_destino",
    "ambiente",
    "componentes",
    "modulo",
    "stack",
    "tipo_proyecto",
    "metodologia",
    "agentes",
    "autonomia",
    "entrada",
    "objetivo",
    "responsable",
    "workspace",
    "compliance",
    "documentos",
    "profundidad",
    "adicionales",
}


def test_all_canonical_fields_exist_in_project_schema_and_ui_map():
    for field in CANONICAL_FIELDS:
        assert f"{field}: ''" in BUILD_SOURCE, f"{field} falta en EMPTY_VARS"
        assert f"'{field}'" in BUILD_SOURCE, f"{field} falta en FIELD_VAR_MAP"


def test_new_context_fields_have_frontend_controls():
    for element_id in (
        "vf-entrada",
        "vf-objetivo",
        "vf-responsable",
        "vf-workspace",
        "vf-compliance",
        "vf-documentos",
        "vf-profundidad",
        "vf-adicionales",
    ):
        assert f'id="{element_id}"' in BUILD_SOURCE


def test_ambiguous_generic_aliases_are_not_auto_replaced():
    forbidden_aliases = (
        "'INDICAR'",
        "'INDICATE'",
        "'NOMBRE'",
        "'NAME'",
        "'NIVEL'",
        "'LEVEL'",
        "'TIPO'",
        "'SEVERITY'",
        "'SEVERIDAD'",
    )
    var_map = BUILD_SOURCE.split("var VAR_MAP = {", 1)[1].split("};", 1)[0]
    for alias in forbidden_aliases:
        assert alias not in var_map, f"Alias ambiguo todavía activo: {alias}"


def test_copy_preserves_user_module_and_warns_about_unresolved_tokens():
    assert "currentVars.modulo || title" in BUILD_SOURCE
    assert "function findUnresolvedPlaceholders" in BUILD_SOURCE
    assert "placeholders requieren captura manual" in BUILD_SOURCE
    assert "function parseAdditionalVars" in BUILD_SOURCE


def test_triage_prompt_uses_configurable_canonical_tokens():
    for suffix in (".md", ".en.md"):
        content = (PROMPTS_DIR / f"02-04-triage-backlog-github{suffix}").read_text(
            encoding="utf-8"
        )
        expected = (
            ("[ENTRADA PRINCIPAL]", "[OBJETIVO ESPECÍFICO]", "[RESPONSABLE]")
            if suffix == ".md"
            else ("[PRIMARY INPUT]", "[SPECIFIC OBJECTIVE]", "[ASSIGNEE]")
        )
        for token in expected:
            assert token in content


def test_requirements_prompt_uses_configurable_canonical_tokens():
    for suffix in (".md", ".en.md"):
        content = (
            PROMPTS_DIR / f"02-05-analisis-integral-requerimientos{suffix}"
        ).read_text(encoding="utf-8")
        expected = (
            ("[ENTRADA PRINCIPAL]", "[OBJETIVO ESPECÍFICO]", "[RAMA DESTINO]")
            if suffix == ".md"
            else ("[PRIMARY INPUT]", "[SPECIFIC OBJECTIVE]", "[TARGET BRANCH]")
        )
        for token in expected:
            assert token in content


def test_framework_context_uses_distinct_configurable_tokens():
    expected_by_file = {
        "00-framework.md": (
            "[WORKSPACE/SUBPROYECTO]",
            "[ESTÁNDAR/COMPLIANCE]",
            "[DOCUMENTOS A REVISAR]",
            "[OBJETIVO ESPECÍFICO]",
            "[NIVEL DE PROFUNDIDAD]",
        ),
        "00-framework.en.md": (
            "[WORKSPACE/SUBPROJECT]",
            "[STANDARD/COMPLIANCE]",
            "[DOCUMENTS TO REVIEW]",
            "[SPECIFIC OBJECTIVE]",
            "[DEPTH LEVEL]",
        ),
    }
    for filename, expected_tokens in expected_by_file.items():
        content = (PROMPTS_DIR / filename).read_text(encoding="utf-8")
        for token in expected_tokens:
            assert token in content


def test_framework_context_controls_expose_expected_options():
    for option in (
        "PSP",
        "TSP",
        "ISO 29110",
        "MOPROSOFT",
        "MAAGTICSI",
        "NINGUNO",
    ):
        assert f'value="{option}"' in BUILD_SOURCE

    for depth in ("bajo", "medio", "alto", "exhaustivo", "forense"):
        assert f'value="{depth}"' in BUILD_SOURCE

    assert "Objetivo puntual de salida" in BUILD_SOURCE
    assert "[INDICAR]" in BUILD_SOURCE
    assert "[NIVEL]" in BUILD_SOURCE
