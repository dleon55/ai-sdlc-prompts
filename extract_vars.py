import argparse
import json
import re
from collections import Counter
from pathlib import Path

import build

ROOT = Path(__file__).parent
PROMPTS = ROOT / "ai_sdlc_pro_prompts"
BUILD_SOURCE = (ROOT / "build.py").read_text(encoding="utf-8")

# Tokens genericos ambiguos que NUNCA deben registrarse como alias canonico
# (colisionarian con significados distintos segun el prompt) -- el gate
# falla si alguno se referencia como si fuera canonico en TOKEN_REGISTRY.
# NOTA: [LISTA]/[DESCRIPCIÓN] son igual de ambiguos semanticamente, pero a
# diferencia de estos SI se usan hoy como placeholder de llenado manual
# dentro de prompts reales (16 y 6 apariciones respectivamente) -- forzarlos
# aqui rompería el build sin razon real, asi que se dejan en 'additional'.
FORBIDDEN = {
    "INDICAR", "INDICATE", "NOMBRE", "NAME", "NIVEL", "LEVEL",
    "TIPO", "TYPE", "SEVERIDAD", "SEVERITY",
}
# Placeholders de formato (no son campos a llenar) -- se reportan pero no
# fallan el gate.
IGNORED = {
    "N", "X", "Y", "Z", "ADR-NNN", "NNN", "YYYYMMDD",
    "SÍ / NO", "SÍ/NO", "YES / NO", "YES/NO",
}

TOKEN_RX = re.compile(
    r"\[([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ0-9_ /.,#()\-]{1,80})\]"
    r"|\{\{([A-Z][A-Z0-9_]{1,60})\}\}"
)

# Encabezados que marcan una seccion de "salida esperada" / ejemplo de
# resultado. Sus tokens son datos ilustrativos de ejemplo (documentacion
# de referencia), no placeholders que el usuario deba llenar antes de
# copiar el prompt -- por eso se auditan aparte y NO participan del gate
# invalid/forbidden (fallar el build por contenido de ejemplo seria
# incorrecto: nunca llega al prompt ejecutable).
EXPECTED_OUTPUT_HEADERS = {"salida esperada", "resultado esperado", "expected output"}


def find_tokens(text):
    return [(m.group(1) or m.group(2)).strip() for m in TOKEN_RX.finditer(text)]


def parse_registry():
    block = BUILD_SOURCE.split("var TOKEN_REGISTRY = {", 1)[1].split("\n};", 1)[0]
    registry = {}
    entries = re.split(r"\n  (?=[a-z_]+:\s*\{)", block)
    for entry in entries:
        field_match = re.match(r"\s*([a-z_]+):\s*\{", entry)
        aliases_match = re.search(r"aliases:\s*\[(.*?)\]\s*\}", entry, re.DOTALL)
        required_match = re.search(r"required:\s*(true|false)", entry)
        if not (field_match and aliases_match and required_match):
            continue
        aliases = [
            left or right
            for left, right in re.findall(r"'([^']*)'|\"([^\"]*)\"", aliases_match.group(1))
        ]
        registry[field_match.group(1)] = {
            "required": required_match.group(1) == "true",
            "aliases": aliases,
        }
    if not registry:
        raise RuntimeError("No se pudo leer TOKEN_REGISTRY desde build.py")
    return registry


def collect_prompt_and_formula_tokens():
    """Tokens del prompt ejecutable y de las formulas de uso, ya separados
    por build.parse_md() (clasificacion por encabezado, no por prefijo de
    texto -- ver issue #44). Antes de ese fix, un scan ingenuo de todos los
    bloques ```text``` mezclaba formula y prompt sin distincion."""
    counts, locations = Counter(), {}
    for path in sorted(PROMPTS.glob("*.md")):
        _, prompt, _, formulas = build.parse_md(path)
        sources = [prompt] + list(formulas)
        for source in sources:
            for token in find_tokens(source):
                counts[token] += 1
                locations.setdefault(token, set()).add(path.name)
    return counts, locations


def collect_expected_output_tokens():
    counts, locations = Counter(), {}
    header_rx = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    for path in sorted(PROMPTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        headers = list(header_rx.finditer(text))
        for i, h in enumerate(headers):
            if h.group(1).strip().lower() not in EXPECTED_OUTPUT_HEADERS:
                continue
            end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
            for token in find_tokens(text[h.end():end]):
                counts[token] += 1
                locations.setdefault(token, set()).add(path.name)
    return counts, locations


def collect_ui_tag_tokens():
    """Tokens mostrados como chips de sugerencia en el panel de variables
    (build.py, spans .var-tag). El primer token de cada chip es la
    sugerencia vigente y debe existir en TOKEN_REGISTRY; un segundo token
    tras 'reemplaza'/'replaces' es una referencia legado intencionalmente
    NO registrada (aviso de migracion) y se ignora."""
    chip_rx = re.compile(
        r'<span class="var-tag"><span class="fw-lang-es">(.*?)</span>'
        r'<span class="fw-lang-en">(.*?)</span></span>'
    )
    bracket_rx = re.compile(r"\[([^\]]+)\]")
    primary_tokens = set()
    for es, en in chip_rx.findall(BUILD_SOURCE):
        for chip_text in (es, en):
            tokens = bracket_rx.findall(chip_text)
            if tokens:
                primary_tokens.add(tokens[0])
    return primary_tokens


def classify():
    registry = parse_registry()
    token_to_field = {
        token: field
        for field, config in registry.items()
        for token in config["aliases"]
    }
    canonical = {
        config["aliases"][0]
        for config in registry.values()
        if config["aliases"]
    }
    all_registered = set(token_to_field)

    counts, locations = collect_prompt_and_formula_tokens()
    report = {key: {} for key in (
        "canonical", "allowed_alias", "additional", "ignored_example", "invalid"
    )}
    for token, count in sorted(counts.items()):
        detail = {"count": count, "files": sorted(locations[token])}
        if token in FORBIDDEN:
            report["invalid"][token] = detail
        elif token in IGNORED:
            report["ignored_example"][token] = detail
        elif token in canonical:
            detail["field"] = token_to_field[token]
            report["canonical"][token] = detail
        elif token in token_to_field:
            detail["field"] = token_to_field[token]
            report["allowed_alias"][token] = detail
        else:
            report["additional"][token] = detail

    eo_counts, eo_locations = collect_expected_output_tokens()
    report["example_output"] = {
        token: {"count": c, "files": sorted(eo_locations[token])}
        for token, c in sorted(eo_counts.items())
    }

    ui_tokens = collect_ui_tag_tokens()
    report["ui_tag_unregistered"] = {
        token: {} for token in sorted(ui_tokens) if token not in all_registered
    }

    return report


def main():
    parser = argparse.ArgumentParser(description="Audita placeholders de prompts")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = classify()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for category, tokens in report.items():
            print(f"{category}: {len(tokens)}")
            for token, detail in tokens.items():
                count = detail.get("count")
                prefix = f"  {count:3d} " if count is not None else "      "
                print(f"{prefix}[{token}]")

    errors = []
    if report["invalid"]:
        errors.append(f"{len(report['invalid'])} token(s) generico(s) invalido(s) en prompt/formula")
    if report["ui_tag_unregistered"]:
        errors.append(f"{len(report['ui_tag_unregistered'])} tag(s) de UI sin registrar en TOKEN_REGISTRY")
    if errors:
        print("ERROR: " + "; ".join(errors))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
