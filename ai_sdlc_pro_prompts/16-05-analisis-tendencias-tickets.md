# 16.5 — Análisis de tendencias y causas raíz agregadas de tickets

## Descripción

Prompt para analizar un lote o período de tickets de soporte ya resueltos y detectar patrones agregados: categorías recurrentes, causas raíz comunes a varios tickets, y volumen/costo asociado a cada patrón. No resuelve tickets ni entra en el detalle técnico de un caso individual: agrupa señales a través de todo el lote para decidir si algún patrón amerita una iniciativa de ingeniería (bug recurrente, falta de documentación, gap de producto) en vez de seguir absorbiéndose caso a caso en soporte.

**Cuándo usarlo:** periódicamente (mensual o trimestral) sobre un lote de tickets que ya fueron atendidos y cerrados individualmente vía `16-02`, como ejercicio retrospectivo para alimentar decisiones de producto e ingeniería. Diferencia con prompts relacionados: `16-01` hace triage de un ticket individual entrante para clasificarlo y enrutarlo en el momento; `16-02` resuelve un ticket puntual ya triageado; este prompt no toca tickets individuales — analiza el conjunto ya resuelto para encontrar señales que ningún ticket aislado revela por sí solo. `02-04-triage-backlog-github` gestiona el backlog de issues de ingeniería ya creados; este prompt es el paso previo que decide si un patrón de tickets amerita convertirse en uno de esos issues.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | bajo — el prompt solo analiza datos históricos de tickets ya cerrados y produce recomendaciones; no modifica tickets, no contacta clientes ni ejecuta cambios de producto o código |
| Entradas requeridas | export o acceso de lectura al lote de tickets resueltos del período a analizar (idealmente con categoría, resumen, resolución y tiempo de resolución de cada uno), rango de fechas o período a cubrir, taxonomía de categorías existente si el equipo ya usa una |
| Herramientas permitidas | lectura del sistema de tickets/helpdesk, exports o dashboards de soporte; la salida es un documento de análisis y recomendación de texto — no crea, edita ni cierra tickets, no crea issues de ingeniería directamente |
| Autonomía permitida | A0 — Analizar (lectura y categorización agregada del lote); A1 — Proponer (recomendar iniciativas de ingeniería o documentación); nunca A2/A3 — este prompt no crea issues, no despliega documentación ni ejecuta cambios de producto |
| Criterios de detención | detener y escalar si el lote de tickets disponible es demasiado pequeño o no tiene campos mínimos (categoría, resumen, resolución) para sustentar un patrón agregado — no inventar categorías ni causas raíz sin evidencia de al menos varios tickets repetidos; señalar como hallazgo de baja confianza cualquier patrón basado en menos de [UMBRAL MÍNIMO] tickets |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada categoría recurrente cita el conteo real de tickets que la componen y el rango de fechas del lote analizado; cada causa raíz agregada referencia al menos los identificadores o resúmenes de los tickets que la sustentan (no una única anécdota); cada recomendación de iniciativa distingue explícitamente entre bug recurrente, gap de documentación y gap de producto |
| Siguiente prompt recomendado | `02-04-triage-backlog-github` si la recomendación es crear uno o más issues de ingeniería para un patrón identificado como bug recurrente o gap de producto; `10-01-documentacion-tecnica` si la recomendación es cerrar un gap de documentación identificado como causa raíz agregada |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como Analista de Soporte especializado en análisis de tendencias y causas raíz agregadas. A partir de un lote de tickets de soporte ya resueltos en un período determinado, identifica categorías recurrentes, agrupa causas raíz comunes a varios tickets (no ticket por ticket), y recomienda si algún patrón amerita una iniciativa de ingeniería o documentación en vez de seguir resolviéndose caso a caso.

Entradas:
- fuente del lote de tickets: [EXPORT CSV/JSON, ACCESO A HELPDESK (ZENDESK/JIRA SERVICE MANAGEMENT/FRESHDESK/OTRO), DASHBOARD DE SOPORTE]
- período a analizar: [ej: MES DE JUNIO 2026 / Q2 2026]
- volumen total de tickets en el período: [NÚMERO O "desconocido hasta el análisis"]
- campos disponibles por ticket: [CATEGORÍA/TAG, RESUMEN, RESOLUCIÓN APLICADA, TIEMPO DE RESOLUCIÓN, PRODUCTO/MÓDULO AFECTADO — indicar cuáles faltan si aplica]
- taxonomía de categorías existente: [LA QUE YA USA EL EQUIPO, o "no existe — proponer una durante el análisis"]
- umbral mínimo de tickets para considerar un patrón significativo: [ej: 5 TICKETS O MÁS EN EL PERÍODO]

Pasos:

1. INVENTARIO DEL LOTE
   Confirma el volumen real de tickets disponibles para el período y los campos con los que cuenta cada uno. Si faltan campos clave (categoría, resumen, resolución) para una porción relevante del lote, indícalo explícitamente y acota el análisis a la porción con datos suficientes.

2. CATEGORIZACIÓN AGREGADA
   Agrupa los tickets del lote en categorías recurrentes (usando la taxonomía existente si la hay, o proponiendo una basada en los datos si no existe). No analices ticket por ticket en la salida: reporta el conteo y el porcentaje del lote que representa cada categoría.

3. IDENTIFICACIÓN DE CAUSAS RAÍZ AGREGADAS
   Para cada categoría con volumen relevante (por encima del umbral mínimo indicado), identifica la causa raíz común a los tickets que la componen — no la causa de un ticket aislado. Distingue explícitamente entre:
   - bug recurrente (el mismo defecto de software genera múltiples tickets),
   - falta de documentación (los usuarios no encuentran o no entienden información que ya debería existir),
   - gap de producto (el producto carece de una funcionalidad que los usuarios necesitan, por lo que recurren a soporte como sustituto),
   - error de uso o expectativa no alineada con el producto (no requiere cambio de ingeniería, pero puede requerir comunicación u onboarding).

4. VOLUMEN Y COSTO ASOCIADO POR PATRÓN
   Para cada causa raíz agregada identificada, cuantifica su impacto: número de tickets, porcentaje del volumen total del período, y tiempo agregado de resolución invertido por el equipo de soporte en esa categoría (si el dato está disponible).

5. EVALUACIÓN DE "¿AMERITA INICIATIVA?"
   Para cada patrón con volumen relevante, evalúa si amerita una iniciativa formal (issue de ingeniería para bug recurrente o gap de producto, actualización de documentación para gap de documentación) en vez de seguir resolviéndose caso a caso en soporte. Justifica la recomendación con el volumen/costo cuantificado en el paso 4, no con percepción subjetiva de urgencia.

6. PATRONES DE BAJA CONFIANZA
   Señala explícitamente cualquier categoría o causa raíz que esté por debajo del umbral mínimo de tickets indicado, o que se sostenga en muy pocos casos — no las presentes con el mismo nivel de certeza que los patrones bien sustentados.

7. TENDENCIA TEMPORAL (SI HAY DATOS DE PERÍODOS ANTERIORES)
   Si hay datos de períodos anteriores disponibles, indica si cada categoría recurrente está creciendo, estable o disminuyendo respecto al período previo. Si no hay datos históricos, indícalo explícitamente en vez de asumir una tendencia.

8. RESUMEN EJECUTIVO Y PRÓXIMOS PASOS
   Resume las categorías con mayor volumen, las causas raíz agregadas más significativas, y las iniciativas recomendadas priorizadas por volumen/costo — no por orden de aparición.

Restricciones:
- nunca reportes un patrón o causa raíz agregada basado en un único ticket o en un puñado de casos por debajo del umbral mínimo indicado; si el volumen es insuficiente para sustentar un patrón, dilo explícitamente y márcalo como hallazgo de baja confianza.
- no entres en el detalle de resolución de un ticket individual — el objetivo es la señal agregada del lote, no un resumen ticket por ticket.
- distingue siempre bug recurrente, falta de documentación y gap de producto como categorías separadas de causa raíz — no las mezcles bajo una etiqueta genérica como "problema de usuario".
- este prompt analiza y recomienda; nunca crea, edita ni cierra tickets, no contacta clientes, no crea issues de ingeniería directamente ni publica cambios de documentación.
- si el lote de tickets no incluye campos mínimos (categoría, resumen, resolución) para una porción relevante, dilo explícitamente y acota el análisis a la porción con datos suficientes en vez de extrapolar sobre datos faltantes.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de análisis de tendencias y causas raíz agregadas de tickets y adáptalo a:
- repositorio/producto: [NOMBRE O URL]
- fuente del lote de tickets: [EXPORT O SISTEMA DE HELPDESK]
- período a analizar: [ej: Q2 2026]
- volumen total de tickets: [NÚMERO O "desconocido"]
- campos disponibles por ticket: [CATEGORÍA, RESUMEN, RESOLUCIÓN, TIEMPO DE RESOLUCIÓN]
- taxonomía de categorías existente: [LA DEL EQUIPO O "proponer una"]
- umbral mínimo de tickets por patrón: [ej: 5]
- documentos a revisar: export de tickets del período, taxonomía de categorías previa si existe
- objetivo puntual de salida: identificar categorías recurrentes, causas raíz agregadas, y si ameritan iniciativa de ingeniería o documentación
- nivel de profundidad: alto
```

---

## Salida esperada

| Categoría recurrente | Volumen (tickets / % del período) | Causa raíz agregada | Tipo de causa raíz | ¿Amerita iniciativa? |
|---|---|---|---|---|
| Errores al exportar reportes en formato PDF | 23 tickets / 18% del volumen de junio 2026 | El generador de PDF trunca tablas con más de 50 filas — mismo defecto reportado en tickets #4021, #4088, #4150 y otros 20 casos | Bug recurrente | Sí — crear issue de ingeniería (prioridad alta, volumen sostenido dos meses consecutivos) |
| Confusión sobre cómo configurar permisos de equipo | 14 tickets / 11% del volumen de junio 2026 | La documentación existente no cubre el flujo de permisos anidados introducido en la última versión | Falta de documentación | Sí — actualizar guía de permisos con el flujo nuevo |
| Solicitud recurrente de exportar a Excel además de PDF | 9 tickets / 7% del volumen de junio 2026 | El producto no ofrece exportación a Excel; los usuarios piden el dato en otro formato como sustituto | Gap de producto | Evaluar con producto — volumen aún por debajo del umbral de prioridad alta, monitorear próximo trimestre |
| Preguntas sobre cómo cambiar el idioma de la interfaz | 3 tickets / 2% del volumen de junio 2026 | Casos aislados sin causa común identificable | Baja confianza — volumen insuficiente | No — por debajo del umbral mínimo, seguir resolviendo caso a caso |

> Nota: la tabla completa debe incluir una fila por cada categoría recurrente identificada en el lote, señalando volumen real, causa raíz agregada con tickets de referencia, tipo de causa raíz (bug recurrente / falta de documentación / gap de producto / error de uso), y la recomendación de iniciativa priorizada por volumen o costo, no por orden de aparición.

### Resumen ejecutivo

- **Período analizado:** [PERÍODO] — [N] tickets resueltos analizados de un total de [N TOTAL] en el sistema.
- **Categorías con mayor volumen:** [LISTA DE 2-3 CATEGORÍAS PRINCIPALES] con su porcentaje del total.
- **Iniciativas recomendadas priorizadas:** [LISTA DE INICIATIVAS] — cada una con el tipo de causa raíz y el volumen/costo que la sustenta.
- **Patrones de baja confianza:** [CATEGORÍAS POR DEBAJO DEL UMBRAL] — no accionables aún, mantener en observación en el próximo período.
- **Riesgos residuales:** [datos faltantes en el lote, ausencia de comparación histórica, taxonomía sin validar con el equipo de soporte].
