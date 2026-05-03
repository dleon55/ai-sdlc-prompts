# 8.4 — Auditoría de Planes de Ejecución y Profiling SQL (DBA)

## Descripción

Prompt especializado para actuar como Database Administrator (DBA). Analiza el output de herramientas como `EXPLAIN ANALYZE` o logs de ORM para detectar cuellos de botella, problemas de N+1, escaneos secuenciales masivos y proponer optimizaciones de índices o reescritura de consultas.

**Cuándo usarlo:** Cuando un endpoint o servicio presenta lentitud (latencia alta) en producción, o durante la revisión de PRs que introducen consultas complejas a la base de datos.

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
