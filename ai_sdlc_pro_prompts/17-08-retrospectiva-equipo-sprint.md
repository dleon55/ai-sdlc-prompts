# 17.8 — Retrospectiva de equipo por sprint/iteración

## Descripción

Prompt para estructurar la retrospectiva de proceso de un equipo al cierre de un sprint o iteración: qué funcionó bien, qué no, patrones que se repiten entre retrospectivas anteriores, y acciones de mejora concretas con responsable y seguimiento. Distinto de `11-07-sre-postmortem-runbook` (post-mortem de un solo incidente técnico), de `17-07-revision-exito-post-lanzamiento` (revisión de KPIs de negocio meses después del lanzamiento, no del proceso del equipo), y de `14-02-psp-tsp-metricas-calidad` (métricas individuales de tiempos/defectos por desarrollador, no una discusión cualitativa de equipo). `00-B-04-metodologia-framework` solo define cuándo y con quién ocurre la ceremonia de retrospectiva; este prompt es el que la ejecuta y produce su resultado.

**Cuándo usarlo:** al cierre de cada sprint o iteración, como insumo estructurado para (o registro posterior de) la reunión de retrospectiva del equipo.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — una retrospectiva que omite o suaviza problemas reales del proceso, o cuyas acciones de mejora nunca se les da seguimiento en el siguiente ciclo, hace que los mismos problemas se repitan sprint tras sprint sin que nadie lo note; el prompt no ejecuta ningún cambio de proceso ni de herramientas por sí mismo |
| Entradas requeridas | qué pasó en el sprint/iteración actual (según lo reportado por el equipo, no inferido), retrospectiva(s) anterior(es) con sus acciones de mejora pendientes, si existen |
| Herramientas permitidas | ninguna de ejecución — lectura de retrospectivas previas y de lo reportado por el equipo; produce un documento de retrospectiva, no modifica proceso, configuración ni herramientas |
| Autonomía permitida | A0 — Analizar; A1 — Proponer (acciones de mejora priorizadas) |
| Criterios de detención | no inventar problemas, logros o causas raíz que el equipo no reportó explícitamente — si algo no fue mencionado por el equipo, no se incluye como si lo hubiera sido; si una acción de mejora de la retrospectiva anterior nunca se completó, reportarlo explícitamente en vez de omitirlo |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada acción de mejora de la retrospectiva anterior aparece con su estado real (completada/parcial/no iniciada); todo patrón reportado como recurrente cita en qué retrospectivas anteriores ya apareció |
| Siguiente prompt recomendado | repetir este mismo prompt al cierre del siguiente sprint/iteración, retomando las acciones de mejora pendientes; `11-03-deuda-tecnica` si la retrospectiva revela deuda técnica no registrada formalmente |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Estructura la retrospectiva de proceso del equipo al cierre del sprint/iteración actual: qué funcionó bien, qué no, patrones recurrentes entre retrospectivas anteriores, y acciones de mejora priorizadas con responsable y criterio de seguimiento.

Entradas:
- sprint/iteración actual: [NÚMERO O NOMBRE, FECHAS]
- qué reportó el equipo sobre este sprint: [PEGAR NOTAS, COMENTARIOS O TRANSCRIPCIÓN DE LA CEREMONIA]
- retrospectiva(s) anterior(es) con sus acciones de mejora: [PEGAR O REFERENCIA, O "primera retrospectiva del equipo"]

Actividades:
1. SEGUIMIENTO DE ACCIONES PREVIAS
   Para cada acción de mejora de la retrospectiva anterior, reporta su estado real: completada, parcial, o no iniciada — con la evidencia citada (no asumas que se completó solo porque nadie mencionó lo contrario). Una acción sin seguimiento reportado se marca como "no iniciada", nunca como "completada" por omisión.

2. QUÉ FUNCIONÓ BIEN
   Lista los aciertos del sprint reportados explícitamente por el equipo, con el motivo de por qué funcionó (para poder repetirlo), no solo la lista.

3. QUÉ NO FUNCIONÓ
   Lista los problemas reportados explícitamente por el equipo — sin suavizarlos ni generalizarlos más allá de lo que se dijo. Si el equipo reportó un síntoma sin causa raíz clara, repórtalo como "causa raíz no identificada", no inventes una.

4. PATRONES RECURRENTES
   Compara los problemas de este sprint contra las retrospectivas anteriores disponibles — identifica cuáles ya aparecieron antes (citando en qué retrospectiva) y distínguelos de los problemas nuevos de este ciclo. Un problema que se repite 2+ veces sin acción efectiva es una señal de que la acción de mejora anterior no atacó la causa real.

5. ACCIONES DE MEJORA
   Propón acciones concretas y accionables para el siguiente ciclo, cada una con responsable sugerido y cómo se sabrá si funcionó — no listes buenas intenciones genéricas ("comunicarnos mejor") sin un cambio de proceso concreto y verificable.

6. CIERRE
   Resume el estado general del equipo en el sprint (mejorando / estable / con problemas crecientes) basado únicamente en lo reportado, no en una impresión general.

Restricciones:
- nunca reportes una acción de mejora anterior como "completada" sin evidencia citada de que ocurrió — sin evidencia, se reporta como no verificable,
- nunca inventes problemas, logros o causas raíz que el equipo no mencionó explícitamente — reporta solo lo reportado,
- un problema recurrente se cita con las retrospectivas anteriores donde ya apareció, no se presenta como si fuera nuevo,
- este prompt no ejecuta ningún cambio de proceso, herramienta o configuración por sí mismo — solo produce el documento de retrospectiva,
- si no existe ninguna retrospectiva anterior, indícalo explícitamente y omite las secciones de seguimiento de acciones previas y patrones recurrentes en vez de inventarlas.

Salida:
0. Bloque JSON de metadatos (claves: status, previous_actions_completed_count, previous_actions_pending_count, recurring_issues_count, confidence_score [0.0 a 1.0]).
1. Seguimiento de acciones de la retrospectiva anterior, con estado real.
2. Qué funcionó bien, con el motivo.
3. Qué no funcionó, con causa raíz si se identificó.
4. Patrones recurrentes entre retrospectivas, citando en cuáles ya aparecieron.
5. Acciones de mejora priorizadas, con responsable sugerido y criterio de verificación.
6. Cierre: estado general del equipo en el sprint.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de retrospectiva de equipo por sprint y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- metodología: [SCRUM / KANBAN / OTRA]
- sprint/iteración actual: [NÚMERO O NOMBRE, FECHAS]
- documentos a revisar: notas de la ceremonia de retrospectiva, retrospectiva(s) anterior(es)
- objetivo puntual de salida: retrospectiva estructurada con seguimiento de acciones y patrones recurrentes
- nivel de profundidad: medio
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen de seguimiento |
| Seguimiento de acciones previas (1) | Estado real (completada/parcial/no iniciada) de cada acción anterior, con evidencia |
| Qué funcionó bien (2) | Aciertos reportados por el equipo, con motivo |
| Qué no funcionó (3) | Problemas reportados, con causa raíz si se identificó |
| Patrones recurrentes (4) | Problemas repetidos, citando en qué retrospectivas anteriores aparecieron |
| Acciones de mejora (5) | Acciones concretas, responsable sugerido, criterio de verificación |
| Cierre (6) | Estado general del equipo en el sprint |

### Ejemplo (fragmento)

```json
{
  "status": "retrospectiva_con_patron_recurrente",
  "previous_actions_completed_count": 1,
  "previous_actions_pending_count": 2,
  "recurring_issues_count": 1,
  "confidence_score": 0.76
}
```

| Acción anterior | Estado | Evidencia |
|---|---|---|
| Agregar revisor adicional a PRs de pagos | No iniciada | No se reportó ningún cambio en el proceso de revisión durante el sprint |
| Documentar el runbook de despliegue | Completada | Runbook agregado en `docs/deploy-runbook.md`, referenciado por el equipo en la ceremonia |

| Patrón recurrente | Retrospectivas donde apareció | Señal |
|---|---|---|
| Estimaciones de historias de integración con terceros consistentemente subestimadas | Sprint 12, Sprint 13, Sprint 14 (actual) | La acción de mejora del Sprint 12 ("revisar estimación con el equipo de integraciones antes de comprometer") nunca se implementó — repetir la misma acción sin cambio de proceso no rompe el patrón |
