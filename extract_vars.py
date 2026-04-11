import re, glob, json, sys

placeholders = {}
for f in sorted(glob.glob('ai_sdlc_pro_prompts/*.md')):
    txt = open(f, encoding='utf-8').read()
    # extraer bloques ```text ... ```
    blocks = re.findall(r'```text\n(.*?)```', txt, re.DOTALL)
    for b in blocks:
        for m in re.findall(r'\[([A-Z][A-Z /\-\.A-Z0-9]*)\]', b):
            placeholders[m] = placeholders.get(m, 0) + 1

for p, cnt in sorted(placeholders.items(), key=lambda x: -x[1]):
    print(f"{cnt:3d}  [{p}]")
