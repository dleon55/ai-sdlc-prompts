#!/usr/bin/env python3
"""
tests/test_nginx_performance_config.py — Contrato de configuración de performance

Bloquea que un futuro cambio a nginx_prompts.conf elimine silenciosamente
la compresión afinada o la revalidación de caché (ver auditoría de
performance: sin gzip_comp_level nginx usa el nivel por defecto -1-, que
transfiere ~24% más bytes que nivel 6 para el index.html actual; sin
Cache-Control cada visita repetida re-descarga el payload completo).
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONF = (PROJECT_ROOT / "nginx_prompts.conf").read_text(encoding="utf-8")


def test_gzip_enabled_with_tuned_compression_level():
    assert "gzip on;" in CONF
    assert "gzip_comp_level" in CONF, "gzip_comp_level ausente: nginx usaría el nivel 1 por defecto"


def test_cache_control_present_for_revalidation():
    assert "Cache-Control" in CONF, (
        "Falta Cache-Control: sin esto cada visita repetida re-descarga "
        "el index.html completo aunque no haya cambiado"
    )
