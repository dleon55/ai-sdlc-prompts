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


def test_http_redirects_to_https():
    assert "return 301 https://$host$request_uri;" in CONF
