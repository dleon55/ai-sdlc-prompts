# Changelog — AI-SDLC Pro

Todos los cambios notables de este proyecto están documentados aquí.  
Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/).  
Este proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

---

## [Unreleased]

### Fixed
- Grafo de "siguiente prompt recomendado": `04-01-diseno-solucion` ahora también recomienda `04-06-diseno-contrato-api`/`04-07-diseno-modelo-datos`, `02-05-analisis-integral-requerimientos` ahora también recomienda `02-07-matriz-trazabilidad-requerimientos`, y `07-00-deteccion-stack-pruebas` ahora también recomienda `07-15-plan-maestro-pruebas` — los 3 eran enlaces unidireccionales reales (el prompt downstream los declaraba como entrada, pero nunca eran recomendados como siguiente paso desde el upstream), detectados en una auditoría de metodología/consistencia cruzada.
- `13-05-dast-analisis-dinamico-seguridad` era un huérfano real en el grafo de recomendaciones (ningún prompt lo recomendaba como siguiente paso, a diferencia de SAST) — ahora `13-03-secure-sdlc-revision` lo recomienda cuando detecta que faltan pruebas DAST.
- `updateLivePreview()`: ahora filtra por el idioma activo en vez de resolver los 228 bloques de código (114 x ES/EN) en cada tecla del panel de variables — medido en ~20-31ms mediana, picos de ~57-77ms antes del fix (por encima del presupuesto de 16ms/60fps). `setLanguage()` fuerza un refresco completo al cambiar de idioma para que el idioma recién activado quede al día.
- Elimina código muerto detectado en la auditoría de eficiencia: el panel flotante de variables de proyecto (`renderProjFloat()`/`toggleProjFloat()`/`closeProjFloat()`, nunca emitido en el HTML generado) y el `<select id="proj-selector">` permanentemente oculto (`style="display:none"`, sin forma de que un usuario real lo interactúe).

### Added
- `11-15-plan-recuperacion-desastres-continuidad` (113 → 114 prompts): plan de recuperación ante desastres y continuidad de negocio (DR/BCP) — validación de RTO/RPO objetivo vs. capacidad real, secuencia de recuperación de dependencias críticas, procedimiento de failover, cadencia de pruebas de backup-restore y criterios de activación/failback. Distinto de `11-04-incident-response` (incidente ya en curso de alcance acotado) y de `11-09-runbook-rollback` (reversión de un solo despliegue reciente) — cierra la última brecha real detectada en una nueva ronda de auditoría de completitud tras el cierre de #137-#141.
- Seis prompts nuevos cerrando la auditoría final de completitud de la biblioteca (107 → 113 prompts): `00-D-05-viabilidad-business-case` (estudio de viabilidad y business case previo al Project Charter — técnica, económica, operativa y legal/regulatoria, con recomendación go/no-go), `02-07-matriz-trazabilidad-requerimientos` (matriz de trazabilidad agregada de todo el proyecto, requerimiento → diseño → implementación → prueba, distinta del cumplimiento por issue de `08-02`), `13-09-dpia-privacidad-datos` (evaluación de impacto de privacidad de datos, base legal, derechos del titular y retención, distinta del threat modeling de seguridad de `13-04`), `10-05-documentacion-api-publica` (documentación de referencia para desarrolladores externos, distinta del diseño de contrato de `04-06` y de la documentación técnica interna de `10-01`), `10-06-materiales-capacitacion-rollout` (materiales de capacitación y plan de rollout para usuarios finales, distinto del onboarding técnico interno de `17-01`), y `17-07-revision-exito-post-lanzamiento` (revisión de realización de beneficios contra los KPIs del Project Charter, semanas/meses después del lanzamiento, distinta del postmortem de incidentes de `11-07` y del reporte de estado en vivo de `17-06`).
- Fase 4 (final) de la capa de gestión de proyecto (issue #138): modo guiado / ruta de proyecto. Nuevo modal ("🧭" junto al selector de proyecto) que recorre paso a paso el orden curado del framework (00-D → 01 → 02 → ... → 17, el mismo en que ya se generan las secciones) con botones Anterior/Siguiente, un atajo "Ir al primero no usado" para retomar donde se quedó, y el estado de uso (✓) de cada paso tomado de la Fase 1. Decisión de diseño documentada: la ruta NO deriva un orden del grafo de "siguiente prompt recomendado" (puede tener ramas o ciclos, ej. el enrutamiento dinámico de `12-orquestador`, sin un único "siguiente" sin una heurística arbitraria) — ese enlace sigue disponible como atajo paralelo dentro del modal ⓘ de cada prompt. Cierra el backlog completo de gestión de proyecto abierto en #137-#140.
- Fases 2 y 3 de la capa de gestión de proyecto (issues #137, #140): personalización por proyecto y guardado de resultados de IA. En el modal ⓘ de cada prompt, dos campos nuevos de texto libre por (proyecto, prompt): "Adiciones personalizadas" (#137, `custom_additions`), que se anexan al final del prompt ya resuelto **solo al copiarlo** — nunca modifican el texto canónico del prompt en el repositorio; y "Resultado de la IA para este proyecto" (#140, `ai_output`), almacenamiento puro de lo que el usuario pega tras ejecutar el prompt en su agente — la herramienta nunca invoca ningún modelo de IA. Ambos con el mismo patrón de auto-guardado (`localStorage` + sync a Supabase con sesión) y sin pisarse entre sí ni con el estado de progreso de la Fase 1. Export/import de proyectos sube a `ai_sdlc_export_version: 2` para incluir este estado; exports v1 previos se siguen importando sin cambios.
- Fase 1 de la capa de gestión de proyecto (issue #139): checklist de progreso por proyecto. Cada copia de un prompt marca automáticamente `used_at` (primera vez únicamente, no se pisa en copias repetidas) en `project_prompt_state`; el panel de variables muestra una barra de progreso agregada ("X / 107 prompts usados en este proyecto") y el modal de información ⓘ de cada prompt muestra su estado de uso en el proyecto activo con un botón para marcar/desmarcar manualmente (por si el prompt se ejecutó fuera de la herramienta). Sincroniza con Supabase solo si hay sesión, mismo patrón fire-and-forget que `trackPromptCopy()`; funciona igual en modo anónimo con `localStorage`. Base para el modo guiado (#138), que reutilizará este mismo estado.
- Fase 0 de la capa de gestión de proyecto (issues #137, #138, #139, #140): nueva tabla `project_prompt_state` (`supabase/project_prompt_state.sql`) con estado por (proyecto, prompt) — `used_at` para el checklist de progreso (#139), `custom_additions` para personalización aditiva sin tocar el prompt canónico (#137), `ai_output` para guardar resultados de IA pegados manualmente (#140). RLS por relación indirecta con `projects.user_id` (esta tabla no tiene columna `user_id` propia). Sin cambios de UI todavía — es solo el esquema base; requiere ejecutarse una vez en el SQL Editor de Supabase, igual que `schema.sql`/`trial_gate.sql`/`subscriptions.sql`.
- `11-14-migracion-cutover-plataforma` (106 → 107 prompts): plan de migración y cutover de un sistema/plataforma/stack antiguo a uno nuevo (estrategia de datos big-bang vs. incremental, dual-write, verificación de consistencia, cutover progresivo con rollback por etapa). Cierra el hueco entre el diseño de arquitectura (`00-D-02`/`04-01`) y el decomiso del sistema origen (`11-11`), y es distinto de `08-05` que solo revisa la seguridad de un cambio de esquema de BD ya escrito. Issue #141.
- Cuatro prompts nuevos para cerrar brechas adicionales de cobertura del ciclo de vida del proyecto (102 → 106 prompts), detectadas en una segunda pasada de auditoría más allá de las 9 categorías originales: `00-D-04-registro-riesgos-proyecto` (registro de riesgos de todo el proyecto en formato RAID — riesgos, supuestos, incidentes y dependencias — distinto del análisis de riesgos por feature de `05-02`), `04-06-diseno-contrato-api` (diseño de contrato de API nueva desde cero: catálogo de endpoints con esquemas de request/response y matriz de errores, distinto de `04-05` que solo versiona/depreca una API ya existente), `04-07-diseno-modelo-datos` (diseño detallado de esquema de base de datos: entidades, relaciones, normalización e índices justificados por patrón de consulta, distinto del esbozo de alto nivel de `00-D-02` y de la revisión de seguridad de migraciones de `08-05`), y `07-15-plan-maestro-pruebas` (estrategia de QA de todo el proyecto: niveles de prueba, cobertura objetivo, criterios de entrada/salida, distinto de la detección de stack de `07-00` y del diseño por tipo de prueba de `07-01`-`07-14`).
- Dos prompts nuevos para cerrar brechas de cobertura del ciclo de vida del proyecto (100 → 102 prompts): `02-06-requerimientos-no-funcionales` (catálogo de RNF — rendimiento, disponibilidad, escalabilidad, seguridad, usabilidad, mantenibilidad, portabilidad y compliance — con umbral medible y método de verificación por requerimiento) y `00-D-03-plan-trabajo-proyecto` (plan de trabajo de todo el proyecto: EDT/WBS, estimación, dependencias, cronograma con ruta crítica y asignación de recursos, distinto del plan de implementación por feature de `05-01`).
- Muro de registro + prueba de 1 semana + renovación por feedback: un visitante anónimo puede copiar 10 prompts libremente (contados por IP en Supabase, no por `localStorage`, acumulados de por vida); al 11vo intento se exige iniciar sesión con GitHub, lo que activa 1 semana de acceso completo. Al vencer, se bloquea la copia hasta enviar una breve retroalimentación (calificación 1-5 + comentario), que renueva otra semana al instante. Fail-open ante cualquier error de red o de configuración pendiente — nunca bloquea a un usuario real por una falla transitoria. Ver `docs/trial-gate-setup.md` y `supabase/trial_gate.sql`. (Nota: el modelo original de esta sección, aún sin desplegar entonces, era de 2 copias / 1 mes; se ajustó a 10 copias / 1 semana antes del piloto, para tener un ciclo de retroalimentación más frecuente.)
- Página `/precios.html`: explica el periodo de prueba vigente (10 copias gratis, 1 semana con registro, renovable por feedback) sin comprometerse a precios fijos todavía — los planes de pago se decidirán con datos reales del piloto.
- Suscripción de pago vía Paddle Billing ($1 USD/mes introductorio): un usuario logueado puede suscribirse desde `/precios.html`; una Supabase Edge Function (`supabase/functions/paddle-webhook/`) recibe y verifica la firma HMAC del webhook de Paddle y actualiza la tabla `subscriptions` (RLS sin políticas de escritura de cliente, mismo patrón que `user_trial`). `check_trial_status()` revisa suscripción activa antes que el estado de la prueba gratuita, dando acceso ilimitado sin tocar el código del cliente. Desplegado automáticamente vía CI (job `deploy-supabase-function`). Ver `docs/paddle-integration.md`.
- Indicador de administrador "prompts más copiados": nueva tabla `prompt_copy_stats` y función `track_prompt_copy()` (security definer, sin políticas de cliente) que registra qué prompts se copian más, sin afectar el flujo de copiado (fire-and-forget). Alimenta el criterio de activación de la Fase 2 (issue #7: gate Free/Pro por prompt, aún no implementada). Ver `supabase/prompt_copy_stats.sql`.
- Registro de usuarios opcional vía Supabase Auth + GitHub OAuth, sin backend propio: sincroniza proyectos/variables entre dispositivos para quien inicia sesión, mientras el uso anónimo con `localStorage` sigue funcionando exactamente igual. Configurado y activo en producción (ver `docs/auth-setup.md` y `supabase/schema.sql`); si `SUPABASE_URL`/`SUPABASE_ANON_KEY` volvieran al centinela `PENDIENTE_CONFIGURAR`, la función queda inerte de nuevo sin ninguna petición de red nueva.
- Panel de variables: amplía los catálogos de compliance y metodología, permite selección múltiple y admite valores personalizados mediante “Otro”.
- Panel de variables: agrega `Workspace / subproyecto`, `Estándar / compliance`, `Documentos a revisar` y `Nivel de profundidad`.
- Panel de variables: agrega `Entrada principal`, `Objetivo específico` y `Responsable / assignee`, con migración automática de proyectos guardados.
- Panel de variables: agrega asignaciones adicionales `TOKEN=valor` para configurar placeholders específicos sin soporte canónico.
- Copiado: detecta placeholders pendientes y muestra una advertencia sin bloquear la copia.
- Pruebas de contrato para evitar campos sin UI, alias ambiguos y regresiones en prompts de triage y análisis de requerimientos.

### Fixed
- `resolvePrompt()`: corrige doble sustitución cruzada entre variables — si el valor de un campo contenía literalmente el placeholder de otro campo procesado después (ej. `repositorio = "mi-repo [STACK]"`), ese texto recién insertado volvía a sustituirse, corrompiendo silenciosamente el valor del usuario. La sustitución ahora ocurre en una sola pasada de regex sobre el texto original, nunca sobre texto ya sustituido.
- `resolvePrompt()`: corrige un falso bloqueo de "placeholder obligatorio sin resolver" cuando un campo requerido se llenaba con un valor idéntico a su propio token (ej. `entrada = "[ENTRADA PRINCIPAL]"`) — la detección de placeholders sin resolver para campos conocidos ahora se basa en si el campo quedó vacío, no en re-escanear el texto ya sustituido.
- Panel de variables: al borrar el proyecto **activo**, el panel ahora se resincroniza con el proyecto sobreviviente (`syncPanelToProject()`) — antes seguía mostrando los valores del proyecto recién eliminado, y editar cualquier campo después sobrescribía silenciosamente las variables del proyecto que sí sobrevivió.
- GitHub Pages: agrega `404.html` (copia de `index.html`) al artefacto publicado — el botón principal de la landing (`href="/app"`, ruteo client-side) devolvía un 404 real de GitHub Pages por falta de rewrite, aunque funcionaba correctamente en producción (GCP/Nginx con `try_files`).
- Modal de modo guiado (🧭): ahora cierra con Escape y con clic fuera del modal, igual que el resto de los overlays — quedó fuera de ambos mecanismos al agregarse después de que se escribiera ese código compartido.
- Barra flotante de multi-select (`.ms-bar`): ya no se corta en los bordes en viewports móviles (~375px) — el contador de seleccionados y el botón "Limpiar selección" quedaban inalcanzables.
- Onboarding: el paso 5 (captura de email) ahora es bilingüe ES/EN — antes era el único paso solo en español, rompiendo la paridad justo en el paso más accionable del wizard.
- Selector de nivel de autonomía y chips de filtro A0-A3: el selector de variables ahora antepone el código (`A0 — solo análisis`, etc.) y los chips de filtro tienen un `title` explicando cada código — antes solo se explicaban una vez en el modal de onboarding, sin forma de consultarlos después.
- Modal de gestión de proyectos: el botón de eliminar ahora tiene color distintivo en reposo (antes solo cambiaba de color al pasar el mouse encima, igual que las demás acciones no destructivas).
- Panel de variables: muestra opciones explícitas de compliance y alinea las etiquetas de objetivo puntual y profundidad con la fórmula del framework.
- Framework `00`: usa tokens configurables independientes y evita reutilizar `tipo de proyecto` como workspace o `componentes` como documentos.
- `02-02` Análisis técnico profundo: elimina contenido duplicado y corrige la referencia del diseño de solución de `02-04` a `04-01`.
- Refuerza el análisis de código existente con preflight Git, alcance explícito, evidencia trazable, flujo por capas, contratos, datos, seguridad, observabilidad, pruebas y riesgos.
- Mantiene paridad funcional entre las versiones en español e inglés y regenera `index.html`.
- Variables: evita sustituciones semánticamente incorrectas de tokens genéricos como `[NOMBRE]`, `[TIPO]`, `[NIVEL]`, `[SEVERIDAD]` e `[INDICAR]`.
- Copiado: conserva el módulo configurado por el usuario en lugar de sobrescribirlo siempre con el título del prompt.
- Prompts `02-04` y `02-05`: normaliza sus entradas a variables configurables desde la interfaz.
- Multi-select: la selección por sección y el contador ya no duplican los prompts. Cada prompt renderiza una card ES y otra EN (ocultas por CSS) con el mismo `data-pid`; ahora la selección se acota al idioma visible y el copiado deduplica por `pid`, evitando que "seleccionar toda la sección" copie cada prompt dos veces y deje el checkbox de sección atascado en estado indeterminado.
- Copiado: la advertencia de placeholders pendientes ahora también detecta alias que empiezan en minúscula (p. ej. `[ej. Python + FastAPI + PostgreSQL / ...]`, `[frontend SPA / API REST / ...]`), que el regex previo (exigía mayúscula inicial) dejaba pasar sin aviso.
- Índice del framework `00-framework.md` / `00-framework.en.md`: se completa con los 10 prompts faltantes en ES (`07-12`, `08-04`, `11-07`, `11-08`, secciones 14 y 15, `02-05`) y se reconstruye el índice EN, que omitía 30 prompts (secciones 13, 14, 15, `00-D` y varios de 07/10/11). Ambos catálogos listan ahora los 75 prompts.
- `README.md`: corrige el conteo (64 → 75 prompts, 17 → 19 grupos), agrega las secciones 14 y 15 a la tabla, actualiza los conteos de las secciones 02/07/08/11 y el tamaño del artefacto `index.html`.

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
