#!/usr/bin/env python3
"""Genera los iconos del sitio a partir del logotipo oficial de LionSystems.

Por qué existen local y no se enlaza el original:

  1. **CSP.** El sitio referenciaba `https://lionsystems.com.mx/.../icon.png`,
     que responde 301 hacia `www.lionsystems.com.mx`. La política que sirve
     el servidor solo permite el dominio sin `www`, así que el navegador
     bloqueaba la imagen y el sitio quedaba SIN favicon en producción.
     Verificado en consola:

         Loading the image 'https://www.lionsystems.com.mx/...' violates the
         following Content Security Policy directive: "img-src 'self' data:
         https://lionsystems.com.mx https://www.googletagmanager.com"

     Servido desde el propio origen, `'self'` lo cubre y deja de depender de
     que la configuración del servidor y la del repositorio coincidan.

  2. **Peso.** El original mide 2048x2048 y pesa 1.3 MB. Para un icono de 32
     píxeles se descargaba más que toda la página comprimida.

  3. **Redirect.** Cada carga gastaba un salto 301 antes de la imagen.

Regenerar (requiere red, solo cuando cambie el logotipo):

    python tools/generar_favicons.py

Fuente oficial: https://lionsystems.com.mx/assets/images/icons/lionsystems_icon.png
"""

import io
import urllib.request
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = "https://lionsystems.com.mx/assets/images/icons/lionsystems_icon.png"

# 32px: la pestaña del navegador. 180px: el icono al agregar a inicio en iOS.
# No se generan más tamaños: cada uno es un archivo más que desplegar y estos
# dos cubren lo que el HTML referencia.
SALIDAS = {
    "favicon-32.png": 32,
    "apple-touch-icon.png": 180,
}


def _recortar_margen(img, umbral=250):
    """Quita el marco blanco del original.

    El logotipo trae mucho aire alrededor. A 2048px no se nota; a 32px hace
    que el león ocupe la mitad del icono y se vuelva ilegible en la pestaña.
    """
    gris = img.convert("L")
    mascara = gris.point(lambda p: 255 if p < umbral else 0)
    caja = mascara.getbbox()
    return img.crop(caja) if caja else img


def generar():
    with urllib.request.urlopen(FUENTE) as r:
        original = Image.open(io.BytesIO(r.read())).convert("RGB")

    recortado = _recortar_margen(original)

    # Se vuelve a poner en un lienzo cuadrado con un margen pequeño: sin él,
    # el león queda pegado al borde y los navegadores que redondean el icono
    # le cortan las orejas.
    lado = max(recortado.size)
    margen = int(lado * 0.08)
    lienzo = Image.new("RGB", (lado + margen * 2, lado + margen * 2), "white")
    lienzo.paste(recortado, ((lienzo.width - recortado.width) // 2,
                             (lienzo.height - recortado.height) // 2))

    for nombre, tam in SALIDAS.items():
        destino = RAIZ / nombre
        lienzo.resize((tam, tam), Image.LANCZOS).save(destino, "PNG", optimize=True)
        print(f"OK -> {nombre}  ({tam}x{tam}, {destino.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    generar()
