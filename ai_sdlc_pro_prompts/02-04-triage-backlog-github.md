# 2.4 — Triage y planificación de backlog de GitHub Issues

## Descripción

Prompt compuesto para analizar un conjunto de issues de GitHub del repositorio actual o de un repositorio objetivo, filtrados por componente, responsable, labels o estatus pendiente. Sirve para clasificar el backlog, detectar agrupaciones lógicas, priorizar la atención y proponer un plan de implementación o remediación alineado con la metodología, arquitectura y estándares del proyecto.

**Cuándo usarlo:** cuando se necesita revisar issues abiertos o pendientes como cartera de trabajo, ordenar su atención por prioridad o componente, o preparar un plan maestro de ejecución para un sprint, remediación o estabilización.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — el resultado influye en la priorización y asignación real de trabajo de un equipo; una consolidación o recomendación de cierre sin evidencia puede descartar issues válidos, aunque el prompt no cierra ni modifica issues por sí mismo |
| Entradas requeridas | fuente de issues (por ejemplo, salida JSON de `gh issue list`), filtro aplicado, criterio de backlog pendiente, componente o responsable objetivo, rama y ambiente objetivo, documentos a revisar |
| Herramientas permitidas | lectura de issues, PRs, ramas y documentación mediante consultas de solo lectura (`gh issue list` u equivalente) — sin cerrar, etiquetar, asignar ni modificar issues |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | no proponer cierre de issues sin evidencia; si la información de un issue no basta para clasificarlo con precisión, declararlo como supuesto y reducir el nivel de confianza en vez de asignarle prioridad definitiva |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada fila de la matriz de issues normalizados debe ser trazable a datos reales de GitHub (número, estado, labels, assignee) citados |
| Siguiente prompt recomendado | `05-01-plan-implementacion` para los issues listos para implementar; `02-01-analisis-issue` para los que requieren aclaración funcional |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza el backlog de GitHub Issues asociado al repositorio indicado y genera un diagnóstico estructurado, una categorización útil para gestión y un plan de atención priorizado, controlado y trazable.

Contexto:
- El trabajo ocurre en entorno multi-agente.
- No asumas que el estado del repositorio, ramas o issues es estático.
- Antes de emitir recomendaciones, considera documentación, procesos, ramas activas, CI/CD, riesgos de concurrencia y dependencias entre issues.

Entradas:
- repositorio: [NOMBRE O URL]
- fuente de issues: [ENTRADA PRINCIPAL]
- filtro aplicado: [OBJETIVO ESPECÍFICO]
- criterio de backlog pendiente: [open / open sin PR / blocked / ready / triage pendiente / otro]
- componente o área objetivo: [COMPONENTES INVOLUCRADOS]
- usuario responsable o assignee: [RESPONSABLE]
- rama objetivo: [RAMA OBJETIVO]
- ambiente objetivo: [DEV / QA / STAGING / PROD]
- documentos a revisar: [README, docs/, arquitectura, workflows, issues relacionados]

Actividades:
1. Validar el contexto:
   - revisar documentación, procesos, políticas, estándares y lineamientos del proyecto;
   - revisar cambios recientes, ramas activas y posibles conflictos con otros agentes;
   - detectar si existen PRs o ramas relacionadas con alguno de los issues analizados.

2. Normalizar la entrada:
   - convertir cada issue a una ficha homogénea con:
     - número,
     - título,
     - estado,
     - labels,
     - milestone,
     - assignee,
     - componente o módulo inferido,
     - tipo de trabajo,
     - severidad o criticidad inferida,
     - dependencia con otros issues,
     - evidencia de bloqueo o espera,
     - relación con PR o rama si existe.

3. Clasificar cada issue por categoría:
   - bug,
   - incidente,
   - requerimiento,
   - mejora,
   - deuda técnica,
   - pruebas / QA,
   - documentación,
   - seguridad / DevSecOps,
   - infraestructura / CI/CD / operación,
   - análisis pendiente,
   - definición funcional faltante.

4. Clasificar cada issue por estado de atención:
   - listo para analizar,
   - requiere aclaración funcional,
   - requiere análisis técnico,
   - bloqueado por dependencia,
   - bloqueado por ambiente,
   - bloqueado por otra rama / PR,
   - listo para implementar,
   - listo para validar,
   - candidato a cierre,
   - duplicado / consolidable.

5. Evaluar prioridad real de atención considerando:
   - impacto al negocio o usuario,
   - criticidad técnica,
   - riesgo de regresión,
   - riesgo operativo,
   - riesgo de seguridad,
   - dependencia con otros issues,
   - esfuerzo estimado,
   - urgencia del ambiente objetivo,
   - existencia de workaround.

6. Identificar agrupaciones y oportunidades de consolidación:
   - issues del mismo componente,
   - issues del mismo flujo funcional,
   - issues de misma causa raíz,
   - issues que deberían atenderse juntos en un solo plan,
   - issues que deben separarse para mantener commits atómicos y bajo riesgo.

7. Proponer orden de atención:
   - primero quick wins seguros,
   - luego bloqueadores funcionales o técnicos,
   - después dependencias estructurales,
   - finalmente mejoras de menor urgencia.

8. Para cada issue o grupo de issues priorizado, proponer:
   - objetivo de atención,
   - alcance,
   - componente afectado,
   - precondiciones,
   - tareas,
   - responsable sugerido por rol,
   - entregables,
   - validaciones,
   - riesgos,
   - recomendación de estrategia de rama / integración.

9. Si detectas falta de información, documenta exactamente qué falta:
   - descripción insuficiente,
   - criterios de aceptación ausentes,
   - componente ambiguo,
   - prioridad no sustentada,
   - dependencia no explicitada,
   - issue que debería dividirse o consolidarse.

10. Si la fuente es `gh issue list`, asume que la salida puede venir cruda o resumida. Si la información no basta para clasificar con precisión, indícalo como supuesto y reduce el nivel de confianza.

Restricciones:
- no propongas cerrar, fusionar o re-etiquetar ningún issue sin indicar explícitamente la evidencia y el razonamiento que sustenta esa recomendación — la decisión final la toma un humano,
- no asignes prioridad alta o crítica sin evidencia concreta (datos de uso, incidentes reportados, impacto de negocio declarado por quien solicita el cambio); si esa evidencia no existe, dilo explícitamente y baja el nivel de confianza en vez de inventarla,
- si detectas issues que parecen duplicados o solapados, no los fusiones ni los descartes silenciosamente: márcalos de forma explícita como "posible duplicado de #N" en la matriz y en los hallazgos, y deja la decisión de consolidación a un humano,
- no inventes dependencias entre issues que no estén documentadas o razonablemente inferibles del contenido real revisado.

Formato de salida obligatorio:
1. Resumen ejecutivo
2. Hechos confirmados
3. Hallazgos
4. Supuestos
5. Riesgos
6. Matriz de issues normalizados
7. Categorización por componente / responsable / prioridad / estado de atención
8. Dependencias y conflictos potenciales
9. Plan de atención o remediación
10. Recomendaciones finales

Formato esperado dentro de la salida:

### Matriz de issues normalizados
| Issue | Título | Estado GH | Componente | Assignee | Tipo | Prioridad | Estado de atención | Dependencias | Observaciones |
|---|---|---|---|---|---|---|---|---|---|

### Categorización por componente
| Componente | Issues | Severidad dominante | Riesgo agregado | Recomendación |
|---|---|---|---|---|

### Categorización por responsable
| Responsable actual | Issues asignados | Estado general | Riesgo de carga | Acción sugerida |
|---|---|---|---|---|

### Plan de atención o remediación
| Orden | Issue o grupo | Prioridad | Objetivo | Tareas clave | Responsable sugerido | Entregables | Dependencias | Riesgos | Validación |
|---|---|---|---|---|---|---|---|---|---|

### Backlog ejecutable sugerido
| Fase | Alcance | Issues incluidos | Resultado esperado |
|---|---|---|---|
| 1 | Quick wins / bajo riesgo | | |
| 2 | Bloqueadores funcionales o técnicos | | |
| 3 | Remediación estructural | | |
| 4 | Mejoras y hardening | | |

Reglas de decisión:
- No mezclar en un mismo bloque de ejecución issues sin dependencia real.
- No proponer cerrar issues sin evidencia.
- No proponer implementación si primero falta análisis funcional o técnico.
- Cuando existan varios issues similares, indicar si conviene:
  - consolidarlos bajo un epic o issue maestro,
  - mantenerlos separados,
  - relacionarlos por dependencia.
- Distinguir siempre entre hechos confirmados y clasificación inferida.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de triage y planificación de backlog de GitHub Issues y adáptalo a:
- repositorio: [NOMBRE O URL]
- fuente de issues: [ENTRADA PRINCIPAL]
- filtro aplicado: [OBJETIVO ESPECÍFICO]
- criterio de pendiente: [open / blocked / sin PR asociado / triage pendiente]
- componente objetivo: [COMPONENTES INVOLUCRADOS]
- responsable objetivo: [RESPONSABLE]
- rama objetivo: [RAMA OBJETIVO]
- ambiente: [DEV / QA / STAGING / PROD]
- documentos a revisar: README, docs/, arquitectura, workflows, PRs e issues relacionados
- objetivo puntual de salida: backlog categorizado y plan de atención con prioridades, tareas, responsables y entregables
- nivel de profundidad: alto
```

```text
Ejemplo con gh issue list:
gh issue list \
  --repo [ORG/REPO] \
  --state open \
  --limit 200 \
  --json number,title,body,labels,assignees,milestone,state,createdAt,updatedAt,url
```

```text
Ejemplo de invocación al agente:
Usa el prompt de triage y planificación de backlog de GitHub Issues y adáptalo a:
- repositorio: [ORG/REPO]
- fuente de issues: [PEGAR JSON DE gh issue list]
- filtro aplicado: assignee + componente
- criterio de pendiente: open sin PR asociado
- componente objetivo: [COMPONENTE]
- responsable objetivo: [USUARIO]
- rama objetivo: main
- ambiente: QA
- documentos a revisar: README, docs/, workflows, arquitectura, issues relacionados
- objetivo puntual de salida: matriz priorizada y plan de atención por fases
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Resumen ejecutivo | Panorama del backlog pendiente y recomendación de atención |
| Hechos confirmados | Datos explícitos obtenidos de issues, ramas, PRs y documentación |
| Hallazgos | Patrones, agrupaciones, vacíos, sobrecarga o desorden detectado |
| Supuestos | Inferencias realizadas por falta de datos completos |
| Riesgos | Riesgos funcionales, técnicos, operativos, de seguridad y concurrencia |
| Matriz de issues | Inventario normalizado y clasificado |
| Categorización | Vista por componente, responsable, prioridad y estado de atención |
| Dependencias | Bloqueos, secuencia y consolidaciones recomendadas |
| Plan de atención | Orden, prioridades, tareas, responsables y entregables |
| Recomendaciones finales | Decisiones sugeridas para ejecución y gobierno del backlog |

### Ejemplo — matriz de issues normalizados (extracto)

| Issue | Título | Estado GH | Componente | Assignee | Tipo | Prioridad | Estado de atención | Dependencias | Observaciones |
|---|---|---|---|---|---|---|---|---|---|
| #142 | Agregar filas de ejemplo en tablas de "Salida esperada" del prompt library | open | `ai_sdlc_pro_prompts/*.md` | dleon | mejora | alta (evidencia: bloquea la revisión de calidad del batch 33) | listo para implementar | ninguna | Afecta 10 archivos ES/EN ya identificados en este mismo triage |
| #138 | Sección "Contexto obligatorio" desalineada entre ES y EN en 07-00 | open | `ai_sdlc_pro_prompts/07-00-*.en.md` | sin asignar | documentación | media (sin datos de impacto; prioridad no sustentada) | requiere aclaración funcional | posible duplicado de #131 | Verificar con el reportante si #131 ya cubre este caso antes de trabajar ambos en paralelo |
