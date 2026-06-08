import argparse
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).parent
PROMPTS = ROOT / "ai_sdlc_pro_prompts"
BUILD_SOURCE = (ROOT / "build.py").read_text(encoding="utf-8")
FORBIDDEN = {
    "INDICAR", "INDICATE", "NOMBRE", "NAME", "NIVEL", "LEVEL",
    "TIPO", "TYPE", "SEVERIDAD", "SEVERITY",
}
IGNORED = {"N", "X", "Y", "Z", "ADR-NNN", "NNN", "YYYYMMDD"}


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


def collect_tokens():
    counts = Counter()
    locations = {}
    token_rx = re.compile(
        r"\[([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ0-9_ /.,#()\-]{1,80})\]"
        r"|\{\{([A-Z][A-Z0-9_]{1,60})\}\}"
    )
    for path in sorted(PROMPTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for block in re.findall(r"```text\n(.*?)```", text, re.DOTALL):
            for match in token_rx.finditer(block):
                token = (match.group(1) or match.group(2)).strip()
                counts[token] += 1
                locations.setdefault(token, set()).add(path.name)
    return counts, locations


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
    counts, locations = collect_tokens()
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
                print(f"  {detail['count']:3d} [{token}]")
    if report["invalid"]:
        print("ERROR: existen tokens genéricos inválidos.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
