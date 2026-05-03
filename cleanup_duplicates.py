import os
from pathlib import Path

files_to_delete = [
    "ai_sdlc_pro_prompts/02-04-analisis-integral-requerimientos.md",
    "ai_sdlc_pro_prompts/02-04-analisis-integral-requerimientos.en.md"
]

for f in files_to_delete:
    p = Path(f)
    if p.exists():
        try:
            os.remove(p)
            print(f"Deleted {f}")
        except Exception as e:
            print(f"Error deleting {f}: {e}")
    else:
        print(f"{f} does not exist")
