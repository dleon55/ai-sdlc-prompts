# Changelog — AI-SDLC Pro

Todos los cambios notables de este proyecto están documentados aquí.  
Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/).  
Este proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

---

## [1.9.2] — 2026-04-22

### Changed
- UX/UI: nuevo acceso flotante de **Variables rápidas** para editar las variables más usadas sin regresar al inicio del scroll
- `build.py`: sincronización bidireccional entre panel completo y acceso rápido, manteniendo el contrato actual basado en `localStorage`
- `build.py`: el CTA del panel cambia de **“Aplicar al copiar”** a **“Listo”** para reflejar que las variables ya se guardan automáticamente

## [1.9.1] — 2026-04-22

### Added
- **2 nuevos prompts — Triage de backlog GitHub Issues** (1 tema × ES+EN):
  - `02-04` — Triage y planificación de backlog de GitHub Issues: análisis de issues filtrados por componente, responsable, label o estatus pendiente; normalización, categorización, priorización, dependencias, riesgos y plan de atención con tareas, responsables y entregables
- Ejemplos de entrada listos para usar con `gh issue list` y con exportaciones JSON/CSV/tabla de issues

### Changed
- `README.md`: conteo actualizado a **64 prompts / 17 grupos** (antes 63/17)
- `README.md`: sección `02` actualizada para reflejar el nuevo prompt de triage de backlog
- `00-framework.md` y `00-framework.en.md`: índice actualizado con la entrada `02-04`

## [1.9.0] — 2026-04-19

### Added
- **4 nuevos prompts — Priority 4: Definición de proyecto (sección 00-D)** (2 temas × ES+EN):
  - `00-D-01` — Project Charter: documento fundacional del proyecto — objetivos SMART, alcance IN/OUT, stakeholders, entregables con criterios de aceptación, hitos, presupuesto, riesgos iniciales, modelo de gobierno y firmas
  - `00-D-02` — Stack y Arquitectura Inicial: selección justificada de tecnologías por capa, topología de infraestructura con diagrama Mermaid C4, patrones arquitectónicos, modelo de datos, seguridad por diseño, estrategia de escalabilidad/resiliencia, deuda técnica anticipada y plan de evolución
- Todos los prompts incluyen versión bilingüe (ES + EN)
- `00-framework.md` actualizado con sección `── DEFINICIÓN DE PROYECTO (00-D)` y entradas 00-D-01, 00-D-02

## [1.8.0] — 2026-04-19

### Added
- **6 nuevos prompts — Priority 3: Observabilidad, Performance en producción, Patch Management** (3 temas × ES+EN):
  - `10-04` — Observabilidad / Instrumentación: pilares RED+USE métricas, logs estructurados, trazas distribuidas, SLOs con error budget, alertas accionables, diseño de dashboards y stack OpenTelemetry
  - `11-05` — Performance en producción: diagnóstico por capa (app/BD/caché/red), análisis de trazas y logs, profiling seguro, plan de optimización priorizado (tabla PERF-XXX), mejoras estructurales
  - `11-06` — Gestión de parches y actualizaciones: inventario por gestor de paquetes/contenedores/SO, matriz de prioridad semver × categoría, plan de aplicación por entorno con rollback, auditoría y automatización preventiva (Dependabot/Renovate)
- Todos los prompts incluyen versión bilingüe (ES + EN)
- `00-framework.md` actualizado con 10-04, 11-05, 11-06

## [1.7.0] — 2026-04-19

### Added
- **8 nuevos prompts — Priority 2: DAST, Pentesting, Secrets, Performance** (4 temas × ES+EN):
  - `13-05` — DAST / Análisis Dinámico de Seguridad: superficie de ataque, transporte TLS, autenticación/sesión, inyección, control de acceso, exposición de información
  - `13-06` — Ethical Hacking / Pentesting: alcance y reglas de compromiso, reconocimiento OSINT, explotación controlada, cadenas de ataque, informe técnico + resumen ejecutivo
  - `13-08` — Gestión de Secretos y Credenciales: detección en código/historial/CI-CD, clasificación, evaluación de prácticas, plan de remediación, política de rotación
  - `07-11` — Implementación de pruebas de performance: scripts ejecutables k6/Locust/JMeter/Artillery para load/stress/spike/soak/benchmark con thresholds codificados e integración CI/CD
- Todos los prompts incluyen versión bilingüe (ES + EN)
- `00-framework.md` actualizado con 07-11, 13-05, 13-06, 13-08

## [1.6.0] — 2026-04-19

### Added
- **5 nuevos prompts — Sección 13: Seguridad y DevSecOps** (nueva sección AppSec — Priority 1):
  - `13-01` — SAST / Análisis estático de seguridad de código: revisión OWASP Top 10, herramientas recomendadas por lenguaje, tabla de hallazgos con CVSS
  - `13-02` — SCA / Análisis de composición de software: inventario de dependencias, CVEs, riesgos de licencia, cadena de suministro
  - `13-03` — Revisión Secure SDLC: checklist OWASP SAMM / NIST SSDF / MS SDL por fase del ciclo de desarrollo
  - `13-04` — Modelado de amenazas — STRIDE: DFD, árbol de ataques, tabla de amenazas con vector CVSS y mitigación
  - `13-07` — Gestión de vulnerabilidades y CVEs: triage, puntuación CVSS v3.1, análisis de explotabilidad (KEV/EPSS), backlog de seguridad, métricas MTTD/MTTR
- Nueva sección `13` registrada en `build.py` (SECTION_META, SECTION_LABEL, SECTION_COLOR, ICON_PATH)
- Todos los prompts incluyen versión bilingüe (ES + EN)

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
