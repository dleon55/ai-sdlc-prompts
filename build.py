#!/usr/bin/env python3
"""
build.py -- Genera index.html desde ai_sdlc_pro_prompts/
Uso:  cd WEB_PROMPTS && python build.py
"""
import re
import json
from pathlib import Path
from collections import defaultdict

import i18n_strings

PROMPTS_DIR = Path(__file__).parent / "ai_sdlc_pro_prompts"
OUTPUT_FILE = Path(__file__).parent / "index.html"

def count_prompts():
    count = 0
    for f in PROMPTS_DIR.glob("*.md"):
        # Ignorar traducciones, el framework base y archivos vacíos/deprecados
        if f.name.endswith(".en.md") or f.name == "00-framework.md":
            continue
        
        # Validar contenido mínimo y que no esté deprecado
        content = f.read_text(encoding="utf-8")
        if len(content.strip()) < 20 or "DEPRECATED" in content:
            continue
            
        count += 1
    return count

TOTAL_PROMPTS = count_prompts()

# (etiqueta, clave-icono)
SECTION_META = {
    "00": ("Framework base",              "framework"),
    "01": ("Comprension del repositorio", "repo"),
    "02": ("Analisis",                    "analysis"),
    "03": ("Incidentes",                  "bug"),
    "04": ("Diseno de solucion",          "design"),
    "05": ("Plan de implementacion",      "plan"),
    "06": ("Ejecucion",                   "code"),
    "07": ("Pruebas",                     "test"),
    "08": ("Revision y remediacion",      "review"),
    "09": ("Integracion y CI/CD",         "ci"),
    "10": ("Documentacion",               "docs"),
    "11": ("Operaciones",                 "ops"),
    "12": ("Orquestador",                 "orchestrator"),
    "13": ("Seguridad y DevSecOps",          "security"),
    "14": ("Monorepo y Estandares",        "orchestrator"),
    "15": ("Negocio y QA Funcional",       "docs"),
}

# Labels con tildes/enye para mostrar en UI
SECTION_LABEL = i18n_strings.SECTION_LABELS_I18N['es']

# Color accent por sección (hue de HSL)
SECTION_COLOR = {
    "00": "#f59e0b",  # amber  — framework
    "01": "#6366f1",  # indigo — repo
    "02": "#3b82f6",  # blue   — analisis
    "03": "#ef4444",  # red    — incidentes
    "04": "#8b5cf6",  # violet — diseno
    "05": "#06b6d4",  # cyan   — plan
    "06": "#10b981",  # emerald — ejecucion
    "07": "#f97316",  # orange — pruebas
    "08": "#ec4899",  # pink   — revision
    "09": "#14b8a6",  # teal   — ci
    "10": "#a3e635",  # lime   — docs
    "11": "#94a3b8",  # slate  — ops
    "12": "#c084fc",  # purple — orquestador
    "13": "#dc2626",  # red    — seguridad
    "14": "#f43f5e",  # rose   — monorepo/estandares
    "15": "#f472b6",  # light pink — negocio/qa-funcional
}

# SVG paths para cada icono (24x24 viewBox, stroke-based)
ICON_PATH = {
    "framework": '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"/>',
    "repo":      '<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 014.5 9.75h15A2.25 2.25 0 0121.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 00-1.061-.44H4.5A2.25 2.25 0 002.25 6v12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9a2.25 2.25 0 00-2.25-2.25h-5.379a1.5 1.5 0 01-1.06-.44z"/>',
    "analysis":  '<path stroke-linecap="round" stroke-linejoin="round" d="M7.5 14.25v2.25m3-4.5v4.5m3-6.75v6.75m3-9v9M6 20.25h12A2.25 2.25 0 0020.25 18V6A2.25 2.25 0 0018 3.75H6A2.25 2.25 0 003.75 6v12A2.25 2.25 0 006 20.25z"/>',
    "bug":       '<path stroke-linecap="round" stroke-linejoin="round" d="M12 12.75c1.148 0 2.278.08 3.383.237 1.037.146 1.866.966 1.866 2.013 0 3.728-2.35 6.75-5.25 6.75S6.75 18.728 6.75 15c0-1.046.83-1.867 1.866-2.013A24.204 24.204 0 0112 12.75zm0 0c2.883 0 5.647.508 8.207 1.44a23.91 23.91 0 01-1.152 6.06M12 12.75c-2.883 0-5.647.508-8.208 1.44a23.91 23.91 0 001.153 6.06M12 12.75a2.25 2.25 0 002.248-2.354M12 12.75a2.25 2.25 0 01-2.248-2.354M12 8.25c.995 0 1.971-.08 2.922-.236.403-.066.74-.358.795-.762a3.778 3.778 0 00-.399-2.25M12 8.25c-.995 0-1.97-.08-2.922-.236-.402-.066-.74-.358-.795-.762a3.778 3.778 0 01.4-2.25m0 0a5.002 5.002 0 019.45 0m-9.45 0A5.002 5.002 0 002.55 5.764"/>',
    "design":    '<path stroke-linecap="round" stroke-linejoin="round" d="M9.53 16.122a3 3 0 00-5.78 1.128 2.25 2.25 0 01-2.4 2.245 4.5 4.5 0 008.4-2.245c0-.399-.078-.78-.22-1.128zm0 0a15.998 15.998 0 003.388-1.62m-5.043-.025a15.994 15.994 0 011.622-3.395m3.42 3.42a15.995 15.995 0 004.764-4.648l3.876-5.814a1.151 1.151 0 00-1.597-1.597L14.146 6.32a15.996 15.996 0 00-4.649 4.763m3.42 3.42a6.776 6.776 0 00-3.42-3.42"/>',
    "plan":      '<path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>',
    "code":      '<path stroke-linecap="round" stroke-linejoin="round" d="M6.75 7.5l3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0021 18V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v12a2.25 2.25 0 002.25 2.25z"/>',
    "test":      '<path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"/>',
    "review":    '<path stroke-linecap="round" stroke-linejoin="round" d="M11.35 3.836c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m8.9-4.414c.376.023.75.05 1.124.08 1.131.094 1.976 1.057 1.976 2.192V16.5A2.25 2.25 0 0118 18.75h-2.25m-7.5-10.5H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V18.75m-7.5-10.5h6.375c.621 0 1.125.504 1.125 1.125v9.375m-8.25-3l1.5 1.5 3-3.75"/>',
    "ci":        '<path stroke-linecap="round" stroke-linejoin="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z"/>',
    "docs":      '<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"/>',
    "ops":       '<path stroke-linecap="round" stroke-linejoin="round" d="M5.25 14.25h13.5m-13.5 0a3 3 0 01-3-3m3 3a3 3 0 100 6h13.5a3 3 0 100-6m-16.5-3a3 3 0 013-3h13.5a3 3 0 013 3m-19.5 0a4.5 4.5 0 01.9-2.7L5.737 5.1a3.375 3.375 0 012.7-1.35h7.126c1.062 0 2.062.5 2.7 1.35l2.587 3.45a4.5 4.5 0 01.9 2.7m0 0a3 3 0 01-3 3m0 3h.008v.008h-.008v-.008zm0-6h.008v.008h-.008v-.008zm-3 6h.008v.008h-.008v-.008zm0-6h.008v.008h-.008v-.008z"/>',
    "orchestrator": '<path stroke-linecap="round" stroke-linejoin="round" d="M13.5 16.875h3.375m0 0h3.375m-3.375 0V13.5m0 3.375v3.375M6 10.5h2.25a2.25 2.25 0 002.25-2.25V6a2.25 2.25 0 00-2.25-2.25H6A2.25 2.25 0 003.75 6v2.25A2.25 2.25 0 006 10.5zm0 9.75h2.25A2.25 2.25 0 0010.5 18v-2.25a2.25 2.25 0 00-2.25-2.25H6a2.25 2.25 0 00-2.25 2.25V18A2.25 2.25 0 006 20.25zm9.75-9.75H18a2.25 2.25 0 002.25-2.25V6A2.25 2.25 0 0018 3.75h-2.25A2.25 2.25 0 0013.5 6v2.25a2.25 2.25 0 002.25 2.25z"/>',
    "security":    '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"/>',
}


def icon_svg(key, color, size=16):
    path = ICON_PATH.get(key, ICON_PATH["docs"])
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="1.7" style="flex-shrink:0;margin-top:1px">'
        f'{path}</svg>'
    )


def chevron_svg():
    return (
        '<svg width="10" height="10" viewBox="0 0 10 10" fill="none">'
        '<path d="M2.5 3.5L5 6 7.5 3.5" stroke="currentColor" stroke-width="1.6"'
        ' stroke-linecap="round" stroke-linejoin="round"/></svg>'
    )


# Clasificación de bloques ```text``` por el encabezado ## que los precede,
# no por el texto literal con el que empiezan. El contenido de cada fórmula
# de uso incluye el nombre del prompt ("Use the SAST prompt and adapt it
# to:", "Usa el prompt de auditoría FinOps y adáptalo a:"), así que matchear
# un prefijo fijo es inherentemente frágil: en inglés el nombre se inserta
# ANTES de la palabra "prompt", por lo que un prefijo como "Use the prompt"
# casi nunca coincide y la fórmula termina filtrándose al prompt ejecutable.
# El encabezado, en cambio, es un ancla estructural estable.
HEADER_CATEGORY = {
    # Bloques ejecutables: se concatenan y forman el prompt copiable.
    "prompt completo": "prompt",
    "complete prompt": "prompt",
    "full prompt": "prompt",
    "complete prompt — plan mode": "prompt",
    "complete prompt — multi-agent protocol": "prompt",
    "prompt completo — modo plan": "prompt",
    "prompt completo — protocolo multi-agente": "prompt",
    "mandatory operating principle for all prompts": "prompt",
    "principio operativo obligatorio para todos los prompts": "prompt",
    "complete master prompt": "prompt",
    "prompt maestro completo": "prompt",
    "execution prompt (second step)": "prompt",
    "prompt de ejecución (segundo paso)": "prompt",
    # Bloques de instrucción humana: se filtran del prompt copiable y quedan
    # disponibles para el modal de fórmulas (ⓘ).
    "uso con fórmula estándar": "formula",
    "use with standard formula": "formula",
    "standard formula usage": "formula",
    "usage with standard formula": "formula",
    "fórmula estándar de uso": "formula",
    "how to use this prompt library": "formula",
    "cómo usar esta biblioteca de prompts": "formula",
    "recommended commit formats": "formula",
    "formatos de commit recomendados": "formula",
}


def _text_blocks_with_headers(content):
    """Devuelve [(header_h2_o_None, bloque), ...] para cada ```text``` del documento."""
    header_positions = [
        (m.start(), m.group(1).strip())
        for m in re.finditer(r"^##\s+(.+)$", content, re.MULTILINE)
    ]
    result = []
    for m in re.finditer(r"```text\n(.*?)```", content, re.DOTALL):
        header = None
        for pos, text in header_positions:
            if pos < m.start():
                header = text
            else:
                break
        result.append((header, m.group(1).strip()))
    return result


def _classify_block(header, is_first_block):
    if header is not None:
        category = HEADER_CATEGORY.get(header.strip().lower())
        if category:
            return category
    # Encabezado ausente o no registrado: el primer bloque conserva el
    # comportamiento histórico (siempre es el prompt real); un bloque
    # posterior no reconocido se trata como fórmula para no dejar pasar
    # contenido no vetado al prompt ejecutable.
    return "prompt" if is_first_block else "formula"


def parse_md(filepath):
    content = filepath.read_text(encoding="utf-8")

    # --- título ---
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filepath.stem

    # --- todos los bloques ```text``` con su encabezado ## más cercano ---
    blocks = _text_blocks_with_headers(content)

    if not blocks:
        return title, content.strip(), "", []

    prompt_parts = []
    formula_blocks = []
    for i, (header, block) in enumerate(blocks):
        if _classify_block(header, is_first_block=(i == 0)) == "formula":
            formula_blocks.append(block)
        else:
            # Prompts reales encadenados (ej. 08-03 ejecución: "Con base en el análisis...")
            prompt_parts.append(block)

    prompt = "\n\n---\n\n".join(prompt_parts)

    # --- descripción de la sección ## Descripción (para el botón ⓘ) ---
    desc_match = re.search(
        r"##\s+Descripci[oó]n\s*\n([\s\S]*?)(?=\n##\s|\Z)", content
    )
    description = ""
    if desc_match:
        raw = desc_match.group(1)
        raw = re.sub(r"\*\*(.*?)\*\*", r"\1", raw)          # **bold** → plain
        raw = re.sub(r"^\s*>\s*", "", raw, flags=re.MULTILINE)  # blockquotes
        raw = re.sub(r"^\s*---+\s*$", "", raw, flags=re.MULTILINE)  # líneas HR
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        description = raw.strip()

    return title, prompt, description, formula_blocks


def h(text):
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


CSS = """
:root {
  --hdr:  58px;
  --bar:  46px;
  --side: 220px;
  --bg:   #080b14;
  --bg2:  #0f1220;
  --bg3:  #161929;
  --bg4:  #1c2035;
  --bdr:  #1f2340;
  --bdr2: #262b45;
  --tx:   #dde1f5;
  --tx2:  #8892c0;
  --tx3:  #454d6e;
  --grn:  #22c55e;
  --warn: #f59e0b;
  --mono: 'JetBrains Mono','Fira Code','Cascadia Code','Courier New',monospace;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html[lang="es"] .card[data-lang="en"],
html[lang="es"] .fw-lang-en,
html[lang="es"] .sec-lang-en,
html[lang="es"] .sid-lang-en { display: none !important; }

html[lang="en"] .card[data-lang="es"],
html[lang="en"] .fw-lang-es,
html[lang="en"] .sec-lang-es,
html[lang="en"] .sid-lang-es { display: none !important; }

/* Selectores requeridos para pruebas de integración */
html[data-lang="es"] .card[data-lang="es"] {}
html[data-lang="en"] .card[data-lang="en"] {}
html { scroll-behavior: smooth; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg); color: var(--tx); font-size: 14px; line-height: 1.5;
  min-height: 100vh;
}
#app-root, #landing-root { min-height: 100vh; display: flex; flex-direction: column; }
#app-root { overflow: visible; } /* Permite scroll del body */

/* ═══════════════════════════ HEADER ════════════════════════════ */
header {
  height: var(--hdr); flex-shrink: 0;
  background: var(--bg2);
  border-bottom: 1px solid var(--bdr);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 1rem; z-index: 300;
  position: sticky; top: 0;
}
.hdr-logo { display: flex; align-items: center; gap: .65rem; }
.hdr-logo svg { flex-shrink: 0; }
.hdr-logo h1 {
  font-size: .95rem; font-weight: 700; letter-spacing: .015em;
  background: linear-gradient(90deg, #818cf8, #c084fc);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hdr-logo p { font-size: .68rem; color: var(--tx3); margin-top: .05rem; }
.hdr-tags { display: flex; align-items: center; gap: .5rem; }
.tag {
  font-size: .62rem; font-weight: 600; letter-spacing: .04em;
  background: var(--bg3); border: 1px solid var(--bdr2);
  color: var(--tx3); border-radius: 4px; padding: .15rem .5rem;
}
.tag-warn { border-color: #78350f; color: var(--warn); background: #1c1006; }
.hdr-brand {
  display: flex; align-items: center; gap: .45rem;
  border-left: 1px solid var(--bdr2); padding-left: .85rem; margin-left: .35rem;
}
.hdr-brand-text { font-size: .7rem; font-weight: 700; letter-spacing: .04em; color: #f59e0b; }
.hdr-brand-sub { font-size: .58rem; color: var(--tx3); display: block; line-height: 1.1; }

.lang-wrap { position: relative; }
.lang-btn {
  background: var(--bg3); border: 1px solid var(--bdr2); border-radius: 6px;
  color: var(--tx2); padding: 5px 10px; cursor: pointer; display: flex; align-items: center; gap: 6px;
  font-size: .72rem; font-weight: 600; transition: all .2s;
}
.lang-btn:hover { border-color: #6366f1; color: #fff; }
.lang-label { font-family: var(--mono); }
.lang-dropdown {
  position: absolute; top: calc(100% + 5px); right: 0; background: var(--bg2);
  border: 1px solid var(--bdr2); border-radius: 8px; min-width: 110px;
  display: none; flex-direction: column; overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5); z-index: 1000;
}
.lang-dropdown.open { display: flex; }
.lang-option {
  padding: 8px 12px; font-size: .78rem; color: var(--tx2); cursor: pointer;
  transition: background .2s, color .2s;
}
.lang-option:hover { background: var(--bg3); color: #fff; }
.lang-option[selected] { color: #6366f1; font-weight: 700; }

/* ═══════════════════════════ SEARCH BAR ════════════════════════ */
.search-bar {
  min-height: var(--bar); height: auto; flex-shrink: 0;
  background: var(--bg); border-bottom: 1px solid var(--bdr);
  display: flex; align-items: center; flex-wrap: wrap;
  padding: 0.5rem 1.25rem 0.5rem calc(var(--side) + 1.25rem);
  gap: .65rem; z-index: 299;
}
.search-wrap { position: relative; flex: 1; max-width: 560px; }
.search-ico {
  position: absolute; left: .65rem; top: 50%; transform: translateY(-50%);
  color: var(--tx3); pointer-events: none;
}
.search-bar input {
  width: 100%; padding: .35rem .85rem .35rem 2rem;
  border-radius: 6px; border: 1px solid var(--bdr2);
  background: var(--bg3); color: var(--tx); font-size: .82rem; outline: none;
  transition: border-color .15s;
}
.search-bar input::placeholder { color: var(--tx3); }
.search-bar input:focus { border-color: #6366f1; box-shadow: 0 0 0 2px rgba(99,102,241,.15); }
.search-count { font-size: .7rem; color: var(--tx3); white-space: nowrap; }

/* ═══════════════════════════ LAYOUT ════════════════════════════ */
.layout { display: flex; flex: 1; }

/* ═══════════════════════════ SIDEBAR ═══════════════════════════ */
.sidebar {
  width: var(--side); flex-shrink: 0;
  background: var(--bg2); border-right: 1px solid var(--bdr);
  display: flex; flex-direction: column;
  transition: transform .25s ease;
}
/* Estilo unificado de menú hamburguesa (Overlay) */
@media (max-width: 1024px) {
  .sidebar { 
    position: fixed; top: var(--hdr); left: 0; bottom: 0; 
    z-index: 400; transform: translateX(-100%); 
    height: calc(100vh - var(--hdr));
    overflow-y: auto; box-shadow: 10px 0 30px rgba(0,0,0,0.5);
  }
  body.menu-open .sidebar { transform: translateX(0); }
  .sidebar-overlay { 
    position: fixed; inset: 0; background: rgba(0,0,0,0.5); 
    z-index: 399; display: none; 
  }
  body.menu-open .sidebar-overlay { display: block; }
}
@media (min-width: 1025px) {
  /* BUG-01 fix #29: regla width:0 eliminada — icon-only (46px) lo maneja body.sidebar-collapsed */
  .menu-toggle-btn { display: none; }
}
body.sidebar-collapsed .sidebar-collapse-btn svg { transform: rotate(180deg); }
.sidebar::-webkit-scrollbar { width: 3px; }
.sidebar::-webkit-scrollbar-thumb { background: var(--bdr2); border-radius: 2px; }
.sid-section { padding: .5rem 0; }
.sid-label {
  font-size: .58rem; font-weight: 700; color: var(--tx3);
  text-transform: uppercase; letter-spacing: .12em;
  padding: .6rem 1rem .3rem;
}
.sid-link {
  display: flex; align-items: center; gap: .5rem;
  padding: .32rem .85rem .32rem 1rem;
  cursor: pointer; text-decoration: none;
  border-left: 2px solid transparent;
  transition: all .12s;
}
.sid-link:hover { background: var(--bg3); }
.sid-link.active { background: rgba(99,102,241,.1); border-left-color: #6366f1; }
.sid-icon { flex-shrink: 0; opacity: .65; transition: opacity .12s; }
.sid-link:hover .sid-icon,
.sid-link.active .sid-icon { opacity: 1; }
.sid-text { flex: 1; font-size: .74rem; color: var(--tx2); line-height: 1.3; transition: color .12s; }
.sid-link:hover .sid-text { color: var(--tx); }
.sid-link.active .sid-text { color: #a5b4fc; font-weight: 500; }
.sid-badge {
  flex-shrink: 0; font-size: .58rem; font-weight: 700;
  background: var(--bg4); border: 1px solid var(--bdr2);
  color: var(--tx3); border-radius: 10px; padding: .05rem .4rem;
  min-width: 18px; text-align: center; transition: all .12s;
}
.sid-link.active .sid-badge { background: #6366f1; border-color: #6366f1; color: #fff; }
.sid-framework { background: rgba(245,158,11,.06); }
.sid-framework .sid-text { color: #d97706; }
.sid-framework.active { background: rgba(245,158,11,.12); border-left-color: var(--warn); }
.sid-framework.active .sid-text { color: var(--warn); }
.sid-framework.active .sid-badge { background: var(--warn); border-color: var(--warn); }

/* ═══════════════════════════ CONTENT ═══════════════════════════ */
.content {
  flex: 1; padding: 1.5rem 1.75rem 5rem;
  min-width: 0;
}
.content::-webkit-scrollbar { width: 5px; }
.content::-webkit-scrollbar-thumb { background: var(--bdr2); border-radius: 3px; }

/* ────── Framework banner ────── */
.framework-banner {
  background: linear-gradient(135deg, #1a1306 0%, #0f1220 60%);
  border: 1px solid #78350f;
  border-radius: 10px; margin-bottom: 2rem; overflow: hidden;
  scroll-margin-top: .5rem;
}
.fw-header {
  display: flex; align-items: center; gap: .75rem;
  padding: .85rem 1rem; border-bottom: 1px solid #78350f;
}
.fw-badge {
  font-size: .6rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: .08em; background: var(--warn); color: #000;
  border-radius: 4px; padding: .15rem .5rem;
}
.fw-title { font-size: .88rem; font-weight: 600; color: #fbbf24; flex: 1; }
.fw-desc { font-size: .72rem; color: #92400e; padding: .5rem 1rem; }
.fw-body { padding: 0; border-top: none; display: none; }
.fw-body.open { display: block; }
.fw-expand svg { transition: transform .2s ease; }
.fw-expand.open svg { transform: rotate(180deg); }
.fw-body pre {
  margin: 0; padding: .85rem 1rem;
  background: #06040a; max-height: 340px; overflow-y: auto; border-radius: 0;
  border: none; border-top: 1px solid #1c1a06;
}
.fw-copy-row {
  display: flex; justify-content: flex-end;
  padding: .45rem .85rem; background: #100d02; border-top: 1px solid #1c1a06;
}
.fw-copy-btn {
  padding: .25rem .75rem; background: var(--warn); border: none;
  border-radius: 5px; color: #000; font-size: .72rem;
  cursor: pointer; font-weight: 700; transition: background .12s; font-family: inherit;
}
.fw-copy-btn:hover { background: #fbbf24; }
.fw-copy-btn.ok { background: var(--grn); color: #fff; }

/* ────── Section group ────── */
.section-group { margin-bottom: 2rem; scroll-margin-top: .5rem; }
.section-header-row {
  display: flex; align-items: center; gap: .6rem;
  padding-bottom: .55rem; margin-bottom: .8rem;
  border-bottom: 1px solid var(--bdr);
}
.sec-num {
  font-size: .6rem; font-weight: 700; font-family: var(--mono);
  letter-spacing: .04em; padding: .12rem .45rem;
  border-radius: 4px; border: 1px solid; flex-shrink: 0;
}
.sec-label {
  font-size: .72rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: .08em; color: var(--tx3); flex: 1;
}
.sec-count {
  font-size: .62rem; color: var(--tx3); background: var(--bg3);
  border: 1px solid var(--bdr); border-radius: 10px; padding: .05rem .45rem;
}

/* ────── Grid de cards ────── */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: .55rem;
}

/* ────── Card ────── */
.card {
  background: var(--bg2); border: 1px solid var(--bdr);
  border-radius: 8px; overflow: hidden; transition: border-color .22s cubic-bezier(0.4, 0, 0.2, 1), box-shadow .22s cubic-bezier(0.4, 0, 0.2, 1), transform .22s cubic-bezier(0.4, 0, 0.2, 1);
}
.card:hover { border-color: #6366f199; box-shadow: 0 8px 24px rgba(99,102,241,0.18); transform: translateY(-3px) scale(1.005); }

/* Card header: siempre visible */
.card-head {
  display: flex; align-items: center; gap: .45rem;
  padding: .55rem .75rem; min-height: 42px;
}
.card-expand {
  flex-shrink: 0; background: none; border: none; cursor: pointer;
  color: var(--tx3); width: 20px; height: 20px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 4px; transition: color .12s, background .12s;
}
.card-expand:hover { color: var(--tx); background: var(--bg4); }
.card-expand svg { transition: transform .18s; }
.card-expand.open svg { transform: rotate(180deg); }
.card-title {
  flex: 1; font-size: .78rem; font-weight: 500; color: #c4c9e8;
  line-height: 1.35; cursor: pointer; min-width: 0;
}
.card-title:hover { color: var(--tx); }
.copy-btn {
  flex-shrink: 0; padding: .2rem .6rem;
  background: var(--bg4); border: 1px solid var(--bdr2);
  border-radius: 5px; color: var(--tx2); font-size: .68rem;
  cursor: pointer; font-weight: 600; transition: all .12s;
  white-space: nowrap; font-family: inherit; display: flex; align-items: center; gap: .3rem;
}
.copy-btn:hover { background: #6366f1; border-color: #6366f1; color: #fff; }
.copy-btn.ok { background: var(--grn); border-color: var(--grn); color: #fff; }

/* Card body: colapsable */
.card-body { display: none; border-top: 1px solid var(--bdr); }
.card-body.open { display: block; }
pre {
  margin: 0; padding: .7rem .9rem;
  background: #04050d; overflow-x: auto; max-height: 400px; overflow-y: auto;
}
code {
  font-family: var(--mono);
  font-size: .7rem; color: #a8b0d8; white-space: pre-wrap; word-break: break-word;
  line-height: 1.6;
}

/* ────── Empty state ────── */
.glbl-empty {
  text-align: center; padding: 3.5rem 1rem; color: var(--tx3);
}
.glbl-empty p { font-size: .88rem; margin-bottom: .4rem; }
.glbl-empty small { font-size: .72rem; color: var(--tx3); }

/* ═══════════════════════════ VARIABLES PANEL ═══════════════════ */
.var-panel {
  position: fixed; top: 0; right: 0; height: 100vh; width: 300px;
  background: var(--bg2); border-left: 1px solid var(--bdr);
  display: flex; flex-direction: column; z-index: 500;
  transform: translateX(100%); transition: transform .22s ease;
}
.var-panel.open { transform: translateX(0); }
.var-panel-hdr {
  display: flex; align-items: center; justify-content: space-between;
  padding: .85rem 1rem; border-bottom: 1px solid var(--bdr); flex-shrink: 0;
}
.var-panel-hdr h2 {
  font-size: .82rem; font-weight: 700; color: var(--tx);
  display: flex; align-items: center; gap: .4rem;
}
.var-close-btn {
  background: none; border: none; cursor: pointer; color: var(--tx3);
  padding: .2rem; border-radius: 4px; font-size: 1rem; line-height: 1;
  transition: color .12s;
}
.var-close-btn:hover { color: var(--tx); }
.var-panel-body {
  flex: 1; overflow-y: auto; padding: .85rem 1rem;
  display: flex; flex-direction: column; gap: .75rem;
}
.var-panel-body::-webkit-scrollbar { width: 3px; }
.var-panel-body::-webkit-scrollbar-thumb { background: var(--bdr2); border-radius: 2px; }
.var-group label {
  display: block; font-size: .66rem; font-weight: 700; color: var(--tx3);
  text-transform: uppercase; letter-spacing: .08em; margin-bottom: .3rem;
}
.var-group input, .var-group select, .var-group textarea {
  width: 100%; background: var(--bg3); border: 1px solid var(--bdr2);
  color: var(--tx); font-size: .76rem; border-radius: 5px; outline: none;
  transition: border-color .12s; font-family: inherit;
}
.var-group input, .var-group select { padding: .35rem .6rem; }
.var-group textarea { padding: .35rem .6rem; resize: vertical; min-height: 56px; }
.var-group select[multiple] { min-height: 132px; padding: .3rem; }
.var-group select[multiple] option { padding: .28rem .4rem; border-radius: 3px; }
.var-group input:focus, .var-group select:focus, .var-group textarea:focus {
  border-color: #6366f1; box-shadow: 0 0 0 2px rgba(99,102,241,.15);
}
.var-group input::placeholder, .var-group textarea::placeholder { color: var(--tx3); }
.var-group.context-hidden { display: none; }
.var-context-status {
  display: none; margin: 0 0 .7rem; padding: .55rem .65rem;
  border: 1px solid var(--bdr); border-radius: 8px;
  background: var(--bg3); color: var(--tx2); font-size: .68rem; line-height: 1.45;
}
.var-context-status.show { display: block; }
.var-group.var-required label::after, .var-group.var-optional label::after {
  margin-left: .35rem; padding: .08rem .28rem; border-radius: 999px;
  font-size: .52rem; letter-spacing: .04em; vertical-align: middle;
}
html[data-lang="es"] .var-group.var-required label::after { content: "REQUERIDA"; }
html[data-lang="en"] .var-group.var-required label::after { content: "REQUIRED"; }
html[data-lang="es"] .var-group.var-optional label::after { content: "OPCIONAL"; }
html[data-lang="en"] .var-group.var-optional label::after { content: "OPTIONAL"; }
.var-group.var-required label::after { color: #fecaca; background: rgba(239,68,68,.14); }
.var-group.var-optional label::after { color: #bae6fd; background: rgba(14,165,233,.14); }
.var-group.var-pending input, .var-group.var-pending select, .var-group.var-pending textarea {
  border-color: #f59e0b;
}
.var-help {
  display: block; margin-top: .35rem; color: var(--tx3);
  font-size: .64rem; line-height: 1.4;
}
.var-other-input { margin-top: .4rem; }
.var-other-input[hidden] { display: none; }
.var-tags { display: flex; flex-wrap: wrap; gap: .25rem; margin-top: .3rem; }
.var-tag {
  font-size: .58rem; font-family: var(--mono); color: var(--tx3);
  background: var(--bg4); border: 1px solid var(--bdr2); border-radius: 3px;
  padding: .08rem .35rem;
}
.var-panel-footer {
  padding: .75rem 1rem; border-top: 1px solid var(--bdr); flex-shrink: 0;
  display: flex; gap: .5rem;
}
.var-apply-btn, .var-clear-btn {
  flex: 1; padding: .35rem; border: none; border-radius: 5px;
  font-size: .74rem; font-weight: 700; cursor: pointer;
  font-family: inherit; transition: background .12s;
}
.var-apply-btn { background: #6366f1; color: #fff; }
.var-apply-btn:hover { background: #4f52d4; }
.var-apply-btn.ok { background: var(--grn); }
.var-clear-btn { background: var(--bg4); color: var(--tx2); border: 1px solid var(--bdr2); }
.var-clear-btn:hover { background: var(--bg3); }

/* ═══════════════════════════ MULTI-SELECT ══════════════════════ */
.ms-toggle-btn {
  padding: .25rem .75rem; background: var(--bg3); border: 1px solid var(--bdr2);
  border-radius: 5px; color: var(--tx2); font-size: .72rem;
  cursor: pointer; font-weight: 600; transition: all .12s; font-family: inherit;
  display: flex; align-items: center; gap: .35rem;
}
.ms-toggle-btn:hover, .ms-toggle-btn.active { background: #4f46e5; border-color: #6366f1; color: #fff; }
.var-toggle-btn {
  padding: .25rem .75rem; background: var(--bg3); border: 1px solid var(--bdr2);
  border-radius: 5px; color: var(--tx2); font-size: .72rem;
  cursor: pointer; font-weight: 600; transition: all .12s; font-family: inherit;
  display: flex; align-items: center; gap: .35rem;
}
.var-toggle-btn:hover, .var-toggle-btn.active { background: #0e7490; border-color: #06b6d4; color: #fff; }

/* Checkbox en card header */
.card-check {
  display: none; flex-shrink: 0;
  width: 16px; height: 16px; cursor: pointer; accent-color: #6366f1;
}
body.ms-mode .card-check { display: block; }

/* Checkbox de sección */
.sec-check {
  display: none; width: 15px; height: 15px; cursor: pointer; accent-color: #6366f1;
  flex-shrink: 0;
}
body.ms-mode .sec-check { display: block; }

/* barra flotante de selección */
.ms-bar {
  position: fixed; bottom: -70px; left: 50%; transform: translateX(-50%);
  background: #1c2035; border: 1px solid #6366f1;
  border-radius: 10px; padding: .65rem 1.25rem;
  display: flex; align-items: center; gap: .85rem;
  box-shadow: 0 8px 32px rgba(0,0,0,.5); z-index: 600;
  transition: bottom .22s ease; white-space: nowrap;
}
.ms-bar.visible { bottom: 1.5rem; }
.ms-count { font-size: .8rem; color: var(--tx2); }
.ms-count strong { color: #a5b4fc; font-size: .85rem; }
.ms-copy-btn {
  padding: .3rem 1rem; background: #6366f1; border: none; border-radius: 6px;
  color: #fff; font-size: .74rem; font-weight: 700; cursor: pointer;
  font-family: inherit; transition: background .12s;
}
.ms-copy-btn:hover { background: #4f52d4; }
.ms-copy-btn.ok { background: var(--grn); }
.ms-clear-btn {
  background: none; border: 1px solid var(--bdr2); border-radius: 6px;
  color: var(--tx3); font-size: .72rem; padding: .3rem .7rem;
  cursor: pointer; font-family: inherit; transition: all .12s;
}
.ms-clear-btn:hover { border-color: var(--tx3); color: var(--tx2); }

/* Highlight card seleccionada */
.card.ms-selected {
  border-color: #6366f1; box-shadow: 0 0 0 1px #6366f133;
}

/* Indicador "vars activas" en barra de búsqueda */
.vars-active-badge {
  font-size: .65rem; font-weight: 700; background: #0e7490;
  border: 1px solid #06b6d4; color: #7dd3fc;
  border-radius: 4px; padding: .12rem .45rem; display: none;
}
.vars-active-badge.show { display: inline; }

/* ═══════════════════════════ BOTÓN ⓘ INFO ══════════════════════ */
.info-btn {
  flex-shrink: 0; width: 22px; height: 22px; padding: 0;
  background: none; border: 1px solid var(--bdr2);
  border-radius: 50%; color: var(--tx3); font-size: .7rem; font-weight: 700;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all .12s; line-height: 1; font-family: inherit;
}
.info-btn:hover { background: rgba(99,102,241,.15); border-color: #6366f1; color: #a5b4fc; }

/* ═══════════════════════════ MODAL INFO ════════════════════════ */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,.65);
  z-index: 700; display: none; align-items: center; justify-content: center;
  padding: 1.5rem;
}
.modal-overlay.open { display: flex; }
.modal-box {
  background: var(--bg2); border: 1px solid var(--bdr2);
  border-radius: 12px; width: 100%; max-width: 640px;
  max-height: 88vh; display: flex; flex-direction: column;
  box-shadow: 0 20px 60px rgba(0,0,0,.6);
}
.modal-hdr {
  display: flex; align-items: flex-start; gap: .65rem;
  padding: .9rem 1.1rem .75rem; border-bottom: 1px solid var(--bdr); flex-shrink: 0;
}
.modal-hdr-icon { flex-shrink: 0; opacity: .8; }
.modal-hdr h2 {
  flex: 1; font-size: .88rem; font-weight: 700; color: var(--tx); line-height: 1.4;
}
.modal-close-btn {
  flex-shrink: 0; background: none; border: none; cursor: pointer;
  color: var(--tx3); font-size: 1.1rem; padding: .1rem .2rem; border-radius: 4px;
  line-height: 1; transition: color .12s;
}
.modal-close-btn:hover { color: var(--tx); }
.modal-body {
  flex: 1; overflow-y: auto; padding: 1rem 1.1rem 1.25rem;
  display: flex; flex-direction: column; gap: .85rem;
}
.modal-body::-webkit-scrollbar { width: 4px; }
.modal-body::-webkit-scrollbar-thumb { background: var(--bdr2); border-radius: 2px; }
.modal-section h3 {
  font-size: .62rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: .1em; color: var(--tx3); margin-bottom: .4rem;
  display: flex; align-items: center; gap: .35rem;
}
.modal-section h3::before {
  content: ''; display: inline-block; width: 6px; height: 6px;
  background: #6366f1; border-radius: 50%; flex-shrink: 0;
}
.modal-desc {
  font-size: .79rem; color: var(--tx2); line-height: 1.65; white-space: pre-wrap;
}
.modal-formula-wrap { margin-top: .3rem; }
.modal-formula {
  background: #04050d; border: 1px solid var(--bdr);
  border-radius: 6px; padding: .65rem .85rem; max-height: 220px; overflow-y: auto;
}
.modal-formula::-webkit-scrollbar { width: 3px; }
.modal-formula::-webkit-scrollbar-thumb { background: var(--bdr2); border-radius: 2px; }
.modal-formula code {
  font-family: var(--mono); font-size: .7rem; color: #8892c0;
  white-space: pre-wrap; word-break: break-word; line-height: 1.6;
}
.modal-copy-formula {
  margin-top: .35rem; padding: .22rem .7rem;
  background: var(--bg4); border: 1px solid var(--bdr2);
  border-radius: 5px; color: var(--tx2); font-size: .68rem;
  cursor: pointer; font-weight: 600; transition: all .12s; font-family: inherit;
}
.modal-copy-formula:hover { background: #6366f1; border-color: #6366f1; color: #fff; }
.modal-copy-formula.ok { background: var(--grn); border-color: var(--grn); color: #fff; }
.modal-note {
  font-size: .72rem; color: var(--tx3); padding: .5rem .75rem;
  background: var(--bg3); border: 1px solid var(--bdr); border-radius: 6px;
  border-left: 3px solid #6366f1; line-height: 1.5;
}

/* ════════════════════  PROYECTOS  ══════════════════════════════ */
.proj-selector-row {
  display: flex; align-items: center; gap: 6px;
  padding: 0 14px 10px; border-bottom: 1px solid var(--bdr);
}
.proj-select {
  flex: 1; background: var(--bg); color: var(--tx); border: 1px solid var(--bdr2);
  border-radius: 6px; padding: 4px 8px; font-size: .76rem; font-family: inherit;
  cursor: pointer; outline: none;
}
.proj-select:focus { border-color: #06b6d4; }
.proj-mgr-btn {
  background: none; border: 1px solid var(--bdr2); border-radius: 6px;
  color: var(--tx3); padding: 4px 8px; font-size: .7rem; cursor: pointer;
  white-space: nowrap; font-family: inherit; transition: border-color .12s, color .12s;
}
.proj-mgr-btn:hover { border-color: #06b6d4; color: #06b6d4; }

/* Modal de proyectos */
#proj-modal {
  position: fixed; inset: 0; background: rgba(0,0,0,.65);
  z-index: 2000; display: none; align-items: center; justify-content: center;
  padding: 1.5rem;
}
.proj-modal-box {
  background: var(--bg2); border: 1px solid var(--bdr2); border-radius: 12px;
  padding: 20px; width: min(480px, 90vw); max-height: 80vh;
  overflow-y: auto; position: relative;
  box-shadow: 0 20px 60px rgba(0,0,0,.6);
}
.proj-modal-box .modal-hdr { padding: 0 0 .75rem; border-bottom: 1px solid var(--bdr); margin-bottom: .75rem; }
.proj-modal-box .modal-hdr h2 { font-size: .92rem; color: var(--tx); }
.proj-list { list-style: none; display: flex; flex-direction: column; gap: 8px; margin-bottom: 12px; }
.proj-item {
  display: flex; align-items: center; gap: 8px;
  background: var(--bg); border: 1px solid var(--bdr2); border-radius: 8px; padding: 7px 10px;
  transition: border-color .12s;
}
.proj-item.active-proj { border-color: #06b6d4; }
.proj-item-name {
  flex: 1; background: none; border: none; color: var(--tx);
  font-size: .82rem; font-family: inherit; outline: none; cursor: pointer;
}
.proj-item-name:focus { border-bottom: 1px solid #06b6d4; cursor: text; }
.proj-def-badge {
  font-size: .62rem; background: #0e7490; color: #fff;
  border-radius: 4px; padding: 1px 5px; white-space: nowrap; flex-shrink: 0;
}
.proj-action-btn {
  background: none; border: none; color: var(--tx3);
  cursor: pointer; padding: 2px 5px; font-size: .82rem;
  border-radius: 4px; transition: color .12s, background .12s;
}
.proj-action-btn:hover { color: var(--tx); background: var(--bg3); }
.proj-add-btn {
  background: #0e7490; color: #fff; border: none; border-radius: 8px;
  padding: 8px 16px; width: 100%; cursor: pointer; font-size: .82rem;
  font-family: inherit; transition: background .12s;
}
.proj-add-btn:hover { background: #0891b2; }

/* ════════════════════  PROYECTO QUICK-SWITCHER  ═══════════════════ */
.proj-quick { position: relative; flex-shrink: 0; }
.proj-quick-btn {
  display: flex; align-items: center; gap: .3rem;
  padding: .26rem .65rem; background: rgba(14,116,144,.12);
  border: 1px solid #0e7490; border-radius: 6px;
  color: #7dd3fc; font-size: .72rem; cursor: pointer;
  font-family: inherit; font-weight: 600; transition: all .12s;
  max-width: 200px; white-space: nowrap;
}
.proj-quick-btn:hover { background: rgba(14,116,144,.25); border-color: #06b6d4; }
.proj-quick-name { overflow: hidden; text-overflow: ellipsis; max-width: 130px; display: inline-block; vertical-align: middle; }
.proj-quick-chevron { flex-shrink: 0; transition: transform .15s; opacity: .7; }
.proj-quick.open .proj-quick-chevron { transform: rotate(180deg); }
.proj-quick-dropdown {
  display: none; position: absolute; top: calc(100% + 6px); left: 0; z-index: 800;
  background: var(--bg2); border: 1px solid var(--bdr2); border-radius: 10px;
  min-width: 210px; max-width: 300px; max-height: 340px; overflow-y: auto;
  box-shadow: 0 12px 40px rgba(0,0,0,.55); padding: .35rem;
}
.proj-quick.open .proj-quick-dropdown { display: block; }
.pq-item {
  display: flex; align-items: center; gap: 7px;
  padding: .38rem .55rem; border-radius: 6px; cursor: pointer; width: 100%;
  border: none; background: none; color: var(--tx2); font-size: .78rem;
  font-family: inherit; text-align: left; transition: background .1s;
}
.pq-item:hover { background: var(--bg3); color: var(--tx); }
.pq-item.pq-active { background: rgba(14,116,144,.14); color: #7dd3fc; }
.pq-item-name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pq-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; background: var(--bdr2); }
.pq-dot.on { background: #06b6d4; box-shadow: 0 0 4px #06b6d4; }
.pq-sep { height: 1px; background: var(--bdr); margin: .3rem 0; }
.pq-footer { display: flex; gap: 5px; padding-top: .3rem; }
.pq-new-btn {
  flex: 1; padding: .28rem .5rem; background: rgba(14,116,144,.1);
  border: 1px solid #0e7490; border-radius: 6px; color: #7dd3fc;
  font-size: .7rem; cursor: pointer; font-family: inherit; transition: all .12s;
}
.pq-new-btn:hover { background: #0e7490; color: #fff; }
.pq-mgr-btn {
  padding: .28rem .55rem; background: var(--bg3); border: 1px solid var(--bdr2);
  border-radius: 6px; color: var(--tx3); font-size: .7rem;
  cursor: pointer; font-family: inherit; transition: all .12s;
}
.pq-mgr-btn:hover { border-color: var(--bdr2); color: var(--tx2); background: var(--bg4); }

/* ════════════════════  SIDEBAR COLLAPSE  ════════════════════════ */
.sidebar-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: .4rem .75rem; border-bottom: 1px solid var(--bdr); flex-shrink: 0;
}
.sidebar-label-text { font-size: .6rem; font-weight: 700; color: var(--tx3); text-transform: uppercase; letter-spacing: .1em; }
.sidebar-collapse-btn {
  background: none; border: none; color: var(--tx3); cursor: pointer;
  padding: 3px 4px; border-radius: 4px; transition: color .12s, background .12s;
  display: flex; align-items: center; flex-shrink: 0;
}
.sidebar-collapse-btn:hover { color: var(--tx); background: var(--bg3); }
body.sidebar-collapsed { --side: 46px; }
body.sidebar-collapsed .sidebar { overflow: hidden; }
body.sidebar-collapsed .sid-text,
body.sidebar-collapsed .sid-badge,
body.sidebar-collapsed .sid-label,
body.sidebar-collapsed .sidebar-label-text { display: none; }
body.sidebar-collapsed .sid-link { padding: .38rem; justify-content: center; gap: 0; }
body.sidebar-collapsed .sidebar-header { justify-content: center; padding: .4rem .25rem; }

/* ════════════════════  RESPONSIVE  ════════════════════════════════ */
@media (max-width: 900px) {
  .hdr-logo p { display: none; }
  .tag-warn { font-size: .58rem; padding: .12rem .35rem; }
}
@media (max-width: 720px) {
  :root { --side: 46px; }
  .sidebar { overflow: hidden; }
  .sid-text, .sid-badge, .sid-label, .sidebar-label-text { display: none !important; }
  .sid-link { padding: .38rem; justify-content: center; gap: 0; }
  .sidebar-header { justify-content: center; padding: .4rem .25rem; }
  .hdr-tags .tag:not(.tag-warn) { display: none; }
}
@media (max-width: 560px) {
  .hdr-tags { display: none; }
  .proj-quick-name { max-width: 70px; }
  .cards-grid { grid-template-columns: 1fr; }
  .ms-label { display: none; }
  .var-label { display: none; }
}
@media (max-width: 400px) {
  .hdr-brand { display: none; }
  header { padding: 0 .75rem; }
  .proj-quick-btn { max-width: 90px; padding: .22rem .45rem; }
}

/* ═════════════════ WELCOME BANNER ══════════════════════════════ */
.welcome-banner {
  background: linear-gradient(135deg,#12103a 0%,#0f1220 100%);
  border-bottom: 1px solid #3730a3;
  padding: .6rem 1.25rem .6rem calc(var(--side) + 1.5rem);
  display: flex; align-items: center; gap: .85rem; flex-shrink: 0;
}
.welcome-banner.hidden { display: none; }
.wb-lead { font-size: .7rem; font-weight: 700; color: #a5b4fc; white-space: nowrap; flex-shrink: 0; }
.wb-pills { display: flex; align-items: center; gap: .45rem; flex: 1; flex-wrap: wrap; }
.wb-pill {
  display: flex; align-items: center; gap: .28rem;
  font-size: .66rem; color: #c7d2fe;
  background: rgba(99,102,241,.1); border: 1px solid rgba(99,102,241,.22);
  border-radius: 20px; padding: .16rem .52rem; white-space: nowrap;
}
.wb-dismiss {
  flex-shrink: 0; background: none; border: 1px solid var(--bdr2);
  border-radius: 5px; color: var(--tx3); font-size: .64rem; padding: .16rem .48rem;
  cursor: pointer; font-family: inherit; transition: all .12s;
}
.wb-dismiss:hover { border-color: #6366f1; color: #a5b4fc; }
@media (max-width: 720px) { .welcome-banner { padding: .5rem .85rem; } }
@media (max-width: 560px) { .wb-lead { display: none; } }

/* ═════════════════ ONBOARDING OVERLAY ══════════════════════════ */
.ob-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,.76);
  z-index: 900; display: flex; align-items: center; justify-content: center;
  padding: 1.5rem;
}
.ob-overlay.hidden { display: none; }
.ob-box {
  background: var(--bg2); border: 1px solid #4338ca; border-radius: 14px;
  width: 100%; max-width: 480px; box-shadow: 0 24px 64px rgba(0,0,0,.65); overflow: hidden;
}
.ob-header {
  display: flex; align-items: flex-start; justify-content: space-between;
  padding: .9rem 1.2rem .8rem; border-bottom: 1px solid var(--bdr);
  background: linear-gradient(135deg,#1e1b4b,#0f1220);
}
.ob-header h2 {
  font-size: .9rem; font-weight: 700;
  background: linear-gradient(90deg,#818cf8,#c084fc);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.ob-header p { font-size: .72rem; color: var(--tx3); margin-top: .15rem; }
.ob-close {
  background: none; border: none; color: var(--tx3); font-size: 1rem;
  cursor: pointer; line-height: 1; padding: .1rem .25rem; flex-shrink: 0;
  transition: color .12s; margin-left: .5rem;
}
.ob-close:hover { color: var(--tx); }
.ob-skip {
  background: none; border: none; color: var(--tx3); font-size: .68rem;
  cursor: pointer; font-family: inherit; transition: color .12s; padding: .15rem;
}
.ob-skip:hover { color: var(--tx2); }
.ob-progress { display: flex; gap: 6px; padding: .4rem 1.2rem; background: var(--bg3); align-items: center; justify-content: center; }
.ob-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--bdr2); transition: background .25s; }
.ob-dot.on { background: #6366f1; }
.ob-step { display: none; padding: 1.1rem 1.2rem 1.2rem; }
.ob-step.active { display: block; }
.ob-step-badge {
  display: flex; align-items: center; gap: .45rem;
  font-size: .73rem; font-weight: 700; color: #a5b4fc;
  margin-bottom: .55rem; text-transform: uppercase; letter-spacing: .04em;
}
.ob-step-badge-dot {
  display: inline-flex; align-items: center; justify-content: center;
  width: 20px; height: 20px; border-radius: 50%;
  background: rgba(99,102,241,.15); border: 1px solid #6366f1;
  color: #a5b4fc; font-size: .72rem; font-weight: 700; flex-shrink: 0;
}
.ob-step h3 { font-size: .9rem; font-weight: 700; color: var(--tx); margin-bottom: .35rem; }
.ob-step p { font-size: .79rem; color: var(--tx2); line-height: 1.65; }
.ob-highlight {
  background: rgba(99,102,241,.15); color: #a5b4fc;
  padding: .05rem .3rem; border-radius: 3px; font-weight: 600; font-size: .9em;
}
.ob-tip {
  margin-top: .65rem; padding: .4rem .7rem;
  background: var(--bg3); border: 1px solid var(--bdr2);
  border-left: 3px solid #6366f1; border-radius: 0 5px 5px 0;
  font-size: .71rem; color: var(--tx3); line-height: 1.55;
}
.ob-footer {
  display: flex; align-items: center; justify-content: space-between;
  padding: .6rem 1.2rem; border-top: 1px solid var(--bdr); background: var(--bg3);
}
.ob-nav { display: flex; align-items: center; gap: .5rem; }
.ob-next {
  padding: .32rem 1rem; background: #6366f1; border: none; border-radius: 6px;
  color: #fff; font-size: .76rem; font-weight: 700; cursor: pointer;
  font-family: inherit; transition: background .12s;
}
.ob-next:hover { background: #4f46e5; }
.ob-prev {
  padding: .32rem 1rem; background: none; border: 1px solid var(--bdr2); border-radius: 6px;
  color: var(--tx2); font-size: .76rem; cursor: pointer;
  font-family: inherit; transition: all .12s;
}
.ob-prev:hover { border-color: #6366f1; color: #a5b4fc; }
.ob-email-form { margin-top: .85rem; }
.ob-email-form label { font-size: .74rem; color: var(--tx2); display: block; margin-bottom: .35rem; }
.ob-email-input {
  width: 100%; padding: .45rem .8rem; border-radius: 7px;
  border: 1px solid var(--bdr2); background: var(--bg3); color: var(--tx);
  font-size: .82rem; font-family: inherit; outline: none; box-sizing: border-box;
  transition: border-color .15s;
}
.ob-email-input:focus { border-color: #6366f1; box-shadow: 0 0 0 2px rgba(99,102,241,.15); }
.ob-email-input::placeholder { color: var(--tx3); }
.ob-email-submit {
  margin-top: .55rem; width: 100%; padding: .42rem 1rem;
  background: linear-gradient(90deg,#6366f1,#8b5cf6); border: none;
  border-radius: 7px; color: #fff; font-size: .8rem; font-weight: 700;
  cursor: pointer; font-family: inherit; transition: opacity .12s;
}
.ob-email-submit:hover { opacity: .88; }
.ob-email-submit.ok { background: var(--grn); }
.ob-email-note { font-size: .66rem; color: var(--tx3); margin-top: .35rem; text-align: center; }

/* ═════════════════ HIGHLIGHT & TOAST & CHIPS ═══════════════════ */
.var-highlight {
  background: rgba(6, 182, 212, 0.12);
  color: #22d3ee;
  border: 1px solid rgba(6, 182, 212, 0.3);
  border-radius: 4px;
  padding: 1px 4px;
  font-weight: 600;
}
#toast-container {
  position: fixed;
  bottom: 1.5rem;
  left: 1.5rem;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  pointer-events: none;
}
.toast {
  background: #090d16;
  border: 1px solid #1e2340;
  border-left: 4px solid #10b981;
  border-radius: 6px;
  padding: 0.6rem 1rem;
  color: #e2e8f0;
  font-size: 0.76rem;
  font-weight: 600;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  animation: toast-in 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  pointer-events: auto;
}
.toast.info { border-left-color: #3b82f6; }
.toast.warn { border-left-color: #f59e0b; }
@keyframes toast-in {
  from { transform: translateY(1rem) scale(0.9); opacity: 0; }
  to { transform: translateY(0) scale(1); opacity: 1; }
}
.toast.fade-out {
  animation: toast-out 0.2s ease-in forwards;
}
@keyframes toast-out {
  from { transform: scale(1); opacity: 1; }
  to { transform: scale(0.9); opacity: 0; }
}
.chips-container {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  overflow-x: auto;
  padding: 0.2rem 0;
  max-width: 480px;
}
.chips-container::-webkit-scrollbar { display: none; }
.chip {
  background: var(--bg3);
  border: 1px solid var(--bdr2);
  color: var(--tx2);
  font-size: 0.68rem;
  font-weight: 700;
  padding: 0.22rem 0.65rem;
  border-radius: 99px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s;
}
.chip:hover {
  background: var(--bg4);
  color: #fff;
}
.chip.active {
  background: var(--active-bg, #6366f1);
  border-color: var(--active-bg, #6366f1);
  color: #fff;
  box-shadow: 0 2px 8px var(--shadow-color, rgba(99, 102, 241, 0.3));
}
/* ═════════════════ LANDING PAGE ════════════════════════════════ */
.landing {
  min-height: 100vh; background: var(--bg);
  display: flex; flex-direction: column; overflow-y: auto;
}
.landing-hidden { display: none !important; }
.app-hidden { display: none !important; }
.landing-nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1rem 2rem; border-bottom: 1px solid var(--bdr);
  background: var(--bg); position: sticky; top: 0; z-index: 100;
}
.landing-nav-logo { display: flex; align-items: center; gap: .55rem; }
.landing-nav-logo h1 { font-size: .95rem; font-weight: 700; color: var(--tx); }
.landing-nav-logo p { font-size: .65rem; color: var(--tx3); display: none; }
.landing-nav-cta {
  padding: .38rem 1.1rem; background: #6366f1; border: none;
  border-radius: 7px; color: #fff; font-size: .8rem; font-weight: 700;
  cursor: pointer; text-decoration: none; font-family: inherit;
  transition: background .12s;
}
.landing-nav-cta:hover { background: #4f46e5; }
.landing-hero {
  flex: 1; display: flex; flex-direction: column; align-items: center;
  justify-content: center; text-align: center;
  padding: 5rem 1.5rem 3rem; max-width: 760px; margin: 0 auto;
}
.landing-badge {
  display: inline-flex; align-items: center; gap: .4rem;
  font-size: .7rem; font-weight: 700; color: #f59e0b;
  background: rgba(245,158,11,.1); border: 1px solid rgba(245,158,11,.25);
  border-radius: 20px; padding: .22rem .75rem; margin-bottom: 1.5rem;
  text-transform: uppercase; letter-spacing: .08em;
}
.landing-hero h2 {
  font-size: clamp(1.8rem, 5vw, 2.8rem); font-weight: 800; line-height: 1.2;
  color: var(--tx); margin-bottom: 1.1rem;
}
.landing-hero h2 em {
  font-style: normal;
  background: linear-gradient(90deg,#818cf8,#c084fc);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.landing-hero p {
  font-size: 1rem; color: var(--tx2); line-height: 1.7;
  margin-bottom: 2rem; max-width: 600px;
}
.landing-cta-group { display: flex; gap: .75rem; flex-wrap: wrap; justify-content: center; }
.landing-cta-primary {
  padding: .75rem 2rem; background: linear-gradient(90deg,#6366f1,#8b5cf6);
  border: none; border-radius: 9px; color: #fff; font-size: .9rem; font-weight: 700;
  cursor: pointer; text-decoration: none; font-family: inherit;
  box-shadow: 0 4px 15px rgba(99,102,241,.35); transition: box-shadow .15s, transform .1s;
}
.landing-cta-primary:hover { box-shadow: 0 6px 22px rgba(99,102,241,.45); transform: translateY(-1px); }
.landing-cta-secondary {
  padding: .75rem 1.5rem; background: none; border: 1px solid var(--bdr2);
  border-radius: 9px; color: var(--tx2); font-size: .9rem;
  cursor: pointer; text-decoration: none; font-family: inherit;
  transition: border-color .15s, color .15s;
}
.landing-cta-secondary:hover { border-color: #6366f1; color: #a5b4fc; }
.landing-pain {
  background: var(--bg2); border-top: 1px solid var(--bdr);
  padding: 4rem 1.5rem;
}
.landing-pain-inner { max-width: 900px; margin: 0 auto; }
.landing-pain h3 {
  text-align: center; font-size: 1.3rem; font-weight: 700;
  color: var(--tx); margin-bottom: .5rem;
}
.landing-pain-sub { text-align: center; color: var(--tx3); font-size: .85rem; margin-bottom: 2.5rem; }
.landing-pain-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}
.pain-card {
  background: var(--bg); border: 1px solid var(--bdr);
  border-radius: 10px; padding: 1.1rem 1.2rem;
}
.pain-card-icon { font-size: 1.4rem; margin-bottom: .5rem; }
.pain-card h4 { font-size: .85rem; font-weight: 700; color: var(--tx); margin-bottom: .3rem; }
.pain-card p { font-size: .78rem; color: var(--tx3); line-height: 1.6; }
.landing-proof {
  padding: 4rem 1.5rem; max-width: 900px; margin: 0 auto;
}
.landing-proof h3 {
  text-align: center; font-size: 1.3rem; font-weight: 700;
  color: var(--tx); margin-bottom: 2rem;
}
.proof-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem; margin-bottom: 3rem;
}
.proof-stat {
  text-align: center; padding: 1.2rem;
  background: var(--bg2); border: 1px solid var(--bdr); border-radius: 10px;
}
.proof-stat-num {
  font-size: 2rem; font-weight: 800;
  background: linear-gradient(90deg,#818cf8,#c084fc);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.proof-stat-label { font-size: .74rem; color: var(--tx3); margin-top: .2rem; }
.landing-final {
  background: linear-gradient(135deg,#1e1b4b,#0f1220);
  border-top: 1px solid #4338ca; padding: 4rem 1.5rem; text-align: center;
}
.landing-final h3 { font-size: 1.4rem; font-weight: 800; color: #e0e7ff; margin-bottom: .75rem; }
.landing-final p { font-size: .9rem; color: #a5b4fc; margin-bottom: 2rem; }
.landing-footer {
  border-top: 1px solid var(--bdr); padding: 1.2rem 2rem;
  display: flex; align-items: center; justify-content: space-between;
  background: var(--bg2); font-size: .72rem; color: var(--tx3);
}

/* ══════════════  FLOATING PROJECT SELECTOR (#30)  ══════════════ */
.bottom-right-floats {
  position: fixed; bottom: 1.25rem; right: 1.25rem; z-index: 505;
  display: flex; flex-direction: column; align-items: flex-end; gap: 0.6rem;
}
.proj-float {
  display: flex; flex-direction: column; align-items: flex-end; position: relative;
}
.proj-float-btn {
  display: flex; align-items: center; gap: .45rem;
  background: var(--bg2); border: 1px solid var(--bdr);
  border-radius: 999px; padding: .35rem .75rem .35rem .55rem;
  color: var(--tx); font-size: .78rem; cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,.35);
  max-width: 200px; white-space: nowrap;
  transition: background .15s, border-color .15s;
}
.proj-float-btn:hover { background: var(--bg3); border-color: var(--acc); }
.proj-float-dot { width: 7px; height: 7px; border-radius: 50%; background: #06b6d4; flex-shrink: 0; }
.proj-float-name { overflow: hidden; text-overflow: ellipsis; flex: 1; min-width: 0; }
.proj-float-chevron { transition: transform .15s; flex-shrink: 0; }
.proj-float.open .proj-float-chevron { transform: rotate(180deg); }
.proj-float-dropdown {
  display: none; margin-bottom: .4rem;
  background: var(--bg2); border: 1px solid var(--bdr);
  border-radius: 10px; padding: .35rem 0;
  box-shadow: 0 4px 16px rgba(0,0,0,.4);
  min-width: 160px; max-width: 240px;
  max-height: 240px; overflow-y: auto;
}
.proj-float.open .proj-float-dropdown { display: block; }
@media (max-width: 560px) { .proj-float-name { display: none; } }

/* ══════════════ FLOATING VARIABLES QUICK ACCESS ══════════════ */
.var-float {
  display: flex; flex-direction: column; align-items: flex-end; position: relative;
}
.var-float-btn {
  display: flex; align-items: center; gap: .45rem;
  background: var(--bg2); border: 1px solid #0e7490;
  border-radius: 999px; padding: .38rem .75rem .38rem .55rem;
  color: var(--tx); font-size: .78rem; cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,.35);
  white-space: nowrap; transition: background .15s, border-color .15s;
}
.var-float-btn:hover, .var-float-btn.has-vars { background: #0f172a; border-color: #06b6d4; }
.var-float-icon {
  width: 22px; height: 22px; border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center;
  background: rgba(6,182,212,.12); color: #67e8f9; flex-shrink: 0;
}
.var-float-label { font-weight: 700; color: #d7f9ff; }
.var-float-count {
  font-size: .66rem; font-weight: 700; border-radius: 999px;
  background: #0f3a46; color: #7dd3fc; padding: .1rem .42rem;
  min-width: 42px; text-align: center;
}
.var-float-count.empty { background: var(--bg4); color: var(--tx3); }
.var-float-chevron { transition: transform .15s; flex-shrink: 0; }
.var-float.open .var-float-chevron { transform: rotate(180deg); }
.var-float-dropdown {
  display: none; margin-bottom: .45rem; width: 320px;
  background: var(--bg2); border: 1px solid var(--bdr);
  border-radius: 12px; padding: .85rem;
  box-shadow: 0 12px 32px rgba(0,0,0,.45);
}
.var-float.open .var-float-dropdown { display: block; }
.var-float-hdr {
  display: flex; align-items: flex-start; justify-content: space-between;
  gap: .75rem; margin-bottom: .75rem;
}
.var-float-title {
  font-size: .78rem; font-weight: 700; color: #d7f9ff; margin-bottom: .18rem;
}
.var-float-sub {
  font-size: .66rem; color: var(--tx3); line-height: 1.45;
}
.var-float-close {
  background: none; border: none; color: var(--tx3); cursor: pointer;
  font-size: 1rem; line-height: 1; border-radius: 4px; padding: .1rem;
}
.var-float-close:hover { color: var(--tx); }
.var-float-form { display: flex; flex-direction: column; gap: .65rem; }
.var-float .var-group label { font-size: .62rem; }
.var-float .var-group textarea { min-height: 48px; }
.var-float-actions {
  margin-top: .75rem; display: flex; align-items: center;
  justify-content: space-between; gap: .5rem;
}
.var-float-link, .var-float-primary {
  border-radius: 7px; padding: .38rem .8rem; font-size: .72rem;
  font-weight: 700; cursor: pointer; font-family: inherit;
}
.var-float-link {
  background: transparent; border: 1px solid var(--bdr2); color: var(--tx2);
}
.var-float-link:hover { background: var(--bg3); }
.var-float-primary {
  background: #0891b2; border: 1px solid #06b6d4; color: #fff;
}
.var-float-primary:hover { background: #0e7490; }
@media (max-width: 640px) {
  .var-float { right: .85rem; bottom: 4.85rem; }
  .var-float-dropdown { width: min(320px, calc(100vw - 1.7rem)); }
}
.ms-float {
  display: flex; flex-direction: column; align-items: flex-end; position: relative;
}
.ms-float-btn {
  display: flex; align-items: center; gap: .45rem;
  background: var(--bg2); border: 1px solid #4f46e5;
  border-radius: 999px; padding: .35rem .75rem .35rem .55rem;
  color: var(--tx); font-size: .78rem; cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,.35);
  white-space: nowrap; transition: background .15s, border-color .15s;
}
.ms-float-btn:hover, .ms-float-btn.active { background: #0f172a; border-color: #6366f1; }
.ms-float-icon {
  width: 22px; height: 22px; border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center;
  background: rgba(99,102,241,.12); color: #a5b4fc; flex-shrink: 0;
}
.ms-float-label { font-weight: 700; color: #e0e7ff; }
@media (max-width: 560px) { .ms-float-label { display: none; } }
"""

JS = """
/* ════════════════════  PROYECTOS — datos  ══════════════════════ */

var LS_KEY_PROJ = 'AI_SDLC_v1_projects';
var LS_KEY_ACTV = 'AI_SDLC_v1_active';
var EMPTY_VARS  = {
  repositorio: '', referencia: '', rama_actual: '',
  rama_destino: '', ambiente: '', componentes: '', modulo: '',
  stack: '', tipo_proyecto: '', metodologia: '', agentes: '', autonomia: '',
  entrada: '', objetivo: '', responsable: '', workspace: '',
  compliance: '', documentos: '', profundidad: '', adicionales: ''
};

function genId() {
  return 'proj_' + Math.random().toString(36).slice(2, 9);
}

function loadProjects() {
  try {
    var raw = localStorage.getItem(LS_KEY_PROJ);
    if (!raw) return null;
    var list = JSON.parse(raw);
    // Migración defensiva: garantizar que proyectos guardados tengan todos los campos nuevos
    list.forEach(function(p) { p.vars = Object.assign({}, EMPTY_VARS, p.vars || {}); });
    return list;
  } catch (e) { return null; }
}

function saveProjects(list) {
  try { localStorage.setItem(LS_KEY_PROJ, JSON.stringify(list)); } catch (e) {}
}

function getActiveProject() {
  var list = loadProjects();
  if (!list || !list.length) return null;
  var id = localStorage.getItem(LS_KEY_ACTV);
  return list.find(function(p) { return p.id === id; }) ||
         list.find(function(p) { return p.isDefault; }) ||
         list[0];
}

/* ════════════════════  PROYECTOS — CRUD  ═══════════════════════ */

function createProject(name) {
  var list = loadProjects() || [];
  var p = {
    id: genId(),
    name: name || ('Proyecto ' + (list.length + 1)),
    isDefault: list.length === 0,
    vars: Object.assign({}, EMPTY_VARS)
  };
  list.push(p);
  saveProjects(list);
  localStorage.setItem(LS_KEY_ACTV, p.id);
  return p;
}

function deleteProject(id) {
  var list = (loadProjects() || []).filter(function(p) { return p.id !== id; });
  if (!list.length) { createProject('Default'); return; }
  if (!list.find(function(p) { return p.isDefault; })) list[0].isDefault = true;
  saveProjects(list);
  var active = localStorage.getItem(LS_KEY_ACTV);
  if (active === id) localStorage.setItem(LS_KEY_ACTV, list[0].id);
}

function duplicateProject(id) {
  var list = loadProjects() || [];
  var src = list.find(function(p) { return p.id === id; });
  if (!src) return;
  var copy = {
    id: genId(), name: src.name + ' (copia)', isDefault: false,
    vars: Object.assign({}, src.vars)
  };
  list.push(copy);
  saveProjects(list);
  localStorage.setItem(LS_KEY_ACTV, copy.id);
  return copy;
}

function renameProject(id, name) {
  var list = loadProjects() || [];
  var p = list.find(function(x) { return x.id === id; });
  if (p && name.trim()) { p.name = name.trim(); saveProjects(list); renderProjectSelector(); renderProjQuick(); renderProjFloat(); }
}

function setDefaultProject(id) {
  var list = loadProjects() || [];
  list.forEach(function(p) { p.isDefault = (p.id === id); });
  saveProjects(list);
}

function switchProject(id) {
  localStorage.setItem(LS_KEY_ACTV, id);
  syncPanelToProject();
  renderProjectSelector();
  renderProjQuick();
  renderProjFloat();
}

/* ════════════════════  PROYECTOS — sync DOM  ════════════════════ */

var FIELD_VAR_MAP = {
  'vf-repositorio': 'repositorio', 'vf-referencia': 'referencia',
  'vf-rama-actual': 'rama_actual', 'vf-rama-destino': 'rama_destino',
  'vf-ambiente': 'ambiente', 'vf-componentes': 'componentes', 'vf-modulo': 'modulo',
  'vf-stack': 'stack', 'vf-tipo-proyecto': 'tipo_proyecto',
  'vf-metodologia': 'metodologia', 'vf-agentes': 'agentes',
  'vf-autonomia': 'autonomia', 'vf-entrada': 'entrada',
  'vf-objetivo': 'objetivo', 'vf-responsable': 'responsable',
  'vf-workspace': 'workspace', 'vf-compliance': 'compliance',
  'vf-documentos': 'documentos', 'vf-profundidad': 'profundidad',
  'vf-adicionales': 'adicionales'
};

var QUICK_FIELD_VAR_MAP = {
  'qv-repositorio': 'repositorio',
  'qv-referencia': 'referencia',
  'qv-rama-actual': 'rama_actual',
  'qv-rama-destino': 'rama_destino',
  'qv-modulo': 'modulo'
};

function syncFieldsToValues(fieldMap, values) {
  Object.keys(fieldMap).forEach(function(eid) {
    var el = document.getElementById(eid);
    if (!el) return;
    var value = values[fieldMap[eid]] || '';
    if (!el.multiple) {
      el.value = value;
      return;
    }
    var selectedValues = value.split(',').map(function(item) { return item.trim(); }).filter(Boolean);
    var knownValues = Array.from(el.options).map(function(option) { return option.value; });
    var customValues = selectedValues.filter(function(item) { return knownValues.indexOf(item) < 0; });
    Array.from(el.options).forEach(function(option) {
      option.selected = selectedValues.indexOf(option.value) >= 0;
    });
    var otherOption = Array.from(el.options).find(function(option) { return option.value === '__OTHER__'; });
    if (otherOption) otherOption.selected = customValues.length > 0;
    el.dataset.selectedValues = JSON.stringify(
      Array.from(el.selectedOptions).map(function(option) { return option.value; })
    );
    var otherInputId = el.getAttribute('data-other-input');
    var otherInput = otherInputId ? document.getElementById(otherInputId) : null;
    if (otherInput) {
      otherInput.value = customValues.join(', ');
      otherInput.hidden = customValues.length === 0;
    }
  });
}

function readFieldValue(el) {
  if (!el.multiple) return el.value;
  var values = Array.from(el.selectedOptions)
    .map(function(option) { return option.value; })
    .filter(function(value) { return value !== '__OTHER__'; });
  var otherInputId = el.getAttribute('data-other-input');
  var otherInput = otherInputId ? document.getElementById(otherInputId) : null;
  if (otherInput && !otherInput.hidden) {
    otherInput.value.split(',').map(function(item) { return item.trim(); }).filter(Boolean)
      .forEach(function(item) { values.push(item); });
  }
  return values.join(', ');
}

function syncMultiSelectOther(selectId) {
  var select = document.getElementById(selectId);
  if (!select) return;
  if (selectId === 'vf-compliance') {
    var previousValues = [];
    try { previousValues = JSON.parse(select.dataset.selectedValues || '[]'); } catch (e) {}
    var currentValues = Array.from(select.selectedOptions).map(function(option) { return option.value; });
    var newlySelected = currentValues.filter(function(value) {
      return previousValues.indexOf(value) < 0;
    });
    var noneOption = Array.from(select.options).find(function(option) {
      return option.value === 'NINGUNO';
    });
    if (noneOption && newlySelected.indexOf('NINGUNO') >= 0) {
      Array.from(select.options).forEach(function(option) {
        option.selected = option.value === 'NINGUNO';
      });
    } else if (noneOption && newlySelected.length > 0) {
      noneOption.selected = false;
    }
  }
  select.dataset.selectedValues = JSON.stringify(
    Array.from(select.selectedOptions).map(function(option) { return option.value; })
  );
  var otherInputId = select.getAttribute('data-other-input');
  var otherInput = otherInputId ? document.getElementById(otherInputId) : null;
  if (!otherInput) return;
  var hasOther = Array.from(select.selectedOptions).some(function(option) {
    return option.value === '__OTHER__';
  });
  otherInput.hidden = !hasOther;
  if (!hasOther) otherInput.value = '';
  syncProjectFromPanel();
  updateVarsBadge();
}

function updateActiveProjectVars(fieldMap) {
  var list = loadProjects();
  if (!list) return null;
  var actId = localStorage.getItem(LS_KEY_ACTV);
  var p = list.find(function(x) { return x.id === actId; });
  if (!p) return null;
  Object.keys(fieldMap).forEach(function(eid) {
    var el = document.getElementById(eid);
    if (el) p.vars[fieldMap[eid]] = readFieldValue(el);
  });
  saveProjects(list);
  return p.vars;
}

function syncQuickVarInputs() {
  syncFieldsToValues(QUICK_FIELD_VAR_MAP, getVarValues());
}

function syncPanelToProject() {
  var p = getActiveProject();
  var v = p ? p.vars : EMPTY_VARS;
  syncFieldsToValues(FIELD_VAR_MAP, v);
  syncQuickVarInputs();
  updateVarsBadge();
  updateContextualVariablePanel();
}

function syncProjectFromPanel() {
  if (!updateActiveProjectVars(FIELD_VAR_MAP)) return;
  syncQuickVarInputs();
  updateVarsBadge();
  updateLivePreview();
}

function syncProjectFromQuickFloat() {
  var vars = updateActiveProjectVars(QUICK_FIELD_VAR_MAP);
  if (!vars) return;
  syncFieldsToValues(FIELD_VAR_MAP, vars);
  updateVarsBadge();
  updateLivePreview();
}

function renderProjectSelector() {
  var sel = document.getElementById('proj-selector');
  var list = loadProjects() || [];
  var active = getActiveProject();
  var activeId = active ? active.id : null;
  if (sel) {
    sel.innerHTML = list.map(function(p) {
      var selAttr = (p.id === activeId) ? ' selected' : '';
      var label = p.name + (p.isDefault ? ' \u2605' : '');
      return '<option value="' + p.id + '"' + selAttr + '>'
             + label.replace(/&/g,'&amp;').replace(/</g,'&lt;') + '</option>';
    }).join('');
  }
  var nameEl = document.getElementById('vp-proj-name');
  if (nameEl && active) nameEl.textContent = active.name + (active.isDefault ? ' \u2605' : '');
  renderProjQuick();
  renderProjFloat();
}

/* ════════════════════  PROYECTOS — modal  ═══════════════════════ */

function renderProjectsModal() {
  var list = loadProjects() || [];
  var active = getActiveProject();
  var activeId = active ? active.id : null;
  var ul = document.getElementById('proj-modal-list');
  if (!ul) return;
  ul.innerHTML = list.map(function(p) {
    var isActive = p.id === activeId;
    var defBadge = p.isDefault ? '<span class="proj-def-badge">default</span>' : '';
    var delBtn = list.length > 1
      ? '<button class="proj-action-btn" title="Eliminar"'
        + ' onclick="deleteProject(\\'' + p.id + '\\');renderProjectsModal();renderProjectSelector();">'
        + '\u2715</button>'
      : '';
    return '<li class="proj-item' + (isActive ? ' active-proj' : '') + '">'
      + defBadge
      + '<input class="proj-item-name" value="'
        + p.name.replace(/&/g,'&amp;').replace(/"/g,'&quot;') + '"'
        + ' onblur="renameProject(\\'' + p.id + '\\',this.value)">'
      + '<button class="proj-action-btn" title="Activar / Activate"'
        + ' onclick="switchProject(\\'' + p.id + '\\');renderProjectsModal();">\u26a1</button>'
      + '<button class="proj-action-btn" title="Predeterminar / Make Default"'
        + ' onclick="setDefaultProject(\\'' + p.id + '\\');renderProjectsModal();renderProjectSelector();">\u2605</button>'
      + '<button class="proj-action-btn" title="Duplicar / Duplicate"'
        + ' onclick="duplicateProject(\\'' + p.id + '\\');renderProjectsModal();renderProjectSelector();syncPanelToProject();">\u2398</button>'
      + delBtn
      + '</li>';
  }).join('');
}

function openProjectsModal() {
  renderProjectsModal();
  var m = document.getElementById('proj-modal');
  if (m) m.style.display = 'flex';
}

function closeProjectsModal() {
  var m = document.getElementById('proj-modal');
  if (m) m.style.display = 'none';
}

/* ════════════════════  PROYECTO QUICK-SWITCHER  ══════════════════ */
function renderProjQuick() {
  var list = loadProjects() || [];
  var active = getActiveProject();
  var activeId = active ? active.id : null;
  var nameEl = document.getElementById('proj-quick-name');
  var fallback = getCurrentLanguage() === 'en' ? 'Project' : 'Proyecto';
  if (nameEl) nameEl.textContent = (active ? active.name : fallback) + (active && active.isDefault ? ' \u2605' : '');
  var dd = document.getElementById('proj-quick-dropdown');
  if (!dd) return;
  var items = list.map(function(p) {
    var isAct = p.id === activeId;
    return '<button class="pq-item' + (isAct ? ' pq-active' : '') + '"'
      + ' onclick="switchProject(\\'' + p.id + '\\');closeProjQuick();">'
      + '<span class="pq-dot' + (isAct ? ' on' : '') + '"></span>'
      + '<span class="pq-item-name">' + p.name.replace(/&/g,'&amp;').replace(/</g,'&lt;') + '</span>'
      + (p.isDefault ? '<span style="font-size:.6rem;color:var(--tx3)">\u2605</span>' : '')
      + '</button>';
  }).join('');
  var labelNew = getCurrentLanguage() === 'en' ? '+ New' : '+ Nuevo';
  var labelMgr = getCurrentLanguage() === 'en' ? '⚙ Manage' : '⚙ Gestionar';
  dd.innerHTML = items
    + '<div class="pq-sep"></div>'
    + '<div class="pq-footer">'
    + '<button class="pq-new-btn" onclick="createProject();renderProjQuick();renderProjectSelector();syncPanelToProject();closeProjQuick();">' + labelNew + '</button>'
    + '<button class="pq-mgr-btn" onclick="openProjectsModal();closeProjQuick();">' + labelMgr + '</button>'
    + '</div>';
}

function toggleProjQuick(e) {
  if (e) e.stopPropagation();
  var wrap = document.getElementById('proj-quick');
  if (!wrap) return;
  var isOpen = wrap.classList.toggle('open');
  if (isOpen) renderProjQuick();
}

function closeProjQuick() {
  var wrap = document.getElementById('proj-quick');
  if (wrap) wrap.classList.remove('open');
}

/* ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀  PROYECTO FLOTANTE — issue #30  ▀▀▀▀▀▀▀▀▀▀▀▀ */
function renderProjFloat() {
  var list = loadProjects() || [];
  var active = getActiveProject();
  var activeId = active ? active.id : null;
  var nameEl = document.getElementById('proj-float-name');
  var fallback = getCurrentLanguage() === 'en' ? 'Project' : 'Proyecto';
  if (nameEl) nameEl.textContent = (active ? active.name : fallback) + (active && active.isDefault ? ' \u2605' : '');
  var dd = document.getElementById('proj-float-dropdown');
  if (!dd) return;
  var items = list.map(function(p) {
    var isAct = p.id === activeId;
    return '<button class="pq-item' + (isAct ? ' pq-active' : '') + '"'
      + ' onclick="switchProject(\\'' + p.id + '\\');closeProjFloat();">' 
      + '<span class="pq-dot' + (isAct ? ' on' : '') + '"></span>'
      + '<span class="pq-item-name">' + p.name.replace(/&/g,'&amp;').replace(/</g,'&lt;') + '</span>'
      + (p.isDefault ? '<span style="font-size:.6rem;color:var(--tx3)">\u2605</span>' : '')
      + '</button>';
  }).join('');
  var labelNew = getCurrentLanguage() === 'en' ? '+ New' : '+ Nuevo';
  var labelMgr = getCurrentLanguage() === 'en' ? '⚙ Manage' : '⚙ Gestionar';
  dd.innerHTML = items
    + '<div class="pq-sep"></div>'
    + '<div class="pq-footer">'
    + '<button class="pq-new-btn" onclick="createProject();renderProjQuick();renderProjFloat();renderProjectSelector();syncPanelToProject();closeProjFloat();">' + labelNew + '</button>'
    + '<button class="pq-mgr-btn" onclick="openProjectsModal();closeProjFloat();">' + labelMgr + '</button>'
    + '</div>';
}

function toggleProjFloat(e) {
  if (e) e.stopPropagation();
  var wrap = document.getElementById('proj-float');
  if (!wrap) return;
  var isOpen = wrap.classList.toggle('open');
  if (isOpen) renderProjFloat();
}

function closeProjFloat() {
  var wrap = document.getElementById('proj-float');
  if (wrap) wrap.classList.remove('open');
}

/* ════════════════════  SIDEBAR  ════════════════════════════════ */
function toggleSidebar() {
  document.body.classList.toggle('sidebar-collapsed');
  try { localStorage.setItem('AI_SDLC_sidebar', document.body.classList.contains('sidebar-collapsed') ? '1' : '0'); } catch(e) {}
}

/* ═══════════════════  VARIABLES  ═══════════════════════════════ */

// Registro único de variables: campo persistente, aliases y obligatoriedad.
var TOKEN_REGISTRY = {
  repositorio: { required: true, aliases: ['NOMBRE O URL', 'ORG/REPO', 'NOMBRE O URL DEL REPOSITORIO', 'NAME OR URL', 'REPO', 'ORG/USER', 'NOMBRE DEL PROYECTO', 'PROJECT NAME'] },
  referencia:  { required: true, aliases: ['REFERENCIA', 'REFERENCE', 'PEGAR TEXTO O REFERENCIA', 'PEGAR TEXTO COMPLETO',
                 'PEGAR LISTA DE INCIDENTES', 'PEGAR REPORTE', 'PEGAR', 'REFERENCE TO ISSUE OR PR',
                 'REFERENCIA AL ISSUE O PR', 'PASTE', 'PEGAR TEXTO...', 'PASTE TEXT OR REFERENCE', 'NUMBER OR REFERENCE', 'PROBLEM DESCRIPTION', 'INCIDENT DESCRIPTION'] },
  rama_actual: { required: false, aliases: ['RAMA ACTUAL', 'CURRENT BRANCH', 'RAMA CON LOS CAMBIOS', 'RAMA EN PRUEBAS',
                 'RAMA AFECTADA', 'RAMA DE TRABAJO', 'RAMA DE PRUEBAS', 'BRANCH WITH CHANGES',
                 'BRANCH IN TESTING', 'WORKING BRANCH', 'BRANCH', 'BRANCH TO ANALYZE', 'RAMA A ANALIZAR', 'AFFECTED BRANCH',
                 'RAMA', 'TEST BRANCH', 'BRANCH IN TEST'] },
  rama_destino:{ required: false, aliases: ['RAMA OBJETIVO', 'TARGET BRANCH', 'RAMA PRINCIPAL', 'RAMA INTEGRADA',
                 'RAMA DESTINO', 'RAMA DE RELEASE', 'DEVELOP / MAIN / RELEASE', 'RELEASE BRANCH',
                 'INTEGRATED BRANCH', 'MAIN BRANCH', 'MAIN/DEVELOP', 'PR OR INTEGRATION BRANCH'] },
  ambiente:    { required: false, aliases: ['DEV / QA / PROD', 'ENVIRONMENT', 'QA / STAGING', 'QA / STAGING / PROD',
                 'DEV / QA / STAGING / PROD', 'PROD / STAGING', 'DEV / QA',
                 'URL DEL AMBIENTE', 'ENVIRONMENT URL', 'URL DE QA O STAGING', 'DEV / QA / STAGING',
                 'QA OR STAGING URL', 'DEV / STAGING / PROD', 'AMBIENTE', 'LOCAL / DEV / QA / PROD'] },
  componentes: { required: false, aliases: ['COMPONENTES INVOLUCRADOS', 'INVOLVED COMPONENTS', 'COMPONENTES MODIFICADOS',
                 'COMPONENTES A MODIFICAR', 'COMPONENTES REVISADOS',
                 'RUTAS DE ARCHIVOS MODIFICADOS', 'FUNCIONES O UNIDADES A PROBAR',
                 'SI YA CONOCES ALGUNO', 'REVIEWED COMPONENTS', 'COMPONENTS TO MODIFY',
                 'MODIFIED COMPONENTS', 'FILES AND MODULES TO MODIFY', 'AFFECTED MODULE OR FILE', 'DIRECTORY/PACKAGE', 'DIRECTORIO/PAQUETE'] },
  modulo:      { required: false, aliases: ['NOMBRE DEL PROCESO', 'PROCESS NAME', 'MODULE OR FUNCTIONALITY',
                 'MÓDULO O FUNCIONALIDAD', 'MODULO O FUNCIONALIDAD', 'MODULO', 'MODULE'] },
  stack:       { required: false, aliases: ['STACK', 'STACK TECNOLÓGICO', 'STACK PRINCIPAL', 'TECH STACK',
                 'ej. Python + FastAPI + PostgreSQL / Node + React + MongoDB / etc.',
                 'ej: Python 3.11 + FastAPI + PostgreSQL + Docker'] },
  tipo_proyecto: { required: false, aliases: ['TIPO DE PROYECTO', 'PROJECT TYPE',
                   'frontend SPA / API REST / full-stack / microservicio / monorepo / librería / data science / IaC / otro',
                   'NEW / INCREMENTAL CHANGE / MAINTENANCE', 'NUEVO / CAMBIO INCREMENTAL / MANTENIMIENTO',
                   'COMMERCIAL / OPEN SOURCE / INTERNAL', 'COMERCIAL / OPEN SOURCE / INTERNO'] },
  metodologia: { required: false, aliases: ['METODOLOGÍA', 'METHODOLOGY', 'METODOLOGÍA DE TRABAJO', 'METODOLOGÍA O "ninguna"',
                 'SCRUM / Kanban / Trunk-Based / GitFlow / GitHub Flow / RUP / otro',
                 'BRANCHING STRATEGY'] },
  agentes:     { required: false, aliases: ['LISTA DE AGENTES', 'AI AGENTS', 'AGENTES A CONFIGURAR', 'AGENTES ACTIVOS',
                 'Copilot / Claude / Codex / Windsurf / Cursor / Antigravity',
                 'GitHub Copilot / Claude / Windsurf / Cursor / Codex / Antigravity / combinación', 'LIST OF AGENTS',
                 'AGENT LIST', 'AGENTS TO CONFIGURE'] },
  autonomia:   { required: false, aliases: ['NIVEL DE AUTONOMÍA', 'AUTONOMY LEVEL',
                  'solo análisis / análisis + propuesta / ejecución controlada / ejecución autónoma',
                  'BAJO / MEDIO / ALTO', 'LOW / MEDIUM / HIGH', 'A0 / A1 / A2 / A3'] },
  entrada:     { required: true, aliases: ['ENTRADA PRINCIPAL', 'PRIMARY INPUT', 'PEGAR REQUERIMIENTO', 'PASTE REQUIREMENT',
                 'FUENTE DE ISSUES', 'ISSUE SOURCE', 'REQUERIMIENTO_USUARIO', 'USER REQUIREMENT'] },
  objetivo:    { required: false, aliases: ['OBJETIVO ESPECÍFICO', 'SPECIFIC OBJECTIVE', 'OBJETIVO PUNTUAL DE SALIDA',
                 'SPECIFIC OUTPUT OBJECTIVE'] },
  responsable: { required: false, aliases: ['RESPONSABLE', 'RESPONSIBLE PERSON', 'USUARIO RESPONSABLE', 'RESPONSIBLE USER',
                 'ASSIGNEE'] },
  workspace:   { required: false, aliases: ['WORKSPACE/SUBPROYECTO', 'WORKSPACE/SUBPROJECT', 'RUTA O NO APLICA',
                 'PATH OR NOT APPLICABLE', 'SI ES ENTORNO MONOREPO', 'IF MONOREPO WORKSPACE',
                 'SI MONOREPO WORKSPACE'] },
  compliance:  { required: false, aliases: ['ESTÁNDAR/COMPLIANCE', 'ESTANDAR/COMPLIANCE', 'STANDARD/COMPLIANCE',
                 'PSP / TSP / ISO 29110 / MOPROSOFT / MAAGTICSI / NINGUNO',
                 'PSP / TSP / ISO 29110 / MOPROSOFT / MAAGTICSI / NONE'] },
  documentos:  { required: false, aliases: ['DOCUMENTOS A REVISAR', 'DOCUMENTS TO REVIEW', 'RUTAS DE ARCHIVOS...',
                 'FILE PATHS...', 'RUTAS O DESCONOCIDO', 'PATHS OR UNKNOWN'] },
  profundidad: { required: false, aliases: ['NIVEL DE PROFUNDIDAD', 'DEPTH LEVEL', 'MEDIO / ALTO / FORENSE',
                 'MEDIUM / HIGH / FORENSIC'] },
};

var PLACEHOLDER_IGNORE = ['N', 'X', 'Y', 'Z', 'ADR-NNN', 'NNN', 'YYYYMMDD'];
var VAR_MAP = {};
Object.keys(TOKEN_REGISTRY).forEach(function(field) {
  VAR_MAP[field] = TOKEN_REGISTRY[field].aliases.slice();
});

function replaceToken(text, token, value) {
  var escaped = token.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
  text = text.replace(new RegExp('\\\\[' + escaped + '\\\\]', 'g'), function() { return value; });
  return text.replace(new RegExp('\\\\{\\\\{' + escaped + '\\\\}\\\\}', 'g'), function() { return value; });
}

function parseAdditionalVars(raw) {
  var result = {};
  (raw || '').split(/\\r?\\n/).forEach(function(line) {
    var idx = line.indexOf('=');
    if (idx < 1) return;
    var token = line.slice(0, idx).trim().replace(/^\\[|\\]$/g, '').replace(/^\\{\\{|\\}\\}$/g, '');
    var value = line.slice(idx + 1).trim();
    if (token && value) result[token] = value;
  });
  return result;
}

function getVarValues() {
  var p = getActiveProject();
  return p ? Object.assign({}, p.vars) : Object.assign({}, EMPTY_VARS);
}

function hasActiveVars() {
  var v = getVarValues();
  return Object.values(v).some(function(x){ return x.trim() !== ''; });
}

function resolvePrompt(template, options) {
  options = options || {};
  var text = template || '';
  var v = Object.assign({}, getVarValues(), options.values || {});
  var replaced = [];
  Object.keys(VAR_MAP).forEach(function(field) {
    var val = (v[field] || '').trim();
    if (!val) return;
    VAR_MAP[field].forEach(function(token) {
      var before = text;
      text = replaceToken(text, token, val);
      if (text !== before && replaced.indexOf(token) === -1) replaced.push(token);
    });
  });
  var additional = parseAdditionalVars(v.adicionales);
  Object.keys(additional).forEach(function(token) {
    var before = text;
    text = replaceToken(text, token, additional[token]);
    if (text !== before && replaced.indexOf(token) === -1) replaced.push(token);
  });
  var unresolved = findUnresolvedPlaceholders(text);
  return {
    text: text,
    replacedTokens: replaced,
    unresolvedRequired: unresolved.filter(function(token) {
      return getTokenField(token) && TOKEN_REGISTRY[getTokenField(token)].required;
    }),
    unresolvedOptional: unresolved.filter(function(token) {
      return !getTokenField(token) || !TOKEN_REGISTRY[getTokenField(token)].required;
    })
  };
}

function getTokenField(token) {
  var found = null;
  Object.keys(TOKEN_REGISTRY).some(function(field) {
    if (TOKEN_REGISTRY[field].aliases.indexOf(token) >= 0) {
      found = field;
      return true;
    }
    return false;
  });
  return found;
}

function applyVars(text, overrides) {
  return resolvePrompt(text, { values: overrides || {} }).text;
}

function findUnresolvedPlaceholders(text) {
  var found = [];
  var rx = /\\[([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ0-9_ /.,#()\\-]{1,80})\\]|\\{\\{([A-Z][A-Z0-9_]{1,60})\\}\\}/g;
  var match;
  while ((match = rx.exec(text)) !== null) {
    var token = (match[1] || match[2] || '').trim();
    if (PLACEHOLDER_IGNORE.indexOf(token) === -1 && found.indexOf(token) === -1) found.push(token);
  }
  // Alias registrados que empiezan en minúscula (p.ej. "[ej. Python + ...]",
  // "[frontend SPA / API REST / ...]") no los captura el regex, que exige
  // mayúscula inicial. Buscarlos explícitamente para no dejar placeholders sin aviso.
  Object.keys(TOKEN_REGISTRY).forEach(function(field) {
    TOKEN_REGISTRY[field].aliases.forEach(function(alias) {
      if (/^[A-ZÁÉÍÓÚÑ]/.test(alias)) return; // ya cubiertos por el regex
      if (found.indexOf(alias) !== -1) return;
      if (text.indexOf('[' + alias + ']') !== -1 || text.indexOf('{{' + alias + '}}') !== -1) {
        found.push(alias);
      }
    });
  });
  return found;
}

function countFilledVars() {
  var v = getVarValues();
  return Object.values(v).filter(function(x){ return x.trim() !== ''; }).length;
}

function updateVarsBadge() {
  var badge = document.getElementById('vars-badge');
  var filled = countFilledVars();
  var total = Object.keys(EMPTY_VARS).length;
  if (badge) {
    badge.classList.toggle('show', filled > 0);
    var label = getCurrentLanguage() === 'en' ? 'Vars active' : 'Vars activas';
    badge.innerHTML = '■ ' + label + ' (' + filled + '/' + total + ')';
  }
  updateVarFloatSummary();
}

function updateVarFloatSummary() {
  var filled = countFilledVars();
  var total = Object.keys(EMPTY_VARS).length;
  var countEl = document.getElementById('var-float-count');
  if (countEl) {
    countEl.textContent = filled + '/' + total;
    countEl.classList.toggle('empty', filled === 0);
  }
  var btn = document.getElementById('var-float-btn');
  if (btn) btn.classList.toggle('has-vars', filled > 0);
}

function openVarPanel() {
  closeVarFloat();
  var p = document.getElementById('var-panel');
  if (p) p.classList.add('open');
  var btn = document.getElementById('var-toggle-btn');
  if (btn) btn.classList.add('active');
  updateContextualVariablePanel();
}

function closeVarPanel() {
  var p = document.getElementById('var-panel');
  if (p) p.classList.remove('open');
  var btn = document.getElementById('var-toggle-btn');
  if (btn) btn.classList.remove('active');
}

function toggleVarPanel() {
  var p = document.getElementById('var-panel');
  if (p && p.classList.contains('open')) closeVarPanel();
  else openVarPanel();
}

function openVarFloat() {
  closeVarPanel();
  syncQuickVarInputs();
  updateVarFloatSummary();
  var wrap = document.getElementById('var-float');
  if (wrap) wrap.classList.add('open');
}

function closeVarFloat() {
  var wrap = document.getElementById('var-float');
  if (wrap) wrap.classList.remove('open');
}

function toggleVarFloat(e) {
  if (e) e.stopPropagation();
  var wrap = document.getElementById('var-float');
  if (!wrap) return;
  if (wrap.classList.contains('open')) closeVarFloat();
  else openVarFloat();
}

function openFullVarPanelFromFloat() {
  closeVarFloat();
  openVarPanel();
}

function clearVars() {
  var list = loadProjects();
  if (list) {
    var actId = localStorage.getItem(LS_KEY_ACTV);
    var p = list.find(function(x) { return x.id === actId; });
    if (p) { p.vars = Object.assign({}, EMPTY_VARS); saveProjects(list); }
  }
  syncPanelToProject();
}

/* ═══════════════════  TOGGLE CARD / COPY  ══════════════════════ */

function toggleMenu() {
  document.body.classList.toggle('menu-open');
}

function closeMenu() {
  document.body.classList.remove('menu-open');
}

/* ═══════════════════  TOGGLE CARD / COPY  ══════════════════════ */

function toggleFramework() {
  var lang = getCurrentLanguage();
  // Sincronizamos el estado de ambos (es/en) para consistencia al cambiar de idioma
  ['es', 'en'].forEach(function(l) {
    var b = document.getElementById('fb-00-' + l);
    var t = document.getElementById('fe-00-' + l);
    if (!b) return;
    var isOpen = b.classList.toggle('open');
    if (t) t.classList.toggle('open', isOpen);
    if (l === lang) { // Solo guardamos una vez
       try { localStorage.setItem('AI_SDLC_fw_expanded', isOpen ? '1' : '0'); } catch(e) {}
    }
  });
}

function initFrameworkState() {
  var saved = '';
  try { saved = localStorage.getItem('AI_SDLC_fw_expanded') || ''; } catch(e) {}
  var isOpen = saved === '1';
  if (isOpen) {
    ['es', 'en'].forEach(function(l) {
      var b = document.getElementById('fb-00-' + l);
      var t = document.getElementById('fe-00-' + l);
      if (b) b.classList.add('open');
      if (t) t.classList.add('open');
    });
  }
}

/* ════════════════════  INTERNACIONALIZACIÓN (i18n)  ══════════════════════ */

var I18N_KEY = 'AI_SDLC_language';
var I18N_DEFAULT = 'es';
var I18N_SUPPORTED = ['es', 'en'];

function detectBrowserLanguage() {
  var navLang = navigator.language || navigator.userLanguage || '';
  var primary = navLang.split('-')[0].toLowerCase();
  if (I18N_SUPPORTED.indexOf(primary) !== -1) return primary;
  return I18N_DEFAULT;
}

function getCurrentLanguage() {
  try {
    var saved = localStorage.getItem(I18N_KEY);
    if (saved && I18N_SUPPORTED.indexOf(saved) !== -1) return saved;
  } catch(e) {}
  return detectBrowserLanguage();
}

function updateFrameworkVisibility(lang) {
  var fwEs = document.getElementById('sec-00-es');
  var fwEn = document.getElementById('sec-00-en');
  if (fwEs) fwEs.style.display = (lang === 'es') ? 'block' : 'none';
  if (fwEn) fwEn.style.display = (lang === 'en') ? 'block' : 'none';
}

function updatePlaceholders(lang) {
  var pSelect = document.getElementById('vf-ambiente');
  if (pSelect && pSelect.options.length > 0) {
    pSelect.options[0].text = lang === 'en' ? '-- select --' : '-- seleccionar --';
  }
  var tSelect = document.getElementById('vf-tipo-proyecto');
  if (tSelect && tSelect.options.length > 9) {
    tSelect.options[0].text = lang === 'en' ? '-- select --' : '-- seleccionar --';
    tSelect.options[4].text = lang === 'en' ? 'microservice' : 'microservicio';
    tSelect.options[4].value = lang === 'en' ? 'microservice' : 'microservicio';
    tSelect.options[6].text = lang === 'en' ? 'library' : 'librería';
    tSelect.options[6].value = lang === 'en' ? 'library' : 'librería';
    tSelect.options[9].text = lang === 'en' ? 'other' : 'otro';
    tSelect.options[9].value = lang === 'en' ? 'other' : 'otro';
  }
  var aSelect = document.getElementById('vf-autonomia');
  if (aSelect && aSelect.options.length > 4) {
    aSelect.options[0].text = lang === 'en' ? '-- select --' : '-- seleccionar --';
    aSelect.options[1].text = lang === 'en' ? 'analysis only' : 'solo análisis';
    aSelect.options[1].value = lang === 'en' ? 'analysis only' : 'solo análisis';
    aSelect.options[2].text = lang === 'en' ? 'analysis + proposal' : 'análisis + propuesta';
    aSelect.options[2].value = lang === 'en' ? 'analysis + proposal' : 'análisis + propuesta';
    aSelect.options[3].text = lang === 'en' ? 'controlled execution' : 'ejecución controlada';
    aSelect.options[3].value = lang === 'en' ? 'controlled execution' : 'ejecución controlada';
    aSelect.options[4].text = lang === 'en' ? 'autonomous execution' : 'ejecución autónoma';
    aSelect.options[4].value = lang === 'en' ? 'autonomous execution' : 'ejecución autónoma';
  }
  
  var inputs = {
    'vf-repositorio': { es: 'org/nombre-repo o URL', en: 'org/repo-name or URL' },
    'vf-referencia': { es: 'Número, URL o texto completo del issue', en: 'Number, URL or full text of the issue' },
    'vf-rama-actual': { es: 'feature/mi-rama', en: 'feature/my-branch' },
    'vf-rama-destino': { es: 'main / develop', en: 'main / develop' },
    'vf-componentes': { es: 'Lista de componentes o rutas de archivos', en: 'List of components or file paths' },
    'vf-modulo': { es: 'Nombre del módulo o funcionalidad', en: 'Module or process name' },
    'vf-stack': { es: 'ej: Python + FastAPI + PostgreSQL + Docker', en: 'e.g., Python + FastAPI + PostgreSQL + Docker' },
    'vf-compliance-other': { es: 'Otro estándar o regulación', en: 'Other standard or regulation' },
    'vf-metodologia-other': { es: 'Otra metodología o proceso', en: 'Other methodology or process' },
    'vf-agentes': { es: 'ej: Copilot, Claude, Codex', en: 'e.g., Copilot, Claude, Codex' },
    
    'qv-repositorio': { es: 'org/nombre-repo o URL', en: 'org/repo-name or URL' },
    'qv-referencia': { es: 'Número, URL o resumen corto', en: 'Number, URL or short summary' },
    'qv-rama-actual': { es: 'feature/mi-rama', en: 'feature/my-branch' },
    'qv-rama-destino': { es: 'main / develop', en: 'main / develop' },
    'qv-modulo': { es: 'Nombre del módulo o funcionalidad', en: 'Module or process name' }
  };
  
  Object.keys(inputs).forEach(function(id) {
    var el = document.getElementById(id);
    if (el) el.placeholder = inputs[id][lang] || '';
  });
}

function setLanguage(lang) {
  if (I18N_SUPPORTED.indexOf(lang) === -1) lang = I18N_DEFAULT;
  try { localStorage.setItem(I18N_KEY, lang); } catch(e) {}
  document.documentElement.lang = lang;
  document.documentElement.setAttribute('data-lang', lang);
  
  // Actualizar UI del selector
  var langLabel = document.getElementById('current-lang-label');
  if (langLabel) langLabel.textContent = lang.toUpperCase();
  
  // Actualizar visibilidad del framework banner
  updateFrameworkVisibility(lang);

  // Enviar evento de analytics
  if (typeof gtag === 'function') {
    gtag('event', 'language_change', { 'language': lang });
  }

  // Traducir input placeholder de búsqueda
  var searchInput = document.querySelector('.search-wrap input');
  if (searchInput) {
    searchInput.placeholder = (lang === 'en')
      ? 'Search by prompt name or content...'
      : 'Buscar por nombre o contenido del prompt...';
  }

  // Traducir empty state
  var emptyEl = document.getElementById('glbl-empty');
  if (emptyEl) {
    emptyEl.innerHTML = (lang === 'en')
      ? '<p>No results.</p><small>Try another search term.</small>'
      : '<p>Sin resultados.</p><small>Intenta con otro término de búsqueda.</small>';
  }

  // Actualizar variables badge
  updateVarsBadge();

  // Actualizar placeholders del panel de variables
  updatePlaceholders(lang);
  ACTIVE_PROMPT_LANG = lang;
  updateContextualVariablePanel();

  // Sincronizar selectores de proyecto
  renderProjQuick();
  renderProjFloat();
  renderProjectSelector();

  if (typeof initChips === 'function') initChips();
}

function initLanguageDetection() {
  var lang = getCurrentLanguage();
  setLanguage(lang);
}

function toggleLanguageDropdown() {
  var dd = document.getElementById('lang-dropdown');
  if (dd) dd.classList.toggle('open');
}

function onLanguageSelect(lang) {
  setLanguage(lang);
  closeLanguageDropdown();
}

function closeLanguageDropdown() {
  var dd = document.getElementById('lang-dropdown');
  if (dd) dd.classList.remove('open');
}

function getFwText() {
  var lang = getCurrentLanguage();
  var fwId = 'code-fw-' + lang;
  var fwEl = document.getElementById(fwId) || document.getElementById('code-fw');
  return fwEl ? fwEl.textContent : '';
}

var RAW_PROMPTS = {};
var ACTIVE_PROMPT_ID = '';
var ACTIVE_PROMPT_LANG = '';

function getPromptContextFields(template) {
  var fields = [];
  Object.keys(TOKEN_REGISTRY).forEach(function(field) {
    if (TOKEN_REGISTRY[field].aliases.some(function(token) {
      return template.indexOf('[' + token + ']') >= 0 || template.indexOf('{{' + token + '}}') >= 0;
    })) fields.push(field);
  });
  return fields;
}

function updateContextualVariablePanel() {
  var status = document.getElementById('var-context-status');
  var groups = Array.from(document.querySelectorAll('.var-panel-body .var-group[data-field]'));
  if (!ACTIVE_PROMPT_ID) {
    groups.forEach(function(group) {
      group.classList.remove('context-hidden', 'var-required', 'var-optional', 'var-pending');
    });
    if (status) status.classList.remove('show');
    return;
  }
  var lang = ACTIVE_PROMPT_LANG || getCurrentLanguage();
  var codeId = 'code-' + ACTIVE_PROMPT_ID + '-' + lang;
  var template = RAW_PROMPTS[codeId] || '';
  var fields = getPromptContextFields(template);
  var values = getVarValues();
  var unknown = findUnresolvedPlaceholders(template).filter(function(token) {
    return !getTokenField(token);
  });
  groups.forEach(function(group) {
    var field = group.dataset.field;
    var applies = fields.indexOf(field) >= 0 || (field === 'adicionales' && unknown.length > 0);
    group.classList.toggle('context-hidden', !applies);
    group.classList.remove('var-required', 'var-optional', 'var-pending');
    if (!applies) return;
    var required = field !== 'adicionales' && TOKEN_REGISTRY[field] && TOKEN_REGISTRY[field].required;
    group.classList.add(required ? 'var-required' : 'var-optional');
    group.classList.toggle('var-pending', required && !(values[field] || '').trim());
  });
  if (status) {
    var pending = fields.filter(function(field) {
      return TOKEN_REGISTRY[field].required && !(values[field] || '').trim();
    });
    status.textContent = getCurrentLanguage() === 'en'
      ? fields.length + ' applicable fields · ' + pending.length + ' required pending'
      : fields.length + ' campos aplicables · ' + pending.length + ' requeridos pendientes';
    if (unknown.length) status.textContent += ' · ' + unknown.length + (getCurrentLanguage() === 'en' ? ' additional tokens' : ' tokens adicionales');
    status.classList.add('show');
  }
}

function updateLivePreview() {
  Object.keys(RAW_PROMPTS).forEach(function(codeId) {
    var codeEl = document.getElementById(codeId);
    if (!codeEl) return;
    var resolved = resolvePrompt(RAW_PROMPTS[codeId]);
    codeEl.textContent = resolved.text;
  });
  updateContextualVariablePanel();
}

function showUnresolvedWarning(result) {
  var unresolved = result.unresolvedRequired.concat(result.unresolvedOptional);
  if (!unresolved.length) return;
  var warning = getCurrentLanguage() === 'en'
    ? unresolved.length + ' placeholders still need manual input: '
    : unresolved.length + ' placeholders requieren captura manual: ';
  showToast(warning + unresolved.slice(0, 3).join(', ') + (unresolved.length > 3 ? '...' : ''), 'warn');
}

function showToast(msg, type) {
  var container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  var toast = document.createElement('div');
  toast.className = 'toast' + (type ? ' ' + type : '');
  
  var icon = '&#10004;';
  if (type === 'info') icon = '&#8505;';
  if (type === 'warn') icon = '&#9888;';
  
  toast.innerHTML = '<span>' + icon + '</span> ' + msg;
  container.appendChild(toast);
  
  setTimeout(function() {
    toast.classList.add('fade-out');
    setTimeout(function() { if (toast.parentNode) container.removeChild(toast); }, 200);
  }, 3000);
}

function initChips() {
  var container = document.getElementById('category-chips');
  if (!container) return;
  var lang = getCurrentLanguage();
  var sidebarLinks = Array.from(document.querySelectorAll('.sidebar .sid-link'));
  
  var html = sidebarLinks.map(function(link) {
    var href = link.getAttribute('href');
    if (!href || href === '#sec-00') return ''; // Ignorar el framework en los chips ya que es el banner principal
    var secCode = href.replace('#sec-', '');
    var textEl = link.querySelector(lang === 'es' ? '.sid-lang-es' : '.sid-lang-en');
    var label = textEl ? textEl.textContent : (link.querySelector('.sid-text') ? link.querySelector('.sid-text').textContent : '');
    label = label.replace(/^[0-9]+ — /, ''); // Remover número
    
    var svg = link.querySelector('svg');
    var color = svg ? svg.getAttribute('stroke') : '#6366f1';
    
    return '<button class="chip" data-sec="' + secCode + '" style="--active-bg: ' + color + '; --shadow-color: ' + color + '55" onclick="filterByChip(\\\'' + secCode + '\\\')">' + label + '</button>';
  }).join('');
  
  container.innerHTML = html;
}

function filterByChip(secCode) {
  document.querySelectorAll('.chip').forEach(function(c) {
    var active = c.getAttribute('data-sec') === secCode;
    c.classList.toggle('active', active);
  });
  
  var target = document.getElementById('sec-' + secCode);
  if (target) {
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    var header = target.querySelector('.section-header-row');
    if (header) {
       header.style.transition = 'background 0.5s';
       header.style.background = 'rgba(99,102,241,0.12)';
       setTimeout(function() { header.style.background = 'none'; }, 1000);
    }
  }
}

function copyPromptLang(pid, lang, btn) {
  var codeId = 'code-' + pid + '-' + lang;
  var codeEl = document.getElementById(codeId);
  if (!codeEl) return;
  
  // Leer plantilla limpia de RAW_PROMPTS para evitar copiar etiquetas de highlight HTML
  var raw = RAW_PROMPTS[codeId] || codeEl.textContent;
  var resolved = resolvePrompt(raw);
  var text = resolved.text;
  
  if (pid !== 'fw') {
    var fwId = 'code-fw-' + lang;
    var fwEl = document.getElementById(fwId) || document.getElementById('code-fw');
    if (fwEl) {
      var fwRaw = RAW_PROMPTS[fwId] || fwEl.textContent;
      var fwResolved = resolvePrompt(fwRaw);
      if (fwResolved.text) text = fwResolved.text + '\\n\\n---\\n\\n' + text;
      resolved.unresolvedRequired = fwResolved.unresolvedRequired.concat(resolved.unresolvedRequired);
      resolved.unresolvedOptional = fwResolved.unresolvedOptional.concat(resolved.unresolvedOptional);
    }
  }
  showUnresolvedWarning(resolved);
  doCopy(text, btn);
}

function openInfoLang(pid, lang) {
  var info = (typeof PROMPT_INFO !== 'undefined') ? PROMPT_INFO[pid] : null;
  if (!info) return;
  var modal = document.getElementById('info-modal');
  if (!modal) return;

  var titleEl = document.getElementById('modal-title');
  if (titleEl) {
    titleEl.textContent = (lang === 'en' ? info.title_en : info.title_es) || pid;
  }

  var descSec = document.getElementById('modal-desc-section');
  var descEl  = document.getElementById('modal-desc');
  var desc = lang === 'en' ? info.desc_en : info.desc_es;
  if (descEl && descSec) {
    descSec.style.display = desc ? '' : 'none';
    descEl.textContent = desc || '';
  }

  var formulas = lang === 'en' ? info.formulas_en : info.formulas_es;
  var formulasEl = document.getElementById('modal-formulas');
  if (formulasEl) {
    formulasEl.innerHTML = '';
    if (formulas && formulas.length) {
      formulas.forEach(function(f, i) {
        var sec = document.createElement('div');
        sec.className = 'modal-section';
        var h = document.createElement('h3');
        h.textContent = lang === 'en'
          ? (formulas.length > 1 ? 'Usage formula ' + (i + 1) : 'Standard usage formula')
          : (formulas.length > 1 ? 'Fórmula de uso ' + (i + 1) : 'Fórmula de uso estándar');
        var wrap = document.createElement('div');
        wrap.className = 'modal-formula-wrap';
        var box = document.createElement('div');
        box.className = 'modal-formula';
        var code = document.createElement('code');
        code.textContent = f;
        box.appendChild(code);
        var btn = document.createElement('button');
        btn.className = 'modal-copy-formula';
        btn.innerHTML = lang === 'en' ? '&#10697; Copy formula' : '&#10697; Copiar fórmula';
        (function(formula, b) {
          b.addEventListener('click', function() {
            var result = resolvePrompt(formula);
            showUnresolvedWarning(result);
            doCopy(result.text, b);
          });
        })(f, btn);
        wrap.appendChild(box);
        wrap.appendChild(btn);
        sec.appendChild(h);
        sec.appendChild(wrap);
        formulasEl.appendChild(sec);
      });
    } else {
      var note = document.createElement('p');
      note.className = 'modal-note';
      note.textContent = lang === 'en'
        ? 'This prompt has no standardized usage formula — it is used directly after the framework.'
        : 'Este prompt no tiene fórmula de uso estandarizada — se usa directamente después del framework.';
      formulasEl.appendChild(note);
    }
  }

  modal.classList.add('open');
}

function copyPrompt(pid, btn) {
  var lang = getCurrentLanguage();
  copyPromptLang(pid, lang, btn);
}

function doCopy(text, btn) {
  var isFw = btn.classList.contains('fw-copy-btn');
  var label = isFw ? 'Framework completo copiado' : 'Prompt copiado con éxito';
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text)
      .then(function() { flash(btn); showToast(label, 'success'); })
      .catch(function() { fbCopy(text, btn, label); });
  } else { fbCopy(text, btn, label); }
}

function fbCopy(text, btn, label) {
  var t = document.createElement('textarea');
  t.value = text; t.style.cssText = 'position:fixed;opacity:0;top:0;left:0';
  document.body.appendChild(t); t.focus(); t.select();
  var copied = false;
  try { copied = document.execCommand('copy'); } catch(e) {}
  document.body.removeChild(t);
  if (copied) {
    flash(btn);
    showToast(label, 'success');
  } else {
    showToast(getCurrentLanguage() === 'en' ? 'Clipboard copy failed' : 'No fue posible copiar al portapapeles', 'warn');
  }
}

function flash(btn) {
  var orig = btn.innerHTML;
  btn.innerHTML = '<span>&#10003;</span> Copiado';
  btn.classList.add('ok');
  setTimeout(function() { btn.innerHTML = orig; btn.classList.remove('ok'); }, 2000);
}

/* ═══════════════════  MULTI-SELECT  ════════════════════════════ */

var msMode = false;

function toggleCard(pid) {
  var b = document.getElementById('cb-' + pid);
  var t = document.getElementById('ce-' + pid);
  if (!b) return;
  ACTIVE_PROMPT_ID = pid;
  ACTIVE_PROMPT_LANG = getCurrentLanguage();
  updateContextualVariablePanel();
  var isOpen = b.classList.toggle('open');
  if (t) t.classList.toggle('open', isOpen);
}

function initMsMode() {
  try {
    var saved = localStorage.getItem('AI_SDLC_ms_mode');
    if (saved === '1') {
      msMode = true;
      document.body.classList.add('ms-mode');
      var btn = document.getElementById('ms-toggle-btn');
      if (btn) btn.classList.add('active');
      var floatBtn = document.getElementById('ms-float-btn');
      if (floatBtn) floatBtn.classList.add('active');
      updateMsBar();
    }
  } catch(e) {}
}

function toggleMsMode() {
  msMode = !msMode;
  document.body.classList.toggle('ms-mode', msMode);
  var btn = document.getElementById('ms-toggle-btn');
  if (btn) btn.classList.toggle('active', msMode);
  var floatBtn = document.getElementById('ms-float-btn');
  if (floatBtn) floatBtn.classList.toggle('active', msMode);
  try {
    localStorage.setItem('AI_SDLC_ms_mode', msMode ? '1' : '0');
  } catch(e) {}
  if (!msMode) {
    clearSelection();
  }
  updateMsBar();
}

// Solo los checkboxes del idioma visible: cada prompt renderiza una card ES y
// una EN (ocultas por CSS), ambas con el mismo data-pid. Filtrar por idioma
// evita seleccionar/contar/copiar el prompt dos veces.
function langCardChecks(scope) {
  var lang = getCurrentLanguage();
  return (scope || document).querySelectorAll('.card[data-lang="' + lang + '"] .card-check');
}

function getSelected() {
  return Array.from(langCardChecks(document)).filter(function(cb) { return cb.checked; });
}

function updateMsBar() {
  var sel = getSelected();
  var bar = document.getElementById('ms-bar');
  if (!bar) return;
  bar.classList.toggle('visible', msMode && sel.length > 0);
  var countEl = document.getElementById('ms-sel-count');
  if (countEl) countEl.textContent = sel.length;
}

function clearSelection() {
  document.querySelectorAll('.card-check').forEach(function(cb) { cb.checked = false; });
  document.querySelectorAll('.card').forEach(function(c) { c.classList.remove('ms-selected'); });
  document.querySelectorAll('.sec-check').forEach(function(cb) { cb.checked = false; cb.indeterminate = false; });
  updateMsBar();
}

function onCardCheck(cb) {
  var card = cb.closest('.card');
  if (card) card.classList.toggle('ms-selected', cb.checked);
  // sync section checkbox
  var group = cb.closest('.section-group');
  if (group) {
    var secCb = group.querySelector('.sec-check');
    var all = langCardChecks(group);
    var checked = Array.from(all).filter(function(cc) { return cc.checked; });
    if (secCb) {
      secCb.indeterminate = checked.length > 0 && checked.length < all.length;
      secCb.checked = all.length > 0 && checked.length === all.length;
    }
  }
  updateMsBar();
}

function onSecCheck(cb) {
  var group = cb.closest('.section-group');
  if (!group) return;
  langCardChecks(group).forEach(function(cc) {
    cc.checked = cb.checked;
    var card = cc.closest('.card');
    if (card) card.classList.toggle('ms-selected', cb.checked);
  });
  cb.indeterminate = false;
  updateMsBar();
}

function copySelected(btn) {
  var checks = getSelected();
  if (!checks.length) return;
  var lang = getCurrentLanguage();
  // obtener prompts en orden DOM (orden de proceso)
  var aggregate = { unresolvedRequired: [], unresolvedOptional: [] };
  var seenPids = {};
  var parts = checks.map(function(cb) {
    var pid = cb.dataset.pid;
    if (seenPids[pid]) return '';
    seenPids[pid] = true;
    var codeId = 'code-' + pid + '-' + lang;
    var el = document.getElementById(codeId);
    if (!el) return '';
    var result = resolvePrompt(RAW_PROMPTS[codeId] || el.textContent);
    aggregate.unresolvedRequired = aggregate.unresolvedRequired.concat(result.unresolvedRequired);
    aggregate.unresolvedOptional = aggregate.unresolvedOptional.concat(result.unresolvedOptional);
    return result.text;
  }).filter(Boolean);
  var fwId = 'code-fw-' + lang;
  var fwResult = resolvePrompt(RAW_PROMPTS[fwId] || getFwText());
  aggregate.unresolvedRequired = aggregate.unresolvedRequired.concat(fwResult.unresolvedRequired);
  aggregate.unresolvedOptional = aggregate.unresolvedOptional.concat(fwResult.unresolvedOptional);
  var text = (fwResult.text ? fwResult.text + '\\n\\n---\\n\\n' : '') + parts.join('\\n\\n---\\n\\n');
  showUnresolvedWarning(aggregate);
  doCopy(text, btn);
}

/* ═══════════════════  SEARCH / FILTER  ═════════════════════════ */

function filterPrompts(q) {
  q = q.toLowerCase().trim();
  var groups = document.querySelectorAll('.section-group');
  var total = 0;
  groups.forEach(function(g) {
    var cards = g.querySelectorAll('.card');
    var vis = 0;
    cards.forEach(function(card) {
      var title = (card.querySelector('.card-title') || {}).textContent || '';
      var codeEl = card.querySelector('code');
      var code = codeEl ? codeEl.textContent : '';
      var match = !q || title.toLowerCase().includes(q) || code.toLowerCase().includes(q);
      card.style.display = match ? '' : 'none';
      if (match) vis++;
    });
    g.style.display = vis ? '' : 'none';
    total += vis;
  });
  var fw = document.getElementById('sec-00');
  if (fw) fw.style.display = '';
  var empty = document.getElementById('glbl-empty');
  if (empty) empty.style.display = total === 0 ? '' : 'none';
  var countEl = document.getElementById('vis-count');
  if (countEl) countEl.textContent = total + (q ? ' coincidencia' + (total!==1?'s':'') : ' prompts en total');
}

/* ═══════════════════  INFO MODAL  ══════════════════════════════ */

function openInfo(pid) {
  var lang = getCurrentLanguage();
  openInfoLang(pid, lang);
}

function closeInfo() {
  var modal = document.getElementById('info-modal');
  if (modal) modal.classList.remove('open');
}

/* ═══════════════════  WELCOME BANNER  ═════════════════════════ */
var LS_WELCOME = 'AI_SDLC_welcome_seen';
var LS_ONBOARD = 'AI_SDLC_onboarding_done';
var LS_EMAIL  = 'AI_SDLC_email_collected';

function initWelcomeBanner() {
  try {
    var banner = document.getElementById('welcome-banner');
    if (!banner) return;
    if (localStorage.getItem(LS_WELCOME) === '1') banner.classList.add('hidden');
  } catch(e) {}
}

function dismissWelcomeBanner() {
  try {
    var banner = document.getElementById('welcome-banner');
    if (banner) banner.classList.add('hidden');
    localStorage.setItem(LS_WELCOME, '1');
  } catch(e) {}
}

/* ═══════════════════  ONBOARDING  ══════════════════════════════ */
var _obStep = 0;
var _obTotal = 4;

function initOnboarding() {
  try {
    if (localStorage.getItem(LS_ONBOARD) === '1') return;
    var overlay = document.getElementById('ob-overlay');
    if (overlay) overlay.classList.remove('hidden');
    _obStep = 0;
    renderObStep();
  } catch(e) {}
}

function renderObStep() {
  for (var i = 0; i < _obTotal; i++) {
    var step = document.getElementById('ob-step-' + i);
    if (step) step.classList.toggle('active', i === _obStep);
    var dot = document.getElementById('ob-dot-' + i);
    if (dot) dot.classList.toggle('on', i === _obStep);
  }
  var prevBtn = document.getElementById('ob-prev-btn');
  var nextBtn = document.getElementById('ob-next-btn');
  var lang = getCurrentLanguage();
  if (prevBtn) prevBtn.style.display = _obStep > 0 ? 'inline-block' : 'none';
  if (nextBtn) {
    if (_obStep < _obTotal - 1) {
      nextBtn.innerHTML = lang === 'en' ? 'Next &#8250;' : 'Siguiente &#8250;';
    } else {
      nextBtn.innerHTML = lang === 'en' ? '&#10003; Start' : '&#10003; Comenzar';
    }
  }
}

function obNext() {
  if (_obStep < _obTotal - 1) { _obStep++; renderObStep(); }
  else { closeOnboarding(true); }
}

function obPrev() {
  if (_obStep > 0) { _obStep--; renderObStep(); }
}

function closeOnboarding(permanent) {
  try {
    var overlay = document.getElementById('ob-overlay');
    if (overlay) overlay.classList.add('hidden');
    if (permanent) localStorage.setItem(LS_ONBOARD, '1');
  } catch(e) {}
}

function skipOnboarding() { closeOnboarding(false); }

function submitObEmail() {
  try {
    var input = document.getElementById('ob-email-input');
    var btn   = document.getElementById('ob-email-submit-btn');
    var email = input ? input.value.trim() : '';
    if (!email || !email.includes('@')) {
      if (input) input.focus();
      return;
    }
    // Guardar localmente
    localStorage.setItem(LS_EMAIL, email);
    // Enviar a Mailchimp (POST silencioso — sin redirección)
    var MC_URL = 'https://lionsystems.us22.list-manage.com/subscribe/post-json?u=MAILCHIMP_U&id=MAILCHIMP_ID&c=?';
    var formData = 'EMAIL=' + encodeURIComponent(email) + '&b_MAILCHIMP_U_MAILCHIMP_ID=';
    var script = document.createElement('script');
    var callbackName = 'mc_cb_' + Date.now();
    window[callbackName] = function() { delete window[callbackName]; };
    // Construir URL JSONP (Mailchimp free tier)
    var url = MC_URL + '&' + formData;
    script.src = url;
    document.body.appendChild(script);
    // Feedback visual
    if (btn) {
      var lang = getCurrentLanguage();
      btn.textContent = lang === 'en' ? '\u2713 Done' : '\u2713 Listo';
      btn.classList.add('ok');
      btn.disabled = true;
    }
    setTimeout(function() { obNext(); }, 900);
  } catch(e) { obNext(); }
}

/* ═══════════════════  INIT  ════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function() {
  // Capturar plantillas limpias para Live Preview antes de inyectar variables
  document.querySelectorAll('code[id^="code-"]').forEach(function(codeEl) {
    RAW_PROMPTS[codeEl.id] = codeEl.textContent;
  });

  // ── Inicializar proyectos ──
  if (!loadProjects()) createProject('Default');
  renderProjectSelector();
  syncPanelToProject();
  renderProjQuick();
  renderProjFloat();

  // Restaurar estado del sidebar
  try { if (localStorage.getItem('AI_SDLC_sidebar') === '1') document.body.classList.add('sidebar-collapsed'); } catch(e) {}

  initMsMode();

  // Welcome banner y onboarding — solo primera visita
  initWelcomeBanner();
  initOnboarding();

  initLanguageDetection();
  initFrameworkState();

  updateLivePreview();
  if (typeof initChips === 'function') initChips();

  // Cerrar menús al hacer clic fuera
  document.addEventListener('click', function(e) {
    var wrap = document.getElementById('proj-quick');
    if (wrap && !wrap.contains(e.target)) closeProjQuick();
    
    var floatWrap = document.getElementById('proj-float');
    if (floatWrap && !floatWrap.contains(e.target)) closeProjFloat();

    var varFloat = document.getElementById('var-float');
    if (varFloat && !varFloat.contains(e.target)) closeVarFloat();
    
    var dd = document.getElementById('lang-dropdown');
    var btn = document.getElementById('lang-btn');
    if (dd && !dd.contains(e.target) && btn && !btn.contains(e.target)) closeLanguageDropdown();
    
    // Cerrar menú hamburguesa si se hace clic fuera del sidebar en móvil
    if (document.body.classList.contains('menu-open') && !e.target.closest('.sidebar') && !e.target.closest('.menu-toggle-btn')) {
      closeMenu();
    }
  });

  // Cerrar modal de info al pulsar Escape o clic en overlay
  var overlay = document.getElementById('info-modal');
  if (overlay) {
    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) closeInfo();
    });
  }
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') { 
      closeInfo(); closeVarPanel(); closeVarFloat(); closeProjectsModal(); 
      closeProjQuick(); skipOnboarding(); closeMenu(); closeLanguageDropdown();
    }
  });

  var content = document.querySelector('.content');
  if (!content) return;
  var targets = document.querySelectorAll('[data-observe]');
  if (!targets.length) return;
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      var link = document.querySelector('.sid-link[href="#' + entry.target.id + '"]');
      if (link) link.classList.toggle('active', entry.isIntersecting);
    });
  }, { root: content, threshold: 0.04, rootMargin: '-2% 0px -88% 0px' });
  targets.forEach(function(el) { obs.observe(el); });
});
"""

LANDING_JS = """
/* ═══════ ROUTING client-side ═══════ */
(function() {
  function route() {
    var path = window.location.pathname;
    var search = window.location.search;
    var hash = window.location.hash;
    // Soporte para producción (/app) y local (?view=app o #app)
    var isApp = path === '/app' || path.startsWith('/app/') || search.includes('view=app') || hash === '#app';
    var lr = document.getElementById('landing-root');
    var ar = document.getElementById('app-root');
    if (lr) lr.classList.toggle('landing-hidden', isApp);
    if (ar) ar.classList.toggle('app-hidden', !isApp);
    
    // Si entramos a la app, inicializar i18n si no se ha hecho
    if (isApp && typeof initLanguageDetection === 'function') {
      initLanguageDetection();
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', route);
  } else {
    route();
  }
  window.addEventListener('popstate', route);
  window.addEventListener('hashchange', route);
})();
"""

def get_landing_html(n):
    ls = i18n_strings.LANDING_STRINGS['es']
    return (
        f'<div id="landing-root" class="landing">\n'
        f'  <nav class="landing-nav">\n'
        f'    <div class="landing-nav-logo">\n'
        f'      <img src="https://lionsystems.com.mx/assets/images/icons/lionsystems_icon.png" width="28" height="28" alt="Lionsystems" style="border-radius:4px;flex-shrink:0;">\n'
        f'      <h1>AI-SDLC Pro</h1>\n'
        f'    </div>\n'
        f'    <a class="landing-nav-cta" href="/app">{ls["cta_nav"]}</a>\n'
        f'  </nav>\n'
        f'  <section class="landing-hero">\n'
        f'    <span class="landing-badge">\u25cf {ls["hero_badge"].format(n=n)}</span>\n'
        f'    <h2>{ls["hero_title"]}</h2>\n'
        f'    <p>{ls["hero_subtitle"].format(n=n)}</p>\n'
        f'    <div class="landing-cta-group">\n'
        f'      <a class="landing-cta-primary" href="/app">{ls["cta_primary"]}</a>\n'
        f'      <a class="landing-cta-secondary" href="https://github.com/dleon55/ai-sdlc-prompts" target="_blank" rel="noopener">{ls["cta_secondary"]}</a>\n'
        f'    </div>\n'
        f'  </section>\n'
        f'  <section class="landing-pain">\n'
        f'    <div class="landing-pain-inner">\n'
        f'      <h3>{ls["pain_title"]}</h3>\n'
        f'      <p class="landing-pain-sub">{ls["pain_subtitle"]}</p>\n'
        f'      <div class="landing-pain-grid">\n'
        f'        <div class="pain-card"><div class="pain-card-icon">\U0001f3b2</div>\n'
        f'          <h4>{ls["pain_1_title"]}</h4>\n'
        f'          <p>{ls["pain_1_desc"]}</p>\n'
        f'        </div>\n'
        f'        <div class="pain-card"><div class="pain-card-icon">\U0001f501</div>\n'
        f'          <h4>{ls["pain_2_title"]}</h4>\n'
        f'          <p>{ls["pain_2_desc"]}</p>\n'
        f'        </div>\n'
        f'        <div class="pain-card"><div class="pain-card-icon">\U0001f9e9</div>\n'
        f'          <h4>{ls["pain_3_title"]}</h4>\n'
        f'          <p>{ls["pain_3_desc"]}</p>\n'
        f'        </div>\n'
        f'        <div class="pain-card"><div class="pain-card-icon">\u26a0\ufe0f</div>\n'
        f'          <h4>{ls["pain_4_title"]}</h4>\n'
        f'          <p>{ls["pain_4_desc"]}</p>\n'
        f'        </div>\n'
        f'      </div>\n'
        f'    </div>\n'
        f'  </section>\n'
        f'  <section class="landing-proof">\n'
        f'    <h3>{ls["proof_title"]}</h3>\n'
        f'    <div class="proof-grid">\n'
        f'      <div class="proof-stat"><div class="proof-stat-num">{n}</div><div class="proof-stat-label">{ls["proof_stat_1_label"]}</div></div>\n'
        f'      <div class="proof-stat"><div class="proof-stat-num">15</div><div class="proof-stat-label">{ls["proof_stat_2_label"]}</div></div>\n'
        f'      <div class="proof-stat"><div class="proof-stat-num">6</div><div class="proof-stat-label">{ls["proof_stat_3_label"]}</div></div>\n'
        f'      <div class="proof-stat"><div class="proof-stat-num">0</div><div class="proof-stat-label">{ls["proof_stat_4_label"]}</div></div>\n'
        f'    </div>\n'
        f'  </section>\n'
        f'  <section class="landing-final">\n'
        f'    <h3>{ls["final_title"]}</h3>\n'
        f'    <p>{ls["final_subtitle"]}</p>\n'
        f'    <div class="landing-cta-group">\n'
        f'      <a class="landing-cta-primary" href="/app">{ls["cta_nav"]}</a>\n'
        f'    </div>\n'
        f'  </section>\n'
        f'  <footer class="landing-footer">\n'
        f'    <span>{ls["footer_copyright"]}</span>\n'
        f'    <a class="landing-cta-secondary" style="font-size:.72rem;padding:.25rem .75rem;" href="https://lionsystems.com.mx" target="_blank" rel="noopener">lionsystems.com.mx \u2197</a>\n'
        f'  </footer>\n'
        f'</div>\n'
    )

LANDING_HTML = get_landing_html(TOTAL_PROMPTS)


def build():
    # ── leer framework en ambos idiomas ──
    fw_file_es = PROMPTS_DIR / "00-framework.md"
    fw_file_en = PROMPTS_DIR / "00-framework.en.md"
    _, fw_prompt_es, _, _ = parse_md(fw_file_es) if fw_file_es.exists() else ("", "", "", [])
    _, fw_prompt_en, _, _ = parse_md(fw_file_en) if fw_file_en.exists() else ("", fw_prompt_es, "", [])

    # ── leer prompts (ES y EN) ──
    sections = defaultdict(list)
    for md_file in sorted(PROMPTS_DIR.glob("*.md")):
        name = md_file.stem
        if name == "00-framework": continue
        if name.endswith(".en"): continue
        parts = name.split("-")
        sk = parts[0]
        if sk not in SECTION_META: continue
        title_es, prompt_es, description_es, formulas_es = parse_md(md_file)
        en_file = md_file.with_suffix(".en.md")
        if en_file.exists():
            title_en, prompt_en, description_en, formulas_en = parse_md(en_file)
        else:
            title_en, prompt_en, description_en, formulas_en = title_es, prompt_es, description_es, formulas_es
        sections[sk].append({
            "id": name,
            "title_es": title_es, "prompt_es": prompt_es,
            "description_es": description_es, "formulas_es": formulas_es,
            "title_en": title_en, "prompt_en": prompt_en,
            "description_en": description_en, "formulas_en": formulas_en,
        })

    total = sum(len(v) for v in sections.values())

    # ── PROMPT_INFO para el modal de ⓘ ──
    info_data = {}
    for sk, items in sections.items():
        for p in items:
            info_data[p["id"]] = {
                "title_es": p["title_es"], "title_en": p["title_en"],
                "desc_es":  p.get("description_es", ""), "desc_en": p.get("description_en", ""),
                "formulas_es": p.get("formulas_es", []), "formulas_en": p.get("formulas_en", []),
            }
    prompt_info_js = "var PROMPT_INFO = " + json.dumps(info_data, ensure_ascii=False) + ";"

    # ── sidebar ──
    COPY_ICO = (
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="1.8"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>'
        '<path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>'
    )

    fw_color = SECTION_COLOR["00"]
    fw_icon_key = SECTION_META["00"][1]

    # ── Sidebar ──
    sidebar_html = (
        '<div class="sid-section">'
        '<div class="sid-label sid-lang-es">Framework</div>'
        '<div class="sid-label sid-lang-en">Framework</div>'
        '<a class="sid-link sid-framework active" href="#sec-00" onclick="closeMenu()">'
        '<span class="sid-icon">' + icon_svg(fw_icon_key, fw_color, 15) + '</span>'
        '<span class="sid-text sid-lang-es">00 — Framework base</span>'
        '<span class="sid-text sid-lang-en">00 — Base Framework</span>'
        '<span class="sid-badge">★</span>'
        '</a>'
        '</div>'
        '<div class="sid-section">'
        '<div class="sid-label sid-lang-es">Prompts</div>'
        '<div class="sid-label sid-lang-en">Prompts</div>'
    )

    # Mapeo de labels para sidebar (usado en generación estática)
    SEC_LABELS = i18n_strings.SECTION_LABELS_I18N

    for sk in sorted(k for k in sections if k != "00"):
        label_es = SEC_LABELS['es'].get(sk, sk)
        label_en = SEC_LABELS['en'].get(sk, sk)
        icon_key = SECTION_META.get(sk, ("", "docs"))[1]
        color = SECTION_COLOR.get(sk, "#6366f1")
        cnt = len(sections[sk])
        sidebar_html += (
            '<a class="sid-link" href="#sec-' + sk + '" onclick="closeMenu()">'
            + icon_svg(icon_key, color, 15) +
            '<span class="sid-text sid-lang-es">' + sk + ' — ' + label_es + '</span>'
            '<span class="sid-text sid-lang-en">' + sk + ' — ' + label_en + '</span>'
            '<span class="sid-badge">' + str(cnt) + '</span>'
            '</a>'
        )
    sidebar_html += '</div>'

    # ── framework banner bilingüe ──
    chevron = chevron_svg()
    fw_escaped_es = h(fw_prompt_es)
    fw_escaped_en = h(fw_prompt_en)
    
    # Banner en español
    fw_block_es = (
        '<div class="framework-banner fw-lang-es" id="sec-00-es" data-observe>'
        '<div class="fw-header" onclick="toggleFramework()" title="Click para expandir/colapsar">'
        '<span class="fw-badge">&#9888; Obligatorio</span>'
        + icon_svg("framework", SECTION_COLOR["00"], 18) +
        '<span class="fw-title">&#128204; PASO 1 — Copia este bloque antes de usar cualquier prompt</span>'
        '<button class="fw-expand" id="fe-00-es" onclick="event.stopPropagation(); toggleFramework();" title="Expandir / colapsar">'
        + chevron +
        '</button>'
        '</div>'
        '<div class="fw-body" id="fb-00-es">'
        '<p class="fw-desc">Este bloque define el rol del agente, el contexto multi-agente y las reglas obligatorias de ingenier\u00eda. '
        'Sin \u00e9l, el agente responde de forma gen\u00e9rica. C\u00f3pialo y p\u00e9galo <strong>siempre primero</strong> en tu conversaci\u00f3n con el agente IA.</p>'
        '<pre><code id="code-fw-es">' + fw_escaped_es + '</code></pre>'
        '</div>'
        '<div class="fw-copy-row">'
        '<button class="fw-copy-btn" onclick="copyPromptLang(\'fw\', \'es\', this)">'
        + COPY_ICO + ' Copiar framework completo'
        '</button>'
        '</div>'
        '</div>'
    )
    
    # Banner en inglés
    fw_block_en = (
        '<div class="framework-banner fw-lang-en" id="sec-00-en" data-observe>'
        '<div class="fw-header" onclick="toggleFramework()" title="Click to expand/collapse">'
        '<span class="fw-badge">&#9888; Required</span>'
        + icon_svg("framework", SECTION_COLOR["00"], 18) +
        '<span class="fw-title">&#128204; STEP 1 — Copy this block before using any prompt</span>'
        '<button class="fw-expand" id="fe-00-en" onclick="event.stopPropagation(); toggleFramework();" title="Expand / collapse">'
        + chevron +
        '</button>'
        '</div>'
        '<div class="fw-body" id="fb-00-en">'
        '<p class="fw-desc">This block defines the agent role, multi-agent context, and mandatory engineering rules. '
        'Without it, the agent responds generically. Copy and paste it <strong>always first</strong> in your conversation with the AI agent.</p>'
        '<pre><code id="code-fw-en">' + fw_escaped_en + '</code></pre>'
        '</div>'
        '<div class="fw-copy-row">'
        '<button class="fw-copy-btn" onclick="copyPromptLang(\'fw\', \'en\', this)">'
        + COPY_ICO + ' Copy complete framework'
        '</button>'
        '</div>'
        '</div>'
    )
    
    fw_block = fw_block_es + fw_block_en

    # ── section groups ──
    groups_html = ""
    for sk in sorted(sections.keys()):
        label_es = SEC_LABELS['es'].get(sk, sk)
        label_en = SEC_LABELS['en'].get(sk, sk)
        icon_key = SECTION_META.get(sk, ("", "docs"))[1]
        color = SECTION_COLOR.get(sk, "#6366f1")
        cnt = len(sections[sk])
        gid = "sec-" + sk

        # section header
        groups_html += (
            '<div class="section-group" id="' + gid + '" data-observe>'
            '<div class="section-header-row">'
            '<input type="checkbox" class="sec-check" title="Seleccionar toda la sección" onchange="onSecCheck(this)">'
            '<span class="sec-num" style="color:' + color + ';border-color:' + color + '22;background:' + color + '11">'
            + sk + '</span>'
            + icon_svg(icon_key, color, 16) +
            '<span class="sec-label sec-lang-es">' + label_es + '</span>'
            '<span class="sec-label sec-lang-en">' + label_en + '</span>'
            '<span class="sec-count">' + str(cnt) + '</span>'
            '</div>'
            '<div class="cards-grid">'
        )

        for p in sections[sk]:
            pid = p["id"]
            has_info_es = bool(p.get("description_es") or p.get("formulas_es"))
            has_info_en = bool(p.get("description_en") or p.get("formulas_en"))

            # Limpiar títulos (remover prefijos numéricos tipo "01-01 — ")
            clean_t_es = re.sub(r'^[0-9.-]+\s*[—–-]\s*', '', p["title_es"])
            clean_t_en = re.sub(r'^[0-9.-]+\s*[—–-]\s*', '', p["title_en"])
            t_es_attr = clean_t_es.replace('"', '&quot;')
            t_en_attr = clean_t_en.replace('"', '&quot;')

            # Card en Español
            groups_html += (
                '<div class="card" data-lang="es">'
                '<div class="card-head">'
                '<input type="checkbox" class="card-check" data-pid="' + pid + '"'
                ' onchange="onCardCheck(this)" title="Seleccionar prompt">'
                '<button class="card-expand" id="ce-' + pid + '-es"'
                ' onclick="toggleCard(\'' + pid + '-es\')" title="Ver / ocultar prompt">'
                + chevron +
                '</button>'
                '<span class="card-title" onclick="toggleCard(\'' + pid + '-es\')">'
                + h(p["title_es"]) +
                '</span>'
            )
            if has_info_es:
                groups_html += (
                    '<button class="info-btn" onclick="openInfoLang(\'' + pid + '\', \'es\')"'
                    ' title="Cuándo usar · Fórmula de uso estándar">&#9432;</button>'
                )
            groups_html += (
                '<button class="copy-btn" data-title="' + t_es_attr + '" onclick="copyPromptLang(\'' + pid + '\', \'es\', this)">'
                + COPY_ICO + ' Copiar'
                '</button>'
                '</div>'
                '<div class="card-body" id="cb-' + pid + '-es">'
                '<pre><code id="code-' + pid + '-es">' + h(p["prompt_es"]) + '</code></pre>'
                '</div>'
                '</div>'
            )

            # Card en Inglés
            groups_html += (
                '<div class="card" data-lang="en">'
                '<div class="card-head">'
                '<input type="checkbox" class="card-check" data-pid="' + pid + '"'
                ' onchange="onCardCheck(this)" title="Select prompt">'
                '<button class="card-expand" id="ce-' + pid + '-en"'
                ' onclick="toggleCard(\'' + pid + '-en\')" title="Show / hide prompt">'
                + chevron +
                '</button>'
                '<span class="card-title" onclick="toggleCard(\'' + pid + '-en\')">'
                + h(p["title_en"]) +
                '</span>'
            )
            if has_info_en:
                groups_html += (
                    '<button class="info-btn" onclick="openInfoLang(\'' + pid + '\', \'en\')"'
                    ' title="When to use · Standard usage formula">&#9432;</button>'
                )
            groups_html += (
                '<button class="copy-btn" data-title="' + t_en_attr + '" onclick="copyPromptLang(\'' + pid + '\', \'en\', this)">'
                + COPY_ICO + ' Copy'
                '</button>'
                '</div>'
                '<div class="card-body" id="cb-' + pid + '-en">'
                '<pre><code id="code-' + pid + '-en">' + h(p["prompt_en"]) + '</code></pre>'
                '</div>'
                '</div>'
            )

        groups_html += '</div></div>'

    # ── HTML final ──
    html = (
        '<!DOCTYPE html>\n<html lang="es">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
        f'<title>{i18n_strings.LANDING_STRINGS["es"]["page_title"]}</title>\n'
        f'<meta name="description" content="{i18n_strings.LANDING_STRINGS["es"]["meta_description"].format(n=TOTAL_PROMPTS)}">\n'
        '<meta name="keywords" content="prompts ingenieria software IA, prompts GitHub Copilot SDLC, prompts Claude desarrollo software, AI-SDLC framework espanol, prompts multi-agente desarrollo software, biblioteca prompts cursor windsurf">\n'
        '<meta name="author" content="LionSystems">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:url" content="https://prompts.lionsystems.com.mx">\n'
        f'<meta property="og:title" content="{i18n_strings.LANDING_STRINGS["es"]["page_title"]}">\n'
        f'<meta property="og:description" content="{i18n_strings.LANDING_STRINGS["es"]["meta_description"].format(n=TOTAL_PROMPTS)}">\n'
        '<meta property="og:image" content="https://prompts.lionsystems.com.mx/og-image.png">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{i18n_strings.LANDING_STRINGS["es"]["page_title"]}">\n'
        '<link rel="canonical" href="https://prompts.lionsystems.com.mx">\n'
        '<link rel="alternate" hreflang="es" href="https://prompts.lionsystems.com.mx">\n'
        '<link rel="alternate" hreflang="en" href="https://prompts.lionsystems.com.mx">\n'
        '<link rel="alternate" hreflang="x-default" href="https://prompts.lionsystems.com.mx">\n'
        '<script async src="https://www.googletagmanager.com/gtag/js?id=G-C5JKYNZ62F"></script>\n'
        '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-C5JKYNZ62F");</script>\n'
        '<style>' + CSS + '</style>\n'
        '</head>\n<body>\n'

        + LANDING_HTML +

        '<div id="app-root" class="app-hidden">\n'

        '<header>\n'
        '  <div class="hdr-logo">'
        '    <button class="menu-toggle-btn" onclick="toggleMenu()" title="Menú">'
        '      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '        <line x1="3" y1="12" x2="21" y2="12"></line>'
        '        <line x1="3" y1="6" x2="21" y2="6"></line>'
        '        <line x1="3" y1="18" x2="21" y2="18"></line>'
        '      </svg>'
        '    </button>'
        '    <div class="hdr-logo-icon">'
        '      <img src="https://lionsystems.com.mx/assets/images/icons/lionsystems_icon.png" width="28" height="28" alt="Lionsystems" style="border-radius:4px;flex-shrink:0;">'
        '    </div>'
        '    <div>'
        '      <h1>AI-SDLC Pro</h1>'
        '      <p>Biblioteca de Prompts / Lionsystems</p>'
        '    </div>'
        '  </div>\n'
        '  <div class="hdr-tags">'
        '    <div class="tag">v1.2.0</div>'
        '    <div class="lang-wrap">'
        '      <button class="lang-btn" id="lang-btn" onclick="toggleLanguageDropdown()" title="Cambiar idioma / Change language">'
        '        <span class="flag">&#127760;</span><span class="lang-label" id="current-lang-label">ES</span>'
        '      </button>'
        '      <div class="lang-dropdown" id="lang-dropdown">'
        '        <div class="lang-option" data-lang="es" onclick="onLanguageSelect(\'es\')">Español</div>'
        '        <div class="lang-option" data-lang="en" onclick="onLanguageSelect(\'en\')">English</div>'
        '      </div>'
        '    </div>'
        '    <div class="hdr-brand">'
        '      <div><span class="hdr-brand-text">Lionsystems</span>'
        '      <span class="hdr-brand-sub">Prueba gratis &middot; Plan Pro</span></div>'
        '    </div>'
        '  </div>\n'
        '</header>\n'

        # welcome banner (primer uso — se oculta con localStorage)
        '<div class="welcome-banner" id="welcome-banner">\n'
        '  <span class="wb-lead fw-lang-es">&#128640; Bienvenido a AI-SDLC Pro</span>\n'
        '  <span class="wb-lead fw-lang-en">&#128640; Welcome to AI-SDLC Pro</span>\n'
        '  <div class="wb-pills fw-lang-es">\n'
        '    <span class="wb-pill">&#9654; Ciclo SDLC completo: del an\u00e1lisis al incident response</span>\n'
        '    <span class="wb-pill">&#9656; Variables de contexto que adaptan cada prompt a tu proyecto</span>\n'
        '    <span class="wb-pill">&#9656; Gobernanza multi-agente: Copilot, Claude, Cursor, Windsurf</span>\n'
        '  </div>\n'
        '  <div class="wb-pills fw-lang-en">\n'
        '    <span class="wb-pill">&#9654; Complete SDLC cycle: from analysis to incident response</span>\n'
        '    <span class="wb-pill">&#9656; Context variables that adapt each prompt to your project</span>\n'
        '    <span class="wb-pill">&#9656; Multi-agent governance: Copilot, Claude, Cursor, Windsurf</span>\n'
        '  </div>\n'
        '  <button class="wb-dismiss fw-lang-es" onclick="dismissWelcomeBanner()">Entendido &#x2715;</button>\n'
        '  <button class="wb-dismiss fw-lang-en" onclick="dismissWelcomeBanner()">Got it &#x2715;</button>\n'
        '</div>\n'

        # search bar
        '<div class="search-bar">\n'
        '  <div class="proj-quick" id="proj-quick">'
        '<button class="proj-quick-btn" id="proj-quick-btn" onclick="toggleProjQuick(event)" title="Cambiar proyecto activo / Change active project">'
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7h18M3 12h18M3 17h18"/></svg>'
        '<span class="proj-quick-name" id="proj-quick-name">Proyecto</span>'
        '<span class="proj-quick-chevron"><svg width="9" height="9" viewBox="0 0 10 10" fill="none"><path d="M2.5 3.5L5 6 7.5 3.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
        '</button>'
        '<div class="proj-quick-dropdown" id="proj-quick-dropdown"></div>'
        '</div>\n'
        '  <div class="search-wrap">'
        '<span class="search-ico">'
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>'
        '</span>'
        '<input type="text" placeholder="Buscar por nombre o contenido del prompt..."'
        ' oninput="filterPrompts(this.value)" autocomplete="off">'
        '</div>\n'
        '  <div class="chips-container" id="category-chips"></div>\n'
        '  <span class="search-count" id="vis-count">prompts</span>\n'
        '  <span class="vars-active-badge" id="vars-badge">■ Vars activas</span>\n'
        '  <button class="ms-toggle-btn" id="ms-toggle-btn" onclick="toggleMsMode()" title="Activar selección múltiple">'
        '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<rect x="3" y="5" width="13" height="13" rx="2"/><path d="M8 10l3 3 5-5"/>'
        '</svg><span class="ms-label"> Multi-select</span></button>\n'
        '  <button class="var-toggle-btn" id="var-toggle-btn" onclick="toggleVarPanel()" title="Panel de variables">'
        '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<path d="M12 20h9M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/>'
        '</svg><span class="var-label"> Variables</span></button>\n'
        '</div>\n'

        # layout
        '<div class="layout">\n'
        '  <nav class="sidebar">\n'
        '<div class="sidebar-header">'
        '<span class="sidebar-label-text">Nav</span>'
        '<button class="sidebar-collapse-btn" onclick="toggleSidebar()" title="Colapsar / expandir menú">'
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<path stroke-linecap="round" stroke-linejoin="round" d="M11 19l-7-7 7-7m8 14l-7-7 7-7"/>'
        '</svg>'
        '</button>'
        '</div>'
        + sidebar_html + '  </nav>\n'
        '  <div class="content">\n'
        + fw_block
        + groups_html +
        '    <div class="glbl-empty" id="glbl-empty" style="display:none">'
        '<p>Sin resultados.</p><small>Intenta con otro término de búsqueda.</small>'
        '</div>\n'
        '  </div>\n'
        '</div>\n'

        # ── Panel de variables ──
        '<div class="var-panel" id="var-panel">\n'
        '  <div class="var-panel-hdr">'
        '<h2><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2">'
        '<path d="M12 20h9M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>'
        ' <span class="fw-lang-es">Variables del prompt</span><span class="fw-lang-en">Prompt Variables</span></h2>'
        '<button class="var-close-btn" onclick="closeVarPanel()" title="Cerrar / Close">&#x2715;</button>'
        '</div>\n'
        '<div class="proj-selector-row">'
        '<select id="proj-selector" class="proj-select" onchange="switchProject(this.value)" style="display:none"></select>'
        '<div style="flex:1;font-size:.74rem;color:var(--tx2);display:flex;align-items:center;gap:5px;overflow:hidden;">'
        '<span style="color:var(--tx3);flex-shrink:0;"><span class="fw-lang-es">Proyecto\u00a0</span><span class="fw-lang-en">Project\u00a0</span></span>'
        '<span id="vp-proj-name" style="color:#7dd3fc;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"></span>'
        '</div>'
        '<button class="proj-mgr-btn" onclick="openProjectsModal()" title="Gestionar proyectos / Manage projects">&#x2699;</button>'
        '</div>\n'
        '  <div class="var-panel-body">\n'
        '    <div class="var-context-status" id="var-context-status"></div>\n'

        # repositorio
        '    <div class="var-group" data-field="repositorio">'
        '<label for="vf-repositorio"><span class="fw-lang-es">Repositorio</span><span class="fw-lang-en">Repository</span></label>'
        '<input id="vf-repositorio" type="text" placeholder="" oninput="syncProjectFromPanel();updateVarsBadge();">'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[NOMBRE O URL]</span><span class="fw-lang-en">[NAME OR URL]</span></span>'
        '</div>'
        '</div>\n'

        # referencia / issue
        '    <div class="var-group" data-field="referencia">'
        '<label for="vf-referencia"><span class="fw-lang-es">Issue / Referencia</span><span class="fw-lang-en">Issue / Reference</span></label>'
        '<textarea id="vf-referencia" placeholder="" oninput="syncProjectFromPanel();updateVarsBadge();"></textarea>'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[REFERENCIA]</span><span class="fw-lang-en">[REFERENCE]</span></span>'
        '</div>'
        '</div>\n'

        # entrada principal
        '    <div class="var-group" data-field="entrada">'
        '<label for="vf-entrada"><span class="fw-lang-es">Entrada principal</span><span class="fw-lang-en">Primary input</span></label>'
        '<textarea id="vf-entrada" rows="4" placeholder="Requerimiento, lista de issues, reporte o contexto a analizar" oninput="syncProjectFromPanel();updateVarsBadge();"></textarea>'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[ENTRADA PRINCIPAL]</span><span class="fw-lang-en">[PRIMARY INPUT]</span></span>'
        '</div>'
        '</div>\n'

        # objetivo puntual de salida
        '    <div class="var-group" data-field="objetivo">'
        '<label for="vf-objetivo"><span class="fw-lang-es">Objetivo puntual de salida</span><span class="fw-lang-en">Specific output objective</span></label>'
        '<textarea id="vf-objetivo" placeholder="Indica el resultado concreto esperado del prompt" oninput="syncProjectFromPanel();updateVarsBadge();"></textarea>'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[OBJETIVO ESPECÍFICO] reemplaza [INDICAR]</span><span class="fw-lang-en">[SPECIFIC OBJECTIVE] replaces [INDICATE]</span></span>'
        '</div>'
        '</div>\n'

        # responsable
        '    <div class="var-group" data-field="responsable">'
        '<label for="vf-responsable"><span class="fw-lang-es">Responsable / assignee</span><span class="fw-lang-en">Responsible person / assignee</span></label>'
        '<input id="vf-responsable" type="text" placeholder="usuario, equipo o rol" oninput="syncProjectFromPanel();updateVarsBadge();">'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[RESPONSABLE]</span><span class="fw-lang-en">[ASSIGNEE]</span></span>'
        '</div>'
        '</div>\n'

        # workspace / subproyecto
        '    <div class="var-group" data-field="workspace">'
        '<label for="vf-workspace"><span class="fw-lang-es">Workspace / subproyecto</span><span class="fw-lang-en">Workspace / subproject</span></label>'
        '<input id="vf-workspace" type="text" placeholder="apps/admin, packages/api o no aplica" oninput="syncProjectFromPanel();updateVarsBadge();">'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[WORKSPACE/SUBPROYECTO]</span><span class="fw-lang-en">[WORKSPACE/SUBPROJECT]</span></span>'
        '</div>'
        '</div>\n'

        # estándar / compliance
        '    <div class="var-group" data-field="compliance">'
        '<label for="vf-compliance"><span class="fw-lang-es">Estándar / compliance</span><span class="fw-lang-en">Standard / compliance</span></label>'
        '<select id="vf-compliance" multiple data-other-input="vf-compliance-other" aria-describedby="vf-compliance-help" onchange="syncMultiSelectOther(\'vf-compliance\')">'
        '<option value="PSP">PSP</option>'
        '<option value="TSP">TSP</option>'
        '<option value="ISO 29110">ISO/IEC 29110</option>'
        '<option value="ISO 9001">ISO 9001</option>'
        '<option value="ISO 12207">ISO/IEC/IEEE 12207</option>'
        '<option value="ISO 25010">ISO/IEC 25010</option>'
        '<option value="ISO 27001">ISO/IEC 27001</option>'
        '<option value="ISO 27002">ISO/IEC 27002</option>'
        '<option value="ISO 27701">ISO/IEC 27701</option>'
        '<option value="CMMI-DEV">CMMI-DEV</option>'
        '<option value="MOPROSOFT">MOPROSOFT</option>'
        '<option value="MAAGTICSI">MAAGTICSI</option>'
        '<option value="NIST CSF">NIST CSF</option>'
        '<option value="NIST SSDF">NIST SSDF</option>'
        '<option value="OWASP SAMM">OWASP SAMM</option>'
        '<option value="PCI DSS">PCI DSS</option>'
        '<option value="SOC 2">SOC 2</option>'
        '<option value="GDPR">GDPR</option>'
        '<option value="HIPAA">HIPAA</option>'
        '<option value="NINGUNO">NINGUNO / NONE (exclusivo)</option>'
        '<option value="__OTHER__">Otro / Other...</option>'
        '</select>'
        '<small class="var-help" id="vf-compliance-help"><span class="fw-lang-es">Selecciona uno o varios con Ctrl/Cmd. “NINGUNO” es exclusivo. Usa “Otro” para valores adicionales.</span><span class="fw-lang-en">Select one or more with Ctrl/Cmd. “NONE” is exclusive. Use “Other” for additional values.</span></small>'
        '<input id="vf-compliance-other" class="var-other-input" type="text" hidden placeholder="Otro estándar o regulación" oninput="syncProjectFromPanel();updateVarsBadge();">'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[ESTÁNDAR/COMPLIANCE]</span><span class="fw-lang-en">[STANDARD/COMPLIANCE]</span></span>'
        '</div>'
        '</div>\n'

        # documentos a revisar
        '    <div class="var-group" data-field="documentos">'
        '<label for="vf-documentos"><span class="fw-lang-es">Documentos a revisar</span><span class="fw-lang-en">Documents to review</span></label>'
        '<textarea id="vf-documentos" rows="3" placeholder="README.md, docs/, ADR o rutas concretas" oninput="syncProjectFromPanel();updateVarsBadge();"></textarea>'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[DOCUMENTOS A REVISAR]</span><span class="fw-lang-en">[DOCUMENTS TO REVIEW]</span></span>'
        '</div>'
        '</div>\n'

        # nivel de profundidad
        '    <div class="var-group" data-field="profundidad">'
        '<label for="vf-profundidad"><span class="fw-lang-es">Nivel de profundidad</span><span class="fw-lang-en">Depth level</span></label>'
        '<select id="vf-profundidad" onchange="syncProjectFromPanel();updateVarsBadge();">'
        '<option value="">— Seleccionar —</option>'
        '<option value="bajo">Bajo / Low</option>'
        '<option value="medio">Medio / Medium</option>'
        '<option value="alto">Alto / High</option>'
        '<option value="exhaustivo">Exhaustivo / Exhaustive</option>'
        '<option value="forense">Forense / Forensic</option>'
        '</select>'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[NIVEL DE PROFUNDIDAD] reemplaza [NIVEL]</span><span class="fw-lang-en">[DEPTH LEVEL] replaces [LEVEL]</span></span>'
        '</div>'
        '</div>\n'

        # variables adicionales
        '    <div class="var-group" data-field="adicionales">'
        '<label for="vf-adicionales"><span class="fw-lang-es">Variables adicionales</span><span class="fw-lang-en">Additional variables</span></label>'
        '<textarea id="vf-adicionales" rows="5" placeholder="TOKEN=valor&#10;OTRO TOKEN=otro valor" oninput="syncProjectFromPanel();updateVarsBadge();"></textarea>'
        '<small style="display:block;margin-top:.35rem;color:var(--tx3);font-size:.64rem;line-height:1.4;">'
        '<span class="fw-lang-es">Una por línea. Permite completar placeholders específicos que no aparecen en los campos anteriores.</span>'
        '<span class="fw-lang-en">One per line. Completes prompt-specific placeholders not covered by the fields above.</span>'
        '</small>'
        '</div>\n'

        # rama actual
        '    <div class="var-group" data-field="rama_actual">'
        '<label for="vf-rama-actual"><span class="fw-lang-es">Rama actual / con cambios</span><span class="fw-lang-en">Current / working branch</span></label>'
        '<input id="vf-rama-actual" type="text" placeholder="" oninput="syncProjectFromPanel();updateVarsBadge();">'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[RAMA ACTUAL]</span><span class="fw-lang-en">[CURRENT BRANCH]</span></span>'
        '<span class="var-tag"><span class="fw-lang-es">[RAMA CON LOS CAMBIOS]</span><span class="fw-lang-en">[BRANCH WITH CHANGES]</span></span>'
        '<span class="var-tag"><span class="fw-lang-es">[RAMA EN PRUEBAS]</span><span class="fw-lang-en">[BRANCH IN TEST]</span></span>'
        '</div>'
        '</div>\n'

        # rama destino
        '    <div class="var-group" data-field="rama_destino">'
        '<label for="vf-rama-destino"><span class="fw-lang-es">Rama destino / principal</span><span class="fw-lang-en">Target / main branch</span></label>'
        '<input id="vf-rama-destino" type="text" placeholder="" oninput="syncProjectFromPanel();updateVarsBadge();">'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[RAMA OBJETIVO]</span><span class="fw-lang-en">[TARGET BRANCH]</span></span>'
        '<span class="var-tag"><span class="fw-lang-es">[RAMA PRINCIPAL]</span><span class="fw-lang-en">[MAIN BRANCH]</span></span>'
        '<span class="var-tag"><span class="fw-lang-es">[RAMA INTEGRADA]</span><span class="fw-lang-en">[INTEGRATED BRANCH]</span></span>'
        '<span class="var-tag"><span class="fw-lang-es">[RAMA DESTINO]</span><span class="fw-lang-en">[TARGET BRANCH]</span></span>'
        '</div>'
        '</div>\n'

        # ambiente
        '    <div class="var-group" data-field="ambiente">'
        '<label for="vf-ambiente"><span class="fw-lang-es">Ambiente</span><span class="fw-lang-en">Environment</span></label>'
        '<select id="vf-ambiente" onchange="syncProjectFromPanel();updateVarsBadge();">'  
        '<option value="">-- seleccionar --</option>'
        '<option>DEV</option>'
        '<option>QA</option>'
        '<option>STAGING</option>'
        '<option>PROD</option>'
        '</select>'
        '<div class="var-tags">'
        '<span class="var-tag">[DEV / QA / PROD]</span>'
        '<span class="var-tag">[QA / STAGING]</span>'
        '<span class="var-tag"><span class="fw-lang-es">[URL DEL AMBIENTE]</span><span class="fw-lang-en">[ENVIRONMENT URL]</span></span>'
        '</div>'
        '</div>\n'

        # componentes
        '    <div class="var-group" data-field="componentes">'
        '<label for="vf-componentes"><span class="fw-lang-es">Componentes / archivos</span><span class="fw-lang-en">Components / file paths</span></label>'
        '<textarea id="vf-componentes" placeholder="" oninput="syncProjectFromPanel();updateVarsBadge();"></textarea>'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[COMPONENTES INVOLUCRADOS]</span><span class="fw-lang-en">[INVOLVED COMPONENTS]</span></span>'
        '<span class="var-tag"><span class="fw-lang-es">[COMPONENTES MODIFICADOS]</span><span class="fw-lang-en">[MODIFIED COMPONENTS]</span></span>'
        '<span class="var-tag"><span class="fw-lang-es">[RUTAS DE ARCHIVOS...]</span><span class="fw-lang-en">[FILE PATHS...]</span></span>'
        '</div>'
        '</div>\n'

        # módulo / proceso
        '    <div class="var-group" data-field="modulo">'
        '<label for="vf-modulo"><span class="fw-lang-es">Módulo / proceso / indicación</span><span class="fw-lang-en">Module / process / indication</span></label>'
        '<input id="vf-modulo" type="text" placeholder="" oninput="syncProjectFromPanel();updateVarsBadge();">'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[NOMBRE DEL PROCESO]</span><span class="fw-lang-en">[PROCESS NAME]</span></span>'
        '<span class="var-tag"><span class="fw-lang-es">[MODULO]</span><span class="fw-lang-en">[MODULE]</span></span>'
        '</div>'
        '</div>\n'

        # separador visual sección IA / agentes
        '    <div style="margin:.2rem 0 .1rem;font-size:.6rem;font-weight:700;color:var(--tx3);'
        'text-transform:uppercase;letter-spacing:.1em;border-top:1px solid var(--bdr);padding-top:.65rem;">'
        '⚙ <span class="fw-lang-es">Stack &amp; Agentes IA</span><span class="fw-lang-en">Stack &amp; AI Agents</span></div>\n'

        # stack tecnológico
        '    <div class="var-group" data-field="stack">'
        '<label for="vf-stack"><span class="fw-lang-es">Stack tecnológico</span><span class="fw-lang-en">Tech stack</span></label>'
        '<input id="vf-stack" type="text" placeholder="" oninput="syncProjectFromPanel();updateVarsBadge();">'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[STACK]</span><span class="fw-lang-en">[STACK]</span></span>'
        '<span class="var-tag"><span class="fw-lang-es">[STACK TECNOLÓGICO]</span><span class="fw-lang-en">[TECH STACK]</span></span>'
        '</div>'
        '</div>\n'

        # tipo de proyecto
        '    <div class="var-group" data-field="tipo_proyecto">'
        '<label for="vf-tipo-proyecto"><span class="fw-lang-es">Tipo de proyecto</span><span class="fw-lang-en">Project type</span></label>'
        '<select id="vf-tipo-proyecto" onchange="syncProjectFromPanel();updateVarsBadge();">'
        '<option value="">-- seleccionar --</option>'
        '<option>frontend SPA</option>'
        '<option>API REST</option>'
        '<option>full-stack</option>'
        '<option>microservicio</option>'
        '<option>monorepo</option>'
        '<option>librería</option>'
        '<option>data science</option>'
        '<option>IaC</option>'
        '<option>otro</option>'
        '</select>'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[TIPO DE PROYECTO]</span><span class="fw-lang-en">[PROJECT TYPE]</span></span>'
        '</div>'
        '</div>\n'

        # metodología
        '    <div class="var-group" data-field="metodologia">'
        '<label for="vf-metodologia"><span class="fw-lang-es">Metodologías / proceso / branching</span><span class="fw-lang-en">Methodologies / process / branching</span></label>'
        '<select id="vf-metodologia" multiple data-other-input="vf-metodologia-other" aria-describedby="vf-metodologia-help" onchange="syncMultiSelectOther(\'vf-metodologia\')">'
        '<option value="Scrum">Scrum</option>'
        '<option value="Kanban">Kanban</option>'
        '<option value="RUP">RUP</option>'
        '<option value="Cascada">Cascada / Waterfall</option>'
        '<option value="Espiral">Espiral / Spiral</option>'
        '<option value="XP">XP</option>'
        '<option value="Lean">Lean</option>'
        '<option value="SAFe">SAFe</option>'
        '<option value="DevOps">DevOps</option>'
        '<option value="DevSecOps">DevSecOps</option>'
        '<option value="Trunk-Based Development">Trunk-Based Development</option>'
        '<option value="GitHub Flow">GitHub Flow</option>'
        '<option value="GitFlow">GitFlow</option>'
        '<option value="__OTHER__">Otro / Other...</option>'
        '</select>'
        '<small class="var-help" id="vf-metodologia-help"><span class="fw-lang-es">Permite combinar metodología, proceso y estrategia de ramas.</span><span class="fw-lang-en">Allows combining methodology, process and branching strategy.</span></small>'
        '<input id="vf-metodologia-other" class="var-other-input" type="text" hidden placeholder="Otra metodología o proceso" oninput="syncProjectFromPanel();updateVarsBadge();">'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[METODOLOGÍA]</span><span class="fw-lang-en">[METHODOLOGY]</span></span>'
        '<span class="var-tag"><span class="fw-lang-es">[BRANCHING STRATEGY]</span><span class="fw-lang-en">[BRANCHING STRATEGY]</span></span>'
        '</div>'
        '</div>\n'

        # agentes IA activos
        '    <div class="var-group" data-field="agentes">'
        '<label for="vf-agentes"><span class="fw-lang-es">Agentes IA activos</span><span class="fw-lang-en">Active AI agents</span></label>'
        '<input id="vf-agentes" type="text" placeholder="" oninput="syncProjectFromPanel();updateVarsBadge();">'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[LISTA DE AGENTES]</span><span class="fw-lang-en">[AGENT LIST]</span></span>'
        '<span class="var-tag"><span class="fw-lang-es">[AGENTES A CONFIGURAR]</span><span class="fw-lang-en">[AGENTS TO CONFIGURE]</span></span>'
        '</div>'
        '</div>\n'

        # nivel de autonomía
        '    <div class="var-group" data-field="autonomia">'
        '<label for="vf-autonomia"><span class="fw-lang-es">Nivel de autonomía IA</span><span class="fw-lang-en">AI autonomy level</span></label>'
        '<select id="vf-autonomia" onchange="syncProjectFromPanel();updateVarsBadge();">'
        '<option value="">-- seleccionar --</option>'
        '<option>solo análisis</option>'
        '<option>análisis + propuesta</option>'
        '<option>ejecución controlada</option>'
        '<option>ejecución autónoma</option>'
        '</select>'
        '<div class="var-tags">'
        '<span class="var-tag"><span class="fw-lang-es">[NIVEL DE AUTONOMÍA]</span><span class="fw-lang-en">[AUTONOMY LEVEL]</span></span>'
        '</div>'
        '</div>\n'

        '  </div>\n'  # end var-panel-body  # end var-panel-body
        '  <div class="var-panel-footer">'
        '<button class="var-apply-btn" id="var-apply-btn" onclick="closeVarPanel(); flash(this)"><span class="fw-lang-es">&#10003; Listo</span><span class="fw-lang-en">&#10003; Done</span></button>'
        '<button class="var-clear-btn" onclick="clearVars()"><span class="fw-lang-es">Limpiar</span><span class="fw-lang-en">Clear</span></button>'
        '</div>\n'
        '</div>\n'

        # ── Barra flotante multi-select ──
        '<div class="ms-bar" id="ms-bar">\n'
        '  <span class="ms-count"><strong id="ms-sel-count">0</strong> <span class="fw-lang-es">seleccionados</span><span class="fw-lang-en">selected</span></span>\n'
        '  <button class="ms-copy-btn" onclick="copySelected(this)">'
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>'
        '</svg> <span class="fw-lang-es">Copiar seleccionados</span><span class="fw-lang-en">Copy selected</span></button>\n'
        '  <button class="ms-clear-btn" onclick="clearSelection()"><span class="fw-lang-es">Limpiar selecci\u00f3n</span><span class="fw-lang-en">Clear selection</span></button>\n'
        '</div>\n'

        # ── Modal de información ⓘ ──
        '<div class="modal-overlay" id="info-modal">\n'
        '  <div class="modal-box">\n'
        '    <div class="modal-hdr">\n'
        '      <span class="modal-hdr-icon">'
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="1.8">'
        '<circle cx="12" cy="12" r="10"/>'
        '<path stroke-linecap="round" d="M12 16v-4m0-4h.01"/>'
        '</svg></span>\n'
        '      <h2 id="modal-title"></h2>\n'
        '      <button class="modal-close-btn" onclick="closeInfo()">&#x2715;</button>\n'
        '    </div>\n'
        '    <div class="modal-body">\n'
        '      <div class="modal-section" id="modal-desc-section">'
        '<h3>Descripci\u00f3n y cu\u00e1ndo usarlo</h3>'
        '<p class="modal-desc" id="modal-desc"></p>'
        '</div>\n'
        '      <div id="modal-formulas"></div>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>\n'

        # ── Modal de proyectos ──
        '<div id="proj-modal" onclick="if(event.target===this)closeProjectsModal()">\n'
        '  <div class="proj-modal-box">\n'
        '    <div class="modal-hdr">\n'
        '      <h2><span class="fw-lang-es">Gesti\u00f3n de Proyectos</span><span class="fw-lang-en">Project Management</span></h2>\n'
        '      <button class="modal-close-btn" onclick="closeProjectsModal()">&#x2715;</button>\n'
        '    </div>\n'
        '    <ul class="proj-list" id="proj-modal-list"></ul>\n'
        '    <button class="proj-add-btn"'
        ' onclick="createProject();renderProjectsModal();renderProjectSelector();syncPanelToProject();">'
        '<span class="fw-lang-es">+ Nuevo proyecto</span><span class="fw-lang-en">+ New project</span></button>\n'
        '  </div>\n'
        '</div>\n'

        # ── Onboarding modal (UX-01) ──
        '<div class="ob-overlay hidden" id="ob-overlay">\n'
        '  <div class="ob-box">\n'
        '    <div class="ob-header">\n'
        '      <div class="ob-header-text">\n'
        '        <h2 class="fw-lang-es">Bienvenido a AI-SDLC Pro</h2>\n'
        '        <h2 class="fw-lang-en">Welcome to AI-SDLC Pro</h2>\n'
        '        <p class="fw-lang-es">3 cosas clave antes de copiar tu primer prompt.</p>\n'
        '        <p class="fw-lang-en">3 key things before copying your first prompt.</p>\n'
        '      </div>\n'
        '      <button class="ob-close" onclick="closeOnboarding(false)" title="Cerrar / Close">&#x2715;</button>\n'
        '    </div>\n'
        '    <div class="ob-steps">\n'
        '      <div class="ob-step active" id="ob-step-0">\n'
        '        <div class="ob-step-badge"><span class="ob-step-badge-dot">1</span>\u00a0<span class="fw-lang-es">El framework va primero</span><span class="fw-lang-en">Framework goes first</span></div>\n'
        '        <h3 class="fw-lang-es">El sistema antepone el framework autom\u00e1ticamente</h3>\n'
        '        <h3 class="fw-lang-en">The system prepends the framework automatically</h3>\n'
        '        <p class="fw-lang-es">No tienes que copiarlo a mano. Cada vez que presiones'
        ' <span class="ob-highlight">Copiar</span> en cualquier prompt,'
        ' el bloque de framework se antepone solo con tu contexto incluido.</p>\n'
        '        <p class="fw-lang-en">You don\'t have to copy it manually. Every time you press'
        ' <span class="ob-highlight">Copy</span> on any prompt,'
        ' the framework block is prepended automatically with your context included.</p>\n'
        '        <div class="ob-tip fw-lang-es">&#9888; El banner amarillo <strong>\u201c&#9888; Obligatorio\u201d</strong>'
        ' al inicio contiene ese bloque. Ya est\u00e1 incluido en cada copia \u2014 no tienes que pegarlo manualmente.</div>\n'
        '        <div class="ob-tip fw-lang-en">&#9888; The yellow <strong>\u201c&#9888; Required\u201d</strong> banner'
        ' at the beginning contains this block. It is already included in every copy \u2014 you don\'t need to paste it manually.</div>\n'
        '      </div>\n'
        '      <div class="ob-step" id="ob-step-1">\n'
        '        <div class="ob-step-badge"><span class="ob-step-badge-dot">2</span>\u00a0<span class="fw-lang-es">Configura tus variables</span><span class="fw-lang-en">Configure your variables</span></div>\n'
        '        <h3 class="fw-lang-es">Rellena el contexto de tu proyecto antes de copiar</h3>\n'
        '        <h3 class="fw-lang-en">Fill in your project context before copying</h3>\n'
        '        <p class="fw-lang-es">El bot\u00f3n <span class="ob-highlight">Variables</span> (barra superior)'
        ' abre un panel donde escribes: repositorio, rama, issue, ambiente, stack y agentes IA activos.'
        '<br><br>Esas variables reemplazan los <span class="ob-highlight">[PLACEHOLDER]</span>'
        ' autom\u00e1ticamente en cada prompt copiado \u2014 sin edici\u00f3n manual.</p>\n'
        '      </div>\n'
        '      <div class="ob-step" id="ob-step-2">\n'
        '        <div class="ob-step-badge"><span class="ob-step-badge-dot">3</span>\u00a0Sigue el orden del ciclo</div>\n'
        '        <h3>Los prompts siguen el ciclo de ingenier\u00eda de software</h3>\n'
        '        <p>El sidebar izquierdo lista las secciones en orden:\n'
        '<br><br><strong>01</strong> Comprensi\u00f3n \u2192 <strong>02</strong> An\u00e1lisis'
        ' \u2192 <strong>04</strong> Dise\u00f1o \u2192 <strong>05</strong> Plan'
        ' \u2192 <strong>06</strong> Ejecuci\u00f3n \u2192 <strong>07</strong> Pruebas'
        ' \u2192 <strong>09</strong> CI/CD \u2192 <strong>10</strong> Documentaci\u00f3n'
        '<br><br>El bot\u00f3n <span class="ob-highlight">&#9432;</span>'
        ' en cada card explica cu\u00e1ndo y c\u00f3mo usar ese prompt.</p>\n'
        '      </div>\n'
        '      <div class="ob-step" id="ob-step-3">\n'
        '        <div class="ob-step-badge"><span class="ob-step-badge-dot">4</span>\u00a0Rec\u00edbe nuevos prompts gratis</div>\n'
        '        <h3>Mantente al tanto de cada actualizaci\u00f3n</h3>\n'
        '        <p>Cada mes publicamos nuevos prompts y mejoras al framework.\n'
        'D\u00e9janos tu email y ser\u00e1s el primero en saber.</p>\n'
        '        <form class="ob-email-form" onsubmit="submitObEmail();return false;">\n'
        '          <label for="ob-email-input">Correo electr\u00f3nico</label>\n'
        '          <input class="ob-email-input" id="ob-email-input" type="email"'
        ' placeholder="tu@correo.com" autocomplete="email" required>\n'
        '          <button class="ob-email-submit" id="ob-email-submit-btn" type="submit">\n'
        '            \u2709\ufe0f Recibir nuevos prompts gratis\n'
        '          </button>\n'
        '        </form>\n'
        '        <p class="ob-email-note">Sin spam. Cancelar en cualquier momento.</p>\n'
        '      </div>\n'
        '    </div>\n'
        '    <div class="ob-progress">\n'
        '      <div class="ob-dot on" id="ob-dot-0"></div>\n'
        '      <div class="ob-dot" id="ob-dot-1"></div>\n'
        '      <div class="ob-dot" id="ob-dot-2"></div>\n'
        '      <div class="ob-dot" id="ob-dot-3"></div>\n'
        '    </div>\n'
        '    <div class="ob-footer">\n'
        '      <button class="ob-skip" onclick="closeOnboarding(true)">No volver a mostrar</button>\n'
        '      <div class="ob-nav">\n'
        '        <button class="ob-prev" id="ob-prev-btn" onclick="obPrev()" style="display:none">&#8249; Anterior</button>\n'
        '        <button class="ob-next" id="ob-next-btn" onclick="obNext()">Siguiente &#8250;</button>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>\n'

        '</div>\n'  # close #app-root

        '<script>' + prompt_info_js + '\n' + JS + LANDING_JS + '</script>\n'
        '<!-- ═══ BOTTOM RIGHT FLOATING CONTROLS ═══ -->\n'
        '<div class="bottom-right-floats">\n'
        '<!-- ═══ FLOATING VARIABLES QUICK ACCESS ═══ -->\n'
        '<div class="var-float" id="var-float">\n'
        '  <div class="var-float-dropdown" id="var-float-dropdown">\n'
        '    <div class="var-float-hdr">\n'
        '      <div>\n'
        '        <div class="var-float-title">Variables rápidas</div>\n'
        '        <div class="var-float-sub">Edita el contexto más usado sin perder el scroll.</div>\n'
        '      </div>\n'
        '      <button class="var-float-close" onclick="closeVarFloat()" title="Cerrar">&#x2715;</button>\n'
        '    </div>\n'
        '    <div class="var-float-form">\n'
        '      <div class="var-group">\n'
        '        <label for="qv-repositorio">Repositorio</label>\n'
        '        <input id="qv-repositorio" type="text" placeholder="org/nombre-repo o URL" oninput="syncProjectFromQuickFloat()">\n'
        '      </div>\n'
        '      <div class="var-group">\n'
        '        <label for="qv-referencia">Issue / Referencia</label>\n'
        '        <textarea id="qv-referencia" placeholder="Número, URL o resumen corto" oninput="syncProjectFromQuickFloat()"></textarea>\n'
        '      </div>\n'
        '      <div class="var-group">\n'
        '        <label for="qv-rama-actual">Rama actual</label>\n'
        '        <input id="qv-rama-actual" type="text" placeholder="feature/mi-rama" oninput="syncProjectFromQuickFloat()">\n'
        '      </div>\n'
        '      <div class="var-group">\n'
        '        <label for="qv-rama-destino">Rama destino</label>\n'
        '        <input id="qv-rama-destino" type="text" placeholder="main / develop" oninput="syncProjectFromQuickFloat()">\n'
        '      </div>\n'
        '      <div class="var-group">\n'
        '        <label for="qv-modulo">Módulo / proceso</label>\n'
        '        <input id="qv-modulo" type="text" placeholder="Nombre del módulo o funcionalidad" oninput="syncProjectFromQuickFloat()">\n'
        '      </div>\n'
        '    </div>\n'
        '    <div class="var-float-actions">\n'
        '      <button class="var-float-link" onclick="openFullVarPanelFromFloat()">Más variables</button>\n'
        '      <button class="var-float-primary" onclick="closeVarFloat(); flash(this)">Listo</button>\n'
        '    </div>\n'
        '  </div>\n'
        '  <button class="var-float-btn" id="var-float-btn" onclick="toggleVarFloat(event)" title="Editar variables activas">\n'
        '    <span class="var-float-icon">\n'
        '      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>\n'
        '    </span>\n'
        '    <span class="var-float-label">Vars</span>\n'
        '    <span class="var-float-count empty" id="var-float-count">0/12</span>\n'
        '    <span class="var-float-chevron"><svg width="9" height="9" viewBox="0 0 10 10" fill="none"><path d="M2.5 3.5L5 6 7.5 3.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>\n'
        '  </button>\n'
        '</div>\n'
        '<!-- ═══ FLOATING MULTI-SELECT TOGGLE ═══ -->\n'
        '<div class="ms-float" id="ms-float">\n'
        '  <button class="ms-float-btn" id="ms-float-btn" onclick="toggleMsMode()" title="Activar selección múltiple">\n'
        '    <span class="ms-float-icon">\n'
        '      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">\n'
        '        <rect x="3" y="5" width="13" height="13" rx="2"/><path d="M8 10l3 3 5-5"/>\n'
        '      </svg>\n'
        '    </span>\n'
        '    <span class="ms-float-label">Multi-select</span>\n'
        '  </button>\n'
        '</div>\n'
        '<!-- \u2550\u2550 FLOATING PROJECT SELECTOR \u2014 issue #30 \u2550\u2550 -->\n'
        '<div class="proj-float" id="proj-float">\n'
        '  <div class="proj-float-dropdown" id="proj-float-dropdown"></div>\n'
        '  <button class="proj-float-btn" id="proj-float-btn" onclick="toggleProjFloat(event)" title="Cambiar proyecto activo">\n'
        '    <span class="proj-float-dot"></span>\n'
        '    <span class="proj-float-name" id="proj-float-name">Proyecto</span>\n'
        '    <span class="proj-float-chevron"><svg width="9" height="9" viewBox="0 0 10 10" fill="none"><path d="M2.5 3.5L5 6 7.5 3.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>\n'
        '  </button>\n'
        '</div>\n'
        '</div>\n'
        '<!-- ═══ END BOTTOM RIGHT FLOATS ═══ -->\n'
        '<div id="toast-container"></div>\n'
        '</body>\n</html>\n'
    )

    OUTPUT_FILE.write_text(html, encoding="utf-8")
    size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f"OK  -> {OUTPUT_FILE.name}")
    print(f"Secciones : {len(sections)}")
    print(f"Prompts   : {total}")
    print(f"Framework : incluido")
    print(f"Tamano    : {size_kb:.1f} KB")


if __name__ == "__main__":
    build()
