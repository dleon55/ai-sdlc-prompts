#!/usr/bin/env python3
"""El contrato de operación debe decir lo mismo por las dos vías.

Hay dos implementaciones del mismo bloque, y tiene que ser así: la del sitio
vive en JavaScript generado por build.py (para el botón Copiar) y la del
servidor MCP vive en Node (para los agentes que consumen la biblioteca sin
navegador). No comparten runtime, así que no pueden compartir el código.

Lo que sí no pueden hacer es divergir. Es el mismo contrato editorial: si el
sitio dice "Detente y pregunta cuando" y el MCP dice otra cosa -- o peor, si
uno de los dos deja de anexar un campo -- el mismo prompt tendría límites
distintos según cómo lo pidas, que es exactamente la clase de incoherencia
que este producto vende resolver.

Este test falla si se edita un lado y no el otro.
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BUILD = RAIZ / "build.py"
MCP = RAIZ / "mcp-server" / "src" / "operatingContract.js"

# Campo canónico -> (etiqueta ES, etiqueta EN). Es la fuente de verdad del
# test: si se agrega un campo al contrato, se agrega aquí y el test exige
# que los dos lados lo implementen.
CAMPOS = {
    "permitted_autonomy": ("Autonomía máxima", "Maximum autonomy"),
    "allowed_tools": ("Herramientas permitidas", "Allowed tools"),
    "stop_criteria": ("Detente y pregunta cuando", "Stop and ask when"),
    "minimum_evidence": ("Evidencia mínima de tu salida", "Minimum evidence in your output"),
}


def _sin_comentarios(texto):
    """Descarta las líneas de comentario (// y #).

    Los dos archivos explican en un comentario por qué NO se le ordena al
    agente obedecer "por encima de todo", citando la frase. Escanear el
    archivo crudo hacía fallar el test por su propia documentación: lo que
    importa es lo que se emite al agente, no lo que se explica al humano.
    """
    return "\n".join(
        linea for linea in texto.splitlines()
        if not linea.lstrip().startswith(("//", "#"))
    )


def _build_js():
    return _sin_comentarios(BUILD.read_text(encoding="utf-8"))


def _mcp_js():
    return _sin_comentarios(MCP.read_text(encoding="utf-8"))


def test_las_etiquetas_coinciden_en_ambos_lados():
    sitio, mcp = _build_js(), _mcp_js()
    for campo, (es, en) in CAMPOS.items():
        for etiqueta in (es, en):
            assert etiqueta in sitio, f"falta '{etiqueta}' ({campo}) en el sitio (build.py)"
            assert etiqueta in mcp, f"falta '{etiqueta}' ({campo}) en el servidor MCP"


def test_el_encabezado_es_el_mismo():
    sitio, mcp = _build_js(), _mcp_js()
    for encabezado in ("## Contrato de operación", "## Operating contract"):
        assert encabezado in sitio, f"falta el encabezado '{encabezado}' en el sitio"
        assert encabezado in mcp, f"falta el encabezado '{encabezado}' en el servidor MCP"


def test_ninguno_ordena_obedecer_por_encima_de_la_tarea():
    """Decisión deliberada, y vale para las dos vías.

    Si la tarea contradice al contrato, el agente debe DECLARARLO, no elegir
    en silencio. Un "obedece esto por encima de todo" convierte una guía
    editorial en un secuestro de la instrucción del usuario, y además es la
    clase de frase que un prompt hostil imita.
    """
    for nombre, fuente in (("el sitio", _build_js()), ("el servidor MCP", _mcp_js())):
        assert not re.search(r"por encima de (todo|cualquier)", fuente, re.I), (
            f"{nombre} ordena obedecer el contrato por encima de la tarea del usuario"
        )
    for fuente in (_build_js(), _mcp_js()):
        assert "decláralo en vez de excederlas" in fuente
        assert "say so instead of exceeding them" in fuente


def test_el_orden_de_los_campos_es_el_mismo():
    """Autonomía primero: es el límite que enmarca a los otros tres."""
    mcp = _mcp_js()
    orden = re.search(r"const ORDER = \[(.*?)\]", mcp, re.S)
    assert orden, "no se encontró el orden de campos en el servidor MCP"
    ids_mcp = re.findall(r'"([a-z_]+)"', orden.group(1))
    assert ids_mcp == list(CAMPOS), f"orden inesperado en el MCP: {ids_mcp}"

    # En el sitio el orden vive como claves de una letra (ver
    # _OPERATING_CONTRACT_FIELDS en build.py); se compara la secuencia.
    sitio = _build_js()
    orden_sitio = re.search(r"var CONTRACT_ORDER = \[(.*?)\]", sitio, re.S)
    assert orden_sitio, "no se encontró CONTRACT_ORDER en el sitio"
    claves = re.findall(r"'([a-z])'", orden_sitio.group(1))
    assert claves == ["a", "t", "s", "e"], f"orden inesperado en el sitio: {claves}"
