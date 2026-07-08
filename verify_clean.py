import re
import sys

with open("index.html", encoding="utf-8") as f:
    content = f.read()

# Verificar que ninguna fórmula de uso (ES o EN) aparece en bloques <code>
# visibles. "Usa el prompt"/"Use the prompt" no cubre la fórmula EN real
# ("Use the <nombre> prompt and adapt it to:", nombre insertado antes de
# "prompt"), así que se valida por el marcador de cierre de la fórmula
# ("adáptalo a:" / "adapt it to:"), presente en ambos idiomas sin importar
# el nombre del prompt.
CONTAMINATION_MARKERS = (
    "Usa el prompt",
    "adáptalo a:",
    "lo adaptes a:",
    "adapt it to:",
)
code_blocks = re.findall(r'<code id="code-([^"]+)">(.*?)</code>', content, re.DOTALL)

contaminated = []
for pid, text in code_blocks:
    if any(marker in text for marker in CONTAMINATION_MARKERS):
        contaminated.append(pid)

print(f"Total bloques code: {len(code_blocks)}")
print(f"Bloques con fórmula de uso (ES/EN): {len(contaminated)}")
if contaminated:
    for c in contaminated:
        print(f"  - {c}")

# Verificar 02-01 como ejemplo
for pid, text in code_blocks:
    if pid == "02-01-analisis-issue":
        print(f"\nPrompt 02-01 ({len(text)} chars):")
        print(text[:400].strip())
        print("---")
        print("Contiene formula:", any(marker in text for marker in CONTAMINATION_MARKERS))
        break

# Contar prompts con info-btn
info_buttons = content.count('class="info-btn"')
print(f"\nInfo buttons en HTML: {info_buttons}")

# Exit code para CI: falla si hay contaminados
if contaminated:
    print(f"\nERROR: {len(contaminated)} prompt(s) contaminado(s). Abortar CI.")
    sys.exit(1)
print("OK: 0 prompts contaminados.")
