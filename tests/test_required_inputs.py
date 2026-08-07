#!/usr/bin/env python3
"""`required_inputs`: qué debe tener a la mano la persona antes de copiar.

Era el último campo del contrato editorial sin usar. Está escrito en los 224
contratos (112 prompts × ES/EN) y no aparecía en ninguna parte: ni en la
página, ni en el copiado, ni por MCP.

Importa porque **solo 17 de los 112 prompts listan sus inputs en su propio
texto**. Para los otros 95, el contrato es la única fuente estructurada de
esa información, y la persona la descubría a mitad de la conversación con el
agente -- cuando ya era tarde para prepararse.
"""

import json
import re
from pathlib import Path

import pytest

import build

RAIZ = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def html():
    return (RAIZ / "index.html").read_text(encoding="utf-8", errors="replace")


@pytest.fixture(scope="module")
def prompt_info(html):
    m = re.search(r"var PROMPT_INFO = (\{.*?\});", html, re.S)
    assert m, "PROMPT_INFO no llegó al navegador"
    return json.loads(m.group(1))


# ── El separador ──────────────────────────────────────────────────────

def test_no_parte_las_comas_dentro_de_parentesis():
    """68 de los 112 contratos las tienen; partirlas rompe el significado.

    "estado local del repositorio (rama, worktrees, commits recientes)" es UN
    requisito. Un split por comas lo convierte en cuatro, y tres quedan
    incomprensibles fuera de su paréntesis.
    """
    items = build.required_inputs_items({
        "required_inputs": "issue de referencia, estado local (rama, worktrees, commits), rama objetivo"
    })
    assert items == [
        "issue de referencia",
        "estado local (rama, worktrees, commits)",
        "rama objetivo",
    ]


def test_respeta_el_codigo_entre_backticks():
    items = build.required_inputs_items({
        "required_inputs": "plan de `04-05-versionado, deprecacion`, lista de clientes"
    })
    assert items == ["plan de `04-05-versionado, deprecacion`", "lista de clientes"]


def test_tambien_corta_en_punto_y_coma():
    """Varios contratos agrupan ideas distintas con `;`."""
    items = build.required_inputs_items({"required_inputs": "rama objetivo; agentes activos"})
    assert items == ["rama objetivo", "agentes activos"]


def test_un_contrato_sin_el_campo_no_produce_nada():
    assert build.required_inputs_items({}) == []
    assert build.required_inputs_items({"required_inputs": "   "}) == []


# ── Lo que llega al navegador ─────────────────────────────────────────

def test_todos_los_prompts_declaran_sus_inputs(prompt_info):
    """Cobertura parcial es peor que ninguna: si a veces aparece y a veces
    no, la ausencia se lee como "no necesitas nada" en vez de "no se sabe"."""
    faltantes = [
        pid for pid, info in prompt_info.items()
        if pid != "fw" and not (info.get("inputs_es") and info.get("inputs_en"))
    ]
    assert not faltantes, f"estos prompts no traen sus inputs: {faltantes[:5]}"


def test_la_tarjeta_muestra_el_conteo(html):
    """224 badges: los 112 prompts en sus dos idiomas."""
    assert html.count('class="badge-inputs"') == 224


def test_el_badge_dice_el_numero_no_solo_una_etiqueta(html):
    """"Necesitas datos" no ayuda a decidir; "6 datos" sí."""
    assert re.search(r'class="badge-inputs"[^>]*>\d+ datos?<', html)
    assert re.search(r'class="badge-inputs"[^>]*>\d+ inputs?<', html)


def test_el_conteo_del_badge_coincide_con_la_lista_del_modal(html, prompt_info):
    """El badge y el modal salen del mismo dato; si divergen, uno miente."""
    pid = next(p for p in prompt_info if p != "fw" and prompt_info[p].get("inputs_es"))
    esperado = len(prompt_info[pid]["inputs_es"])
    # Se busca el badge dentro de la card del prompt, no en todo el documento:
    # los badges van en la cabecera, antes del <code> con el texto.
    ventana = html[max(0, html.find(f'code-{pid}-es') - 6000):html.find(f'code-{pid}-es')]
    m = re.findall(r'class="badge-inputs"[^>]*>(\d+) datos?<', ventana)
    assert m, f"no se encontró el badge de {pid}"
    assert int(m[-1]) == esperado


# ── La lista completa vive en el modal ────────────────────────────────

def test_el_modal_tiene_donde_mostrarlos(html):
    for marca in ('id="modal-inputs-section"', 'id="modal-inputs"', 'id="modal-inputs-title"'):
        assert marca in html, f"falta {marca} en el modal"


def test_el_modal_los_pinta_como_texto_no_como_html(html):
    """Es texto editorial, no marcado: innerHTML aquí sería una vía de
    inyección desde el contrato, que se edita en Markdown."""
    assert "li.textContent = texto" in html
    assert "inputsEl.innerHTML = ''" in html


def test_la_lista_no_se_duplica_en_la_tarjeta(html):
    """El texto viaja UNA vez, en PROMPT_INFO.

    Repetirlo en un `title=` de cada card costaba 38.7 KB extra sin agregar
    nada: en móvil un tooltip de 4 renglones ni siquiera se puede abrir.
    """
    largo = max(
        (len(t) for t in re.findall(r'class="badge-inputs" title="([^"]*)"', html)),
        default=0,
    )
    assert largo < 60, (
        f"el tooltip del badge mide {largo} caracteres; si lleva la lista completa "
        "se está duplicando el payload en las 224 cards"
    )
