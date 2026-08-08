#!/usr/bin/env python3
"""El texto de los prompts se sirve aparte, no dentro de index.html.

Los 226 bloques `<code>` pesaban 803 KB crudos -- el 40% del archivo -- y
viajaban a cada visitante **duplicados** en ES y EN, aunque la página muestra
un idioma a la vez y `.card-body` está oculto por defecto. Es decir: el 40%
del peso era texto que la primera carga ni siquiera pintaba.

Eso ataba cada mejora al tamaño del HTML. El tope subió tres veces en dos
días, y cada subida era una discusión sobre si la funcionalidad "cabía".

Ahora el texto vive en `prompts-text.<lang>.json` y se pide una sola vez,
solo del idioma que se está leyendo.

Lo que estas pruebas protegen no es el ahorro: es que el texto **siga
llegando**. Un fallo aquí no rompe la página -- carga, se ve bien, y los
prompts salen vacíos. Es la clase de defecto que pasa una revisión visual.
"""

import json
import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
WORKFLOW = RAIZ / ".github" / "workflows" / "deploy.yml"
ARCHIVOS = {lang: RAIZ / f"prompts-text.{lang}.json" for lang in ("es", "en")}


@pytest.fixture(scope="module")
def html():
    return (RAIZ / "index.html").read_text(encoding="utf-8", errors="replace")


@pytest.fixture(scope="module")
def textos():
    return {lang: json.loads(f.read_text(encoding="utf-8")) for lang, f in ARCHIVOS.items()}


# ── El texto salió del HTML ───────────────────────────────────────────

def test_los_bloques_de_codigo_quedan_vacios(html):
    # `[^<]+` y no `.+?`: como los bloques quedan vacíos, un patrón perezoso
    # con re.S salta al `</code>` del bloque siguiente y arrastra el markup
    # intermedio, reportando 113 falsos positivos. El texto va escapado, así
    # que dentro de un <code> con contenido nunca hay un `<`.
    con_texto = re.findall(r'<code id="code-[^"]+">([^<]+)</code>', html)
    assert not con_texto, (
        f"{len(con_texto)} bloques <code> siguen trayendo el texto embebido; "
        "el ahorro depende de que estén vacíos y se llenen al vuelo"
    )


def test_los_226_bloques_siguen_existiendo(html):
    """Vacíos, pero presentes: el JS los rellena por id."""
    assert len(re.findall(r'<code id="code-[^"]+"></code>', html)) == 226


# ── El texto sigue llegando ───────────────────────────────────────────

@pytest.mark.parametrize("lang", ["es", "en"])
def test_cada_idioma_trae_sus_113_textos(lang, textos):
    """112 prompts + el preámbulo del framework."""
    assert len(textos[lang]) == 113
    assert f"code-fw-{lang}" in textos[lang], "falta el preámbulo del framework"


@pytest.mark.parametrize("lang", ["es", "en"])
def test_ningun_texto_llega_vacio(lang, textos):
    vacios = [k for k, v in textos[lang].items() if not v or not v.strip()]
    assert not vacios, f"textos vacíos en {lang}: {vacios[:5]}"


def test_cada_bloque_del_html_tiene_su_texto(html, textos):
    """Si un id no coincide, ese prompt queda mudo y nada más falla."""
    ids = set(re.findall(r'<code id="(code-[^"]+)"></code>', html))
    disponibles = set(textos["es"]) | set(textos["en"])
    huerfanos = sorted(ids - disponibles)
    assert not huerfanos, f"estos bloques no tienen texto que cargar: {huerfanos[:5]}"


# ── El mecanismo de carga ─────────────────────────────────────────────

def test_la_pagina_sabe_pedir_el_texto(html):
    assert "function ensurePromptTexts" in html
    assert "fetch('prompts-text.' + l + '.json')" in html


def test_se_pide_una_sola_vez_por_idioma(html):
    """Sin la promesa compartida, cada card abierta dispararía otra descarga."""
    assert "_textosPendientes[l]" in html
    assert "_textosCargados[l]" in html


def test_un_fallo_de_red_no_deja_la_pagina_muda_para_siempre(html):
    """Se limpia la promesa en el catch: el siguiente intento reintenta."""
    assert "_textosPendientes[l] = null" in html


def test_la_busqueda_usa_el_texto_cargado_no_el_dom_vacio(html):
    """El `<code>` está vacío hasta que llega el JSON.

    Buscar contra `codeEl.textContent` daría cero resultados de cuerpo
    mientras carga, y nadie lo notaría: parecería que no hay coincidencias.
    """
    assert "RAW_PROMPTS[codeEl.id] || codeEl.textContent" in html


def test_copiar_espera_al_texto(html):
    """Copiar sin texto deja el portapapeles vacío, y el usuario no se entera
    hasta que pega en el agente y no pasa nada."""
    assert "ensurePromptTexts(lang)" in html
    assert "No se pudo cargar el texto del prompt" in html


def test_cambiar_de_idioma_trae_el_otro_archivo(html):
    """El idioma inactivo nunca se descargó: cambiar sin pedirlo dejaría
    todas las cards sin prompt."""
    bloque = html[html.find("function setLanguage"):][:1400]
    assert "ensurePromptTexts(lang)" in bloque


# ── Que lleguen a producción ──────────────────────────────────────────

@pytest.mark.parametrize("lang", ["es", "en"])
def test_el_despliegue_copia_los_archivos(lang):
    """Existir en el repo no basta: el deploy enumera archivos por nombre, y
    nginx responde index.html con HTTP 200 para lo que falte -- así que
    JSON.parse recibiría HTML y la página quedaría sin prompts.
    """
    w = WORKFLOW.read_text(encoding="utf-8")
    n = f"prompts-text.{lang}.json"
    assert f"cp {n} dist/{n}" in w, f"{n} no se copia a dist/ (GitHub Pages)"
    assert f'dist/{n} "${{U}}@${{H}}' in w, f"{n} no se envía al servidor de GCP"
    assert f"{n}.new ${{D}}/{n}" in w, f"{n} no se instala en producción"


# ── El ahorro ─────────────────────────────────────────────────────────

def test_index_html_ya_no_carga_el_texto_de_los_prompts(html, textos):
    """Comprobación de fondo, no de forma: el HTML no debe contener el
    cuerpo de los prompts por ninguna vía."""
    muestra = textos["es"]["code-00-B-01-scaffolding-repositorio-es"]
    fragmento = muestra.strip().splitlines()[1][:60]
    assert fragmento not in html, "el texto del prompt sigue dentro de index.html"
