# AI-SDLC Skills — para Claude Code y Codex

**[Español](#español) · [English](#english)**

{{TOTAL}} prompts de ingeniería de software del marco **AI-SDLC Pro**, empaquetados como
*skills* (`SKILL.md`) por fase del ciclo de vida: {{N_SKILLS}} skills en español y {{N_SKILLS}} en inglés.

{{TOTAL}} software engineering prompts from the **AI-SDLC Pro** framework, packaged as
`SKILL.md` *skills* per lifecycle phase: {{N_SKILLS}} skills in Spanish and {{N_SKILLS}} in English.

> Proyecto independiente de Lion Systems; no es un producto oficial de Anthropic ni de OpenAI.
> Independent project by Lion Systems; not an official Anthropic or OpenAI product.

---

## Español

### Qué es

Cada skill corresponde a una fase (análisis, diseño, pruebas, revisión, operación, seguridad…).
El agente ve sólo el nombre y la descripción de cada fase; cuando tu petición encaja
(«analiza este issue», «diseña las pruebas de integración»), carga la skill y abre únicamente
el prompt que necesita desde `references/`, junto con el contexto `00-framework.md`.

| Skill | Fase | Prompts |
|---|---|---|
{{TABLA_ES}}

### Instalación en Claude Code

Como *marketplace* de plugins (recomendado; se actualiza con `/plugin marketplace update`):

```text
/plugin marketplace add {{REPO}}
/plugin install ai-sdlc-es@{{MARKETPLACE}}
```

Desde la terminal: `claude plugin marketplace add {{REPO}}` y
`claude plugin install ai-sdlc-es@{{MARKETPLACE}}`. Las skills quedan como
`/ai-sdlc-es:sdlc-analisis`, `/ai-sdlc-es:sdlc-pruebas`, etc., y también se activan solas.

Copiándolas a mano a `~/.claude/skills/` (o a `.claude/skills/` de un proyecto):

```bash
git clone https://github.com/{{REPO}}.git
cd ai-sdlc-skills
scripts/install.sh es claude                      # ~/.claude/skills/
scripts/install.sh es claude --project ../mi-repo # ../mi-repo/.claude/skills/
```

### Instalación en Codex

Codex lee skills con el mismo formato (`SKILL.md` con `name` y `description`) desde
`~/.agents/skills/` (personales) o `.agents/skills/` del repositorio:

```bash
git clone https://github.com/{{REPO}}.git
cd ai-sdlc-skills
scripts/install.sh es codex                       # ~/.agents/skills/
scripts/install.sh es codex --project ../mi-repo  # ../mi-repo/.agents/skills/
```

Reinicia Codex para que las detecte.

### Uso

Pide el trabajo con naturalidad: «analiza el issue #42», «revisa este PR», «haz el plan de
recuperación ante desastres». La skill pide las variables entre corchetes (`[MODULO]`,
`[PEGAR]`…) que no pueda deducir del repositorio y respeta la autonomía y los criterios de
detención de cada prompt.

### ¿Y el plan Pro?

Los prompts son libres (CC BY 4.0). Lo que ofrece la plataforma es lo que una carpeta de
archivos no puede: **varios proyectos con sus variables guardadas**, prompts ya rellenados,
progreso por proyecto, personalización y resultados de IA por prompt, sincronizados entre
dispositivos → **[ver planes]({{PRECIOS_URL}})**.

---

## English

### What it is

Each skill is one phase (analysis, design, testing, review, operations, security…). The agent
only sees each phase's name and description; when your request matches ("analyze this issue",
"design the integration tests") it loads the skill and opens only the prompt it needs from
`references/`, together with the `00-framework.md` context.

| Skill | Phase | Prompts |
|---|---|---|
{{TABLA_EN}}

### Install in Claude Code

As a plugin marketplace (recommended; update with `/plugin marketplace update`):

```text
/plugin marketplace add {{REPO}}
/plugin install ai-sdlc-en@{{MARKETPLACE}}
```

From the shell: `claude plugin marketplace add {{REPO}}` and
`claude plugin install ai-sdlc-en@{{MARKETPLACE}}`. Skills appear as
`/ai-sdlc-en:sdlc-analysis`, `/ai-sdlc-en:sdlc-testing`, etc., and also trigger on their own.

By copying them into `~/.claude/skills/` (or a project's `.claude/skills/`):

```bash
git clone https://github.com/{{REPO}}.git
cd ai-sdlc-skills
scripts/install.sh en claude                       # ~/.claude/skills/
scripts/install.sh en claude --project ../my-repo  # ../my-repo/.claude/skills/
```

### Install in Codex

Codex reads skills in the same format (`SKILL.md` with `name` and `description`) from
`~/.agents/skills/` (personal) or the repository's `.agents/skills/`:

```bash
git clone https://github.com/{{REPO}}.git
cd ai-sdlc-skills
scripts/install.sh en codex                        # ~/.agents/skills/
scripts/install.sh en codex --project ../my-repo   # ../my-repo/.agents/skills/
```

Restart Codex so it picks them up.

### Usage

Ask naturally: "analyze issue #42", "review this PR", "write the disaster recovery plan".
The skill asks for the bracketed variables (`[MODULE]`, `[PASTE]`…) it cannot infer from the
repository and respects each prompt's permitted autonomy and stop criteria.

### What about Pro?

The prompts are free (CC BY 4.0). The platform offers what a folder of files cannot:
**multiple projects with saved variables**, pre-filled prompts, per-project progress, and
per-prompt customization and AI results, synced across devices →
**[see plans]({{PRECIOS_URL}})**.

---

## Licencia / License

- Skills (`plugins/**`): **CC BY 4.0** — adaptación de [AI-SDLC Pro]({{SITE_URL}}) al formato
  `SKILL.md`; el texto de los prompts no cambió. / adapted from AI-SDLC Pro; prompt text unchanged.
- Scripts (`scripts/**`): **MIT**.

Ver / See [LICENSE](LICENSE).

## Mantenimiento / Maintenance

Este repositorio se **genera** desde [dleon55/ai-sdlc-prompts](https://github.com/dleon55/ai-sdlc-prompts);
no se edita a mano. Para proponer cambios a un prompt, abre un issue o PR allí.
`python3 scripts/validate_skills.py` comprueba el frontmatter, los enlaces, la atribución y
que no haya secretos. / This repository is **generated** from the source repo; do not edit by hand.

Versión / Version: {{VERSION}}
