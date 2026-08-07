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
    """Se prueba la función, no el archivo generado.

    Este test falló dos veces en CI antes de quedar bien, y las dos por leer
    archivos del disco:

      1. Comparaba `index.html` (construido con las variables de producción,
         9 USD) contra `build.precio_mensual_usd()` leído en el proceso de
         pruebas, sin variables (1 USD).
      2. Al corregirlo comparando `index.html` contra `terminos.html`, falló
         igual: varias pruebas de la suite regeneran los estáticos con la
         configuración por defecto a mitad de la corrida -- el propio
         workflow lo documenta y por eso reconstruye antes de desplegar. Los
         dos archivos ya no venían del mismo build.

    `ofertas_structured_data()` no toca disco, así que da el mismo resultado
    sin importar qué pruebas corrieron antes ni con qué configuración.
    """
    ofertas = {o["name"]: o for o in build.ofertas_structured_data()}

    assert ofertas["Pro mensual"]["price"] == build.precio_mensual_usd(), (
        "los datos estructurados anunciarían un precio distinto al que cobra Paddle; "
        "quien busca en Google lo vería antes de entrar al sitio"
    )

    anual = build.paddle_public_config()["annual_amount"]
    if anual:
        assert ofertas["Pro anual"]["price"] == anual
    else:
        assert "Pro anual" not in ofertas, (
            "no debe anunciarse un plan anual que no está configurado para cobrarse"
        )


def test_la_portada_publica_las_ofertas_declaradas():
    """Que la función sea correcta no sirve si la página no la usa.

    Aquí solo se comprueba la estructura, nunca el monto: el `index.html` del
    disco puede venir de otro build (ver el test anterior), y afirmar sobre
    su precio es justo lo que hizo fallar la CI dos veces.
    """
    ofertas = _por_tipo("SoftwareApplication")["offers"]
    nombres = {o["name"] for o in ofertas}
    assert {"Free", "Pro mensual"} <= nombres, f"faltan ofertas en la portada: {nombres}"
    for oferta in ofertas:
        assert oferta["priceCurrency"] == "USD"
        assert re.fullmatch(r"\d+(\.\d{1,2})?", oferta["price"]), (
            f"precio con formato inválido para schema.org: {oferta['price']!r}"
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
