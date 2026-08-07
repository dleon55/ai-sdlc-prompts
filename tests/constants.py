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
# Elevado de 1720 a 1800 KB al agregar la recomendación de modelo por
# prompt: un badge con tooltip explicativo en cada una de las 222 cards
# (ES+EN), +41.6 KB medidos. El tooltip lleva el porqué completo ("riesgo
# alto: necesita un modelo de razonamiento; se sube un nivel porque
# ejecuta cambios...") a propósito -- una recomendación sin justificación
# es un oráculo, y el usuario nunca aprende a decidir solo.
# Elevado de 1800 a 1900 KB al sacar el "siguiente paso" del modal a la
# tarjeta: 324 chips navegables en 220 cards (ES+EN), +76 KB medidos. El
# grafo de 175 aristas ya viajaba al navegador; solo se consumía tres
# clics adentro del modal de información, así que casi nadie lo veía.
# El costo es payload; lo que compra es que el producto deje de leerse
# como catálogo de 226 tarjetas y se lea como el flujo que ya es.
# Elevado de 1900 a 2050 KB al hacer que el contrato de operación viaje con
# el prompt copiado: techo de autonomía, herramientas permitidas, criterios
# de detención y evidencia mínima, en los 112 prompts x ES/EN, +165 KB
# medidos. Es el único de estos aumentos que NO es para pintar algo: ese
# texto se pega en el agente. Los cuatro campos estaban escritos al 100% en
# los 224 contratos y llegaban al modelo en 0% -- la gobernanza existía en
# la página y no en la sesión, que es donde hace falta.
#
# Sobre el costo: nginx comprime text/html siempre (ver nginx_prompts.conf),
# y esta prosa comprime ~4x, así que en la red son ~50 KB, no 165. El tope
# de aquí mide el archivo crudo; si se sigue subiendo conviene medir gzip o
# cargar el catálogo bajo demanda en vez de elevarlo otra vez.
# Elevado de 2050 a 2150 KB y DEGRADADO a red de seguridad. El tope crudo
# resultó ser la métrica equivocada, por dos razones medidas:
#
#   1. nginx comprime text/html siempre y esta prosa comprime ~4x, así que
#      nadie descarga esos 2 MB: son ~515 KB en la red. Un tope sobre bytes
#      crudos presupuesta algo que no existe.
#   2. El archivo en disco pesa ~15 KB más en Windows que en el runner Linux
#      por CRLF, así que el mismo commit da números distintos según dónde se
#      mida -- y el tope llegó a fallar por eso, no por contenido.
#
# El presupuesto real vive ahora en MAX_INDEX_GZIP_KB. Este se conserva como
# backstop grueso contra un error que multiplique el archivo (un bucle que
# repita el catálogo, un binario embebido por accidente), no para arbitrar
# si una funcionalidad cabe.
MAX_INDEX_SIZE_KB = 2150

# Presupuesto real: lo que el visitante descarga. Hoy son ~515 KB.
#
# Al subirlo, la pregunta correcta no es "¿cuánto creció?" sino "¿esto se
# puede cargar bajo demanda en vez de embeberlo?" -- ver el issue de carga
# diferida. Los 226 bloques <code> con el texto de los prompts pesan 803 KB
# crudos por sí solos y se envían completos aunque se abra un solo prompt:
# ese es el corte grande que sigue pendiente, y ninguna subida de tope lo
# sustituye.
MAX_INDEX_GZIP_KB = 560
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
