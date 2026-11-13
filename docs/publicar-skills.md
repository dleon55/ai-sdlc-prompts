# Publicar las skills (SKILL.md) para Claude Code y Codex

Spec: E2 (`campanas/productos/specs/E-ai-sdlc-prueba-y-skills.md`). Repo público generado:
https://github.com/dleon55/ai-sdlc-skills

## Qué se publica y qué no

| Cuerpo (LICENSE de este repo) | ¿Va al repo de skills? |
|---|---|
| §1 Prompts (`ai_sdlc_pro_prompts/**`, `prompts-index.json`) — CC BY 4.0 | **Sí**, como `references/` (texto sin cambios + nota de atribución) |
| §2 Servidor MCP — MIT | No |
| §3 Plataforma (`build.py`, `backend/**`, HTML, **este generador**) — propietario | **No**. Lo de pago es la plataforma (proyectos múltiples, variables persistentes, personalización y resultados por prompt), no el texto. |

El repo público lleva su propio `LICENSE`: CC BY 4.0 para `plugins/**`, `README.md` y
`marketplace.json`, con atribución e indicación de cambios; MIT para `scripts/**`
(`validate_skills.py`, `install.sh`, generados desde `tools/skills_templates/`).

## Formato (verificado el 13-nov-2026)

- **Claude Code** (code.claude.com/docs/en/skills y /plugin-marketplaces): skill = carpeta con
  `SKILL.md`; *frontmatter* YAML en la primera línea; `description` decide la activación
  (la lista la trunca a 1,536 caracteres con `when_to_use`). Claves portables fuera de Claude
  Code: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`; usamos
  sólo `name`, `description` y `license`. Marketplace: `.claude-plugin/marketplace.json` con
  `name`, `owner`, `plugins[]` (`name`, `source` relativo `./plugins/…`); cada plugin con
  `.claude-plugin/plugin.json` cuyo `name` coincide con la entrada. Instalación:
  `/plugin marketplace add dleon55/ai-sdlc-skills` y `/plugin install ai-sdlc-es@ai-sdlc-skills`.
- **Codex** (learn.chatgpt.com/docs/build-skills, antes developers.openai.com/codex/skills):
  mismo `SKILL.md`, exige `name` y `description`. Rutas: `$HOME/.agents/skills` (usuario),
  `.agents/skills` desde el directorio actual hasta la raíz del repo, `/etc/codex/skills`
  (admin). Sigue enlaces simbólicos; hay que reiniciar Codex. `agents/openai.yaml` es opcional
  (no lo emitimos). Por eso **no hace falta una segunda variante**: el `install.sh` público
  copia las mismas carpetas a `~/.claude/skills` o `~/.agents/skills`.

Límites que aplicamos (los más estrictos): `name` `^[a-z0-9-]{1,64}$`, igual a la carpeta y
único entre ES y EN (se pueden instalar ambos idiomas en el mismo directorio);
`description` ≤ 1024; `SKILL.md` ≤ 500 líneas.

## Diseño

- Una skill por sección (18 por idioma), no por prompt: 224 descripciones competirían por
  activarse. Los prompts van en `references/` (carga progresiva) y cada skill lleva su copia
  de `00-framework.md` para funcionar aunque se copie sola.
- Los disparadores (`description`) se escriben a mano en `SECCIONES` de
  `tools/build_skills.py`: si una skill se activa mal, se corrige ahí.
- `SKILL.md` no lleva publicidad: sólo una línea final de atribución CC BY con el enlace a
  precios (UTM `utm_source=github&utm_medium=skills&utm_campaign=ai-sdlc-skills`). El CTA
  va en el README, en la `description` de cada plugin y en la nota final de cada referencia.

## Procedimiento

```bash
python tools/build_skills.py                   # escribe dist/skills/ (ignorado por git)
python dist/skills/scripts/validate_skills.py  # frontmatter, enlaces, atribución, secretos
python -m pytest tests/test_build_skills.py -q

git clone https://github.com/dleon55/ai-sdlc-skills.git <clon>
scripts/publicar-skills.sh <clon>              # rama sync/skills-<sha> con commit, sin push
cd <clon> && git push -u origin <rama> && gh pr create
```

Cuando cambie un prompt, se vuelve a correr el procedimiento; el repo público nunca se edita
a mano (el validador rechaza archivos que el generador no produce). Para una versión nueva,
sube `SKILLS_VERSION` en el generador.

## Prueba manual

En Claude Code: `/plugin marketplace add dleon55/ai-sdlc-skills`,
`/plugin install ai-sdlc-es@ai-sdlc-skills`, y pedir «analiza este issue»: debe activarse
`sdlc-analisis` y leer `references/02-01-analisis-issue.md`.
