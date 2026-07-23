#!/usr/bin/env python3
"""
tests/test_nginx_security_headers.py — Contrato de headers de seguridad

Bloquea que un futuro cambio a nginx_prompts.conf elimine silenciosamente
alguno de los headers de seguridad ya establecidos (ver auditoría de
seguridad: HSTS agregado tras detectar que su ausencia permitía
SSL-stripping en la primera petición HTTP antes del redirect a HTTPS).
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONF = (PROJECT_ROOT / "nginx_prompts.conf").read_text(encoding="utf-8")


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
