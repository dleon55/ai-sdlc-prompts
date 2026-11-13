#!/usr/bin/env python3
"""Contrato del generador de skills (spec E2 §5).

Las skills del repo público `dleon55/ai-sdlc-skills` se generan desde aquí.
Si el generador deja fuera un prompt, rompe el frontmatter o mete algo de la
plataforma (propietaria) en la salida, el daño aparece en un repo público:
estas pruebas lo detienen antes.
"""

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))
import build_skills  # noqa: E402

PRECIOS_UTM = "https://prompts.lionsystems.com.mx/precios.html?utm_source=github&utm_medium=skills"


@pytest.fixture(scope="module")
def salida(tmp_path_factory):
    out = tmp_path_factory.mktemp("skills") / "dist"
    build_skills.generar(out)
    return out


def _validador(out):
    spec = importlib.util.spec_from_file_location("validate_skills", out / "scripts" / "validate_skills.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _hash_arbol(d: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(p for p in d.rglob("*") if p.is_file()):
        h.update(f.relative_to(d).as_posix().encode())
        h.update(f.read_bytes())
    return h.hexdigest()


def test_validador_publico_en_verde(salida):
    assert _validador(salida).validar(salida) == []


def test_dos_plugins_con_una_skill_por_seccion(salida):
    mp = json.loads((salida / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert [p["name"] for p in mp["plugins"]] == ["ai-sdlc-es", "ai-sdlc-en"]
    for lang in ("es", "en"):
        skills = sorted((salida / "plugins" / f"ai-sdlc-{lang}" / "skills").iterdir())
        assert len(skills) == len(build_skills.SECCIONES)


def test_frontmatter_valido_y_nombres_unicos(salida):
    yaml = pytest.importorskip("yaml")
    nombres = []
    for sm in salida.glob("plugins/*/skills/*/SKILL.md"):
        texto = sm.read_text(encoding="utf-8")
        assert texto.startswith("---\n")
        fm = yaml.safe_load(texto.split("---\n")[1])
        assert re.fullmatch(r"[a-z0-9-]{1,64}", fm["name"])
        assert fm["name"] == sm.parent.name
        assert 0 < len(fm["description"]) <= 1024
        nombres.append(fm["name"])
    assert len(nombres) == len(set(nombres)), "un nombre de skill se repite entre ES y EN"


def test_cada_prompt_una_vez_por_idioma(salida):
    ids = [p["id"] for p in json.loads((RAIZ / "prompts-index.json").read_text(encoding="utf-8"))["prompts"]]
    for lang in ("es", "en"):
        refs = [f.stem for f in salida.glob(f"plugins/ai-sdlc-{lang}/skills/*/references/*.md")
                if f.name != "00-framework.md"]
        assert sorted(refs) == sorted(ids)


def test_paridad_con_el_mcp(salida):
    datos = json.loads((RAIZ / "mcp-server" / "data" / "prompts-full.json").read_text(encoding="utf-8"))
    prompts = datos["prompts"] if isinstance(datos, dict) else datos
    n = len(list(salida.glob("plugins/ai-sdlc-es/skills/*/references/*.md"))) - len(build_skills.SECCIONES)
    assert n == len(prompts)


def test_texto_del_prompt_intacto_y_con_atribucion(salida):
    for ref in salida.glob("plugins/ai-sdlc-es/skills/*/references/*.md"):
        original = (RAIZ / "ai_sdlc_pro_prompts" / ref.name).read_text(encoding="utf-8").rstrip("\n")
        texto = ref.read_text(encoding="utf-8")
        assert texto.startswith(original), f"{ref.name}: el texto del prompt cambió"
        assert "CC BY 4.0" in texto and PRECIOS_UTM in texto


def test_skill_md_sin_publicidad_mas_alla_de_la_atribucion(salida):
    for sm in salida.glob("plugins/*/skills/*/SKILL.md"):
        texto = sm.read_text(encoding="utf-8")
        assert texto.count("lionsystems.com.mx") == 2, f"{sm}: sólo la línea final de atribución enlaza al sitio"
        assert texto.rstrip().splitlines()[-1].count(PRECIOS_UTM) == 1


def test_sin_codigo_de_la_plataforma(salida):
    publicados = {f.relative_to(salida).as_posix() for f in salida.rglob("*") if f.is_file()}
    assert not any(p.endswith((".ts", ".html", ".sql", ".js")) for p in publicados)
    assert "scripts/build_skills.py" not in publicados and not any("build_skills" in p for p in publicados)
    fuente_build = (RAIZ / "build.py").read_text(encoding="utf-8")
    muestra = [ln for ln in fuente_build.splitlines() if len(ln.strip()) > 60][:200]
    for f in salida.rglob("*.md"):
        texto = f.read_text(encoding="utf-8")
        assert not any(ln in texto for ln in muestra), f"{f}: contiene líneas de build.py"


def test_validador_detecta_secretos_y_codigo_propietario(salida, tmp_path):
    import shutil
    copia = tmp_path / "copia"
    shutil.copytree(salida, copia)
    sm = next(copia.glob("plugins/ai-sdlc-es/skills/*/SKILL.md"))
    sm.write_text(sm.read_text(encoding="utf-8") + "\nghp_" + "a" * 36 + "\ndef parse_md(x):\n", encoding="utf-8")
    (copia / "build.py").write_text("x = 1\n", encoding="utf-8")
    errores = "\n".join(_validador(copia).validar(copia))
    assert "secreto" in errores and "parse_md" in errores and "build.py" in errores


def test_validador_detecta_frontmatter_roto(salida, tmp_path):
    import shutil
    copia = tmp_path / "copia"
    shutil.copytree(salida, copia)
    sm = next(copia.glob("plugins/ai-sdlc-en/skills/*/SKILL.md"))
    sm.write_text(sm.read_text(encoding="utf-8").replace("name: ", "name: Mal_Nombre", 1), encoding="utf-8")
    assert any("name" in e for e in _validador(copia).validar(copia))


def test_determinista(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    build_skills.generar(a)
    build_skills.generar(b)
    assert _hash_arbol(a) == _hash_arbol(b)


def test_cli_termina_en_cero(tmp_path):
    r = subprocess.run([sys.executable, str(RAIZ / "tools" / "build_skills.py"), "--out", str(tmp_path / "o")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "es: 18 skills, 112 prompts" in r.stdout
