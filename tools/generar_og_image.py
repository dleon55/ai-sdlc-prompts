#!/usr/bin/env python3
"""Genera og-image.png, la tarjeta que ven LinkedIn, WhatsApp y Slack.

Por qué existe este script y no un PNG suelto: la imagen es parte de cómo se
presenta el producto y va a cambiar (precio, número de prompts, mensaje).
Un binario sin origen no se puede revisar en un diff ni regenerar cuando la
paleta del sitio cambie; este script sí.

Se ejecuta a mano cuando cambie el mensaje:

    python tools/generar_og_image.py

Contexto: el sitio referenciaba og-image.png desde hace meses y el archivo
nunca existió. nginx respondía con index.html (HTTP 200, text/html, 2 MB), así
que cada vez que alguien compartía el enlace no aparecía vista previa -- y el
200 impedía que nada lo señalara como roto. Mismo patrón que ocultó las
páginas legales.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "og-image.png"

# 1200x630 es la proporción que piden Open Graph y Twitter Cards. Otras
# medidas se recortan solas, normalmente por donde está el texto.
ANCHO, ALTO = 1200, 630

# Paleta del sitio (ver las variables CSS en build.py). Se repite aquí porque
# la imagen se genera fuera del navegador; si cambia el tema, cambiar ambas.
BG = "#080b14"
BG_TARJETA = "#0f1220"
BORDE = "#262b45"
TX = "#dde1f5"
TX2 = "#8892c0"
VERDE = "#22c55e"

FUENTES = "C:/Windows/Fonts"


def _fuente(archivo, tam):
    try:
        return ImageFont.truetype(f"{FUENTES}/{archivo}", tam)
    except OSError:
        # En Linux (CI) no están las fuentes de Windows. La imagen se genera
        # a mano y se commitea, así que aquí basta con no reventar.
        return ImageFont.load_default()


def _ancho(draw, texto, fuente):
    izq, _, der, _ = draw.textbbox((0, 0), texto, font=fuente)
    return der - izq


def generar():
    img = Image.new("RGB", (ANCHO, ALTO), BG)
    d = ImageDraw.Draw(img)

    # Marco interior: da un borde visible cuando la tarjeta se muestra sobre
    # fondos claros (LinkedIn) y oscuros (Slack) sin depender del contraste.
    d.rounded_rectangle([28, 28, ANCHO - 28, ALTO - 28], radius=18,
                        fill=BG_TARJETA, outline=BORDE, width=2)

    # Barra de acento: ancla la vista arriba a la izquierda, que es por donde
    # se lee y lo último que se recorta.
    d.rounded_rectangle([72, 96, 82, 168], radius=5, fill=VERDE)

    f_titulo = _fuente("arialbd.ttf", 76)
    f_sub = _fuente("arial.ttf", 33)
    f_chip = _fuente("arialbd.ttf", 22)
    f_pie = _fuente("arial.ttf", 25)

    d.text((110, 92), "AI-SDLC Pro", font=f_titulo, fill=TX)
    d.text((112, 182), "112 prompts estructurados para dirigir", font=f_sub, fill=TX2)
    d.text((112, 224), "agentes de IA en todo el ciclo de software", font=f_sub, fill=TX2)

    # Los tres diferenciadores reales del producto, no adjetivos. Cada uno
    # corresponde a algo que existe y se puede verificar en el sitio.
    chips = ["Riesgo y autonomía por prompt", "Contrato de operación", "ES · EN"]
    x = 112
    for texto in chips:
        w = _ancho(d, texto, f_chip)
        d.rounded_rectangle([x, 316, x + w + 40, 368], radius=26,
                            fill=BG, outline=BORDE, width=2)
        d.text((x + 20, 331), texto, font=f_chip, fill=TX2)
        x += w + 40 + 16

    d.line([112, 452, ANCHO - 112, 452], fill=BORDE, width=2)
    d.text((112, 486), "prompts.lionsystems.com.mx", font=f_pie, fill=VERDE)

    pie = "Copiar · pegar · ejecutar"
    d.text((ANCHO - 112 - _ancho(d, pie, f_pie), 486), pie, font=f_pie, fill=TX2)

    img.save(SALIDA, "PNG", optimize=True)
    print(f"OK -> {SALIDA.name}  ({SALIDA.stat().st_size / 1024:.0f} KB, {ANCHO}x{ALTO})")


if __name__ == "__main__":
    generar()
