# AI-SDLC Pro — Biblioteca de Prompts de Ingeniería de Software

Biblioteca interactiva de prompts estructurados bajo el **AI-SDLC Enterprise Framework**: **45 prompts** organizados en **15 grupos** que cubren el ciclo completo de ingeniería de software asistida por IA.

## Entornos activos

| Entorno | URL | Plataforma | Estado |
|---|---|---|---|
| **Producción** | https://prompts.lionsystems.com.mx | GCP Nginx + TLS | ✅ Live |
| **GitHub Pages** | https://dleon55.github.io/ai-sdlc-prompts | GitHub Pages CI/CD | ✅ Live |

---

## Funcionalidades del sitio

- **Proyectos con variables por entorno** — múltiples proyectos, cada uno con **12 variables** (`repositorio`, `issue`, `rama actual/destino`, `ambiente`, `componentes`, `módulo`, `stack`, `tipo de proyecto`, `metodología`, `agentes IA`, `nivel de autonomía`). Variables persisten en `localStorage`.
- **Framework auto-prepend** — el bloque de contexto del framework se antepone automáticamente a cada prompt copiado.
- **Onboarding guiado** — banner + overlay de bienvenida para nuevos usuarios con guía de primeros pasos.
- **Multi-select** — selección de varios prompts para copiarlos en bloque.
- **Búsqueda/filtrado** — filtro en tiempo real por texto.
- **Modal de información ⓘ** — descripción y fórmulas de uso de cada prompt sin contaminar el contenido del prompt.
- **Sidebar colapsable** — navegación por sección.
- **Diseño oscuro responsive** (self-contained, sin CDN).

---

## Estructura del proyecto

```
ai_sdlc_pro_prompts/    # 45 fuentes Markdown (15 grupos, ciclo SDLC completo)
build.py                # Generador: produce index.html desde los .md
extract_vars.py         # Analiza tokens [PLACEHOLDER] en los prompts
verify_clean.py         # QA gate: valida prompts limpios (integrado en CI)
nginx_prompts.conf      # Config Nginx para producción GCP
deploy-to-gcp.sh        # Script de re-deploy manual a GCP
index.html              # Artefacto generado (~255 KB, no editar manualmente)
docs/                   # Memorias técnicas (MT-001, MT-002)
.github/workflows/      # CI/CD — build + QA gate + deploy GitHub Pages + GCP
CONTRIBUTING.md         # Guía de contribución y convenciones
LICENSE                 # Licencia del proyecto
```

---

## Desarrollo local

```bash
# Regenerar index.html
python build.py

# Validar prompts limpios
python verify_clean.py

# Ver el sitio (Live Server en VSCode o doble clic)
# index.html se abre en el navegador — funciona sin servidor
```

---

## Despliegue a producción (GCP)

```bash
# 1. Regenerar
python build.py

# 2. Subir al servidor
bash deploy-to-gcp.sh

# 3. Registrar cambio
git add -A && git commit -m "feat: descripcion" && git push origin main
```

El push a `main` también actualiza GitHub Pages automáticamente vía el workflow `.github/workflows/deploy.yml`.

---

## Agregar un nuevo prompt

1. Crea `ai_sdlc_pro_prompts/XX-YY-nombre-del-prompt.md` siguiendo el patrón existente.
2. Ejecuta `python build.py` y verifica localmente.
3. Ejecuta `python verify_clean.py` — debe reportar 0 prompts contaminados.
4. `git push origin main` — CI/CD despliega a GitHub Pages automáticamente.
5. `bash deploy-to-gcp.sh` — actualiza producción GCP.

---

## Secciones de prompts

| Grupo | Sección | Prompts |
|---|---|---|
| 00 | Framework base (obligatorio — se antepone en cada copia) | 1 |
| 00-B | Scaffolding: repositorio, gobernanza, GitHub, metodología, stack | 5 |
| 00-C | Multi-agente: issues para IA, plan mode, configuración por agente | 3 |
| 01 | Comprensión del repositorio | 2 |
| 02 | Análisis (issue, técnico, impacto cruzado) | 3 |
| 03 | Incidentes (GitHub, causa raíz) | 2 |
| 04 | Diseño de solución (diseño, Mermaid, casos de uso, ADR) | 4 |
| 05 | Plan de implementación (plan, riesgos) | 2 |
| 06 | Ejecución (multi-agente, commits) | 2 |
| 07 | Pruebas (unitarias, integración, E2E, humo, automatización, performance) | 6 |
| 08 | Revisión y remediación (estática, cumplimiento, maestro) | 3 |
| 09 | Integración y CI/CD (ramas, monitoreo, workflows, promotion) | 4 |
| 10 | Documentación (técnica, memoria, changelog) | 3 |
| 11 | Operaciones (troubleshooting, hardening, deuda técnica, incident response) | 4 |
| 12 | Orquestador maestro (ciclo completo) | 1 |
| **Total** | | **45** |

---

## Documentación técnica

| Documento | Descripción |
|---|---|
| [docs/MT-001](docs/MT-001-publicacion-github-pages.md) | Memoria técnica — publicación GitHub Pages con CI/CD |
| [docs/MT-002](docs/MT-002-feature-proyectos-gcp-deploy.md) | Memoria técnica — feature Proyectos + despliegue GCP |
| [CHANGELOG.md](CHANGELOG.md) | Historial de cambios por versión |

---

> Parte del stack AI-SDLC Enterprise — LionSystems © 2026
