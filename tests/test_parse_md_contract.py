#!/usr/bin/env python3
"""
tests/test_parse_md_contract.py — Contrato de build.parse_md

Verifica que parse_md separe el prompt ejecutable de las fórmulas de uso
sin depender de que la fórmula empiece literalmente con un prefijo fijo
("Usa el prompt" / "Use the prompt") — esa asimetría dejaba pasar la
mayoría de las fórmulas EN ("Use the <nombre> prompt and adapt it to:")
directo al contenido copiable.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
PROMPTS_DIR = PROJECT_ROOT / "ai_sdlc_pro_prompts"

import build  # noqa: E402


ES_FORMULA_MARKERS = ("adáptalo a:", "lo adaptes a:")
EN_FORMULA_MARKERS = ("adapt it to:",)


def _all_prompt_files():
    return sorted(PROMPTS_DIR.glob("*.md"))


def test_no_es_formula_markers_leak_into_executable_prompt():
    offenders = []
    for fp in _all_prompt_files():
        if fp.name.endswith(".en.md"):
            continue
        _, prompt, _, _ = build.parse_md(fp)
        if any(marker in prompt for marker in ES_FORMULA_MARKERS):
            offenders.append(fp.name)
    assert not offenders, f"Fórmula ES filtrada al prompt ejecutable en: {offenders}"


def test_no_en_formula_markers_leak_into_executable_prompt():
    offenders = []
    for fp in _all_prompt_files():
        if not fp.name.endswith(".en.md"):
            continue
        _, prompt, _, _ = build.parse_md(fp)
        if any(marker in prompt for marker in EN_FORMULA_MARKERS):
            offenders.append(fp.name)
    assert not offenders, f"Fórmula EN filtrada al prompt ejecutable en: {offenders}"


def test_framework_prompt_contains_only_operating_principle_es():
    _, prompt, _, formulas = build.parse_md(PROMPTS_DIR / "00-framework.md")
    assert prompt.startswith("Actúa como un Principal Software Engineer")
    assert prompt.rstrip().endswith("acciones que requieren decisión humana.")
    for marker in ES_FORMULA_MARKERS:
        assert marker not in prompt
    assert any("Quiero que uses el prompt" in f for f in formulas)


def test_framework_prompt_contains_only_operating_principle_en():
    _, prompt, _, formulas = build.parse_md(PROMPTS_DIR / "00-framework.en.md")
    assert prompt.startswith("Act as a Principal Software Engineer")
    for marker in EN_FORMULA_MARKERS:
        assert marker not in prompt
    assert any("I want you to use the prompt from" in f for f in formulas)


def test_chained_multiblock_prompts_are_preserved():
    # 00-C-02: Plan Mode + Multi-Agent Protocol son fases encadenadas
    # legítimas (no fórmula) y deben permanecer ambas en el prompt ejecutable.
    _, prompt, _, _ = build.parse_md(PROMPTS_DIR / "00-C-02-plan-mode-multiagente.md")
    assert "Opera en MODO PLAN" in prompt
    assert "protocolo de coordinación multi-agente" in prompt

    # 08-03: análisis + ejecución (segundo paso) deben permanecer ambos.
    _, prompt, _, _ = build.parse_md(PROMPTS_DIR / "08-03-remediacion-maestro.md")
    assert "Actúa como un Ingeniero de Software Senior" in prompt
    assert "Con base en el análisis y plan generado previamente" in prompt


def test_all_non_first_block_headers_are_recognized():
    """
    Todo encabezado ## que precede un bloque ```text NO-inicial debe estar
    registrado en build.HEADER_CATEGORY. Si esto falla, un prompt nuevo
    introdujo una variante de encabezado no contemplada: hay que agregarla
    al registro en vez de dejar que caiga en el fallback silencioso.
    """
    unknown = []
    for fp in _all_prompt_files():
        content = fp.read_text(encoding="utf-8")
        blocks = build._text_blocks_with_headers(content)
        for i, (header, _block) in enumerate(blocks):
            if i == 0:
                continue
            if header is None or header.strip().lower() not in build.HEADER_CATEGORY:
                unknown.append((fp.name, i, header))
    assert not unknown, f"Headers no reconocidos (agregar a HEADER_CATEGORY): {unknown}"
