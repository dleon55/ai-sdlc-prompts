#!/usr/bin/env python3
"""Genera las «skills» (SKILL.md) de AI-SDLC Pro para Claude Code y Codex.

Lee `prompts-index.json` y `ai_sdlc_pro_prompts/*.md` y escribe en
`dist/skills/` el contenido completo del repo público `dleon55/ai-sdlc-skills`:

    README.md, LICENSE, scripts/validate_skills.py, scripts/install.sh
    .claude-plugin/marketplace.json
    plugins/ai-sdlc-es/.claude-plugin/plugin.json
    plugins/ai-sdlc-es/skills/<skill>/SKILL.md
    plugins/ai-sdlc-es/skills/<skill>/references/<id>.md   (+ 00-framework.md)
    plugins/ai-sdlc-en/...                                  (igual, en inglés)

Una skill por sección (fase), no por prompt: cada skill expone su
`description` al agente todo el tiempo; 224 skills competirían por activarse.
Los prompts van como `references/` y se cargan sólo cuando hacen falta.

Sólo se publica el cuerpo CC BY 4.0 de LICENSE §1 (los prompts). Nada del
código de la plataforma (§3, propietario) entra en la salida; este mismo
generador es plataforma y NO se copia al repo público.

El generador es determinista (sin fechas ni rutas absolutas) y falla si un
prompt del índice queda fuera, se duplica o le falta su archivo.

Uso:
    python tools/build_skills.py [--out dist/skills]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PROMPTS_DIR = RAIZ / "ai_sdlc_pro_prompts"
INDEX = RAIZ / "prompts-index.json"
TEMPLATES = Path(__file__).resolve().parent / "skills_templates"

SKILLS_VERSION = "1.0.0"
REPO_PUBLICO = "dleon55/ai-sdlc-skills"
MARKETPLACE_NAME = "ai-sdlc-skills"
SITE = "https://prompts.lionsystems.com.mx"
UTM = "utm_source=github&utm_medium=skills&utm_campaign=ai-sdlc-skills"
PRECIOS_URL = f"{SITE}/precios.html?{UTM}"
SITE_URL = f"{SITE}/?{UTM}"
LANGS = ("es", "en")

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DESC_MAX = 1024

# Sección -> (slug, etiqueta, disparadores «Úsala cuando…») por idioma.
# Los disparadores se escriben a mano: una descripción demasiado amplia
# activa la skill equivocada (spec E2 §6).
SECCIONES: dict[str, dict[str, tuple[str, str, str]]] = {
    "00": {
        "es": ("sdlc-fundamentos", "Fundamentos del proyecto y gobernanza de agentes",
               "Úsala al arrancar un proyecto o un repositorio nuevo: acta (project charter), caso de negocio, stack y arquitectura inicial, plan de trabajo, registro de riesgos, estructura del repositorio, configuración de GitHub, gobernanza de agentes de IA, metodología, calidad de código, o redactar un issue y un plan para que lo ejecute un agente."),
        "en": ("sdlc-foundations", "Project foundations and agent governance",
               "Use it when starting a project or a new repository: project charter, business case, initial stack and architecture, work plan, risk register, repository scaffolding, GitHub configuration, AI agent governance, methodology, code-quality stack, or writing an issue and a plan for an AI agent to execute."),
    },
    "01": {
        "es": ("sdlc-comprension", "Comprensión del repositorio y de los procesos",
               "Úsala cuando haya que entender un repositorio o sistema existente antes de tocarlo: arranque y mapa del código, módulos, dependencias, flujos y procesos de negocio que implementa."),
        "en": ("sdlc-comprehension", "Repository and process comprehension",
               "Use it when you need to understand an existing repository or system before changing it: onboarding and code map, modules, dependencies, flows and the business processes it implements."),
    },
    "02": {
        "es": ("sdlc-analisis", "Análisis de requerimientos e issues",
               "Úsala cuando pidan analizar un issue, requerimiento o cambio: alcance funcional, análisis técnico, impacto cruzado, elicitación con interesados, requerimientos no funcionales, triage del backlog de GitHub o matriz de trazabilidad."),
        "en": ("sdlc-analysis", "Requirements and issue analysis",
               "Use it when asked to analyze an issue, requirement or change: functional scope, technical analysis, cross-impact, stakeholder elicitation, non-functional requirements, GitHub backlog triage or a traceability matrix."),
    },
    "03": {
        "es": ("sdlc-incidentes", "Incidentes y causa raíz",
               "Úsala cuando haya un bug, falla o incidente reportado en GitHub y se necesite investigarlo: reproducción, evidencia, análisis de causa raíz (RCA) y propuesta de corrección."),
        "en": ("sdlc-incidents", "Incidents and root cause",
               "Use it when there is a bug, failure or incident reported on GitHub that needs investigating: reproduction, evidence, root cause analysis (RCA) and a proposed fix."),
    },
    "04": {
        "es": ("sdlc-diseno", "Diseño de la solución",
               "Úsala cuando haya que diseñar antes de implementar: diseño de solución, diagramas Mermaid, casos de uso, ADR (decisiones de arquitectura), contrato de API, versionado y deprecación de API o modelo de datos."),
        "en": ("sdlc-design", "Solution design",
               "Use it when design is needed before implementation: solution design, Mermaid diagrams, use cases, ADRs (architecture decisions), API contract, API versioning and deprecation, or data model."),
    },
    "05": {
        "es": ("sdlc-planificacion", "Planificación de la implementación",
               "Úsala cuando haya que convertir un diseño aprobado en un plan de implementación por pasos o evaluar los riesgos de implementarlo."),
        "en": ("sdlc-planning", "Implementation planning",
               "Use it when an approved design must be turned into a step-by-step implementation plan or when assessing the risks of implementing it."),
    },
    "06": {
        "es": ("sdlc-implementacion", "Implementación y commits",
               "Úsala cuando toque implementar cambios con uno o varios agentes de IA, coordinar un programa multiagente o preparar commits limpios y convencionales."),
        "en": ("sdlc-implementation", "Implementation and commits",
               "Use it when implementing changes with one or more AI agents, coordinating a multi-agent program, or preparing clean conventional commits."),
    },
    "07": {
        "es": ("sdlc-pruebas", "Pruebas",
               "Úsala cuando pidan diseñar o implementar pruebas: unitarias, de integración, E2E, de humo, de rendimiento y carga, accesibilidad, diagnóstico de pruebas inestables (flaky), datos de prueba, detección del stack de pruebas o plan maestro de pruebas."),
        "en": ("sdlc-testing", "Testing",
               "Use it when asked to design or implement tests: unit, integration, E2E, smoke, performance and load, accessibility, flaky test diagnosis, test data, test stack detection or a master test plan."),
    },
    "08": {
        "es": ("sdlc-revision", "Revisión de código y PR",
               "Úsala cuando pidan revisar un pull request completo, un plan de remediación de hallazgos, perfilar consultas SQL o revisar una migración de esquema de base de datos."),
        "en": ("sdlc-review", "Code and PR review",
               "Use it when asked to review a full pull request, plan remediation of findings, profile SQL queries or review a database schema migration."),
    },
    "09": {
        "es": ("sdlc-integracion", "Integración y entrega continua",
               "Úsala cuando trabajes con CI/CD: workflows de GitHub Actions, checklist de promoción entre ambientes, estrategia de feature flags o coordinación de cambios incompatibles (breaking changes)."),
        "en": ("sdlc-integration", "Continuous integration and delivery",
               "Use it when working on CI/CD: GitHub Actions workflows, environment promotion checklist, feature flag strategy, or coordinating breaking changes."),
    },
    "10": {
        "es": ("sdlc-documentacion", "Documentación",
               "Úsala cuando haya que documentar: documentación técnica, memoria técnica del proyecto, notas de versión y CHANGELOG, observabilidad e instrumentación, documentación de API pública o materiales de capacitación para el despliegue."),
        "en": ("sdlc-documentation", "Documentation",
               "Use it when documentation is needed: technical docs, project technical record, release notes and CHANGELOG, observability and instrumentation, public API docs, or rollout training materials."),
    },
    "11": {
        "es": ("sdlc-operaciones", "Operaciones y SRE",
               "Úsala en operación de sistemas en producción: troubleshooting, hardening, deuda técnica, respuesta a incidentes, rendimiento en producción, parches, postmortem y runbooks, rollback, costos de nube (FinOps), capacidad, decomiso de legado, ruido de alertas, guardias, migración o cutover y recuperación ante desastres."),
        "en": ("sdlc-operations", "Operations and SRE",
               "Use it for operating production systems: troubleshooting, hardening, technical debt, incident response, production performance, patching, postmortems and runbooks, rollback, cloud cost (FinOps), capacity, legacy decommissioning, alert noise, on-call health, migration or cutover, and disaster recovery."),
    },
    "12": {
        "es": ("sdlc-orquestador", "Orquestador del ciclo completo",
               "Úsala cuando una asignación grande requiera coordinar varias fases, capacidades o agentes y haya que decidir el flujo mínimo suficiente; para una tarea simple usa directamente la skill de su fase."),
        "en": ("sdlc-orchestrator", "Full-cycle orchestrator",
               "Use it when a large assignment needs several phases, capabilities or agents coordinated and you must choose the minimum sufficient flow; for a simple task use the phase skill directly."),
    },
    "13": {
        "es": ("sdlc-seguridad", "Seguridad",
               "Úsala para trabajo de seguridad autorizado: SAST, análisis de dependencias (SCA), revisión de Secure SDLC, modelado de amenazas, DAST, pruebas de penetración con autorización, gestión de vulnerabilidades y CVE, gestión de secretos o evaluación de impacto de privacidad (DPIA)."),
        "en": ("sdlc-security", "Security",
               "Use it for authorized security work: SAST, dependency analysis (SCA), Secure SDLC review, threat modeling, DAST, authorized penetration testing, vulnerability and CVE management, secrets management, or data privacy impact assessment (DPIA)."),
    },
    "14": {
        "es": ("sdlc-monorepo-estandares", "Monorepo y estándares de calidad",
               "Úsala cuando trabajes un monorepo (workspaces y dependencias) o haya que medir calidad y cumplimiento con PSP/TSP, ISO o MoProSoft."),
        "en": ("sdlc-monorepo-standards", "Monorepo and quality standards",
               "Use it when working on a monorepo (workspaces and dependencies) or measuring quality and compliance with PSP/TSP, ISO or MoProSoft."),
    },
    "15": {
        "es": ("sdlc-negocio-qa", "Negocio y QA funcional",
               "Úsala cuando haya que redactar historias de usuario con Gherkin, casos de prueba manuales o analizar defectos desde el punto de vista del negocio."),
        "en": ("sdlc-business-qa", "Business and functional QA",
               "Use it when writing user stories with Gherkin, manual test cases, or analyzing defects from a business point of view."),
    },
    "16": {
        "es": ("sdlc-soporte", "Soporte y mesa de ayuda",
               "Úsala en soporte a usuarios: triage de tickets, diagnóstico y respuesta de un incidente de soporte, artículos de base de conocimiento, matriz de escalamiento y SLA, tendencias de tickets o auditoría de la base de conocimiento."),
        "en": ("sdlc-support", "Support and help desk",
               "Use it for user support: ticket triage, diagnosing and answering a support incident, knowledge base articles, escalation matrix and SLA, ticket trends, or knowledge base audits."),
    },
    "17": {
        "es": ("sdlc-backoffice-ingenieria", "Back office de ingeniería",
               "Úsala en gestión del equipo de ingeniería: onboarding y offboarding técnico, evaluación de herramientas y licencias, capacidad del equipo, renovación de proveedores, reporte de estado a interesados, revisión posterior al lanzamiento o retrospectiva de sprint."),
        "en": ("sdlc-engineering-backoffice", "Engineering back office",
               "Use it for engineering team management: technical onboarding and offboarding, tool and license evaluation, team capacity, vendor renewals, stakeholder status reports, post-launch review or sprint retrospective."),
    },
}

T = {
    "es": {
        "fase": "Fase AI-SDLC",
        "intro": "Esta skill agrupa los prompts de la fase **{label}** del marco AI-SDLC. Cada prompt está completo en `references/`.",
        "como": "## Cómo usarla",
        "pasos": [
            "Lee primero `references/00-framework.md`: es el contexto obligatorio que antecede a todo prompt.",
            "Elige en la lista de abajo el prompt que corresponde a la petición y abre sólo ese archivo de `references/`.",
            "Pide al usuario los valores de las variables entre corchetes (`[MODULO]`, `[PEGAR]`, …) que no puedas obtener del repositorio; no las inventes.",
            "Respeta la autonomía permitida y detente en cuanto se cumpla un criterio de detención: declara el hueco en lugar de suponer.",
            "Al terminar, sugiere el siguiente prompt recomendado.",
        ],
        "prompts": "## Prompts de esta fase",
        "archivo": "Archivo",
        "cuando": "Cuándo usarlo",
        "entradas": "Entradas",
        "autonomia": "Autonomía permitida",
        "detencion": "Detente si",
        "siguiente": "Siguiente",
        "en_skill": "skill",
        "atrib": "Adaptado al formato SKILL.md a partir de AI-SDLC Pro — {site} — CC BY 4.0. Planes: {precios}",
        "ref_footer": ("---\n\n*Fuente: AI-SDLC Pro ({site}), licencia CC BY 4.0. "
                       "Adaptado al formato SKILL.md: se añadió esta nota; el texto del prompt no cambió. "
                       "Versión con proyectos, variables persistentes y resultados por prompt: {precios}*\n"),
    },
    "en": {
        "fase": "AI-SDLC phase",
        "intro": "This skill groups the prompts of the **{label}** phase of the AI-SDLC framework. Each prompt is complete under `references/`.",
        "como": "## How to use it",
        "pasos": [
            "Read `references/00-framework.md` first: it is the mandatory context that precedes every prompt.",
            "Pick the prompt below that matches the request and open only that file from `references/`.",
            "Ask the user for the bracketed variables (`[MODULE]`, `[PASTE]`, …) you cannot obtain from the repository; do not invent them.",
            "Respect the permitted autonomy and stop as soon as a stop criterion is met: state the gap instead of assuming.",
            "When done, suggest the recommended next prompt.",
        ],
        "prompts": "## Prompts in this phase",
        "archivo": "File",
        "cuando": "When to use it",
        "entradas": "Inputs",
        "autonomia": "Permitted autonomy",
        "detencion": "Stop if",
        "siguiente": "Next",
        "en_skill": "skill",
        "atrib": "Adapted to the SKILL.md format from AI-SDLC Pro — {site} — CC BY 4.0. Plans: {precios}",
        "ref_footer": ("---\n\n*Source: AI-SDLC Pro ({site}), CC BY 4.0 license. "
                       "Adapted to the SKILL.md format: this note was added; the prompt text is unchanged. "
                       "Version with projects, persistent variables and per-prompt results: {precios}*\n"),
    },
}


class ErrorGeneracion(Exception):
    pass


def _archivo_prompt(pid: str, lang: str) -> Path:
    return PROMPTS_DIR / (f"{pid}.md" if lang == "es" else f"{pid}.en.md")


def _seccion_md(texto: str, encabezados: tuple[str, ...]) -> str:
    """Devuelve el cuerpo de la primera sección `## <encabezado>` encontrada."""
    lineas = texto.splitlines()
    dentro, out = False, []
    for ln in lineas:
        if ln.startswith("## "):
            if dentro:
                break
            dentro = ln[3:].strip() in encabezados
            continue
        if dentro:
            if ln.strip() == "---":
                break
            out.append(ln)
    return "\n".join(out).strip()


def _una_linea(s: str, maximo: int = 320) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= maximo:
        return s
    corte = s.rfind(". ", 0, maximo)
    return (s[: corte + 1] if corte > 80 else s[: maximo - 1].rstrip() + "…")


def cuando_usarlo(texto: str, lang: str) -> str:
    desc = _seccion_md(texto, ("Descripción", "Description"))
    marca = "**Cuándo usarlo:**" if lang == "es" else "**When to use it:**"
    for ln in desc.splitlines():
        if ln.strip().startswith(marca):
            return _una_linea(ln.strip()[len(marca):])
    primer_parrafo = desc.split("\n\n")[0] if desc else ""
    return _una_linea(primer_parrafo)


def _titulo(texto: str) -> str:
    for ln in texto.splitlines():
        if ln.startswith("# "):
            return ln[2:].strip()
    raise ErrorGeneracion("prompt sin título `# …`")


def _yaml_str(s: str) -> str:
    # Una cadena JSON es un escalar YAML entre comillas dobles válido.
    return json.dumps(s, ensure_ascii=False)


def cargar_indice() -> list[dict]:
    datos = json.loads(INDEX.read_text(encoding="utf-8"))["prompts"]
    vistos: set[str] = set()
    for p in datos:
        if p["id"] in vistos:
            raise ErrorGeneracion(f"id duplicado en el índice: {p['id']}")
        vistos.add(p["id"])
        if p["section"] not in SECCIONES:
            raise ErrorGeneracion(f"{p['id']}: sección {p['section']} sin skill asignada")
    return datos


def descripcion_skill(sec: str, lang: str, titulos: list[str]) -> str:
    slug, label, disparo = SECCIONES[sec][lang]
    pre = "Prompts AI-SDLC de" if lang == "es" else "AI-SDLC prompts for"
    desc = f"{pre} {label.lower() if lang == 'es' else label}. {disparo}"
    if len(desc) > DESC_MAX:
        raise ErrorGeneracion(f"{slug}: description de {len(desc)} > {DESC_MAX}")
    return desc


def generar(out: Path) -> dict:
    indice = cargar_indice()
    por_seccion: dict[str, list[dict]] = {}
    for p in indice:
        por_seccion.setdefault(p["section"], []).append(p)
    seccion_de = {p["id"]: p["section"] for p in indice}

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    resumen = {"skills": {}, "references": {}}

    for lang in LANGS:
        t = T[lang]
        plugin = f"ai-sdlc-{lang}"
        base = out / "plugins" / plugin
        framework = PROMPTS_DIR / ("00-framework.md" if lang == "es" else "00-framework.en.md")
        if not framework.exists():
            raise ErrorGeneracion(f"falta {framework.name}")
        footer = t["ref_footer"].format(site=SITE, precios=PRECIOS_URL)
        n_refs = 0
        for sec in sorted(SECCIONES):
            prompts = sorted(por_seccion.get(sec, []), key=lambda p: p["id"])
            if not prompts:
                raise ErrorGeneracion(f"sección {sec} sin prompts")
            slug, label, _ = SECCIONES[sec][lang]
            sdir = base / "skills" / slug
            rdir = sdir / "references"
            rdir.mkdir(parents=True)
            (rdir / "00-framework.md").write_text(
                framework.read_text(encoding="utf-8").rstrip("\n") + "\n\n" + footer, encoding="utf-8")

            bloques, titulos = [], []
            for p in prompts:
                f = _archivo_prompt(p["id"], lang)
                if not f.exists():
                    raise ErrorGeneracion(f"falta el archivo {f.name}")
                texto = f.read_text(encoding="utf-8")
                (rdir / f"{p['id']}.md").write_text(texto.rstrip("\n") + "\n\n" + footer, encoding="utf-8")
                n_refs += 1
                titulo = _titulo(texto)
                titulos.append(titulo)
                c = p["contract"][lang]
                sig = []
                for nid in c.get("recommended_next_prompt_ids", []):
                    s2 = seccion_de.get(nid)
                    if s2 is None:
                        continue
                    sig.append(f"`{nid}`" if s2 == sec else f"`{nid}` ({t['en_skill']} `{SECCIONES[s2][lang][0]}`)")
                lineas = [
                    f"### {titulo}",
                    f"- {t['archivo']}: [references/{p['id']}.md](references/{p['id']}.md)",
                    f"- {t['cuando']}: {cuando_usarlo(texto, lang)}",
                ]
                if c.get("required_inputs"):
                    lineas.append(f"- {t['entradas']}: {_una_linea(c['required_inputs'], 260)}")
                lineas.append(f"- {t['autonomia']}: {c.get('permitted_autonomy', '').strip()}")
                if c.get("stop_criteria"):
                    lineas.append(f"- {t['detencion']}: {_una_linea(c['stop_criteria'], 300)}")
                if sig:
                    lineas.append(f"- {t['siguiente']}: " + ", ".join(sig))
                bloques.append("\n".join(lineas))

            desc = descripcion_skill(sec, lang, titulos)
            pasos = "\n".join(f"{i}. {s}" for i, s in enumerate(t["pasos"], 1))
            skill_md = (
                "---\n"
                f"name: {slug}\n"
                f"description: {_yaml_str(desc)}\n"
                "license: CC-BY-4.0\n"
                "---\n\n"
                f"# {t['fase']} {sec} — {label}\n\n"
                f"{t['intro'].format(label=label)}\n\n"
                f"{t['como']}\n\n{pasos}\n\n"
                f"{t['prompts']}\n\n" + "\n\n".join(bloques) + "\n\n"
                "---\n\n"
                f"{t['atrib'].format(site=SITE, precios=PRECIOS_URL)}\n"
            )
            (sdir / "SKILL.md").write_text(skill_md, encoding="utf-8")
            resumen["skills"].setdefault(lang, []).append(slug)
        resumen["references"][lang] = n_refs

        plugin_json = {
            "name": plugin,
            "version": SKILLS_VERSION,
            "description": (
                "112 prompts AI-SDLC en español como skills por fase (análisis, diseño, pruebas, revisión, operación, seguridad…). "
                f"Proyectos y variables persistentes en el plan Pro: {PRECIOS_URL}"
                if lang == "es" else
                "112 AI-SDLC prompts in English as per-phase skills (analysis, design, testing, review, operations, security…). "
                f"Projects and persistent variables in the Pro plan: {PRECIOS_URL}"
            ),
            "author": {"name": "Lion Systems", "url": SITE},
            "homepage": SITE_URL,
            "repository": f"https://github.com/{REPO_PUBLICO}",
            "license": "CC-BY-4.0",
            "keywords": ["sdlc", "prompts", "software-engineering", "testing", "code-review", lang],
        }
        _json(base / ".claude-plugin" / "plugin.json", plugin_json)

    # Paridad: cada id una vez por idioma.
    for lang in LANGS:
        if resumen["references"][lang] != len(indice):
            raise ErrorGeneracion(f"{lang}: {resumen['references'][lang]} referencias != {len(indice)} prompts")

    marketplace = {
        "name": MARKETPLACE_NAME,
        "description": "AI-SDLC prompts as skills for Claude Code and Codex (ES/EN) — by Lion Systems",
        "owner": {"name": "Lion Systems", "url": SITE},
        "plugins": [
            {
                "name": f"ai-sdlc-{lang}",
                "source": f"./plugins/ai-sdlc-{lang}",
                "description": ("Prompts AI-SDLC en español, una skill por fase" if lang == "es"
                                else "AI-SDLC prompts in English, one skill per phase"),
                "version": SKILLS_VERSION,
            }
            for lang in LANGS
        ],
    }
    _json(out / ".claude-plugin" / "marketplace.json", marketplace)

    tabla = {lang: "\n".join(
        f"| `{SECCIONES[s][lang][0]}` | {SECCIONES[s][lang][1]} | {len(por_seccion[s])} |"
        for s in sorted(SECCIONES)) for lang in LANGS}
    reemplazos = {
        "{{VERSION}}": SKILLS_VERSION,
        "{{REPO}}": REPO_PUBLICO,
        "{{MARKETPLACE}}": MARKETPLACE_NAME,
        "{{SITE}}": SITE,
        "{{SITE_URL}}": SITE_URL,
        "{{PRECIOS_URL}}": PRECIOS_URL,
        "{{TOTAL}}": str(len(indice)),
        "{{N_SKILLS}}": str(len(SECCIONES)),
        "{{TABLA_ES}}": tabla["es"],
        "{{TABLA_EN}}": tabla["en"],
    }
    for nombre, destino in (("README.md", "README.md"), ("LICENSE", "LICENSE"),
                            ("validate_skills.py", "scripts/validate_skills.py"),
                            ("install.sh", "scripts/install.sh"), ("gitignore", ".gitignore")):
        texto = (TEMPLATES / nombre).read_text(encoding="utf-8")
        for k, v in reemplazos.items():
            texto = texto.replace(k, v)
        if "{{" in texto:
            raise ErrorGeneracion(f"plantilla {nombre} con marcador sin reemplazar")
        d = out / destino
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_text(texto, encoding="utf-8")
        if destino.endswith((".py", ".sh")):
            d.chmod(0o755)
    return resumen


def _json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(RAIZ / "dist" / "skills"))
    a = ap.parse_args(argv)
    try:
        r = generar(Path(a.out))
    except ErrorGeneracion as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    for lang in LANGS:
        print(f"{lang}: {len(r['skills'][lang])} skills, {r['references'][lang]} prompts")
    print(f"salida: {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
