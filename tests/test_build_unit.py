#!/usr/bin/env python3
"""
tests/test_build_unit.py — Pruebas unitarias de build.py sobre fixtures

A diferencia del resto de la suite (que solo lee el index.html ya generado
y compara substrings), estas pruebas invocan directamente las funciones de
build.py — incluida build.build() — sobre directorios de prompts temporales,
para poder ejercitar casos borde que no existen hoy en ai_sdlc_pro_prompts/
(archivo sin bloques ```text```, prefijo de sección desconocido, etc.) sin
depender del contenido real del repo.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import build  # noqa: E402


def test_h_escapes_html_special_chars():
    assert build.h('<script>alert("x")</script> & co') == (
        '&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt; &amp; co'
    )


def test_icon_svg_unknown_key_falls_back_to_docs():
    unknown = build.icon_svg("clave-inexistente", "#000", 16)
    docs = build.icon_svg("docs", "#000", 16)
    assert unknown == docs


def test_parse_md_without_text_blocks_returns_full_content_as_prompt(tmp_path):
    md_file = tmp_path / "01-99-sin-bloques.md"
    md_file.write_text("# Prompt sin bloques\n\nSolo texto plano, sin ```text```.\n", encoding="utf-8")

    title, prompt, description, formulas = build.parse_md(md_file)

    assert title == "Prompt sin bloques"
    assert prompt == "# Prompt sin bloques\n\nSolo texto plano, sin ```text```."
    assert description == ""
    assert formulas == []


def test_count_prompts_skips_translations_framework_deprecated_and_empty(tmp_path, monkeypatch):
    (tmp_path / "00-framework.md").write_text("# Framework\n\n```text\nActua como...\n```\n", encoding="utf-8")
    (tmp_path / "01-01-normal.md").write_text("# Normal\n\n```text\nPrompt normal\n```\n", encoding="utf-8")
    (tmp_path / "01-01-normal.en.md").write_text("# Normal EN\n\n```text\nNormal prompt\n```\n", encoding="utf-8")
    (tmp_path / "01-02-deprecated.md").write_text("# DEPRECATED viejo\n\n```text\nviejo\n```\n", encoding="utf-8")
    (tmp_path / "01-03-vacio.md").write_text("   \n", encoding="utf-8")

    monkeypatch.setattr(build, "PROMPTS_DIR", tmp_path)

    assert build.count_prompts() == 1


def test_build_writes_html_and_skips_unknown_section_prefix(tmp_path, monkeypatch):
    (tmp_path / "00-framework.md").write_text(
        "# Framework\n\n```text\nActua como Principal Software Engineer.\n```\n", encoding="utf-8"
    )
    (tmp_path / "01-01-prompt-valido.md").write_text(
        "# Prompt valido\n\n```text\nContenido del prompt valido.\n```\n", encoding="utf-8"
    )
    (tmp_path / "99-01-seccion-desconocida.md").write_text(
        "# Seccion fuera de SECTION_META\n\n```text\nNo deberia aparecer.\n```\n", encoding="utf-8"
    )

    out_file = tmp_path / "out.html"
    monkeypatch.setattr(build, "PROMPTS_DIR", tmp_path)
    monkeypatch.setattr(build, "OUTPUT_FILE", out_file)
    monkeypatch.setattr(build, "INDEX_OUTPUT_FILE", tmp_path / "out-index.json")

    build.build()

    assert out_file.exists()
    html = out_file.read_text(encoding="utf-8")
    assert "Contenido del prompt valido." in html
    assert "01-01-prompt-valido" in html
    assert "99-01-seccion-desconocida" not in html


def test_is_deprecated_or_empty():
    assert build._is_deprecated_or_empty("   \n")
    assert build._is_deprecated_or_empty("corto")
    assert build._is_deprecated_or_empty("# DEPRECATED\n\nContenido suficientemente largo.")
    assert not build._is_deprecated_or_empty("# Prompt vigente\n\nContenido suficientemente largo.")


def test_build_excludes_deprecated_prompts_same_as_count_prompts(tmp_path, monkeypatch):
    """
    count_prompts() (usado para TOTAL_PROMPTS, el numero que se muestra en
    landing) y el loop de build() que arma `sections` comparten ahora el
    mismo filtro (_is_deprecated_or_empty): un prompt marcado DEPRECATED no
    debe aparecer ni en el total ni como card renderizada.
    """
    (tmp_path / "00-framework.md").write_text(
        "# Framework\n\n```text\nActua como Principal Software Engineer.\n```\n", encoding="utf-8"
    )
    (tmp_path / "01-01-normal.md").write_text(
        "# Normal\n\n```text\nPrompt normal.\n```\n", encoding="utf-8"
    )
    (tmp_path / "01-02-deprecated.md").write_text(
        "# DEPRECATED viejo\n\n```text\nPrompt viejo.\n```\n", encoding="utf-8"
    )

    out_file = tmp_path / "out.html"
    monkeypatch.setattr(build, "PROMPTS_DIR", tmp_path)
    monkeypatch.setattr(build, "OUTPUT_FILE", out_file)
    monkeypatch.setattr(build, "INDEX_OUTPUT_FILE", tmp_path / "out-index.json")

    assert build.count_prompts() == 1  # excluye el DEPRECATED

    build.build()
    html = out_file.read_text(encoding="utf-8")
    assert "01-02-deprecated" not in html  # build() ahora lo excluye también
    assert "Prompt normal." in html
