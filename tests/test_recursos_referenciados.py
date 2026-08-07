#!/usr/bin/env python3
"""Todo recurso propio que el sitio referencia debe existir Y desplegarse.

Este test nace de un fallo que duró meses sin que nada lo señalara.

`index.html` declaraba `og:image` y `twitter:image` apuntando a
`/og-image.png`. El archivo nunca existió. nginx tiene
`try_files $uri $uri/ /index.html`, así que la petición devolvía **HTTP 200**
con `index.html` (2 MB de `text/html`) en vez de un 404. Cualquier
comprobación basada en el código de estado lo daba por bueno, y el resultado
era que cada vez que alguien compartía el sitio en LinkedIn, WhatsApp o Slack
no aparecía vista previa: justo el momento en que el producto se presenta a
alguien nuevo.

Es el mismo patrón que ya había ocultado las tres páginas legales.

Se comprueban dos cosas distintas, y ambas hacen falta:

  1. Que el archivo exista en el repositorio.
  2. Que el workflow de despliegue lo copie, en las DOS rutas (GitHub Pages y
     GCP). El deploy enumera archivos por nombre, no copia directorios, así
     que un recurso puede existir aquí y no llegar nunca a producción -- que
     es indistinguible de no existir para quien lo comparte.
"""

import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
WORKFLOW = RAIZ / ".github" / "workflows" / "deploy.yml"
DOMINIO = "https://prompts.lionsystems.com.mx"

# Extensiones que corresponden a un archivo servido por este sitio.
EXTENSIONES = {".png", ".ico", ".svg", ".jpg", ".jpeg", ".webp", ".gif",
               ".css", ".js", ".xml", ".txt", ".json", ".html", ".webmanifest"}

PAGINAS = ["index.html", "precios.html", "terminos.html", "privacidad.html", "reembolsos.html"]


def _recursos_propios(html):
    """Recursos servidos por este sitio, sean relativos o absolutos.

    Los externos (lionsystems.com.mx, Paddle, Supabase, Google) quedan fuera a
    propósito: no dependen de este despliegue y comprobarlos convertiría la
    suite en un monitor de terceros que falla por razones ajenas al cambio.
    """
    encontrados = set()
    for url in re.findall(r'(?:content|href|src)="([^"]+)"', html):
        if url.startswith(DOMINIO):
            ruta = url[len(DOMINIO):].split("?")[0].split("#")[0]
        elif url.startswith(("http://", "https://", "#", "mailto:", "data:", "javascript:")):
            continue
        else:
            ruta = url.split("?")[0].split("#")[0]
        ruta = ruta.lstrip("/")
        # Se exige una extensión estática conocida, no solo un punto. El
        # atributo `content` también lo usan las meta descripciones, cuyo
        # texto lleva puntos y se colaba como si fuera una ruta.
        #
        # Quedan fuera las rutas de la SPA (/app), que resuelve el ruteo
        # client-side y no corresponden a ningún archivo en disco.
        if ruta and Path(ruta).suffix.lower() in EXTENSIONES:
            encontrados.add(ruta)
    return encontrados


def _todos_los_recursos():
    recursos = {}
    for pagina in PAGINAS:
        f = RAIZ / pagina
        if not f.exists():
            continue
        for r in _recursos_propios(f.read_text(encoding="utf-8", errors="replace")):
            recursos.setdefault(r, []).append(pagina)
    return recursos


def test_los_recursos_referenciados_existen():
    faltantes = {r: p for r, p in _todos_los_recursos().items() if not (RAIZ / r).exists()}
    assert not faltantes, (
        "estos recursos se referencian y no existen: "
        + "; ".join(f"{r} (en {', '.join(p)})" for r, p in faltantes.items())
        + ". No fallan con 404: nginx responde index.html con HTTP 200, así que "
        "el error es invisible salvo para quien comparte el enlace."
    )


def test_los_recursos_se_copian_al_despliegue():
    """Existir en el repositorio no basta: el deploy enumera archivos a mano."""
    workflow = WORKFLOW.read_text(encoding="utf-8")
    sin_desplegar = [
        r for r in _todos_los_recursos()
        # Las páginas HTML ya tienen su propia cobertura; aquí interesan los
        # recursos estáticos, que son los que se olvidan al agregarse.
        if not r.endswith(".html") and f"dist/{r}" not in workflow
    ]
    assert not sin_desplegar, (
        f"estos recursos existen pero el workflow no los copia a dist/: {sin_desplegar}. "
        "Llegarían a producción como un 200 con index.html, igual que si no existieran."
    )


def test_la_tarjeta_social_llega_a_las_dos_rutas_de_despliegue():
    """GitHub Pages y GCP se despliegan por caminos distintos.

    Agregar el recurso solo a `dist/` lo publica en Pages pero no en el
    servidor de producción, que copia archivo por archivo vía scp.
    """
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "cp og-image.png dist/og-image.png" in workflow, "falta en el paso que arma dist/"
    assert "dist/og-image.png \"${U}@${H}" in workflow, "falta el scp al servidor de GCP"
    assert "og-image.png.new ${D}/og-image.png" in workflow, "falta la copia atómica en producción"


@pytest.mark.parametrize("campo", ["og:image", "twitter:image"])
def test_la_tarjeta_social_se_declara_en_la_portada(campo):
    html = (RAIZ / "index.html").read_text(encoding="utf-8", errors="replace")
    assert re.search(rf'(?:property|name)="{re.escape(campo)}" content="[^"]+"', html), (
        f"sin {campo} el enlace se comparte como texto plano, sin tarjeta"
    )


def test_la_tarjeta_social_tiene_la_proporcion_correcta():
    """1200x630. Otras medidas se recortan solas, casi siempre por el texto."""
    png = RAIZ / "og-image.png"
    assert png.exists(), "og-image.png no existe; correr python tools/generar_og_image.py"
    # Cabecera PNG: ancho y alto son big-endian de 4 bytes en el chunk IHDR.
    datos = png.read_bytes()[16:24]
    ancho = int.from_bytes(datos[0:4], "big")
    alto = int.from_bytes(datos[4:8], "big")
    assert (ancho, alto) == (1200, 630), f"se esperaba 1200x630, es {ancho}x{alto}"
