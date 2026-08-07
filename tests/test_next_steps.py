#!/usr/bin/env python3
"""Contrato del "siguiente paso" en la tarjeta.

110 de los 112 prompts declaran a dónde seguir -- 175 aristas de un grafo
de flujo curado a mano. Ese dato ya viajaba al navegador de cada
visitante, pero solo se consumía dentro del modal de información: tres
clics adentro (icono pequeño, abrir, bajar al final). La mayoría nunca lo
veía, y el producto se leía como un catálogo de 226 tarjetas cuando en
los datos es un flujo de trabajo.
"""
import re
from pathlib import Path

import build

PROJECT_ROOT = Path(__file__).parent.parent
INDEX_HTML = (PROJECT_ROOT / "index.html").read_text(encoding="utf-8")

TITULOS = {
    "a": {"es": "Prompt A", "en": "Prompt A"},
    "b": {"es": "Prompt B", "en": "Prompt B"},
    "c": {"es": "Prompt C", "en": "Prompt C"},
    "d": {"es": "Prompt D", "en": "Prompt D"},
}


def test_no_next_steps_renders_nothing():
    """Los 2 prompts sin siguiente declarado no deben dejar un bloque
    vacío ocupando espacio en la tarjeta."""
    assert build._next_steps_html([], TITULOS, "es") == ""
    assert build._next_steps_html(None, TITULOS, "es") == ""


def test_next_steps_are_capped_so_a_hint_does_not_become_a_wall():
    """Algunos prompts declaran hasta 4 siguientes. Pintarlos todos
    convierte una pista de navegación en otro muro -- justo el problema
    que esto viene a resolver. Los demás siguen en el modal."""
    html = build._next_steps_html(["a", "b", "c", "d"], TITULOS, "es")
    assert html.count("next-chip") == build._MAX_NEXT_ON_CARD
    # Y se avisa cuántos quedaron fuera, para no ocultar que hay más.
    assert "next-more" in html
    assert "+2" in html


def test_unknown_ids_are_skipped_not_rendered_as_raw_ids():
    """Un id que no exista en el catálogo (typo en el contrato editorial,
    prompt archivado) no debe pintar un chip con el identificador crudo:
    el usuario vería '11-04-runbook' en vez de un título."""
    html = build._next_steps_html(["a", "no-existe"], TITULOS, "es")
    assert html.count("next-chip") == 1
    assert "no-existe" not in html


def test_long_titles_are_truncated_but_kept_whole_in_the_tooltip():
    """El chip se corta para que dos quepan en una línea sin romper la
    tarjeta; el título completo queda en el title= para no perder
    información."""
    largo = "Prompt con un título deliberadamente larguísimo que no cabe en un chip"
    html = build._next_steps_html(["x"], {"x": {"es": largo, "en": largo}}, "es")
    assert "…" in html
    assert 'title="' + largo + '"' in html


def test_chips_navigate_to_the_target_prompt():
    """El chip debe invocar goToPrompt con el id y el idioma, que es la
    función que ya existía para el modal."""
    html = build._next_steps_html(["a"], TITULOS, "en")
    assert "goToPrompt('a', 'en')" in html


def test_the_graph_reaches_the_rendered_page():
    """Sobre el HTML real: si la extracción de next_ids se rompe, los
    chips desaparecen sin aviso y volvemos al catálogo plano."""
    bloques = len(re.findall(r'class="card-next"', INDEX_HTML))
    chips = len(re.findall(r'class="next-chip"', INDEX_HTML))

    assert bloques > 150, f"solo {bloques} tarjetas muestran siguiente paso"
    assert chips > bloques, "debería haber más chips que bloques (varios siguientes por prompt)"
    # El grafo es lo caro de este producto: 175 aristas curadas a mano.
    # Si esto cae, es que algo se rompió aguas arriba.
    assert "goToPrompt(" in INDEX_HTML
