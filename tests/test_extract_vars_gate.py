#!/usr/bin/env python3
"""
tests/test_extract_vars_gate.py — Contrato del gate extract_vars.py

Bloquea que un cambio futuro rompa la clasificacion de placeholders
(canonico / alias permitido / adicional / ejemplo ignorado / invalido /
tag UI no registrado) o vuelva a introducir un tag de UI cuya sugerencia
no corresponde a ningun alias real de TOKEN_REGISTRY.
"""
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import extract_vars  # noqa: E402


REQUIRED_CATEGORIES = {
    "canonical", "allowed_alias", "additional",
    "ignored_example", "invalid", "ui_tag_unregistered",
}


def test_classify_reports_all_required_categories():
    report = extract_vars.classify()
    assert REQUIRED_CATEGORIES.issubset(report.keys())
    # example_output es una categoria adicional (informativa), no reemplaza
    # a las 6 requeridas por el criterio de aceptacion.
    assert "example_output" in report


def test_no_invalid_tokens_in_current_corpus():
    report = extract_vars.classify()
    assert report["invalid"] == {}, report["invalid"]


def test_no_unregistered_ui_tags_in_current_corpus():
    report = extract_vars.classify()
    assert report["ui_tag_unregistered"] == {}, report["ui_tag_unregistered"]


def test_ui_tag_scan_finds_a_real_mismatch_when_alias_is_missing(monkeypatch):
    """Regresion: antes de este fix, los chips [AGENT LIST]/[TECH STACK]/
    etc. sugerian tokens que no existian en ningun alias -- simula ese
    estado quitando el alias 'TECH STACK' y confirma que el scanner lo
    detecta como no registrado."""
    fake_source = (
        '<span class="var-tag"><span class="fw-lang-es">[STACK TECNOLÓGICO]</span>'
        '<span class="fw-lang-en">[TECH STACK]</span></span>'
    )
    monkeypatch.setattr(extract_vars, "BUILD_SOURCE", fake_source)
    tokens = extract_vars.collect_ui_tag_tokens()
    assert "TECH STACK" in tokens

    registry_without_tech_stack = {"stack": {"required": False, "aliases": ["STACK TECNOLÓGICO"]}}
    all_registered = {
        alias for cfg in registry_without_tech_stack.values() for alias in cfg["aliases"]
    }
    unregistered = {t for t in tokens if t not in all_registered}
    assert unregistered == {"TECH STACK"}


def test_ui_tag_scan_ignores_legacy_replaces_reference():
    """El segundo token de un chip 'X reemplaza Y' / 'X replaces Y' es una
    referencia legado intencionalmente NO registrada -- no debe reportarse
    como principal."""
    fake_source = (
        '<span class="var-tag"><span class="fw-lang-es">[OBJETIVO ESPECÍFICO] reemplaza [INDICAR]</span>'
        '<span class="fw-lang-en">[SPECIFIC OBJECTIVE] replaces [INDICATE]</span></span>'
    )
    import extract_vars as ev
    original = ev.BUILD_SOURCE
    ev.BUILD_SOURCE = fake_source
    try:
        tokens = ev.collect_ui_tag_tokens()
    finally:
        ev.BUILD_SOURCE = original
    assert tokens == {"OBJETIVO ESPECÍFICO", "SPECIFIC OBJECTIVE"}
    assert "INDICAR" not in tokens
    assert "INDICATE" not in tokens


def test_expected_output_tokens_are_separated_from_prompt_formula_pool():
    """Los tokens dentro de 'Salida esperada' son ejemplos de documentacion
    (no placeholders ejecutables) y no deben aparecer en invalid/forbidden
    aunque coincidan textualmente con un token generico prohibido."""
    report = extract_vars.classify()
    assert "NOMBRE" in report["example_output"]
    assert "NOMBRE" not in report["invalid"]


def test_forbidden_tokens_still_excluded_from_registry_aliases():
    registry = extract_vars.parse_registry()
    all_aliases = {alias for cfg in registry.values() for alias in cfg["aliases"]}
    assert extract_vars.FORBIDDEN.isdisjoint(all_aliases)


def test_main_exits_nonzero_when_invalid_token_present(monkeypatch, capsys):
    monkeypatch.setattr(extract_vars, "classify", lambda: {
        "canonical": {}, "allowed_alias": {}, "additional": {},
        "ignored_example": {}, "invalid": {"NOMBRE": {"count": 1, "files": ["x.md"]}},
        "example_output": {}, "ui_tag_unregistered": {},
    })
    monkeypatch.setattr(sys, "argv", ["extract_vars.py"])
    try:
        extract_vars.main()
        assert False, "main() debio salir con SystemExit"
    except SystemExit as exc:
        assert exc.code == 1


def test_main_exits_nonzero_when_ui_tag_unregistered_present(monkeypatch):
    monkeypatch.setattr(extract_vars, "classify", lambda: {
        "canonical": {}, "allowed_alias": {}, "additional": {},
        "ignored_example": {}, "invalid": {},
        "example_output": {}, "ui_tag_unregistered": {"TECH STACK": {}},
    })
    monkeypatch.setattr(sys, "argv", ["extract_vars.py"])
    try:
        extract_vars.main()
        assert False, "main() debio salir con SystemExit"
    except SystemExit as exc:
        assert exc.code == 1


def test_main_exits_zero_when_everything_clean(monkeypatch):
    monkeypatch.setattr(extract_vars, "classify", lambda: {
        "canonical": {}, "allowed_alias": {}, "additional": {},
        "ignored_example": {}, "invalid": {},
        "example_output": {}, "ui_tag_unregistered": {},
    })
    monkeypatch.setattr(sys, "argv", ["extract_vars.py"])
    extract_vars.main()  # no debe lanzar SystemExit


def test_top_frequency_additional_tokens_were_promoted():
    """Los tokens 'adicionales' con mas apariciones en el corpus deben
    haberse promovido a alias de un campo existente (o excluirse a
    proposito por ser ambiguos) -- ninguno de los 5 mas frecuentes de la
    auditoria original queda sin decision."""
    report = extract_vars.classify()
    promoted = {"RAMA", "TEST BRANCH", "NOMBRE DEL PROYECTO", "PROJECT NAME", "LOCAL / DEV / QA / PROD"}
    for token in promoted:
        assert token not in report["additional"], f"{token} debio promoverse a allowed_alias"
        assert token in report["allowed_alias"], f"{token} no quedo registrado"
