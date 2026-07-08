# 11.7 — Post-Mortem Blameless y Generación de Runbook (SRE)

## Descripción

Prompt diseñado para adoptar la cultura SRE (Site Reliability Engineering). Toma los datos crudos de un incidente resuelto (logs, chat de slack, métricas) y genera un documento Post-Mortem "sin culpa" (Blameless), identificando la verdadera causa raíz y extrayendo un Runbook automatizable para mitigar futuros incidentes similares.

**Cuándo usarlo:** Inmediatamente después de haber resuelto un incidente crítico o caída en producción (Fase 03 finalizada), para documentar el aprendizaje institucional.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | medio — el runbook resultante puede ser ejecutado directamente por el equipo on-call en incidentes futuros, así que un paso incorrecto o sin revisar puede agravar un incidente real |
| Entradas requeridas | datos crudos del incidente (timeline, logs, chat), resolución aplicada; opcionalmente resultado de análisis de causa raíz `03-02` |
| Herramientas permitidas | solo lectura de los datos del incidente proporcionados; no ejecuta comandos contra sistemas en vivo, el incidente ya está resuelto |
| Autonomía permitida | A1 — Proponer: entrega el documento post-mortem y el runbook propuesto; adoptarlo como runbook oficial operable por on-call requiere revisión humana (A3) |
| Criterios de detención | si el análisis de 5 porqués converge en atribuir la falla a una persona en vez de a un sistema o proceso, debe reformular el hallazgo en términos blameless antes de continuar; si faltan datos suficientes del incidente, debe señalarlo en vez de inventar la cronología |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | timeline con horas y fases verificables, action items formulados como tickets accionables, y runbook con comandos/queries ejecutables y comprobables |
| Siguiente prompt recomendado | `10-04-observabilidad-instrumentacion` si el post-mortem revela puntos ciegos de monitoreo; `11-06-gestion-parches-actualizaciones` si la causa raíz es una dependencia desactualizada |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Adjunta el resultado del análisis de causa raíz (`03-02`) si está disponible.

---

## Prompt completo

```text
Objetivo:
Actúa como un Site Reliability Engineer (SRE). Redacta un documento Post-Mortem Blameless (sin culpa) basado en los datos del incidente proporcionado, y genera un Runbook accionable para el equipo de guardia (On-Call).

Entradas:
- datos_incidente: [PEGA AQUÍ TIMELINES, LOGS, O RESUMEN DEL INCIDENTE]
- resolucion_aplicada: [CÓMO SE SOLUCIONÓ EL PROBLEMA]

Actividades de Análisis:
1. TIMELINE DE INCIDENTE: Reconstruye cronológicamente el evento (Detección, Triaje, Mitigación, Resolución).
2. ANÁLISIS BLAMELESS: Identifica fallas en el sistema, la observabilidad o los procesos, NUNCA en las personas ("El sistema permitió que un push directo rompiera producción" en lugar de "Juan rompió producción").
3. CAUSA RAÍZ (5 Whys): Ejecuta los 5 porqués para llegar al defecto estructural subyacente.
4. DISEÑO DE RUNBOOK: Crea pasos deterministas para que un ingeniero on-call mitigador (o un bot) resuelva esto en el futuro.

Salida Obligatoria:
1. POST-MORTEM DOCUMENT: Estructurado con: Impacto al usuario, Línea de tiempo, Causa Raíz y Action Items (tickets preventivos).
2. ON-CALL RUNBOOK: Instrucciones paso a paso (comandos de terminal, queries, dashboards a mirar) para mitigar si vuelve a ocurrir.

Restricciones:
- mantén el principio blameless en todo el documento, no solo en el análisis de 5 porqués: si una recomendación o action item implica "que la persona tenga más cuidado", reformúlala como un cambio de sistema o proceso (mejor validación, gate automatizado, alerta adicional).
- no publiques el post-mortem con afirmaciones de la cronología que no estén respaldadas por evidencia (timestamps de logs, mensajes de chat, métricas) — si un hito es incierto, márcalo explícitamente como estimado en vez de presentarlo como un hecho verificado.
- distingue explícitamente entre factores contribuyentes (condiciones que empeoraron el incidente o retrasaron su detección o mitigación) y la causa raíz (el defecto estructural que, de no existir, habría evitado el incidente) — no los mezcles en una sola lista sin etiquetarlos.
- si los datos del incidente proporcionados no alcanzan para reconstruir un paso de la cronología o para confirmar la causa raíz, señala el vacío explícitamente en el documento en vez de completarlo con una suposición razonable.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de post-mortem SRE y adáptalo a:
- datos_incidente: [TEXTO DEL INCIDENTE]
- resolucion_aplicada: [TEXTO]
- objetivo puntual de salida: generar documento institucional post-mortem y playbook on-call.
- nivel de profundidad: exhaustivo
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Post-Mortem | Documento SRE estándar (Impacto, Timeline, 5 Whys, Action Items) |
| Enfoque Blameless | Lenguaje que audita procesos y sistemas, no individuos |
| Runbook | Comandos ejecutables y comprobaciones para On-Call |

### Ejemplo aplicado

| Sección | Ejemplo de contenido |
|---|---|
| Post-Mortem | "El 12 de marzo, un deploy sin revisión de límites de conexión removió el máximo configurado en el pool de la API de checkout, agotando las conexiones a la base de datos. Duración: 38 minutos. Impacto: ~2.400 usuarios con checkout fallido (tasa de error 6.8%)." |
| Runbook | "1. Verificar `SELECT count(*) FROM pg_stat_activity;` — si supera el 90% del pool configurado, 2. Ejecutar `kubectl rollout restart deploy/checkout-api` para liberar conexiones huérfanas, 3. Si el conteo no baja en 2 minutos, escalar al DBA de guardia." |
