#!/usr/bin/env bash
# Genera data/prompts-full.json para el servidor MCP, que vive en
# https://github.com/dleon55/ai-sdlc-mcp. build.py sigue siendo la única
# fuente de verdad del parseo; este script solo le pide escribir el export
# en la ruta indicada para copiarlo vía PR al repo del MCP.
#
# Uso: scripts/exportar-datos-mcp.sh <ruta-de-salida.json>
#   p. ej. scripts/exportar-datos-mcp.sh ../ai-sdlc-mcp/data/prompts-full.json
set -euo pipefail
if [ "$#" -ne 1 ]; then
  echo "uso: $0 <ruta-de-salida.json>" >&2
  exit 2
fi
raiz="$(cd "$(dirname "$0")/.." && pwd)"
salida="$(realpath -m "$1")"
cd "$raiz"
AI_SDLC_MCP_DATA_OUT="$salida" python3 build.py
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print("OK ->", sys.argv[1], len(d["prompts"]), "prompts")' "$salida"
