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
- repositorio:
- issue o requerimiento:
- rama:
- ambiente:
- componentes:
- documentos a revisar:
- objetivo puntual de salida:
- nivel de profundidad:
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
| `05-01-plan-implementacion.md` | 5.1 | Plan de implementación detallado y trazable |
| `05-02-riesgos-implementacion.md` | 5.2 | Análisis de riesgos e impacto de implementación |
| `06-01-implementacion-multiagente.md` | 6.1 | Implementación multi-agente segura y controlada |
| `06-02-commits.md` | 6.2 | Generación de mensajes de commit de calidad |
| `07-01-pruebas-unitarias.md` | 7.1 | Diseño de pruebas unitarias |
| `07-02-pruebas-integracion.md` | 7.2 | Diseño de pruebas de integración |
| `07-03-pruebas-e2e.md` | 7.3 | Diseño de pruebas E2E |
| `07-04-pruebas-humo.md` | 7.4 | Plan de pruebas de humo |
| `07-05-automatizacion-antigravity.md` | 7.5 | Automatización en navegador con Chrome Antigravity |
| `08-01-revision-estatica.md` | 8.1 | Revisión estática de código |
| `08-02-cumplimiento-requerimiento.md` | 8.2 | Revisión de cumplimiento contra requerimiento |
| `08-03-remediacion-maestro.md` | 8.3 | Prompt maestro de remediación de revisión estática |
| `09-01-integracion-ramas.md` | 9.1 | Integración controlada con ramas |
| `09-02-monitoreo-ci.md` | 9.2 | Monitoreo de CI local y remoto |
| `09-03-workflows-github-actions.md` | 9.3 | Revisión de workflows de GitHub Actions |
| `10-01-documentacion-tecnica.md` | 10.1 | Actualizar documentación técnica |
| `10-02-memoria-tecnica.md` | 10.2 | Memoria técnica del cambio |
| `10-03-release-changelog.md` | 10.3 | Documentación de release o changelog |
| `11-01-troubleshooting.md` | 11.1 | Troubleshooting de ambiente |
| `11-02-hardening-seguridad.md` | 11.2 | Hardening y seguridad operativa |
| `11-03-deuda-tecnica.md` | 11.3 | Deuda técnica y mejora continua |
| `12-orquestador.md` | 12 | Prompt maestro orquestador del ciclo completo |

---

## Principios del framework

- Trabajo obligatorio por fases (analiza → diseña → ejecuta → valida → documenta)
- Separación de responsabilidades por agente
- Commits atómicos y trazables
- CI/CD obligatorio antes de integrar
- No implementación sin diseño previo aprobado
- Control de concurrencia en entornos multi-agente
- Todo entregable distingue hechos, hallazgos, supuestos, riesgos y recomendaciones
5. Integración
6. Monitoreo

## Reglas críticas

- git pull antes de trabajar
- no sobrescribir cambios
- detener ante conflictos
- trazabilidad completa
