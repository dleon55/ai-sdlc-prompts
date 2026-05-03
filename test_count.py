import i18n_strings
from pathlib import Path

PROMPTS_DIR = Path("ai_sdlc_pro_prompts")

def count_prompts():
    count = 0
    for f in PROMPTS_DIR.glob("*.md"):
        # Ignorar traducciones, el framework base y archivos vacíos/deprecados
        if f.name.endswith(".en.md") or f.name == "00-framework.md":
            continue
        
        # Validar contenido mínimo y que no esté deprecado
        content = f.read_text(encoding="utf-8")
        if len(content.strip()) < 20 or "DEPRECATED" in content:
            continue
            
        count += 1
    return count

print(f"Count: {count_prompts()}")
