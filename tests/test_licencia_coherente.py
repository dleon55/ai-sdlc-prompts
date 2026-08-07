#!/usr/bin/env python3
"""La licencia debe permitir lo que el producto promete.

Este test existe porque el repositorio ya vivió la incoherencia: `LICENSE`
decía "All Rights Reserved / UNAUTHORIZED USE PROHIBITED" mientras
`docs/STRATEGY.md` prometía "los 112 prompts, copia ilimitada y para
siempre, sin cuenta", y `mcp-server` se preparaba para publicarse en npm
(donde instalar es reproducir y ejecutar es usar).

Nadie lo notó durante meses porque una licencia no rompe ninguna prueba: el
sitio compila, los tests pasan y el paquete se empaqueta igual. El daño solo
aparece cuando alguien la lee.

Cubre también los correos de contacto: dos direcciones publicadas ya
resultaron no tener registros MX y rebotaban, dejando sin destinatario justo
a quien quería pagar o licenciar.
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LICENSE = RAIZ / "LICENSE"
LICENSE_MCP = RAIZ / "mcp-server" / "LICENSE"
PKG_MCP = RAIZ / "mcp-server" / "package.json"

# Confirmada como no entregable: sin registros MX, rebota.
CORREO_QUE_REBOTA = "contacto@lionsystems.com.mx"
CORREO_VIGENTE = "dleon555@live.com.mx"

ARCHIVOS_PUBLICOS = [
    LICENSE,
    RAIZ / "CONTRIBUTING.md",
    RAIZ / "README.md",
    RAIZ / "mcp-server" / "README.md",
    RAIZ / "docs" / "publicar-mcp.md",
]


def _texto(archivo):
    """Colapsa los saltos de línea del ajuste a 78 columnas.

    Sin esto, una frase partida entre dos renglones ("con fines\\ncomerciales")
    haría fallar la búsqueda por una razón de formato, no de contenido.
    """
    return re.sub(r"\s+", " ", archivo.read_text(encoding="utf-8"))


def test_ningun_documento_publica_un_correo_que_rebota():
    culpables = [
        f.relative_to(RAIZ).as_posix()
        for f in ARCHIVOS_PUBLICOS
        if f.exists() and CORREO_QUE_REBOTA in f.read_text(encoding="utf-8")
    ]
    assert not culpables, (
        f"estos archivos publican una dirección que rebota: {culpables}. "
        f"Quien quiera licenciar o contribuir no tiene a dónde escribir."
    )


def test_la_licencia_da_un_contacto_alcanzable():
    texto = _texto(LICENSE)
    assert CORREO_VIGENTE in texto, "LICENSE debe dar un contacto de licenciamiento vigente"


def test_los_prompts_permiten_uso_comercial():
    """CC BY, no CC BY-NC.

    El freelancer/consultor es la persona con mayor disposición a pagar
    según STRATEGY.md. Una cláusula no-comercial le prohibiría usar los
    prompts con un cliente, que es exactamente para lo que los quiere.
    """
    texto = _texto(LICENSE)
    assert "CC BY 4.0" in texto, "los prompts deben declarar su licencia"
    assert not re.search(r"BY-NC|NonCommercial|no comercial", texto, re.I), (
        "una cláusula no comercial dejaría fuera al freelancer, la persona "
        "con mayor disposición a pagar (ver docs/STRATEGY.md)"
    )
    assert "fines comerciales" in texto, "debe decir explícitamente que el uso comercial está permitido"


def test_el_servidor_mcp_se_puede_instalar_y_ejecutar():
    """Sin permiso explícito, publicar en npm distribuye algo inusable.

    Instalar un paquete es reproducirlo y ejecutarlo es usarlo: con la
    licencia propietaria anterior, cada usuario estaba en violación.
    """
    assert LICENSE_MCP.exists(), "mcp-server debe llevar su propia licencia en el paquete"
    mit = _texto(LICENSE_MCP)
    assert "MIT License" in mit
    assert "without restriction" in mit

    pkg = PKG_MCP.read_text(encoding="utf-8")
    assert '"UNLICENSED"' not in pkg, (
        "UNLICENSED marca el paquete como no distribuible: contradice publicarlo"
    )
    assert "MIT" in pkg
    # El paquete embebe los prompts, que NO son MIT. La expresión SPDX debe
    # declarar ambas licencias o estaría relicenciando contenido ajeno al código.
    assert "CC-BY-4.0" in pkg, (
        "data/prompts-full.json va embebido y es CC BY 4.0; la licencia del "
        "paquete debe declararlo, no presentarlo como MIT"
    )


def test_la_licencia_se_incluye_en_el_paquete_publicado():
    pkg = PKG_MCP.read_text(encoding="utf-8")
    archivos = re.search(r'"files"\s*:\s*\[(.*?)\]', pkg, re.S)
    assert archivos, "package.json debe declarar 'files'"
    assert "LICENSE" in archivos.group(1), (
        "publicar sin la licencia deja al usuario sin saber qué se le permite"
    )


def test_la_plataforma_sigue_siendo_propietaria():
    """El texto es libre; lo que se vende, no.

    Es la decisión del 2026-07-30 en STRATEGY.md. Si alguien relaja esto,
    que sea deliberadamente y no por arrastre al tocar la licencia.
    """
    texto = _texto(LICENSE)
    assert "build.py" in texto, "la licencia debe delimitar qué es plataforma"
    assert re.search(r"todos los derechos reservados", texto, re.I)
    assert "no otorga licencia de uso" in texto
