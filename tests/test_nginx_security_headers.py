#!/usr/bin/env python3
"""
tests/test_nginx_security_headers.py — Contrato de headers de seguridad

Bloquea que un futuro cambio a nginx_prompts.conf elimine silenciosamente
alguno de los headers de seguridad ya establecidos (ver auditoría de
seguridad: HSTS agregado tras detectar que su ausencia permitía
SSL-stripping en la primera petición HTTP antes del redirect a HTTPS).
"""
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONF = (PROJECT_ROOT / "nginx_prompts.conf").read_text(encoding="utf-8")

# Solo el VALOR del header CSP (entre comillas) -- los comentarios de este
# mismo archivo mencionan nombres de directivas ("frame-src", etc.) en
# prosa, así que buscar sobre el archivo completo da falsos positivos si
# esas palabras aparecen en un comentario antes que en el header real.
_CSP_MATCH = re.search(r'Content-Security-Policy\s+"([^"]*)"', CONF)
CSP_VALUE = _CSP_MATCH.group(1) if _CSP_MATCH else ""


def test_hsts_header_present_with_minimum_max_age():
    assert "Strict-Transport-Security" in CONF, "Falta el header HSTS"
    assert "includeSubDomains" in CONF
    assert "max-age=63072000" in CONF or "max-age=31536000" in CONF, \
        "max-age de HSTS ausente o menor al mínimo recomendado (1 año)"


def test_core_security_headers_present():
    for header in (
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Content-Security-Policy",
    ):
        assert header in CONF, f"Header de seguridad faltante: {header}"


def test_csp_restricts_object_src_and_frame_ancestors():
    assert "object-src 'none'" in CONF
    assert "frame-ancestors 'none'" in CONF


def test_csp_allows_supabase_sdk_script_and_api():
    """Regresión: al integrar el SDK de Supabase (registro de usuarios, ver
    docs/auth-setup.md) se agregó el <script src="https://cdn.jsdelivr.net/...">
    en build.py, pero se nos olvidó actualizar el CSP de producción -- el
    navegador bloqueaba silenciosamente la carga del script (violación de
    script-src) y el botón de inicio de sesión se quedaba atascado para
    siempre en "Aún cargando". connect-src también debe permitir el dominio
    del proyecto de Supabase: aunque el script cargue, cada llamada real a
    su API (auth, REST) usa fetch/XHR y quedaría bloqueada igual sin esto."""
    assert "https://cdn.jsdelivr.net" in CONF, (
        "CSP script-src no permite cdn.jsdelivr.net -- el SDK de Supabase no podría cargar"
    )
    assert "supabase.co" in CONF, (
        "CSP connect-src no permite el dominio de Supabase -- las llamadas a su API quedarían bloqueadas"
    )


def test_http_redirects_to_https():
    assert "return 301 https://$host$request_uri;" in CONF


def test_csp_allows_paddle_checkout_script_style_api_and_frame():
    """Regresión: al integrar el checkout de Paddle en /precios.html (ver
    docs/paddle-integration.md) se agregó el <script src="https://cdn.paddle.com/...">
    en build.py, pero -- mismo bug exacto que el de Supabase -- se nos
    olvidó actualizar el CSP de producción -- el botón "Suscribirme" no
    hacía nada, sin ningún aviso visible para el usuario (solo en la
    consola del navegador). A diferencia de Supabase (que solo carga un
    script y hace fetch/XHR), el checkout de Paddle se abre como iframe --
    sin frame-src también quedaría bloqueado aunque el script sí cargara.

    Segundo hallazgo real confirmado en producción (mismo despliegue):
    Paddle carga su hoja de estilos desde un SUBDOMINIO DISTINTO al del
    script en modo Sandbox (sandbox-cdn.paddle.com, no cdn.paddle.com) --
    por eso se usa un comodín *.paddle.com en vez de listar un subdominio
    exacto, que además puede diferir entre Sandbox y producción."""
    script_src = CSP_VALUE.split("script-src", 1)[1].split(";", 1)[0]
    style_src = CSP_VALUE.split("style-src", 1)[1].split(";", 1)[0]
    connect_src = CSP_VALUE.split("connect-src", 1)[1].split(";", 1)[0]
    assert "paddle.com" in script_src, (
        "CSP script-src no permite paddle.com -- el SDK de Paddle no podría cargar"
    )
    assert "paddle.com" in style_src, (
        "CSP style-src no permite paddle.com -- la hoja de estilos del checkout de Paddle quedaría bloqueada"
    )
    assert "paddle.com" in connect_src, (
        "CSP connect-src no permite paddle.com -- las llamadas del checkout a la API de Paddle quedarían bloqueadas"
    )
    assert "frame-src" in CSP_VALUE, "CSP no tiene ninguna directiva frame-src"
    frame_src = CSP_VALUE.split("frame-src", 1)[1].split(";", 1)[0]
    assert "paddle.com" in frame_src, (
        "CSP frame-src no permite paddle.com -- el iframe del checkout de Paddle quedaría bloqueado"
    )
