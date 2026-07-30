#!/usr/bin/env python3
"""
tests/constants.py — Constantes para pruebas
Extrae magic numbers del código de pruebas para mantenibilidad.
"""

# Límites de tamaño para index.html
# Elevado de 1024 a 1200 KB al conectar prompts-index.json a la UI (badges de
# riesgo/autonomía en 152 cards, chips de filtro por faceta, CONTRACT_TAGS
# embebido, y un paso nuevo de onboarding bilingüe) -- crecimiento de
# funcionalidad real, no bloat; con margen para crecimiento futuro moderado.
# Elevado de 1200 a 1400 KB al agregar las secciones 16 (Soporte y Mesa de
# Ayuda) y 17 (Back Office de Ingeniería) -- 10 prompts nuevos x ES/EN con
# contrato editorial completo (82 -> 92 prompts totales), issue #100.
# Elevado de 1400 a 1600 KB al agregar 8 prompts nuevos x ES/EN cubriendo
# gaps reales para analistas, testers, PM y mantenimiento/soporte (92 -> 100
# prompts totales) -- crecimiento de contenido, no bloat; con margen para
# crecimiento futuro moderado.
# Elevado de 1600 a 1650 KB al agregar 7 prompts nuevos x ES/EN (100 -> 107)
# y la capa de gestión de proyecto completa (issues #137-#140): esquema +
# checklist de progreso + personalización + resultados de IA + modo guiado
# (nuevo modal, CSS y funciones JS) -- crecimiento de funcionalidad real, no
# bloat; con margen moderado para crecimiento futuro.
# Elevado de 1650 a 1720 KB al agregar 6 prompts nuevos x ES/EN (107 -> 113)
# cerrando la auditoría final de completitud: viabilidad/business case,
# matriz de trazabilidad de requerimientos de todo el proyecto, DPIA de
# privacidad de datos, documentación pública de API, capacitación/rollout
# para usuarios finales, y revisión de éxito post-lanzamiento -- crecimiento
# de contenido real, no bloat; con margen moderado para crecimiento futuro.
MAX_INDEX_SIZE_KB = 1720
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
