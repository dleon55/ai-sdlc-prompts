#!/usr/bin/env python3
"""Los datos estructurados deben decir lo que el producto realmente cobra.

Son el bloque JSON-LD que Google lee para mostrar la ficha del resultado:
categoría, idiomas y precio. A diferencia del texto visible, nadie los revisa
al navegar -- se quedan viejos en silencio, y el precio equivocado lo ve quien
todavía no entró al sitio.

Ya pasó cuatro veces en este repositorio con el precio escrito a mano en
pruebas y documentos legales. Por eso los montos salen de la misma
configuración que cobra Paddle (`build.precio_mensual_usd()`), y este test
falla si alguien los vuelve a fijar por su cuenta.
"""

import json
import re
from pathlib import Path

import pytest

import build

RAIZ = Path(__file__).resolve().parent.parent


def _bloques():
    html = (RAIZ / "index.html").read_text(encoding="utf-8", errors="replace")
    crudos = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert crudos, "index.html no declara datos estructurados"
    return [json.loads(c) for c in crudos]


def _por_tipo(tipo):
    for b in _bloques():
        if b.get("@type") == tipo:
            return b
    return None


def test_se_declara_como_software_y_no_solo_como_sitio():
    """`WebSite` dice que existe una página; no que es software con precio.

    La gente busca "prompts para agentes de IA", no el nombre del sitio. Sin
    SoftwareApplication el resultado sale como un enlace más, sin la ficha
    que muestra categoría y precio.
    """
    assert _por_tipo("WebSite"), "falta el bloque WebSite"
    app = _por_tipo("SoftwareApplication")
    assert app, "falta el bloque SoftwareApplication"
    assert app["applicationCategory"] == "DeveloperApplication"
    assert set(app["inLanguage"]) == {"es", "en"}, "el catálogo es bilingüe y debe declararlo"


def test_el_precio_publicado_es_el_que_se_cobra():
    """Se compara artefacto contra artefacto, nunca contra la configuración viva.

    La primera versión de este test llamaba a `build.precio_mensual_usd()` y
    lo comparaba con el `index.html` del disco. Falló en CI con `'9' == '1'`:
    la página se genera con las variables de producción y el test leía el
    entorno vacío del runner. Dos fuentes distintas para el mismo dato --
    exactamente el error que este archivo existe para evitar, y el mismo que
    ya rompió el build cuatro veces antes en este repositorio.

    `index.html` y `terminos.html` salen de la MISMA corrida de build.py, así
    que compararlos entre sí verifica la coherencia real sin depender de qué
    variables tenga el proceso que ejecuta las pruebas.
    """
    ofertas = {o["name"]: o for o in _por_tipo("SoftwareApplication")["offers"]}

    terminos = (RAIZ / "terminos.html").read_text(encoding="utf-8", errors="replace")
    cobrado = re.search(r"([\d.]+) USD al mes", terminos)
    assert cobrado, "terminos.html no declara el monto mensual"
    assert ofertas["Pro mensual"]["price"] == cobrado.group(1), (
        f"los datos estructurados anuncian {ofertas['Pro mensual']['price']} USD y los "
        f"términos dicen {cobrado.group(1)} USD; quien busca en Google vería el precio "
        "equivocado antes de entrar al sitio"
    )

    # El plan anual solo debe anunciarse si está configurado para cobrarse.
    # precios.html es el artefacto que sabe si existe.
    precios = (RAIZ / "precios.html").read_text(encoding="utf-8", errors="replace")
    hay_anual = bool(re.search(r'PADDLE_PRICE_ID_ANNUAL\s*=\s*"[^"]+"', precios))
    assert ("Pro anual" in ofertas) == hay_anual, (
        "se anuncia un plan anual que no está configurado para cobrarse"
        if "Pro anual" in ofertas else
        "hay plan anual configurado y no se declara en los datos estructurados"
    )


def test_el_plan_gratuito_se_declara():
    """El plan Free es la puerta de entrada; ocultarlo desperdicia el mejor gancho."""
    ofertas = {o["name"]: o for o in _por_tipo("SoftwareApplication")["offers"]}
    assert ofertas["Free"]["price"] == "0"
    assert _por_tipo("SoftwareApplication")["isAccessibleForFree"] is True


def test_no_se_inventan_resenas_ni_calificaciones():
    """Fabricar `aggregateRating` sin reseñas reales es inventar evidencia.

    Además de deshonesto, Google penaliza el marcado no verificable. Si algún
    día hay reseñas reales, este test se actualiza junto con su origen.
    """
    for bloque in _bloques():
        for campo in ("aggregateRating", "review", "ratingValue"):
            assert campo not in bloque, (
                f"'{campo}' declara evidencia social que no existe todavía"
            )


@pytest.mark.parametrize("campo", ["og:image", "twitter:image", "og:url", "og:description"])
def test_la_portada_declara_lo_necesario_para_compartirse(campo):
    html = (RAIZ / "index.html").read_text(encoding="utf-8", errors="replace")
    assert re.search(rf'(?:property|name)="{re.escape(campo)}" content="[^"]+"', html)
