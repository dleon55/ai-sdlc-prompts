#!/usr/bin/env python3
"""Valida las skills de este repositorio antes de publicarlas.

Validates the skills in this repository before publishing them.

Comprueba / Checks:
  - marketplace.json y plugin.json: JSON válido, nombres coherentes, rutas existentes.
  - Cada SKILL.md: frontmatter YAML en la primera línea, `name` en minúsculas
    y guiones (<= 64, igual al nombre de la carpeta, único), `description`
    no vacía (<= 1024) y sólo claves portables (Claude Code y Codex).
  - Cada enlace a references/ existe; cada archivo lleva atribución CC BY 4.0
    y el enlace con UTM a la página de planes.
  - Sólo hay archivos de los tipos esperados (nada de código de la plataforma).
  - No hay secretos (tokens, llaves privadas) ni marcas del código propietario.

Uso / Usage:  python3 scripts/validate_skills.py [--root .]
Sale con 0 si todo está bien; 1 y la lista de errores si no.

Licencia del script: MIT. Copyright (c) 2026 LionSystems.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
CLAVES_PORTABLES = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
DESC_MAX = 1024
SITE = "https://prompts.lionsystems.com.mx"
UTM = "utm_source=github&utm_medium=skills"
PRECIOS = f"{SITE}/precios.html?{UTM}"

ARCHIVOS_RAIZ = {"README.md", "LICENSE", ".gitignore", ".claude-plugin/marketplace.json",
                 "scripts/validate_skills.py", "scripts/install.sh"}

SECRETOS = [
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"), "token de GitHub"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{40,}"), "token de GitHub"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "llave de AWS"),
    (re.compile(r"sk-(?:ant-|proj-)?[A-Za-z0-9_-]{32,}"), "llave de API"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "token de Slack"),
    (re.compile(r"AIza[0-9A-Za-z_-]{35}"), "llave de Google"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----\s*\n\s*[A-Za-z0-9+/=]{40,}"), "llave privada"),
    (re.compile(r"(?:pdl_live|pdl_sdbx)_apikey_[A-Za-z0-9_]{20,}"), "llave de Paddle"),
]

# Fragmentos de CÓDIGO que sólo existen en la plataforma (propietario). Un
# prompt puede citar un nombre como ejemplo (lo hace 08-01); lo que no debe
# aparecer es la definición. Si aparece, algo del cuerpo de pago se coló.
MARCAS_PROPIETARIAS = [
    "function checkProFeatureGate", "function openFeedbackWall", "function submitFeedbackWall",
    "SECTION_META = {", "SECTION_LABELS_I18N = {", "def parse_editorial_contract(",
    "def parse_md(", "create table if not exists user_trial", "TRIAL_MAX_RENEWALS",
    "project_prompt_state (", "PADDLE_API_KEY", "PADDLE_WEBHOOK_SECRET",
]


def frontmatter(texto: str) -> tuple[dict, str]:
    if not texto.startswith("---\n"):
        raise ValueError("el archivo no empieza con '---' (frontmatter)")
    fin = texto.find("\n---\n", 4)
    if fin < 0:
        raise ValueError("frontmatter sin cierre '---'")
    bloque = texto[4:fin]
    try:
        import yaml  # type: ignore
        datos = yaml.safe_load(bloque)
    except ImportError:
        datos = {}
        for ln in bloque.splitlines():
            if not ln.strip():
                continue
            m = re.match(r"^([a-z][a-z0-9_-]*):\s*(.*)$", ln)
            if not m:
                raise ValueError(f"línea de frontmatter no reconocida: {ln!r}")
            v = m.group(2).strip()
            if v.startswith('"'):
                v = json.loads(v)
            elif v.startswith("'") and v.endswith("'"):
                v = v[1:-1].replace("''", "'")
            datos[m.group(1)] = v
    if not isinstance(datos, dict):
        raise ValueError("el frontmatter no es un mapa YAML")
    return datos, texto[fin + 5:]


def validar(root: Path) -> list[str]:
    err: list[str] = []
    mp_path = root / ".claude-plugin" / "marketplace.json"
    try:
        mp = json.loads(mp_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"marketplace.json ilegible: {e}"]
    for campo in ("name", "owner", "plugins"):
        if campo not in mp:
            err.append(f"marketplace.json: falta '{campo}'")

    permitidos = set(ARCHIVOS_RAIZ)
    nombres_skill: dict[str, str] = {}
    for entrada in mp.get("plugins", []):
        pname, src = entrada.get("name"), entrada.get("source", "")
        if not isinstance(src, str) or not src.startswith("./") or ".." in src:
            err.append(f"plugin {pname}: 'source' debe ser ruta relativa './…' sin '..'")
            continue
        pdir = root / src[2:]
        try:
            pj = json.loads((pdir / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            err.append(f"plugin {pname}: plugin.json ilegible: {e}")
            continue
        permitidos.add(f"{src[2:]}/.claude-plugin/plugin.json")
        if pj.get("name") != pname:
            err.append(f"plugin {pname}: el name de plugin.json ({pj.get('name')}) no coincide")
        if PRECIOS not in pj.get("description", ""):
            err.append(f"plugin {pname}: la description no enlaza a la página de planes con UTM")
        skills = sorted((pdir / "skills").glob("*/SKILL.md"))
        if not skills:
            err.append(f"plugin {pname}: sin skills")
        for sm in skills:
            rel = sm.relative_to(root).as_posix()
            permitidos.add(rel)
            sdir = sm.parent
            texto = sm.read_text(encoding="utf-8")
            try:
                fm, cuerpo = frontmatter(texto)
            except ValueError as e:
                err.append(f"{rel}: {e}")
                continue
            extra = set(fm) - CLAVES_PORTABLES
            if extra:
                err.append(f"{rel}: claves no portables en el frontmatter: {sorted(extra)}")
            name, desc = fm.get("name"), fm.get("description")
            if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
                err.append(f"{rel}: name inválido {name!r}")
            elif name != sdir.name:
                err.append(f"{rel}: name {name!r} distinto de la carpeta {sdir.name!r}")
            elif name in nombres_skill:
                err.append(f"{rel}: name {name!r} repetido (también en {nombres_skill[name]})")
            else:
                nombres_skill[name] = rel
            if not isinstance(desc, str) or not desc.strip():
                err.append(f"{rel}: description vacía")
            elif len(desc) > DESC_MAX:
                err.append(f"{rel}: description de {len(desc)} caracteres (> {DESC_MAX})")
            if len(texto.splitlines()) > 500:
                err.append(f"{rel}: más de 500 líneas")
            if PRECIOS not in cuerpo:
                err.append(f"{rel}: falta el enlace a la página de planes con UTM")
            if "CC BY 4.0" not in cuerpo:
                err.append(f"{rel}: falta la atribución CC BY 4.0")
            enlazados = set(re.findall(r"\(references/([^)\s]+\.md)\)", cuerpo))
            for ref in sorted(enlazados):
                if not (sdir / "references" / ref).is_file():
                    err.append(f"{rel}: enlaza references/{ref}, que no existe")
            if "references/00-framework.md" in cuerpo and not (sdir / "references" / "00-framework.md").is_file():
                err.append(f"{rel}: falta references/00-framework.md")
            for ref in sorted((sdir / "references").glob("*.md")):
                rrel = ref.relative_to(root).as_posix()
                permitidos.add(rrel)
                if ref.name != "00-framework.md" and ref.name not in enlazados:
                    err.append(f"{rrel}: no está enlazado desde SKILL.md")
                rt = ref.read_text(encoding="utf-8")
                if "CC BY 4.0" not in rt or PRECIOS not in rt:
                    err.append(f"{rrel}: falta la atribución CC BY 4.0 o el enlace con UTM")

    for f in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = f.relative_to(root).as_posix()
        if rel.startswith(".git/") or "/__pycache__/" in f"/{rel}":
            continue
        if rel not in permitidos:
            err.append(f"{rel}: archivo no esperado en la publicación")
            continue
        try:
            texto = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            err.append(f"{rel}: no es texto UTF-8")
            continue
        for rx, que in SECRETOS:
            if rx.search(texto):
                err.append(f"{rel}: posible secreto ({que})")
        if rel != "scripts/validate_skills.py":
            for marca in MARCAS_PROPIETARIAS:
                if marca in texto:
                    err.append(f"{rel}: contiene '{marca}', propio del código de la plataforma")
    return err


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Valida las skills / validates the skills")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    errores = validar(root)
    n = len(list(root.glob("plugins/*/skills/*/SKILL.md")))
    if errores:
        print(f"FALLA: {len(errores)} problema(s) en {n} skills", file=sys.stderr)
        for e in errores:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"OK: {n} skills válidas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
