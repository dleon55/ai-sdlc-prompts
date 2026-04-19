# Changelog — AI-SDLC Pro

Todos los cambios notables de este proyecto están documentados aquí.  
Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/).  
Este proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

---

## [1.5.0] — 2026-04-18

### Added
- **5 nuevos prompts — Fase 7: Implementación de pruebas** (ciclo SDLC completo):
  - `07-00` — Detección de stack de pruebas: genera perfil reutilizable del framework de pruebas del proyecto (frameworks, convenciones, CI/CD, estado actual)
  - `07-07` — Implementación de pruebas unitarias: genera código ejecutable AAA a partir del diseño `07-01`
  - `07-08` — Implementación de pruebas de integración: genera código ejecutable con fixtures/containers a partir del diseño `07-02`
  - `07-09` — Implementación de pruebas E2E: genera scripts automatizados (Playwright/Cypress/Selenium) a partir del diseño `07-03`
  - `07-10` — Implementación de smoke tests: genera script ejecutable en pipeline (< 15 min) a partir del diseño `07-04`
- Todos los prompts incluyen versión bilingüe (ES + EN)
- Prompts `07-07` al `07-10` referencian obligatoriamente el perfil de `07-00` como contexto previo

### Changed
- `00-framework.md`: índice actualizado con entradas 7.0 — 7.10 (5 nuevas filas)
- `README.md`: conteo actualizado a **49 prompts / 15 grupos** (antes 44/15)

### Notes
- Los prompts `07-01` al `07-04` (diseño de pruebas) permanecen sin cambios
- El grupo 07-Pruebas ahora cubre el ciclo completo: Diseño → Detección de stack → Implementación
- Flujo recomendado: `07-00` (una vez por proyecto) → `07-0x` Diseño → `07-0x+6` Implementación

---

## [1.4.0] — 2026-04-11

### Added
- **Onboarding guiado**: welcome banner + overlay de bienvenida con guía de primeros pasos (pasos 1-4)
  - Dismissable — se guarda en `localStorage` (`AI_SDLC_v1_onboarded`)
  - Responsive: adaptado para móvil/tablet
- **4 nuevos prompts**:
  - `04-04` — Architecture Decision Records (ADR) con plantilla numerada ADR-NNN
  - `07-06` — Pruebas de performance/carga (load, stress, spike, soak) + scripts k6
  - `09-04` — Promotion checklist: dev → staging → prod con go/no-go y rollback
  - `11-04` — Runbook de incident response SEV1-4, escalación, post-mortem blameless
- **Pipeline CI/CD dual** en `.github/workflows/deploy.yml`:
  - Job `build`: Python 3.11 + QA gate (`verify_clean.py`) + artefacto compartido
  - Job `deploy-pages`: GitHub Pages (ambiente de staging/pruebas)
  - Job `deploy-gcp`: Producción GCP vía SSH/SCP (requiere secrets `GCP_SSH_KEY`, `GCP_HOST`, `GCP_USER`, `GCP_PORT`)
  - `concurrency: deploy-main` — previene deploys paralelos

### Fixed
- 6 bugs en `renderProjectsModal()` / sincronización JS↔HTML del onboarding
- CSS: clases del onboarding alineadas con estructura HTML

### Changed
- README: conteo actualizado a **45 prompts / 15 grupos** (antes 33/12)
- README: sección de funcionalidades actualizada con 12 variables de panel y onboarding
- `00-framework.md`: índice actualizado con 4 nuevas entradas

---

## [1.3.0] — 2026-04-10

### Added
- Panel de variables extendido con campos adicionales: **stack tecnológico** y **configuración de agentes IA**
  - Campos nuevos integrados en el sistema de proyectos (`AI_SDLC_v1_projects`)
  - Variables disponibles para sustitución en prompts de la sección 00-B y 00-C
- `verify_clean.py` integrado al pipeline CI como QA gate (step "Validate prompts")
  - Ahora emite `sys.exit(1)` ante prompts contaminados — el CI falla correctamente

### Fixed
- `StrictHostKeyChecking=no` → `StrictHostKeyChecking=accept-new` en `deploy-to-gcp.sh` (3 ocurrencias) — mitigación MITM
- `verify_clean.py` excluido incorrectamente de git tracking — removido de `.gitignore`

---

## [1.2.0] — 2026-04-10

### Added
- **Sistema de Proyectos** (estilo Postman/Codex): múltiples proyectos con sets de variables independientes
  - CRUD completo: crear, renombrar, eliminar, duplicar, establecer como default
  - Quick-switcher `<select>` en la cabecera del panel de variables
  - Modal de gestión de proyectos (botón ⚙)
  - Persistencia en `localStorage` (`AI_SDLC_v1_projects`, `AI_SDLC_v1_active`)
- **Despliegue GCP Producción**: `https://prompts.lionsystems.com.mx`
  - Servidor Nginx 1.22.1 en GCP (`34.51.112.6:2288`)
  - TLS/HTTPS con Let's Encrypt (Certbot, auto-renew — expira 2026-07-10)
  - Security headers: `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`
  - HTTP 301 → HTTPS redirect
- `deploy-to-gcp.sh` — script reproducible de re-despliegue manual
- `nginx_prompts.conf` — configuración Nginx versionada en el repositorio

### Fixed
- `SyntaxError: Unexpected string` (línea 151 del JS embebido): `\'` en Python triple-quoted string se consumía como secuencia de escape, generando `''` adyacentes en el JS → todo el JS del sitio dejaba de funcionar. **Fix:** `\'` → `\\'` en 5 líneas de `renderProjectsModal()`.

### Changed
- `getVarValues()` ahora lee desde `getActiveProject().vars` (localStorage) en lugar del DOM
- `clearVars()` ahora limpia sólo `project.vars` del proyecto activo, no los inputs del DOM directamente

---

## [1.1.0] — 2026-04-10

### Added
- Sidebar colapsable (toggle hamburger)
- Diseño responsive para móvil/tablet
- Secciones de framework nuevas:
  - `00-B` — Scaffolding de repositorio
  - `00-C` — Gobernanza multi-agente IA
- `docs/MT-001-publicacion-github-pages.md` — primera memoria técnica (arquitectura GitHub Pages + CI/CD)

### Changed
- Sidebar: navegación con scroll posicional mejorado

---

## [1.0.0] — 2026-04-10

### Added
- **33 prompts** organizados en **12 secciones** del ciclo SDLC:
  - 00-Framework, 01-Arranque, 02-Análisis, 03-Implementación, 04-Pruebas, 05-CI/CD, 06-Integración, 07-Documentación, 08-Incidentes, 09-Orquestador, 10-Remediación
- `build.py` — generador Python → `index.html` autocontenido (sin CDN, sin dependencias externas)
- Panel de variables con 7 campos: `{{REPO}}`, `{{ISSUE}}`, `{{STACK}}`, `{{EQUIPO}}`, `{{PRIORIDAD}}`, `{{MODULO}}`, `{{CONTEXTO}}`
- Botón "Copiar prompt" con sustitución de variables
- Modo multi-selección para copiar varios prompts concatenados
- Barra de búsqueda / filtro de prompts en tiempo real
- Modal ⓘ de información con contexto de uso por prompt
- Campo fórmula en prompts (bloques "Usa el prompt" separados del texto limpio)
- GitHub Pages CI/CD via `.github/workflows/deploy.yml`
- `verify_clean.py` — script de validación: 0 prompts contaminados con marcadores de uso
- `extract_vars.py` — análisis de tokens y variables por sección
