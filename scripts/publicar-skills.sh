#!/usr/bin/env bash
# Sincroniza las skills generadas con un clon del repo público dleon55/ai-sdlc-skills
# y deja una rama lista para PR. No hace push ni abre el PR: eso es deliberado.
#
# Uso: scripts/publicar-skills.sh <ruta-del-clon-ai-sdlc-skills> [rama]
# Ver docs/publicar-skills.md.
set -euo pipefail

clon="${1:?uso: $0 <ruta-del-clon-ai-sdlc-skills> [rama]}"
rama="${2:-sync/skills-$(git -C "$(dirname "$0")/.." rev-parse --short HEAD)}"
raiz="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out="$raiz/dist/skills"

[[ -d "$clon/.git" ]] || { echo "ERROR: $clon no es un clon de git" >&2; exit 1; }
[[ -z "$(git -C "$clon" status --porcelain)" ]] || { echo "ERROR: el clon tiene cambios sin confirmar" >&2; exit 1; }

python3 "$raiz/tools/build_skills.py" --out "$out"
python3 "$out/scripts/validate_skills.py" --root "$out"

git -C "$clon" checkout -B "$rama"
# Espejo exacto: lo que no genera el generador no debe quedar en el repo público.
find "$clon" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -R "$out"/. "$clon"/
python3 "$clon/scripts/validate_skills.py" --root "$clon"

fuente="$(git -C "$raiz" rev-parse --short HEAD)"
git -C "$clon" add -A
if git -C "$clon" diff --cached --quiet; then
  echo "Sin cambios: el repo público ya coincide con $fuente."
  exit 0
fi
git -C "$clon" commit -q -m "chore: regenerar skills desde ai-sdlc-prompts@$fuente"
echo "Listo: rama '$rama' en $clon con las skills de ai-sdlc-prompts@$fuente."
echo "Siguiente: git -C $clon push -u origin $rama && gh pr create (en $clon)."
