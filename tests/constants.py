#!/usr/bin/env python3
"""
tests/constants.py — Constantes para pruebas
Extrae magic numbers del código de pruebas para mantenibilidad.
"""

# Límites de tamaño para index.html
MAX_INDEX_SIZE_KB = 1024  # 1MB límite según plan de implementación
MIN_INDEX_SIZE_KB = 100   # Mínimo esperado para contenido válido

# Cobertura de prompts
EXPECTED_PROMPT_COUNT = 44  # Total de prompts principales (00-12)
MIN_DATA_LANG_MATCHES = 44  # Mínimo 1 por prompt en cada idioma
MAX_DATA_LANG_MATCHES = 100  # Tolerancia superior

# SEO
EXPECTED_HREFLANG_COUNT = 3  # es, en, x-default

# Build performance
MAX_BUILD_TIME_SECONDS = 5

# Versiones de localStorage
CURRENT_LS_VERSION = "v1"
LS_KEY_PREFIX = f"AI_SDLC_{CURRENT_LS_VERSION}_"

# I18N
SUPPORTED_LANGUAGES = ["es", "en"]
DEFAULT_LANGUAGE = "es"
I18N_KEY = "AI_SDLC_language"
