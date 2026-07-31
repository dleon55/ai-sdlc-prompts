# 8.4 — Auditoría de Planes de Ejecución y Profiling SQL (DBA)

## Descripción

Prompt especializado para actuar como Database Administrator (DBA). Analiza el output de herramientas como `EXPLAIN ANALYZE` o logs de ORM para detectar cuellos de botella, problemas de N+1, escaneos secuenciales masivos y proponer optimizaciones de índices o reescritura de consultas.

**Cuándo usarlo:** Cuando un endpoint o servicio presenta lentitud (latencia alta) en producción, o durante la revisión de PRs que introducen consultas complejas a la base de datos.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — no ejecuta ni aplica cambios en la base de datos; el riesgo real está en que el DDL o la query propuestos se apliquen en producción sin validación adicional |
| Entradas requeridas | `EXPLAIN ANALYZE` o log del ORM, DDL o modelos del esquema relevante, motor de base de datos usado |
| Herramientas permitidas | lectura del plan de ejecución/log y del esquema proporcionados — sin acceso a la base de datos real ni ejecución de consultas |
| Autonomía permitida | A1 — Proponer (entrega diagnóstico, query optimizada y DDL de índices como propuesta; no los ejecuta) |
| Criterios de detención | si el esquema o el plan de ejecución no incluye volumetría real ni estadísticas actualizadas de las tablas, presentar el diagnóstico como preliminar y no garantizar el impacto estimado |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | el diagnóstico debe citar el nodo específico del plan de ejecución (o la consulta N+1 exacta) responsable del cuello de botella |
| Siguiente prompt recomendado | `08-01-revision-completa-pr` para validar la query optimizada y el DDL de índices antes de aplicarlos |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como un Database Administrator (DBA) Senior. Analiza el plan de ejecución SQL o los logs del ORM proporcionados para identificar problemas de rendimiento y proponer soluciones de optimización.

Entradas:
- motor_bd: [PostgreSQL / MySQL / SQL Server / MongoDB / etc.]
- log_o_explain: [PEGA AQUÍ EL EXPLAIN ANALYZE O LOG DEL ORM]
- esquema_relevante: [PEGA EL DDL DE LAS TABLAS INVOLUCRADAS O MODELOS DEL ORM]

Actividades de Análisis:
1. DETECCIÓN DE CUELLOS DE BOTELLA: Identifica los nodos más costosos del plan de ejecución (e.g., Seq Scan, Hash Join costosos, Sort en memoria).
2. ANÁLISIS DE ÍNDICES: Evalúa si se están utilizando los índices correctos o si falta un índice compuesto/cubierto.
3. ANTI-PATRONES DE ORM: Si es un log de ORM (Hibernate, Prisma, Eloquent, etc.), busca el problema de N+1 queries o fetching innecesario de columnas pesadas.
4. OPTIMIZACIÓN DE RECURSOS: Revisa si hay operaciones de filtrado o agregación que podrían realizarse de manera más eficiente.

Restricciones:
- nunca ejecutes el profiling ni el `EXPLAIN ANALYZE` directamente contra producción; si el `log_o_explain` proporcionado no indica claramente el ambiente de origen, pide confirmación explícita antes de asumir que es seguro reproducirlo o de dar por buenos sus resultados,
- toda recomendación de índice o reescritura de consulta debe basarse en evidencia concreta del plan de ejecución o del log proporcionado (nodo específico, costo, filas escaneadas) — no propongas optimizaciones basadas en suposiciones genéricas de "buenas prácticas" sin esa evidencia,
- si una recomendación implica un cambio de esquema (nueva columna, tipo de dato, normalización), señala explícitamente el riesgo de migración: bloqueo de tabla, tiempo de aplicación estimado, compatibilidad con datos existentes,
- el DDL de índices propuesto es una entrega para revisión humana: nunca lo ejecutes ni des a entender que ya fue aplicado.

Salida Obligatoria:
1. DIAGNÓSTICO: Resumen claro de por qué la consulta es lenta (e.g., "Falta un índice en la columna X, causando un escaneo secuencial de 1M de filas").
2. QUERY OPTIMIZADA: La consulta SQL reescrita (o el código ORM ajustado) aplicando las mejores prácticas.
3. DDL DE ÍNDICES: Código SQL exacto para crear los índices recomendados (e.g., `CREATE INDEX CONCURRENTLY...`).
4. IMPACTO ESTIMADO: Reducción esperada en costo computacional o tiempo de ejecución.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de auditoría de profiling SQL y adáptalo a:
- motor_bd: [MOTOR]
- log_o_explain: [TEXTO]
- esquema_relevante: [DDL]
- objetivo puntual de salida: identificar cuellos de botella y generar índices.
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Diagnóstico | Explicación técnica del cuello de botella (Seq Scan, N+1, etc.) |
| Query Optimizada | Consulta SQL o código ORM refactorizado |
| DDL de Índices | Scripts exactos para aplicar los índices faltantes |
| Impacto | Beneficio esperado en latencia o consumo de CPU/I/O |

### Ejemplo concreto

| Sección | Contenido |
|---|---|
| Diagnóstico | El nodo `Seq Scan on orders (cost=0.00..48291.00 rows=1200000 width=64)` muestra que la consulta no usa ningún índice sobre `orders.customer_id`, escaneando 1.2M de filas en cada ejecución |
| Query optimizada | `SELECT id, total FROM orders WHERE customer_id = $1 AND status = 'paid' ORDER BY created_at DESC LIMIT 20;` |
| DDL de índices | `CREATE INDEX CONCURRENTLY idx_orders_customer_status ON orders (customer_id, status, created_at DESC);` |
| Impacto estimado | Reduce el costo del plan de ~48000 a ~120 (estimado por el planner), pasando de un escaneo secuencial a un índice compuesto — requiere validar con `EXPLAIN ANALYZE` sobre datos reales antes de confirmar la mejora |
