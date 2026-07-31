#!/usr/bin/env python3
"""
build_gumroad_pack.py -- Empaqueta el catálogo completo de prompts en un
.zip listo para subir a Gumroad (issue #9, "Pack completo unico" -- canal de
adquisicion, "pay what you want" sugerido $5 USD; el precio fijo de $499 MXN
quedo obsoleto al bajar la suscripcion a $1 USD/mes,
ver docs/STRATEGY.md "Canal alternativo -- Producto digital").

No publica nada por su cuenta -- Gumroad no tiene API pública de creación de
producto sin credenciales de la cuenta del propietario, así que este script
solo prepara el .zip y deja la publicación manual (ver docs/gumroad-listing.md
para el texto del listado). Reutiliza el mismo filtro de prompts "reales" que
count_prompts() en build.py, para que el pack nunca incluya nada deprecado,
vacío o de una sección no reconocida.

Uso: python3 build_gumroad_pack.py
Salida: dist/ai-sdlc-pro-pack-completo.zip (dist/ está en .gitignore --
esto es intencional: es una "versión del día", no un artefacto versionado).
"""
import zipfile
from datetime import date
from pathlib import Path

from build import PROMPTS_DIR, SECTION_META, _is_deprecated_or_empty

DIST_DIR = Path(__file__).parent / "dist"
OUTPUT_ZIP = DIST_DIR / "ai-sdlc-pro-pack-completo.zip"


def _valid_prompt_ids():
    """Mismo filtro que count_prompts(): sin traducciones, sin el framework
    base (se empaqueta aparte), sin vacíos/deprecados, sin secciones no
    reconocidas. Orden natural por nombre de archivo (prefijo numérico de
    sección ya garantiza el orden curado del framework)."""
    ids = []
    for f in sorted(PROMPTS_DIR.glob("*.md")):
        if f.name.endswith(".en.md") or f.name == "00-framework.md":
            continue
        if _is_deprecated_or_empty(f.read_text(encoding="utf-8")):
            continue
        if f.stem.split("-")[0] not in SECTION_META:
            continue
        ids.append(f.stem)
    return ids


def _readme(lang, prompt_count):
    today = date.today().isoformat()
    if lang == "es":
        return f"""# AI-SDLC Pro — Pack completo de prompts

Versión del día: {today} · {prompt_count} prompts (ES + EN) + framework de contexto multi-agente
LionSystems © 2026 — https://prompts.lionsystems.com.mx

## Qué es esto

Este pack contiene el mismo catálogo que ya está disponible gratis en
{"https://prompts.lionsystems.com.mx"} — pagar por este pack no compra
contenido exclusivo, compra una **copia offline organizada** de todo el
catálogo para trabajar sin conexión, integrarla a tus propias herramientas,
o simplemente apoyar el proyecto. La app web sigue siendo la forma
recomendada de usarlos día a día: resuelve las 19 variables por proyecto
automáticamente y siempre tiene la versión más reciente.

## Si te sirvió, esto es lo que sigue

Los {prompt_count} prompts son gratis para siempre, aquí y en la web: no hay
muro que desbloquear para leerlos ni para copiarlos.

Lo que sí cuesta es la **plataforma**, por **$1 USD al mes**:

- Resuelve las 19 variables de tu proyecto automáticamente en cada prompt,
  en vez de reemplazar placeholders a mano.
- Proyectos ilimitados, cada uno con su propio contexto y checklist de avance.
- Guarda los resultados que te devuelve la IA, ligados al prompt que los generó.
- Modo guiado: te dice cuál es el siguiente prompt según dónde vas.

Se cancela cuando quieras y hay 14 días de reembolso sin preguntas:
{"https://prompts.lionsystems.com.mx/precios.html"}

## Estructura

- `es/` — los {prompt_count} prompts en español, un archivo `.md` por prompt.
- `en/` — los mismos {prompt_count} prompts en inglés.
- `framework/` — el framework de contexto multi-agente (`00-framework.md` /
  `.en.md`) que se antepone a cualquier prompt del catálogo para dirigir
  agentes IA (GitHub Copilot, Claude, Cursor, Windsurf, Codex, Antigravity)
  con el contexto completo del ciclo de ingeniería de software.

## Cómo usar un prompt

1. Abre el archivo `.md` del prompt que necesitas.
2. Reemplaza cada placeholder entre corchetes (ej. `[NOMBRE DEL SERVICIO]`,
   `[STACK TECNOLÓGICO]`) con los valores reales de tu proyecto.
3. Pega el resultado (opcionalmente precedido del framework de
   `framework/00-framework.md`) en tu agente de IA de preferencia.

Cada prompt en la app web resuelve estos placeholders automáticamente a
partir de 19 variables de proyecto reutilizables entre prompts -- si
prefieres esa experiencia en vez de reemplazo manual, la app sigue siendo
gratuita en {"https://prompts.lionsystems.com.mx"}.

## Licencia

Copyright (c) 2026 LionSystems. Este pack es para uso individual de quien lo
adquirió -- no redistribuir, revender ni republicar el contenido. Consultas
de licenciamiento: dleon555@live.com.mx
"""
    return f"""# AI-SDLC Pro — Complete Prompt Pack

Snapshot date: {today} · {prompt_count} prompts (ES + EN) + multi-agent context framework
LionSystems © 2026 — https://prompts.lionsystems.com.mx

## What this is

This pack contains the same catalog already available for free at
{"https://prompts.lionsystems.com.mx"} — paying for this pack does not buy
exclusive content, it buys an **organized offline copy** of the whole
catalog to work without a connection, wire it into your own tooling, or
simply support the project. The web app remains the recommended way to use
these day to day: it resolves the 19 per-project variables automatically and
always has the latest version.

## If this was useful, here's what's next

The {prompt_count} prompts are free forever, here and on the web: there is no
wall to unlock in order to read or copy them.

What does cost money is the **platform**, at **$1 USD per month**:

- Resolves your project's 19 variables automatically in every prompt, instead
  of replacing placeholders by hand.
- Unlimited projects, each with its own context and progress checklist.
- Saves the output your AI returns, linked to the prompt that produced it.
- Guided mode: tells you which prompt comes next based on where you are.

Cancel anytime, with a 14-day no-questions refund:
{"https://prompts.lionsystems.com.mx/precios.html"}

## Structure

- `es/` — all {prompt_count} prompts in Spanish, one `.md` file per prompt.
- `en/` — the same {prompt_count} prompts in English.
- `framework/` — the multi-agent context framework (`00-framework.md` /
  `.en.md`) prepended to any prompt in the catalog to steer AI agents
  (GitHub Copilot, Claude, Cursor, Windsurf, Codex, Antigravity) with full
  software-engineering-lifecycle context.

## How to use a prompt

1. Open the `.md` file for the prompt you need.
2. Replace every bracketed placeholder (e.g. `[SERVICE NAME]`,
   `[TECH STACK]`) with your project's real values.
3. Paste the result (optionally preceded by `framework/00-framework.md`)
   into your AI agent of choice.

Every prompt in the web app resolves these placeholders automatically from
19 reusable project variables -- if you'd rather have that experience than
manual replacement, the app is still free at
{"https://prompts.lionsystems.com.mx"}.

## License

Copyright (c) 2026 LionSystems. This pack is for the individual use of the
person who acquired it -- do not redistribute, resell, or republish the
content. Licensing inquiries: dleon555@live.com.mx
"""


def build_pack():
    ids = _valid_prompt_ids()
    if not ids:
        raise RuntimeError("No se encontraron prompts válidos -- revisa PROMPTS_DIR")

    DIST_DIR.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for pid in ids:
            es_file = PROMPTS_DIR / f"{pid}.md"
            en_file = PROMPTS_DIR / f"{pid}.en.md"
            zf.write(es_file, f"es/{pid}.md")
            if en_file.exists():
                zf.write(en_file, f"en/{pid}.en.md")

        fw_es = PROMPTS_DIR / "00-framework.md"
        fw_en = PROMPTS_DIR / "00-framework.en.md"
        if fw_es.exists():
            zf.write(fw_es, "framework/00-framework.md")
        if fw_en.exists():
            zf.write(fw_en, "framework/00-framework.en.md")

        zf.writestr("LEEME.md", _readme("es", len(ids)))
        zf.writestr("README.md", _readme("en", len(ids)))

    size_kb = OUTPUT_ZIP.stat().st_size / 1024
    print(f"OK  -> {OUTPUT_ZIP}")
    print(f"Prompts empaquetados: {len(ids)} (ES + EN) + framework")
    print(f"Tamaño: {size_kb:.1f} KB")


if __name__ == "__main__":
    build_pack()
