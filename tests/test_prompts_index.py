#!/usr/bin/env python3
"""
tests/test_prompts_index.py — Contrato de prompts-index.json (issue #63)

Verifica que build.build() derive un índice JSON machine-readable desde la
tabla "## Contrato editorial" / "## Editorial Contract" (issue #47/#60) de
cada prompt, para que un orquestador pueda seleccionar el prompt correcto
por consulta estructurada en vez de leer todos los archivos Markdown completos.
"""
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
PROMPTS_DIR = PROJECT_ROOT / "ai_sdlc_pro_prompts"

import build  # noqa: E402


def _all_prompt_ids():
    ids = set()
    for f in PROMPTS_DIR.glob("*.md"):
        name = f.stem
        if name == "00-framework" or name.endswith(".en"):
            continue
        parts = name.split("-")
        if parts[0] not in build.SECTION_META:
            continue
        if build._is_deprecated_or_empty(f.read_text(encoding="utf-8")):
            continue
        ids.add(name)
    return ids


def test_index_file_generated_by_build(tmp_path, monkeypatch):
    out_html = tmp_path / "out.html"
    out_index = tmp_path / "out-index.json"
    monkeypatch.setattr(build, "OUTPUT_FILE", out_html)
    monkeypatch.setattr(build, "INDEX_OUTPUT_FILE", out_index)

    build.build()

    assert out_index.exists()
    data = json.loads(out_index.read_text(encoding="utf-8"))
    assert "prompts" in data
    assert len(data["prompts"]) > 0


def test_all_prompts_have_contract_in_index(tmp_path, monkeypatch):
    """Todo prompt del índice debe tener contrato editorial completo (issue #60)."""
    out_index = tmp_path / "out-index.json"
    monkeypatch.setattr(build, "OUTPUT_FILE", tmp_path / "out.html")
    monkeypatch.setattr(build, "INDEX_OUTPUT_FILE", out_index)
    build.build()

    data = json.loads(out_index.read_text(encoding="utf-8"))
    expected_ids = _all_prompt_ids()
    indexed_ids = {p["id"] for p in data["prompts"]}
    assert indexed_ids == expected_ids

    missing_contract = [
        p["id"] for p in data["prompts"]
        if not p["contract"]["es"] or not p["contract"]["en"]
    ]
    assert missing_contract == [], f"Prompts sin contrato editorial: {missing_contract}"


def test_entry_structure_has_required_shape(tmp_path, monkeypatch):
    out_index = tmp_path / "out-index.json"
    monkeypatch.setattr(build, "OUTPUT_FILE", tmp_path / "out.html")
    monkeypatch.setattr(build, "INDEX_OUTPUT_FILE", out_index)
    build.build()

    data = json.loads(out_index.read_text(encoding="utf-8"))
    required_fields = {
        "type", "expected_risk", "required_inputs", "allowed_tools",
        "permitted_autonomy", "stop_criteria", "expected_output",
        "minimum_evidence", "recommended_next_prompt",
    }
    for p in data["prompts"]:
        assert set(p.keys()) == {"id", "section", "title", "contract"}
        assert set(p["title"].keys()) == {"es", "en"}
        for lang in ("es", "en"):
            fields = p["contract"][lang]
            assert required_fields <= set(fields.keys()), (
                f"{p['id']} ({lang}) le faltan campos: {required_fields - set(fields.keys())}"
            )


# 12-orquestador es un meta-prompt de enrutamiento: su autonomía real la
# determina dinámicamente el propio prompt (Paso 3, "Crear contrato") según
# lo que enrute, así que "permitted_autonomy" declara eso en prosa en vez de
# un nivel A0-A3 fijo -- correcto y a propósito, no forzamos un tag falso.
_DYNAMIC_AUTONOMY_EXCEPTIONS = {"12-orquestador"}


def test_categorical_tags_are_queryable_and_non_empty():
    """Cada prompt real del repo debe tener al menos un tag de tipo, riesgo
    y autonomía extraído — si esto falla, el campo categórico usa una
    palabra no reconocida por el diccionario de tags y hay que revisarlo."""
    build.build()
    data = json.loads(build.INDEX_OUTPUT_FILE.read_text(encoding="utf-8"))

    for p in data["prompts"]:
        for lang in ("es", "en"):
            c = p["contract"][lang]
            assert c["type_tags"], f"{p['id']} ({lang}): sin type_tags reconocido en '{c['type']}'"
            assert c["expected_risk_tags"], (
                f"{p['id']} ({lang}): sin expected_risk_tags reconocido en '{c['expected_risk']}'"
            )
            if p["id"] in _DYNAMIC_AUTONOMY_EXCEPTIONS:
                continue
            assert c["permitted_autonomy_tags"], (
                f"{p['id']} ({lang}): sin permitted_autonomy_tags (A0-A3) en '{c['permitted_autonomy']}'"
            )


def test_multi_level_autonomy_captures_all_levels():
    """08-03 es un prompt de dos fases (A1 análisis, A2 ejecución) -- el
    índice debe capturar ambos niveles, no solo el primero."""
    build.build()
    data = json.loads(build.INDEX_OUTPUT_FILE.read_text(encoding="utf-8"))
    p = next(x for x in data["prompts"] if x["id"] == "08-03-remediacion-maestro")
    assert set(p["contract"]["es"]["permitted_autonomy_tags"]) >= {"A1", "A2"}


def test_recommended_next_prompt_ids_resolve_to_real_prompts():
    """Los IDs extraídos de 'siguiente prompt recomendado' deben apuntar a
    prompts que existen de verdad -- si no, el regex de extracción está mal
    calibrado o el prompt referenciado fue renombrado."""
    build.build()
    data = json.loads(build.INDEX_OUTPUT_FILE.read_text(encoding="utf-8"))
    all_ids = {p["id"] for p in data["prompts"]}

    checked_any = False
    for p in data["prompts"]:
        for lang in ("es", "en"):
            for ref_id in p["contract"][lang].get("recommended_next_prompt_ids", []):
                checked_any = True
                assert ref_id in all_ids, (
                    f"{p['id']} ({lang}) referencia '{ref_id}', que no existe como prompt"
                )
    assert checked_any, "Ningún prompt produjo recommended_next_prompt_ids -- regex de extracción roto"


def test_contract_table_never_leaks_into_executable_prompt():
    """El contrato editorial vive fuera de cualquier fence ```text``` (issue
    #47) -- confirma que parse_md() nunca lo incluye en el prompt copiable,
    ni siquiera después de agregarlo al 100% de los prompts (issue #60)."""
    for f in PROMPTS_DIR.glob("*.md"):
        if f.stem == "00-framework":
            continue
        _, prompt, _, _ = build.parse_md(f)
        assert "Contrato editorial" not in prompt, f"{f.name}: fuga al prompt ejecutable"
        assert "Editorial Contract" not in prompt, f"{f.name}: fuga al prompt ejecutable"


def test_index_is_deterministic_across_runs(tmp_path, monkeypatch):
    out_index = tmp_path / "out-index.json"
    monkeypatch.setattr(build, "OUTPUT_FILE", tmp_path / "out.html")
    monkeypatch.setattr(build, "INDEX_OUTPUT_FILE", out_index)

    build.build()
    first = out_index.read_text(encoding="utf-8")
    build.build()
    second = out_index.read_text(encoding="utf-8")

    assert first == second


def test_parse_editorial_contract_handles_missing_section():
    content = "# Title\n\n## Descripción\n\nSin contrato todavía.\n\n## Contexto obligatorio previo\n"
    assert build.parse_editorial_contract(content, "es") == {}


def test_parse_editorial_contract_extracts_all_nine_fields():
    content = (
        "## Contrato editorial\n\n"
        "| Campo | Valor |\n"
        "|---|---|\n"
        "| Tipo | análisis |\n"
        "| Riesgo esperado | bajo |\n"
        "| Entradas requeridas | X |\n"
        "| Herramientas permitidas | Y |\n"
        "| Autonomía permitida | A0 |\n"
        "| Criterios de detención | Z |\n"
        "| Salida esperada | ver tabla |\n"
        "| Evidencia mínima | W |\n"
        "| Siguiente prompt recomendado | `01-02-analisis-procesos` |\n"
        "\n---\n\n## Contexto obligatorio previo\n"
    )
    fields = build.parse_editorial_contract(content, "es")
    assert fields == {
        "type": "análisis",
        "expected_risk": "bajo",
        "required_inputs": "X",
        "allowed_tools": "Y",
        "permitted_autonomy": "A0",
        "stop_criteria": "Z",
        "expected_output": "ver tabla",
        "minimum_evidence": "W",
        "recommended_next_prompt": "`01-02-analisis-procesos`",
    }
