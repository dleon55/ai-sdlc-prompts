import re
import sys

with open("index.html", encoding="utf-8") as f:
    content = f.read()

# Verificar que "Usa el prompt" no aparece en bloques <code> visibles
code_blocks = re.findall(r'<code id="code-([^"]+)">(.*?)</code>', content, re.DOTALL)

contaminated = []
for pid, text in code_blocks:
    if "Usa el prompt" in text or "Usa el prompt".lower() in text.lower():
        contaminated.append(pid)

print(f"Total bloques code: {len(code_blocks)}")
print(f"Bloques con 'Usa el prompt': {len(contaminated)}")
if contaminated:
    for c in contaminated:
        print(f"  - {c}")

# Verificar 02-01 como ejemplo
for pid, text in code_blocks:
    if pid == "02-01-analisis-issue":
        print(f"\nPrompt 02-01 ({len(text)} chars):")
        print(text[:400].strip())
        print("---")
        print("Contiene formula:", "Usa el prompt" in text)
        break

# Contar prompts con info-btn
info_buttons = content.count('class="info-btn"')
print(f"\nInfo buttons en HTML: {info_buttons}")

# Exit code para CI: falla si hay contaminados
if contaminated:
    print(f"\nERROR: {len(contaminated)} prompt(s) contaminado(s). Abortar CI.")
    sys.exit(1)
print("OK: 0 prompts contaminados.")
