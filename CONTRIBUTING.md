# Guía de Contribución — AI-SDLC Pro Prompts

## Requisitos previos

- Python 3.8+
- Git configurado con [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/)
- Acceso al repositorio con rama `main` como base

---

## Convención de nombres de archivo

Los prompts siguen el esquema `{sec}-{sub}-{nombre}.md`:

| Segmento | Descripción | Ejemplo |
|----------|-------------|---------|
| `{sec}` | Número de sección con cero (00–12) | `04` |
| `{sub}` | Número de subsección con cero (01–99) | `04` |
| `{nombre}` | Kebab-case descriptivo | `adr-decisiones-arquitectura` |

**Ejemplo completo:** `04-04-adr-decisiones-arquitectura.md`

Secciones activas:

| Prefijo | Grupo |
|---------|-------|
| `00-` | Framework general |
| `00-B-` | Comprensión de repositorio |
| `00-C-` | Análisis de procesos |
| `01-` → `12-` | Fases SDLC (Análisis → CI/CD → Documentación → …) |

---

## Formato de un prompt

Cada archivo `.md` debe seguir esta estructura mínima:

```markdown
# Título del Prompt

## Descripción

Breve descripción del propósito y cuándo usar este prompt (2-4 oraciones).

## Prompt

```text
[Contenido del prompt aquí. Usar {{VARIABLE}} para variables sustituibles.]
```

## Variables (opcional)

| Variable | Descripción |
|----------|-------------|
| `{{REPO}}` | URL o nombre del repositorio |
| `{{TECH_STACK}}` | Stack tecnológico del proyecto |

## Usa el prompt (opcional)

Fórmula o ejemplo de uso contextualizado.
```

Reglas:
- El bloque de prompt **siempre** dentro de ` ```text ``` `
- Variables en formato `{{NOMBRE_VARIABLE}}` — en MAYÚSCULAS con guiones bajos
- Sin frontmatter YAML (no se usa en este proyecto)
- Encoding UTF-8, saltos de línea LF

---

## Flujo de contribución

```
prompt nuevo → build.py → verify_clean.py → commit → push → CI auto-despliega
```

### Paso a paso

1. **Crear o editar** el archivo `.md` en `ai_sdlc_pro_prompts/`
2. **Regenerar** el sitio estático:
   ```bash
   python build.py
   ```
3. **Validar** que no hay placeholders sin resolver:
   ```bash
   python verify_clean.py
   # Debe terminar con exit code 0
   ```
4. **Commit** usando Conventional Commits:
   ```bash
   git add ai_sdlc_pro_prompts/<archivo>.md index.html
   git commit -m "feat(prompts): agregar prompt 04-04 ADR decisiones de arquitectura"
   ```
5. **Push** a `main`:
   ```bash
   git push origin main
   ```
6. **CI/CD** ejecuta automáticamente:
   - QA gate: `build.py` + `verify_clean.py`
   - Deploy a GitHub Pages (staging)
   - Deploy a GCP production (`prompts.lionsystems.com.mx`)

> **Nunca editar `index.html` directamente.** Siempre usar `build.py` como fuente de verdad.

---

## Tipos de commit (Conventional Commits)

| Tipo | Cuándo usar |
|------|-------------|
| `feat(prompts)` | Nuevo prompt o grupo de prompts |
| `fix(prompts)` | Corrección de contenido en un prompt existente |
| `docs` | README, CHANGELOG, CONTRIBUTING u otra documentación |
| `ci` | Cambios en `.github/workflows/` |
| `ops` | Configuración de servidor (Nginx, crones, etc.) |
| `refactor` | Cambios en `build.py` o `verify_clean.py` sin cambio de comportamiento |
| `fix(security)` | Correcciones de seguridad (CSP, SSH, dependencias) |

### Formato

```
<tipo>(<scope>): <descripción imperativa en minúsculas> (ID-riesgo si aplica)

[Cuerpo opcional: qué, por qué, cómo]
[Breaking changes si aplica]
```

---

## Checklist antes de hacer PR / merge

- [ ] `python build.py` termina sin errores
- [ ] `python verify_clean.py` termina con exit 0
- [ ] El nuevo prompt tiene título, descripción y bloque `text`
- [ ] El nombre de archivo sigue la convención `{sec}-{sub}-{nombre}.md`
- [ ] `CHANGELOG.md` actualizado si el cambio es visible para el usuario
- [ ] README actualizado si cambia el conteo de prompts o secciones

---

## Preguntas frecuentes

**¿Puedo añadir imágenes o assets?**  
No. El sitio es 100% self-contained (`index.html` único). Los prompts son solo texto Markdown.

**¿Cómo proponer un nuevo grupo/sección?**  
Abrir una discusión en GitHub Issues con el prefijo `[PROPUESTA]` antes de implementar.

**¿Quién aprueba los cambios?**  
El equipo de LionSystems revisa y aprueba todos los PRs. Contacto: contacto@lionsystems.com.mx
