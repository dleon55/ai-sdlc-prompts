# AI-SDLC Pro — Biblioteca de Prompts de Ingeniería de Software

Biblioteca interactiva de prompts estructurados bajo el **AI-SDLC Enterprise Framework**: 33 prompts organizados en 12 secciones que cubren el ciclo completo de ingeniería de software.

## Entornos activos

| Entorno | URL | Plataforma | Estado |
|---|---|---|---|
| **Producción** | https://prompts.lionsystems.com.mx | GCP Nginx + TLS | ✅ Live |
| **GitHub Pages** | https://dleon55.github.io/ai-sdlc-prompts | GitHub Pages CI/CD | ✅ Live |

---

## Funcionalidades del sitio

- **Proyectos con variables por entorno** — múltiples proyectos, cada uno con su set de 7 variables (`repositorio`, `issue`, `rama actual`, `rama destino`, `ambiente`, `componentes`, `módulo`). Variables persisten en `localStorage`.
- **Framework auto-prepend** — el bloque de contexto del framework se antepone automáticamente a cada prompt copiado.
- **Multi-select** — selección de varios prompts para copiarlos en bloque.
- **Búsqueda/filtrado** — filtro en tiempo real por texto.
- **Modal de información ⓘ** — descripción y fórmulas de uso de cada prompt sin contaminar el contenido del prompt.
- **Sidebar colapsable** — navegación por sección.
- **Diseño oscuro responsive** (self-contained, sin CDN).

---

## Estructura del proyecto

```
ai_sdlc_pro_prompts/    # 33 fuentes Markdown de cada prompt
build.py                # Generador: produce index.html desde los .md
extract_vars.py         # Analiza tokens [PLACEHOLDER] en los prompts
verify_clean.py         # Valida prompts limpios + cuenta info buttons
nginx_prompts.conf      # Config Nginx para producción GCP
deploy-to-gcp.sh        # Script de re-deploy manual a GCP
index.html              # Artefacto generado (no editar manualmente)
docs/                   # Memorias técnicas y documentación
.github/workflows/      # CI/CD — build + deploy automático a GitHub Pages
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

| # | Sección | Prompts |
|---|---|---|
| 00 | Framework base (obligatorio — se antepone en cada copia) | 1 |
| 01 | Comprensión del repositorio | 2 |
| 02 | Análisis | 3 |
| 03 | Incidentes | 2 |
| 04 | Diseño de solución | 3 |
| 05 | Plan de implementación | 2 |
| 06 | Ejecución | 2 |
| 07 | Pruebas | 5 |
| 08 | Revisión y remediación | 3 |
| 09 | Integración y CI/CD | 3 |
| 10 | Documentación | 3 |
| 11 | Operaciones | 3 |
| 12 | Orquestador maestro | 1 |

---

## Documentación técnica

| Documento | Descripción |
|---|---|
| [docs/MT-001](docs/MT-001-publicacion-github-pages.md) | Memoria técnica — publicación GitHub Pages con CI/CD |
| [docs/MT-002](docs/MT-002-feature-proyectos-gcp-deploy.md) | Memoria técnica — feature Proyectos + despliegue GCP |
| [CHANGELOG.md](CHANGELOG.md) | Historial de cambios por versión |

---

> Parte del stack AI-SDLC Enterprise — LionSystems © 2026
