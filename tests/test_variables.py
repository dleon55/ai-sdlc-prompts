import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
BUILD_SOURCE = (PROJECT_ROOT / "build.py").read_text(encoding="utf-8")
PROMPTS_DIR = PROJECT_ROOT / "ai_sdlc_pro_prompts"

sys.path.insert(0, str(PROJECT_ROOT))
import extract_vars  # noqa: E402

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
    assert "currentVars.modulo || title" not in BUILD_SOURCE
    assert "var resolved = resolvePrompt(raw);" in BUILD_SOURCE
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


def test_issue_analysis_prompt_uses_distinct_configurable_tokens():
    expected_by_file = {
        "02-01-analisis-issue.md": (
            "[PEGAR]",
            "[NOMBRE O URL]",
            "[MODULO]",
            "[WORKSPACE/SUBPROYECTO]",
            "[ESTÁNDAR/COMPLIANCE]",
        ),
        "02-01-analisis-issue.en.md": (
            "[PASTE]",
            "[NAME OR URL]",
            "[MODULE]",
            "[WORKSPACE/SUBPROJECT]",
            "[STANDARD/COMPLIANCE]",
        ),
    }
    for filename, expected_tokens in expected_by_file.items():
        content = (PROMPTS_DIR / filename).read_text(encoding="utf-8")
        for token in expected_tokens:
            assert token in content

        assert "[INDICAR]" not in content
        assert "[INDICATE]" not in content
        assert "[INDICAR SI APLICA]" not in content
        assert "[INDICATE IF APPLICABLE]" not in content


def test_module_field_uses_canonical_tokens():
    registry = BUILD_SOURCE.split("var TOKEN_REGISTRY = {", 1)[1].split("};", 1)[0]
    assert "'MODULO'" in registry
    assert "'MODULE'" in registry
    assert '<span class="fw-lang-es">[MODULO]</span>' in BUILD_SOURCE
    assert '<span class="fw-lang-en">[MODULE]</span>' in BUILD_SOURCE


def test_variable_engine_has_single_registry_and_resolver():
    assert "var TOKEN_REGISTRY = {" in BUILD_SOURCE
    assert "function resolvePrompt(template, options)" in BUILD_SOURCE
    assert "var VAR_MAP = {};" in BUILD_SOURCE
    assert "TOKEN_REGISTRY[field].aliases.slice()" in BUILD_SOURCE
    assert "RAW_PROMPTS[codeId] || el.textContent" in BUILD_SOURCE
    # copySelected() valida los placeholders sin resolver del agregado antes
    # de copiar -- desde la conexión de prompts-index.json a la UI, ese
    # chequeo (antes showUnresolvedWarning(aggregate), un toast que no
    # bloqueaba el copiado) pasa por copyResolvedText(), que además bloquea
    # el copiado si hay placeholders OBLIGATORIOS sin resolver (FR-VAR-04).
    assert "function copyResolvedText(resolved, btn)" in BUILD_SOURCE
    assert "unresolvedRequired: aggregate.unresolvedRequired" in BUILD_SOURCE


def test_no_ambiguous_indicate_tokens_remain():
    for path in PROMPTS_DIR.glob("*.md"):
        content = path.read_text(encoding="utf-8")
        assert "[INDICAR]" not in content, path.name
        assert "[INDICATE]" not in content, path.name


def test_contextual_variable_panel_contract_exists():
    assert "function getPromptContextFields" in BUILD_SOURCE
    assert "function updateContextualVariablePanel" in BUILD_SOURCE
    assert 'id="var-context-status"' in BUILD_SOURCE
    for field in CANONICAL_FIELDS - {"adicionales"}:
        assert f'data-field="{field}"' in BUILD_SOURCE


def test_framework_context_controls_expose_expected_options():
    for option in (
        "PSP",
        "TSP",
        "ISO 29110",
        "ISO 9001",
        "ISO 12207",
        "ISO 25010",
        "ISO 27001",
        "ISO 27002",
        "ISO 27701",
        "CMMI-DEV",
        "MOPROSOFT",
        "MAAGTICSI",
        "NIST CSF",
        "NIST SSDF",
        "OWASP SAMM",
        "PCI DSS",
        "SOC 2",
        "GDPR",
        "HIPAA",
        "NINGUNO",
    ):
        assert f'value="{option}"' in BUILD_SOURCE

    for depth in ("bajo", "medio", "alto", "exhaustivo", "forense"):
        assert f'value="{depth}"' in BUILD_SOURCE

    assert "Objetivo puntual de salida" in BUILD_SOURCE
    assert "[INDICAR]" in BUILD_SOURCE
    assert "[NIVEL]" in BUILD_SOURCE


def test_compliance_and_methodology_support_multiple_and_custom_values():
    assert 'id="vf-compliance" multiple' in BUILD_SOURCE
    assert 'id="vf-metodologia" multiple' in BUILD_SOURCE
    assert 'id="vf-compliance-other"' in BUILD_SOURCE
    assert 'id="vf-metodologia-other"' in BUILD_SOURCE
    assert "function readFieldValue" in BUILD_SOURCE
    assert "function syncMultiSelectOther" in BUILD_SOURCE
    assert "newlySelected.indexOf('NINGUNO')" in BUILD_SOURCE
    assert "noneOption.selected = false" in BUILD_SOURCE

    for methodology in (
        "Scrum",
        "Kanban",
        "RUP",
        "Cascada",
        "Espiral",
        "XP",
        "Lean",
        "SAFe",
        "DevOps",
        "DevSecOps",
        "Trunk-Based Development",
        "GitHub Flow",
        "GitFlow",
    ):
        assert f'value="{methodology}"' in BUILD_SOURCE


def test_token_registry_has_no_dead_aliases():
    """Todo alias registrado en TOKEN_REGISTRY debe usarse en algún lado --
    como placeholder real dentro de un prompt (ai_sdlc_pro_prompts/*.md) o
    como chip de sugerencia en el propio panel de variables (.var-tag en
    build.py). Un alias que no aparece en ninguno de los dos es ruido que
    quedó del contenido tal como estaba en una edición anterior, no una
    variable real -- si esto falla, o se restauró el uso real de ese alias
    en algún lado, o hay que podarlo de TOKEN_REGISTRY (issue: limpieza del
    sistema de variables, ~39 alias muertos detectados por auditoría)."""
    registry = extract_vars.parse_registry()
    ui_tokens = extract_vars.collect_ui_tag_tokens()

    prompt_text = ""
    for path in sorted(PROMPTS_DIR.glob("*.md")):
        prompt_text += path.read_text(encoding="utf-8") + "\n"

    dead = []
    for field, config in registry.items():
        for alias in config["aliases"]:
            in_prompts = f"[{alias}]" in prompt_text or f"{{{{{alias}}}}}" in prompt_text
            in_ui = alias in ui_tokens
            if not in_prompts and not in_ui:
                dead.append(f"{field}: '{alias}'")

    assert not dead, "Alias registrados sin ningún uso real (podar de TOKEN_REGISTRY):\n" + "\n".join(dead)


def test_token_registry_scope_field_covers_all_fields():
    """Cada campo de TOKEN_REGISTRY declara scope 'project' o 'task' --
    issue: separación proyecto/tarea en el sistema de variables, para poder
    limpiar solo los campos de tarea sin perder el contexto persistente del
    proyecto (repo, stack, metodología...)."""
    block = BUILD_SOURCE.split("var TOKEN_REGISTRY = {", 1)[1].split("\n};", 1)[0]
    entries = re.split(r"\n  (?=[a-z_]+:\s*\{)", block)
    for entry in entries:
        field_match = re.match(r"\s*([a-z_]+):\s*\{", entry)
        if not field_match:
            continue
        field = field_match.group(1)
        assert "scope: 'project'" in entry or "scope: 'task'" in entry, (
            f"{field} no declara scope 'project'/'task' en TOKEN_REGISTRY"
        )
