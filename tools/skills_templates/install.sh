#!/usr/bin/env bash
# Copia las skills AI-SDLC al directorio de skills de Claude Code o de Codex.
# Copies the AI-SDLC skills into the Claude Code or Codex skills directory.
#
# Uso / Usage:
#   scripts/install.sh <es|en> <claude|codex> [--project DIR]
#
#   claude  -> ~/.claude/skills/        (--project: DIR/.claude/skills/)
#   codex   -> ~/.agents/skills/        (--project: DIR/.agents/skills/)
#
# Licencia del script: MIT. Las skills: CC BY 4.0 (ver LICENSE).
set -euo pipefail

lang="${1:-}"; agent="${2:-}"; project=""
if [[ "${3:-}" == "--project" ]]; then project="${4:?falta DIR / missing DIR}"; fi
case "$lang" in es|en) ;; *) echo "uso: $0 <es|en> <claude|codex> [--project DIR]" >&2; exit 2;; esac

case "$agent" in
  claude) sub=".claude/skills" ;;
  codex)  sub=".agents/skills" ;;
  *) echo "uso: $0 <es|en> <claude|codex> [--project DIR]" >&2; exit 2;;
esac

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
src="$root/plugins/ai-sdlc-$lang/skills"
dest="${project:-$HOME}/$sub"
mkdir -p "$dest"

for d in "$src"/*/; do
  name="$(basename "$d")"
  rm -rf "${dest:?}/$name"
  cp -R "$d" "$dest/$name"
  echo "  + $dest/$name"
done
echo "OK: $(ls -d "$src"/*/ | wc -l | tr -d ' ') skills -> $dest"
[[ "$agent" == "codex" ]] && echo "Reinicia Codex para que las detecte. / Restart Codex to pick them up."
exit 0
