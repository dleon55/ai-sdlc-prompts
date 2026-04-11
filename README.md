# AI-SDLC Pro — Biblioteca de Prompts

Biblioteca interactiva de prompts de ingeniería de software para equipos que trabajan bajo el framework AI-SDLC Enterprise.

**Sitio en vivo:** https://dleon55.github.io/ai-sdlc-prompts

---

## Estructura del proyecto

```
ai_sdlc_pro_prompts/    # Fuentes Markdown de cada prompt
build.py                # Genera index.html desde los .md
extract_vars.py         # Extrae variables {{VAR}} de los prompts
index.html              # Artefacto generado (no editar manualmente)
.github/workflows/      # CI/CD — build + deploy a GitHub Pages
```

## Desarrollo local

```bash
python build.py         # Regenera index.html
# Abrir index.html en el navegador
```

## Agregar un nuevo prompt

1. Crea un archivo `.md` en `ai_sdlc_pro_prompts/` con el naming `XX-YY-nombre.md`
2. Ejecuta `python build.py` para verificar localmente
3. Haz `git push` a `main` — el CI construye y despliega automáticamente

## Secciones disponibles

| # | Sección |
|---|---------|
| 00 | Framework base (obligatorio) |
| 01 | Comprensión del repositorio |
| 02 | Análisis |
| 03 | Incidentes |
| 04 | Diseño de solución |
| 05 | Plan de implementación |
| 06 | Ejecución |
| 07 | Pruebas |
| 08 | Revisión y remediación |
| 09 | Integración y CI/CD |
| 10 | Documentación |
| 11 | Operaciones |
| 12 | Orquestador |

---

> Parte del stack AI-SDLC Enterprise — LionSystems
