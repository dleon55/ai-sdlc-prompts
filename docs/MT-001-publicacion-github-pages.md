# MT-001 — Publicación de AI-SDLC Pro en GitHub Pages con CI/CD

| Campo | Valor |
|---|---|
| **ID** | MT-001 |
| **Tipo** | Infraestructura / DevOps |
| **Fecha** | 2026-04-10 |
| **Autor** | David León Gómez (dleon55) |
| **Repositorio** | https://github.com/dleon55/ai-sdlc-prompts |
| **Commit** | `513891d50d01a0b45c2bb1d7a0b0c319a1c05c83` |
| **Rama** | `main` |
| **Ambiente** | GitHub Pages (producción pública gratuita) |
| **Estado** | Completado ✓ |

---

## 1. Contexto

El proyecto **AI-SDLC Pro** es una biblioteca de prompts de ingeniería de software estructurados bajo un framework empresarial. Los prompts están redactados en Markdown (33 archivos en `ai_sdlc_pro_prompts/`) y se consolidan en un único `index.html` interactivo mediante el script `build.py`.

El código residía localmente en:
```
C:\Users\dleon\OneDrive\Documentos\GitHub\www-lionsystems-odoo\WEB_PROMPTS\
```

No tenía repositorio git, ni pipeline de publicación, ni URL pública.

---

## 2. Requerimiento

**Publicar el sitio web `index.html` en un entorno de desarrollo accesible públicamente**, sin costo y sin afectar el servidor de producción de LionSystems, usando GitHub como plataforma de hospedaje.

URL objetivo: subdominio bajo `github.io` (ambiente dev gratuito), con posibilidad de mapear un dominio personalizado (`prompts-dev.lionsystems.com.mx`) en el futuro.

---

## 3. Análisis

### 3.1 Hechos confirmados previos al cambio

- El directorio `WEB_PROMPTS/` **no tenía repositorio git** (`fatal: not a git repository`).
- La cuenta `dleon55` tiene autenticación GH CLI activa con scopes completos (`repo`, `workflow`, `pages`, etc.).
- El script `build.py` genera `index.html` desde los archivos `.md` de `ai_sdlc_pro_prompts/`.
- Ya existía un `index.html` pre-generado en el directorio.

### 3.2 Hallazgos

- No existía ningún workflow de CI/CD.
- No existía `.gitignore` — archivos temporales (`_tmp_check.js`, `_analysis.txt`) quedaban expuestos.
- No existía `README.md` — ausencia de documentación del proyecto.
- GitHub Pages con `build_type: workflow` requiere que el sitio esté habilitado **antes** del primer push para que el primer run de deploy funcione.

### 3.3 Supuestos

- El `build.py` es estable y puede ejecutarse en Ubuntu 22.04 (runner de GitHub Actions) sin dependencias externas.
- No se requiere autenticación ni back-end — el sitio es totalmente estático.
- La rama principal de trabajo es `main`.

---

## 4. Solución implementada

### 4.1 Arquitectura final

```
Desarrollador
    │
    │  git push origin main
    ▼
GitHub Repository: dleon55/ai-sdlc-prompts
    │
    ▼
GitHub Actions — Workflow: "Build & Deploy AI-SDLC Prompts"
    │
    ├─── Job: build (ubuntu-latest)
    │       ├── actions/checkout@v4
    │       ├── actions/setup-python@v5 (Python 3.11)
    │       ├── python build.py  → genera index.html
    │       ├── cp index.html dist/
    │       └── actions/upload-pages-artifact@v3 (path: dist/)
    │
    └─── Job: deploy (depende de build)
            └── actions/deploy-pages@v4
                    └── Publicación en GitHub Pages
                            URL: https://dleon55.github.io/ai-sdlc-prompts/
```

### 4.2 Componentes creados

| Archivo | Rol | Descripción |
|---|---|---|
| `.github/workflows/deploy.yml` | CI/CD | Workflow de build + deploy en GitHub Actions |
| `.gitignore` | Control de versión | Excluye temporales, `dist/`, `__pycache__` |
| `README.md` | Documentación | Estructura del proyecto, instrucciones de desarrollo y contribución |
| `docs/MT-001-publicacion-github-pages.md` | Memoria técnica | Este documento |

### 4.3 Repositorio GitHub

| Propiedad | Valor |
|---|---|
| Nombre | `ai-sdlc-prompts` |
| Propietario | `dleon55` |
| Visibilidad | **Public** |
| Rama por defecto | `main` |
| Creado | 2026-04-11T00:34:54Z |
| URL | https://github.com/dleon55/ai-sdlc-prompts |

### 4.4 GitHub Pages

| Propiedad | Valor |
|---|---|
| `build_type` | `workflow` (GitHub Actions como source) |
| `html_url` | https://dleon55.github.io/ai-sdlc-prompts/ |
| `https_enforced` | `true` |
| `cname` | `null` (sin dominio personalizado aún) |
| `source.branch` | `main` |

---

## 5. Detalle del Workflow (`.github/workflows/deploy.yml`)

```yaml
on:
  push:
    branches: [main]    # disparo automático en cada push a main
  workflow_dispatch:    # disparo manual desde la UI de GitHub

permissions:
  contents: read
  pages: write          # permiso para escribir en GitHub Pages
  id-token: write       # requerido por OIDC (deploy-pages)

concurrency:
  group: "pages"
  cancel-in-progress: false   # no cancela deploys en curso
```

**Job `build`:**
1. `actions/checkout@v4` — descarga el código
2. `actions/setup-python@v5` (Python 3.11) — configura entorno
3. `python build.py` — genera `index.html` desde los `.md`
4. Copia `index.html` a `dist/`
5. `actions/upload-pages-artifact@v3` — empaqueta `dist/` como artefacto de Pages

**Job `deploy`:**
- Depende del job `build` (`needs: build`)
- Usa environment `github-pages` (requerido por la acción `deploy-pages`)
- `actions/deploy-pages@v4` — publica el artefacto en la CDN de GitHub Pages
- Expone la URL final en `steps.deployment.outputs.page_url`

---

## 6. Comandos gh CLI utilizados

```bash
# 1. Crear repositorio público
gh repo create dleon55/ai-sdlc-prompts \
  --public \
  --description "AI-SDLC Pro — Biblioteca de Prompts de Ingeniería de Software"

# 2. Habilitar GitHub Pages con GitHub Actions como source
gh api repos/dleon55/ai-sdlc-prompts/pages \
  --method POST \
  --field build_type=workflow

# 3. Re-ejecutar run fallido (primer push fue anterior a habilitar Pages)
gh run rerun 24270545629 --repo dleon55/ai-sdlc-prompts

# 4. Verificar estado del run
gh run list --repo dleon55/ai-sdlc-prompts --limit 3
```

---

## 7. Secuencia de comandos git

```bash
cd WEB_PROMPTS/

git init
git remote add origin https://github.com/dleon55/ai-sdlc-prompts.git
git add .
git commit -m "feat: initial commit — AI-SDLC Pro prompt library + GitHub Pages CI/CD"
git branch -M main
git push -u origin main
```

---

## 8. Pruebas ejecutadas

| # | Prueba | Método | Resultado |
|---|---|---|---|
| 1 | Autenticación GH CLI | `gh auth status` | ✓ Logged in como `dleon55` |
| 2 | Creación de repositorio | `gh repo create` | ✓ Repo creado en https://github.com/dleon55/ai-sdlc-prompts |
| 3 | Push y CI | `git push` + `gh run list` | ✓ Workflow disparado automáticamente |
| 4 | Habilitación de Pages | `gh api .../pages` | ✓ `html_url` confirmada, `https_enforced: true` |
| 5 | Re-run tras habilitar Pages | `gh run rerun` | ✓ Run exitoso (27s, status: passed) |
| 6 | Sitio público | Browser / API | ✓ https://dleon55.github.io/ai-sdlc-prompts/ activo |

---

## 9. Matriz de riesgos

| # | Riesgo | Categoría | Prob. | Impacto | Mitigación | Contingencia |
|---|---|---|---|---|---|---|
| R1 | `build.py` falla en Linux por path o encoding | Técnico | Baja | Alto | Usar `pathlib.Path`, probar localmente en WSL antes de push | Agregar step de `pip install` si se añaden dependencias |
| R2 | Límite de espacio en Pages (1 GB) | Operación | Muy baja | Medio | El sitio es estático (<2 MB) | Migrar a Cloudflare Pages si supera límite |
| R3 | GitHub Pages se hace privado o de pago | Negocio | Muy baja | Alto | Sitio público gratuito en repo público — política estable | Cloudflare Pages, Netlify o Vercel como alternativas equivalentes |
| R4 | Conflicto de concurrencia en CI | CI/CD | Baja | Bajo | `concurrency: cancel-in-progress: false` — no se cancelan deploys en curso | Revisar runs con `gh run list` antes de push |
| R5 | Tokens OIDC expirados | Seguridad | Baja | Medio | Tokens ephemeral generados por `id-token: write` — estándar GitHub | Re-ejecutar run manualmente |

---

## 10. Resultados

- **Repositorio creado y operativo:** https://github.com/dleon55/ai-sdlc-prompts
- **Sitio en vivo:** https://dleon55.github.io/ai-sdlc-prompts/
- **CI/CD funcional:** cada `git push origin main` regenera y publica el sitio automáticamente
- **Build exitoso:** 39 archivos, 6127 líneas, run completado en 27 segundos
- **HTTPS habilitado** sin configuración adicional
- **Sin costo:** GitHub Pages gratuito en repositorio público

---

## 11. Puntos pendientes

| # | Ítem | Prioridad | Responsable |
|---|---|---|---|
| P1 | Configurar dominio personalizado `prompts-dev.lionsystems.com.mx` via CNAME + `gh api` | Media | dleon55 |
| P2 | Agregar `CODEOWNERS` para proteger ramas | Baja | dleon55 |
| P3 | Agregar step de linting/validación de Markdown antes del build | Baja | DevOps |
| P4 | Configurar Branch Protection Rule en `main` (require PR + CI verde) | Media | dleon55 |
| P5 | Agregar badge de estado del workflow en el README | Baja | dleon55 |

---

## 12. Cómo agregar dominio personalizado (P1)

Cuando se quiera activar `prompts-dev.lionsystems.com.mx`:

**Paso 1 — DNS:** agregar registro CNAME en el proveedor DNS:
```
prompts-dev.lionsystems.com.mx  →  dleon55.github.io
```

**Paso 2 — GitHub:**
```bash
gh api repos/dleon55/ai-sdlc-prompts/pages \
  --method PUT \
  -f cname="prompts-dev.lionsystems.com.mx"
```

**Paso 3 — Verificar** en `https://github.com/dleon55/ai-sdlc-prompts/settings/pages` que el dominio esté verificado y HTTPS activo.

---

## 13. Cómo contribuir / flujo de trabajo

```
1. git pull origin main          # siempre partir del estado más reciente
2. Editar .md en ai_sdlc_pro_prompts/
3. python build.py               # validar localmente
4. git add . && git commit -m "feat: descripción del cambio"
5. git push origin main          # el CI construye y despliega en ~30 segundos
```

---

*Generado por: GitHub Copilot (Claude Sonnet 4.6) bajo framework AI-SDLC Pro — MT-001*
