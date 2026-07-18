# 11.12 — Auditoría de ruido de alertas (alert fatigue)

## Descripción

Prompt para auditar el historial real de alertas disparadas en un sistema de monitoreo ya desplegado — distinto de diseñar SLOs/alertas nuevas, que cubre `10-04-observabilidad-instrumentacion`. Clasifica cada alerta como ruido (falsos positivos, sin acción tomada, duplicada, silenciada recurrentemente) o señal real, cuantifica la tasa de ruido y su relación con la fatiga del equipo de guardia, y recomienda tuning, consolidación o eliminación por alerta.

**Cuándo usarlo:** cuando el equipo reporta fatiga de alertas (demasiadas notificaciones, alertas ignoradas por costumbre), o periódicamente como salud del sistema de monitoreo ya en producción.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — silenciar o eliminar una alerta que parece ruido pero en realidad detecta un problema real poco frecuente puede dejar un incidente real sin detección futura; el prompt solo analiza y recomienda, no modifica configuración de alertas por sí mismo |
| Entradas requeridas | historial de alertas disparadas en el periodo (nombre, timestamp, severidad, si se tomó acción, si se silenció), acceso a dashboards/reglas de alerta actuales, definición de qué constituye "acción tomada" si existe |
| Herramientas permitidas | lectura del historial de alertas, reglas de alerta configuradas y logs de respuesta/acción asociados; no modifica configuración de alertas ni las silencia — produce el análisis y la recomendación |
| Autonomía permitida | A0 — Analizar (clasificación de alertas por ruido/señal); A1 — Proponer (recomendación de tuning, consolidación o eliminación); nunca A2/A3 — la modificación real de reglas de alerta requiere que un humano la aplique tras revisar la recomendación |
| Criterios de detención | detener y señalar si el historial de alertas no registra si se tomó acción — no asumir "sin acción visible" como equivalente a "ruido confirmado" sin verificar con el equipo; si el periodo analizado es muy corto para alertas de baja frecuencia, señalar la limitación en vez de concluir que es ruido |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada alerta clasificada como ruido cita el patrón que lo sustenta (nunca se tomó acción en N ocurrencias, duplica otra alerta, se silencia recurrentemente sin investigar); cada recomendación de eliminación identifica qué escenario real dejaría de detectarse |
| Siguiente prompt recomendado | `10-04-observabilidad-instrumentacion` si el análisis revela que faltan SLOs/alertas para un punto ciego, no solo ruido en las existentes; `11-13-salud-rotacion-oncall` si el volumen de ruido correlaciona con fatiga del equipo de guardia |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Audita el historial real de alertas disparadas en el periodo indicado para clasificar cada una como ruido o señal real, cuantificar la tasa de ruido, y recomendar tuning, consolidación o eliminación por alerta.

Entradas:
- historial de alertas del periodo: [PEGAR O ENLACE — nombre, timestamp, severidad, acción tomada, si se silenció]
- reglas de alerta actuales: [PEGAR O ENLACE A LA CONFIGURACIÓN]
- definición de "acción tomada": [ej. TICKET ABIERTO, RESPUESTA EN CANAL DE INCIDENTES, RUNBOOK SEGUIDO — O "no definida aún"]
- periodo a analizar: [ej. ÚLTIMO TRIMESTRE]
- canal/sistema de alertas: [ej. PagerDuty / Opsgenie / Slack / otro]

Pasos:
1. CLASIFICACIÓN POR ALERTA
   Para cada regla de alerta distinta en el historial, cuenta cuántas veces se disparó en el periodo, en cuántas se tomó una acción registrada (según la definición provista), en cuántas se silenció sin investigar, y si duplica el mismo síntoma que otra alerta ya contabilizada.

2. CÁLCULO DE TASA DE RUIDO
   Para cada alerta, calcula la proporción de disparos sin acción tomada frente al total. Si la definición de "acción tomada" no fue provista, señálalo explícitamente y usa como proxy conservador solo los casos donde hay evidencia directa de investigación (comentario, ticket, respuesta en el canal) — nunca asumas que "no hay registro" significa "no se investigó".

3. DETECCIÓN DE DUPLICADOS Y CORRELACIÓN
   Identifica alertas que se disparan siempre juntas o en cascada por el mismo síntoma raíz (ej. una alerta de CPU y otra de latencia que siempre coinciden) — estas son candidatas a consolidarse en una sola señal con contexto enriquecido en vez de generar N notificaciones separadas.

4. CLASIFICACIÓN FINAL: RUIDO VS. SEÑAL
   Clasifica cada alerta como: señal real (acción tomada consistentemente, detecta un problema real), ruido confirmado (nunca llevó a acción en el periodo completo, o se silencia sistemáticamente sin investigar), o "necesita más datos" (frecuencia muy baja para concluir con el periodo analizado — no la clasifiques como ruido solo por eso).

5. RECOMENDACIÓN POR ALERTA
   - Ruido confirmado: recomienda ajustar el umbral, cambiar la condición de disparo, o eliminar la alerta — indicando explícitamente qué escenario real (aunque sea poco probable) dejaría de detectarse si se elimina.
   - Duplicada/correlacionada: recomienda consolidar en una alerta compuesta.
   - Señal real pero de alta frecuencia: evalúa si el umbral está mal calibrado (dispara antes de que el problema sea realmente accionable) en vez de solo aceptar el volumen.

6. RELACIÓN CON FATIGA DEL EQUIPO
   Si hay datos de quién recibió cada alerta, señala si el ruido se concentra en ciertos horarios (nocturno/fin de semana) o en ciertas personas, lo cual agrava la fatiga más allá del volumen total.

Restricciones:
- nunca clasifiques una alerta como "ruido confirmado" solo porque no hay registro explícito de acción — si la definición de "acción tomada" no está clara o el registro es incompleto, clasifícala como "necesita más datos" en vez de recomendar eliminarla,
- toda recomendación de eliminar o subir el umbral de una alerta debe declarar explícitamente qué escenario real dejaría de detectarse — nunca recomiendes eliminar sin ese análisis de riesgo,
- no ejecutes ni modifiques ninguna regla de alerta, silenciamiento o configuración — este prompt es de solo análisis y recomendación,
- si el periodo analizado es demasiado corto para una alerta de baja frecuencia esperada (ej. una vez por trimestre y el periodo es de un mes), no la clasifiques como ruido — señala la limitación de datos explícitamente.

Salida:
- tabla de alertas: nombre, disparos en el periodo, tasa de ruido, clasificación (señal/ruido/necesita más datos)
- alertas candidatas a consolidación (duplicadas/correlacionadas)
- recomendación de tuning/consolidación/eliminación por alerta, con el escenario que dejaría de detectarse si aplica
- relación observada entre ruido y horario/persona receptora, si hay datos
- resumen: tasa de ruido global del periodo, cambio de volumen esperado si se aplican las recomendaciones
```

---

## Uso con fórmula estándar

```text
Usa el prompt de auditoría de ruido de alertas y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- historial de alertas: [ENLACE AL HISTORIAL DEL PERIODO]
- reglas de alerta actuales: [ENLACE A LA CONFIGURACIÓN]
- definición de "acción tomada": [ej. TICKET ABIERTO O "no definida aún"]
- periodo a analizar: [ÚLTIMO TRIMESTRE]
- canal/sistema de alertas: [PagerDuty / Opsgenie / Slack / otro]
- documentos a revisar: historial de alertas, reglas de configuración
- objetivo puntual de salida: clasificación de ruido vs. señal con recomendaciones de tuning
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Tabla de alertas | Nombre, disparos, tasa de ruido, clasificación |
| Consolidación | Alertas duplicadas o correlacionadas a fusionar |
| Recomendaciones | Tuning/consolidación/eliminación, con escenario de riesgo si aplica |
| Fatiga del equipo | Concentración de ruido por horario o persona, si hay datos |
| Resumen | Tasa de ruido global y cambio de volumen esperado |

### Ejemplo (fragmento)

| Alerta | Disparos (trimestre) | Tasa de ruido | Clasificación |
|---|---|---|---|
| CPU > 80% por 5 min | 47 | 91% sin acción registrada | Ruido confirmado |
| Latencia P99 > 2s | 12 | 25% sin acción | Señal real, umbral bien calibrado |
| Espacio en disco < 10% (backup nocturno) | 3 | 100% sin acción, siempre coincide con el job de backup programado | Necesita más datos — solo 3 ocurrencias, pero correlaciona con un proceso conocido; candidata a ajustar umbral o excluir la ventana del backup, no a eliminar sin más evidencia |

**Recomendación:** la alerta de CPU dispara 47 veces en el trimestre sin que ninguna llevara a acción registrada ni comentario en el canal de incidentes — subir el umbral a 90% sostenido por 10 min en vez de 5. Riesgo de eliminarla sin ajustar: un pico real de CPU que preceda una caída del servicio dejaría de notificarse; se recomienda ajustar el umbral, no eliminar la alerta.
