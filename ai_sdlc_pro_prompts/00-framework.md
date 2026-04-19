# AI-SDLC ENTERPRISE FRAMEWORK

## Descripción

Este framework define el **principio operativo obligatorio** que se debe incluir al inicio de cualquier prompt de la biblioteca. Establece el rol, el contexto multi-agente y las reglas de ingeniería que rigen todo trabajo dentro del repositorio.

---

## Principio operativo obligatorio para todos los prompts

> Pega este bloque al inicio de cualquier prompt antes de ejecutarlo.

```text
Actúa como un Ingeniero en Sistemas Computacionales, Ingeniero de Software Senior, Arquitecto de Soluciones, Analista Técnico-Funcional, DBA, Server Administrator y especialista en QA, DevOps y DevSecOps, con experiencia práctica en PSP, RUP, ITIL, SCRUM, CI/CD, GitHub, Docker, Linux, arquitectura cloud y desarrollo full stack.

Estás operando en un entorno multi-agente bajo Open Agent Manager. Otros agentes pueden estar trabajando en paralelo sobre el mismo repositorio y el mismo espacio de trabajo.

Reglas obligatorias:
1. Antes de cualquier análisis o cambio, revisa la documentación, procesos, procedimientos, políticas, estándares y lineamientos del proyecto.
2. No asumas que el estado del repositorio es estático.
3. Antes de trabajar:
   - revisa cambios recientes,
   - identifica ramas activas,
   - detecta posibles conflictos con otros agentes.
4. Todo trabajo debe ser controlado, trazable y con commits atómicos.
5. No sobrescribas cambios ajenos sin validar.
6. Sigue el ciclo de ingeniería de software del proyecto.
7. Todo entregable debe distinguir claramente:
   - hechos confirmados,
   - hallazgos,
   - supuestos,
   - riesgos,
   - recomendaciones.
8. Si falta documentación, indícalo y usa buenas prácticas de ingeniería.
9. No implementes primero y pienses después: primero analiza, luego diseña, luego ejecuta, luego valida y documenta.
10. Mantén consistencia con la arquitectura, convenciones, políticas y estándares del repositorio.
```

---

## Cómo usar esta biblioteca de prompts

Usa esta fórmula para obtener mejores resultados al invocar cualquier prompt:

```text
Quiero que uses el prompt de [NOMBRE DEL PROCESO] y lo adaptes a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA ACTUAL]
- ambiente: [DEV / QA / PROD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: [RUTAS DE ARCHIVOS...]
- objetivo puntual de salida: [INDICAR]
- nivel de profundidad: [NIVEL]
```

### Ejemplo real

```text
Usa el prompt de análisis de causa raíz y adáptalo a:
- repositorio: urgemy-api
- issue: #842
- rama: urgemy-test
- ambiente: QA
- componentes: api, notificaciones push, postgres
- documentos a revisar: README, docs/notificaciones, workflows, issues relacionados
- objetivo puntual: confirmar causa raíz y proponer plan de solución
- nivel de profundidad: alto
```

---

## Índice de prompts disponibles

| Archivo | Sección | Propósito |
|---|---|---|
| **── CONFIGURACIÓN DE REPOSITORIO (00-B)** | | |
| `00-B-01-scaffolding-repositorio.md` | 0-B.1 | Estructura base del repositorio: directorios, archivos raíz, .github/, docs/ |
| `00-B-02-gobernanza-ia-agentes.md` | 0-B.2 | Archivos de gobierno para agentes IA: copilot-instructions, .windsurfrules, AGENTS.md |
| `00-B-03-github-configuracion.md` | 0-B.3 | Configuración GitHub: branch protection, issue templates, PR template, Dependabot |
| `00-B-04-metodologia-framework.md` | 0-B.4 | Selección de metodología, branching strategy, Definition of Ready y Done |
| `00-B-05-stack-calidad-codigo.md` | 0-B.5 | Stack y calidad: linters, formatters, pre-commit hooks, quality gates CI |
| **── GOBERNANZA DE AGENTES IA (00-C)** | | |
| `00-C-01-issue-para-agente-ia.md` | 0-C.1 | Issue estructurado listo para ejecución por agente IA con criterios y restricciones |
| `00-C-02-plan-mode-multiagente.md` | 0-C.2 | Modo plan seguro (sin cambios) y protocolo de coordinación multi-agente |
| `00-C-03-configuracion-por-agente.md` | 0-C.3 | Configuración específica por agente: Copilot, Claude, Codex, Windsurf, Cursor, Antigravity |
| **── CICLO DE INGENIERÍA DE SOFTWARE (01–12)** | | |
| `01-01-arranque-comprension-repositorio.md` | 1.1 | Inventario técnico del repositorio |
| `01-02-analisis-procesos.md` | 1.2 | Localizar procesos, políticas y estándares |
| `02-01-analisis-issue.md` | 2.1 | Análisis funcional de requerimiento o issue |
| `02-02-analisis-tecnico.md` | 2.2 | Análisis técnico profundo de código existente |
| `02-03-impacto-cruzado.md` | 2.3 | Análisis de impacto cruzado en todos los módulos |
| `03-01-incidentes-github.md` | 3.1 | Revisión de incidentes de tester contra GitHub Issues |
| `03-02-causa-raiz.md` | 3.2 | Análisis de causa raíz de defectos e incidentes |
| `04-01-diseno-solucion.md` | 4.1 | Diseño funcional y técnico de solución |
| `04-02-diagramas-mermaid.md` | 4.2 | Generación de diagramas Mermaid |
| `04-03-casos-de-uso.md` | 4.3 | Diseño y documentación formal de casos de uso |
| `04-04-adr-decisiones-arquitectura.md` | 4.4 | Architecture Decision Records (ADR) |
| `05-01-plan-implementacion.md` | 5.1 | Plan de implementación detallado y trazable |
| `05-02-riesgos-implementacion.md` | 5.2 | Análisis de riesgos e impacto de implementación |
| `06-01-implementacion-multiagente.md` | 6.1 | Implementación multi-agente segura y controlada |
| `06-02-commits.md` | 6.2 | Generación de mensajes de commit de calidad |
| `07-00-deteccion-stack-pruebas.md` | 7.0 | Detección del stack de pruebas del proyecto — genera perfil reutilizable |
| `07-01-pruebas-unitarias.md` | 7.1 | Diseño de pruebas unitarias |
| `07-02-pruebas-integracion.md` | 7.2 | Diseño de pruebas de integración |
| `07-03-pruebas-e2e.md` | 7.3 | Diseño de pruebas E2E |
| `07-04-pruebas-humo.md` | 7.4 | Plan de pruebas de humo |
| `07-05-automatizacion-antigravity.md` | 7.5 | Automatización en navegador con Chrome Antigravity |
| `07-06-pruebas-performance-carga.md` | 7.6 | Pruebas de performance, carga e stress |
| `07-07-implementacion-pruebas-unitarias.md` | 7.7 | Implementación de código de pruebas unitarias ejecutables |
| `07-08-implementacion-pruebas-integracion.md` | 7.8 | Implementación de código de pruebas de integración ejecutables |
| `07-09-implementacion-pruebas-e2e.md` | 7.9 | Implementación de scripts E2E ejecutables |
| `07-10-implementacion-pruebas-humo.md` | 7.10 | Implementación de script de smoke test ejecutable en pipeline |
| `08-01-revision-estatica.md` | 8.1 | Revisión estática de código |
| `08-02-cumplimiento-requerimiento.md` | 8.2 | Revisión de cumplimiento contra requerimiento |
| `08-03-remediacion-maestro.md` | 8.3 | Prompt maestro de remediación de revisión estática |
| `09-01-integracion-ramas.md` | 9.1 | Integración controlada con ramas |
| `09-02-monitoreo-ci.md` | 9.2 | Monitoreo de CI local y remoto |
| `09-03-workflows-github-actions.md` | 9.3 | Revisión de workflows de GitHub Actions |
| `09-04-promotion-checklist.md` | 9.4 | Checklist de promoción entre ambientes (dev→staging→prod) |
| `10-01-documentacion-tecnica.md` | 10.1 | Actualizar documentación técnica |
| `10-02-memoria-tecnica.md` | 10.2 | Memoria técnica del cambio |
| `10-03-release-changelog.md` | 10.3 | Documentación de release o changelog |
| `11-01-troubleshooting.md` | 11.1 | Troubleshooting de ambiente |
| `11-02-hardening-seguridad.md` | 11.2 | Hardening y seguridad operativa |
| `11-03-deuda-tecnica.md` | 11.3 | Deuda técnica y mejora continua |
| `11-04-incident-response.md` | 11.4 | Runbook de incident response en producción |
| `12-orquestador.md` | 12 | Prompt maestro orquestador del ciclo completo |

**── SEGURIDAD Y DEVSECOPS (13)**

| `13-01-sast-analisis-seguridad-codigo.md` | 13.1 | Análisis estático de seguridad (SAST) — OWASP Top 10 |
| `13-02-sca-analisis-dependencias.md` | 13.2 | Análisis de composición de software (SCA) — CVEs en dependencias |
| `13-03-secure-sdlc-revision.md` | 13.3 | Revisión Secure SDLC — OWASP SAMM / NIST SSDF |
| `13-04-threat-modeling.md` | 13.4 | Modelado de amenazas — metodología STRIDE |
| `13-07-gestion-vulnerabilidades-cves.md` | 13.7 | Gestión del ciclo de vida de vulnerabilidades y CVEs |

---

## Principios del framework

- Trabajo obligatorio por fases (analiza → diseña → ejecuta → valida → documenta)
- Separación de responsabilidades por agente
- Commits atómicos y trazables
- CI/CD obligatorio antes de integrar
- No implementación sin diseño previo aprobado
- Control de concurrencia en entornos multi-agente
- Todo entregable distingue hechos, hallazgos, supuestos, riesgos y recomendaciones

## Reglas críticas

- git pull antes de trabajar
- no sobrescribir cambios
- detener ante conflictos
- trazabilidad completa
