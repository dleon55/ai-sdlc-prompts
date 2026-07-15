# 17.4 — Reporte de capacidad y carga del equipo de ingeniería

## Descripción

Prompt para producir un reporte de capacidad de **personas**: dado el backlog o roadmap comprometido y la composición actual del equipo de ingeniería (roles, seniority, disponibilidad, ausencias planeadas), calcula la carga comprometida frente a la capacidad disponible por periodo, identifica riesgos de sobrecarga y cuellos de botella por especialidad (incluyendo bus factor — puntos donde solo una persona sabe hacer algo crítico), y propone recomendaciones de mitigación (redistribuir trabajo, replanificar fechas, contratar, entrenar respaldo). El prompt no ejecuta ninguna de esas recomendaciones: no reasigna tareas, no modifica el roadmap ni gestiona contrataciones — solo reporta el estado y sugiere opciones para que un humano (lead, PM, manager) decida.

**Cuándo usarlo:** al planificar un sprint, quarter o release con compromisos de fecha, o cuando hay señales de sobrecarga del equipo (retrasos recurrentes, burnout, dependencia crítica de una sola persona). **Diferencia con prompts relacionados:** `11-10-capacity-planning` proyecta la capacidad de **infraestructura** (cómputo, base de datos, cache, rate limits) frente a una hipótesis de crecimiento de tráfico o datos — es la contraparte de sistemas. Este prompt, en cambio, reporta la capacidad de **las personas** del equipo: cuánta carga de trabajo humano está comprometida frente a la disponible, y dónde hay riesgo de sobrecarga o de que un solo integrante concentre conocimiento crítico. Ambos prompts responden a la misma pregunta ("¿vamos a llegar al techo?") pero aplicada a dominios distintos y no deben confundirse ni fusionarse: uno mide servidores, el otro mide personas.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis/planificación |
| Riesgo esperado | medio — un reporte de capacidad equivocado puede llevar a comprometer fechas inalcanzables (sobrecarga del equipo, burnout) o a subutilizar personas disponibles, pero el prompt en sí solo analiza y recomienda; la decisión de redistribuir trabajo, replanificar o contratar la toma un humano con autoridad sobre el equipo |
| Entradas requeridas | composición actual del equipo (roles, seniority, especialidades, % de disponibilidad semanal), ausencias planeadas por persona y periodo (vacaciones, licencias, capacitación), backlog o roadmap comprometido con estimaciones de esfuerzo por ítem, periodo a evaluar |
| Herramientas permitidas | lectura de gestor de tareas/backlog, calendario de ausencias, roadmap y estimaciones existentes; la salida es un documento de reporte y recomendación de texto — no reasigna tareas, no modifica el roadmap, no crea ni cierra vacantes ni ejecuta ningún cambio de personal |
| Autonomía permitida | A0 — Analizar (lectura de composición del equipo, ausencias y backlog comprometido); A1 — Proponer (recomendaciones de redistribución, replanificación o contratación); nunca A2/A3 — este prompt no reasigna tareas ni ejecuta decisiones de personal, eso queda delegado a decisión humana del lead o manager responsable |
| Criterios de detención | detener y escalar si no hay backlog/roadmap comprometido con estimaciones de esfuerzo — no inventar estimaciones plausibles; detener si la composición del equipo o las ausencias planeadas no están confirmadas y señalarlo como riesgo residual en vez de asumir disponibilidad completa |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada fila de carga cita la fuente real de la estimación (ítem de backlog, ticket, o "estimado" si no hay ítem formal), cada riesgo de bus factor identifica la persona única y la especialidad o sistema afectado, y cada recomendación indica si aplica al corto plazo (redistribuir dentro del periodo) o al mediano plazo (contratar, entrenar respaldo) |
| Siguiente prompt recomendado | `11-10-capacity-planning` — su contraparte de infraestructura/cómputo, útil como complemento cuando la sobrecarga del equipo coincide con un roadmap de crecimiento técnico (no reemplaza este reporte, evalúa un dominio distinto); `05-01-plan-implementacion` para replanificar el alcance o las fechas de los ítems comprometidos si el reporte revela sobrecarga |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como Engineering Manager o Team Lead especializado en planificación de capacidad de equipo. A partir de la composición actual del equipo de ingeniería y el backlog o roadmap comprometido, calcula la carga de trabajo comprometida frente a la capacidad disponible por periodo, identifica riesgos de sobrecarga y de concentración de conocimiento crítico en una sola persona (bus factor), y propone recomendaciones para mitigar cada riesgo.

Entradas:
- composición del equipo: [LISTA DE INTEGRANTES CON ROL, SENIORITY, ESPECIALIDAD/STACK Y % DE DISPONIBILIDAD SEMANAL]
- ausencias planeadas: [PERSONA, TIPO DE AUSENCIA (VACACIONES/LICENCIA/CAPACITACIÓN), FECHAS — o "ninguna confirmada" si aplica]
- backlog/roadmap comprometido: [LISTA DE ÍTEMS CON ESTIMACIÓN DE ESFUERZO Y FECHA COMPROMETIDA, O ENLACE AL GESTOR DE TAREAS]
- periodo a evaluar: [ej: SPRINT ACTUAL / PRÓXIMO QUARTER / PRÓXIMOS 3 MESES]
- especialidades críticas a vigilar: [ej: ÚNICO EXPERTO EN PAGOS, ÚNICO CON ACCESO/CONOCIMIENTO DE INFRAESTRUCTURA LEGACY — o "ninguna identificada aún" si aplica]

Pasos:

1. LÍNEA BASE DE CAPACIDAD DISPONIBLE
   Para cada integrante del equipo, calcula la capacidad disponible real en el periodo evaluado: % de disponibilidad semanal menos ausencias planeadas menos tiempo ya comprometido en soporte/guardias/reuniones recurrentes si se conoce.
   - si la disponibilidad de una persona no está confirmada, indícalo explícitamente y márcala como "estimado" en vez de asumir 100%.

2. CARGA COMPROMETIDA POR PERSONA Y ROL
   Reúne el backlog/roadmap comprometido y distribuye el esfuerzo estimado por persona o rol/especialidad según asignación actual o planeada. Si un ítem no tiene owner asignado, márcalo como "sin asignar" en vez de repartirlo arbitrariamente.

3. CARGA COMPROMETIDA VS. DISPONIBLE POR PERIODO
   Compara, por persona y por rol/especialidad agregada, la carga comprometida contra la capacidad disponible calculada en el paso 1. Expresa el resultado como % de utilización (carga comprometida / capacidad disponible).

4. IDENTIFICACIÓN DE SOBRECARGA
   Señala explícitamente cualquier persona o especialidad con % de utilización proyectado por encima de un umbral razonable (ej: >100% sostenido, o >85% sin margen para imprevistos). No trates la sobrecarga como aceptable solo porque el compromiso ya fue asumido.

5. IDENTIFICACIÓN DE BUS FACTOR Y CUELLOS DE BOTELLA POR ESPECIALIDAD
   Para cada especialidad o sistema crítico, identifica si hay una sola persona capaz de ejecutar ese trabajo (bus factor = 1). Señala explícitamente el riesgo: qué pasa con el roadmap comprometido si esa persona no está disponible (ausencia, salida, sobrecarga en paralelo).

6. RIESGOS DE REPLANIFICACIÓN
   Para cada caso de sobrecarga o bus factor identificado, evalúa el impacto en las fechas comprometidas del roadmap: qué ítems se retrasarían y en cuánto, si no se toma ninguna acción.

7. RECOMENDACIONES DE MITIGACIÓN
   Para cada riesgo identificado, propone al menos una opción concreta: redistribuir carga hacia personas con capacidad disponible, replanificar fechas o alcance de los ítems afectados, entrenar a una segunda persona como respaldo (reducir bus factor), o señalar la necesidad de contratar si ninguna opción interna cierra la brecha. Indica el tradeoff aproximado de cada opción (tiempo, riesgo de calidad, impacto en otros compromisos).

8. RESUMEN EJECUTIVO Y PRÓXIMOS PASOS
   Resume el estado general de capacidad del periodo, las personas o especialidades en mayor riesgo, y las recomendaciones priorizadas por urgencia.

Restricciones:
- nunca presentes una carga comprometida sin indicar su fuente (ítem de backlog con estimación real, o "estimado" si no hay ítem formal) — toda cifra de esfuerzo debe quedar trazada a su origen.
- distingue siempre disponibilidad confirmada (con fuente citada: calendario de ausencias, contrato de horas) de disponibilidad asumida; marca cada cifra en la salida como "confirmado" o "estimado".
- este prompt analiza y recomienda; nunca reasigna tareas, nunca modifica el roadmap o el backlog, nunca crea, aprueba o cierra vacantes ni ejecuta ningún cambio de personal — todo eso requiere decisión y ejecución humana del lead o manager responsable.
- si la composición del equipo o las ausencias planeadas no están confirmadas para alguna persona, dilo explícitamente y marca como de baja confianza cualquier cálculo de capacidad que dependa de ese dato en vez de asumir disponibilidad completa.
- todo hallazgo de bus factor (una sola persona capaz de cierta tarea crítica) debe señalarse como riesgo aunque no haya sobrecarga de tiempo asociada — la concentración de conocimiento es un riesgo independiente de la carga horaria.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de reporte de capacidad de equipo y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- composición del equipo: [LISTA DE INTEGRANTES CON ROL, SENIORITY, ESPECIALIDAD Y DISPONIBILIDAD]
- ausencias planeadas: [FUENTE O "ninguna confirmada"]
- backlog/roadmap comprometido: [ENLACE AL GESTOR DE TAREAS O LISTA DE ÍTEMS]
- periodo a evaluar: [SPRINT ACTUAL / PRÓXIMO QUARTER]
- especialidades críticas a vigilar: [LISTA O "ninguna identificada aún"]
- documentos a revisar: gestor de tareas/backlog, calendario de ausencias, roadmap comprometido
- objetivo puntual de salida: identificar sobrecarga y bus factor del periodo, con recomendaciones priorizadas
- nivel de profundidad: alto
```

---

## Salida esperada

| Persona / Rol | Capacidad disponible | Carga comprometida | % Utilización | Riesgo identificado | Recomendación |
|---|---|---|---|---|---|
| Ana Torres — Backend Senior, especialista en pagos | 32h/semana (confirmado: 40h contrato − 8h vacaciones semana 3) | 38h/semana (real, 4 ítems de backlog asignados) | 119% — sobrecarga sostenida | única persona capaz de tocar el módulo de pagos (bus factor = 1); si falta, 3 ítems comprometidos del roadmap se retrasan | redistribuir 1 ítem no crítico a otro backend con disponibilidad; iniciar entrenamiento de respaldo con [PERSONA] antes de fin de quarter |

> Nota: la tabla completa debe incluir una fila por cada integrante o especialidad crítica evaluada, señalando explícitamente los casos de bus factor (una sola persona capaz de cierta tarea) aunque no tengan sobrecarga horaria asociada, y separando siempre disponibilidad "confirmada" de "estimada".

### Resumen ejecutivo

- **Estado general de capacidad del periodo:** [SOBRECARGADO / AJUSTADO / CON MARGEN] — % de utilización promedio del equipo: [VALOR].
- **Personas o especialidades en mayor riesgo:** [LISTA] — motivo: [SOBRECARGA / BUS FACTOR / AMBOS].
- **Recomendaciones priorizadas:** [ACCIÓN 1 — urgencia alta], [ACCIÓN 2 — urgencia media], [ACCIÓN 3 — mediano plazo].
- **Riesgos residuales:** [personas sin disponibilidad confirmada, ítems del backlog sin owner asignado, bus factor sin plan de mitigación en curso].
