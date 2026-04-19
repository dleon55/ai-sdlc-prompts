# 11.5 — Performance en Producción: Diagnóstico y Optimización

## Descripción

Prompt para diagnosticar, analizar y remediar problemas de rendimiento en producción: identifica cuellos de botella en la aplicación, base de datos e infraestructura usando señales de observabilidad reales, perfila el sistema bajo carga real y entrega un plan de optimización con cambios cuantificables.

**Cuándo usarlo:** cuando se detecta degradación de rendimiento en producción (alertas de latencia, quejas de usuarios, burn rate del SLO acelerado), tras incorporar observabilidad (`10-04`) y visualizar métricas real-time, o como revisión periódica de salud de rendimiento.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Adjunta métricas, trazas o logs del periodo de degradación (resultado de `10-04` o exportación de Grafana/Datadog/CloudWatch).
> Si existe resultado de `07-06` (diseño de pruebas de performance) o `07-11` (implementación), adjúntalo como contexto de umbrales esperados.

---

## Prompt completo

```text
Objetivo:
Diagnosticar, analizar y remediar problemas de rendimiento en producción usando señales
de observabilidad reales (métricas, trazas, logs), identificar las causas raíz de la
degradación y entregar un plan de optimización priorizado con impacto cuantificable.

Pasos:

1. CARACTERIZACIÓN DEL PROBLEMA
   Describir el problema de rendimiento observado:
   - síntoma exacto: ¿qué métrica o señal indica degradación? (latencia P99, tasa de error, throughput caído)
   - magnitud: ¿cuánto peor está respecto a la línea base? (ej: P95 subió de 200ms a 1.2s)
   - inicio del problema: ¿cuándo comenzó? ¿coincide con un despliegue, aumento de tráfico, cambio de config?
   - alcance: ¿afecta a todos los usuarios o a un subconjunto? ¿a todos los endpoints o solo a algunos?
   - frecuencia: ¿es continuo, periódico o aleatorio?
   - SLO impactado: ¿qué error budget se está consumiendo y a qué velocidad?

2. ANÁLISIS DE TRAZAS Y LOGS
   Con las trazas del periodo de degradación:
   
   a) Identificar la operación más lenta (span más pesado en la traza):
      - ¿es una consulta de BD? ¿una llamada a servicio externo? ¿proceso en CPU?
      - ¿aparece en todas las peticiones afectadas o solo en algunas?
      - ¿tiene correlación con algún parámetro de entrada? (tipo de usuario, tamaño de payload, región)
   
   b) Análisis de logs del periodo:
      - ¿hay errores, warnings o timeouts en el período de degradación que no existían antes?
      - ¿hay logs de "connection pool exhausted", "query timeout", "GC pause", "retry"?
      - ¿algún proceso externo empieza a fallar o a lentificarse en el mismo período?
   
   c) Correlación temporal:
      - ¿la degradación coincide con un pico de tráfico, un job batch, una migración de BD?
      - ¿coincide con rate limiting de un servicio externo?
      - ¿hay memory leak? (memoria subiendo gradualmente sin bajar)

3. DIAGNÓSTICO POR CAPA
   Analizar cada capa del stack para localizar el cuello de botella:
   
   a) Capa de aplicación:
      - ¿hay N+1 queries? (N consultas de BD por cada item en un listado)
      - ¿procesamiento síncrono que debería ser asíncrono?
      - ¿loops costosos o complejidad algorítmica O(n²) o peor?
      - ¿serializaciones/deserializaciones innecesarias o costosas?
      - ¿garbage collection frecuente o pausas largas? (Java, .NET, Go)
      - ¿conexiones de BD no reutilizadas (sin connection pool)?
   
   b) Capa de base de datos:
      - consultas sin índice o con full table scan (EXPLAIN / EXPLAIN ANALYZE)
      - bloqueos de filas o deadlocks (check pg_locks, SHOW PROCESSLIST, etc.)
      - consultas que retornan más datos de los necesarios (SELECT *)
      - índices faltantes en columnas usadas en WHERE, JOIN, ORDER BY
      - estadísticas de BD desactualizadas (no se ejecutó ANALYZE / VACUUM)
      - tamaño de resultado: ¿se pagina correctamente? ¿se aplican límites?
   
   c) Capa de caché:
      - ¿existe caché? ¿cuál es el hit rate? ¿está cayendo?
      - ¿cache stampede? (múltiples peticiones reconstruyen la misma caché simultáneamente)
      - ¿TTL demasiado corto?
      - ¿caché invalidada con demasiada frecuencia?
   
   d) Capa de red e infraestructura:
      - ¿latencia añadida por llamadas síncronas a servicios externos con alta latencia?
      - ¿llamadas sin timeout correctamente configurado?
      - ¿circuit breaker ausente o no activado?
      - ¿saturación de CPU, memoria o red en algún nodo?
      - ¿balanceador de carga distribuyendo inequitativamente?
      - ¿auto-scaling configurado pero con cooldown demasiado largo?

4. PROFILING (SI SE PUEDE EJECUTAR DE FORMA SEGURA)
   Si hay entorno de staging con tráfico real o herramientas de profiling instaladas:
   - CPU profiling: ¿qué función consume más CPU? (flame graph)
   - Memory profiling: ¿qué objeto se acumula en heap?
   - BD profiling: identificar las 10 queries más lentas (pg_stat_statements, slow query log)
   - Profiling de I/O: ¿hay operaciones de disco bloqueantes?
   
   ⚠️ El profiling en producción debe ejecutarse con cuidado — puede añadir overhead.
   Preferir staging con tráfico espejado cuando sea posible.

5. PLAN DE OPTIMIZACIÓN
   Para cada cuello de botella identificado, proponer optimización en orden de impacto/esfuerzo:
   
   Estructura por hallazgo:
   - ID: PERF-XXX
   - capa afectada: [aplicación / BD / caché / infraestructura / red]
   - descripción del problema
   - impacto estimado: reducción de latencia o aumento de throughput esperado (%)
   - esfuerzo estimado: [< 1h / medio día / 1 día / > 1 día]
   - tipo de cambio: [código / configuración / infraestructura / índice de BD]
   - riesgo de regresión: [bajo / medio / alto]
   - cómo medir el impacto: qué métrica verificar antes y después
   - cambio específico propuesto
   
   Priorizar por: impacto alto + esfuerzo bajo primero (quick wins), luego impacto alto + esfuerzo alto.

6. VALIDACIÓN DEL IMPACTO
   Después de implementar cada optimización:
   - comparar métricas antes/después: P50, P95, P99, throughput, tasa de error
   - ejecutar benchmark de referencia (`07-11`) si existe
   - verificar que no se introdujeron regresiones funcionales
   - actualizar la línea base de rendimiento en la documentación

7. MEJORAS ESTRUCTURALES (LARGO PLAZO)
   Si los problemas revelan limitaciones de arquitectura:
   - ¿se necesita caché donde no existe? (Redis, Memcached, caché en memoria)
   - ¿hay operaciones síncronas que deberían ser asíncronas? (colas de mensajes)
   - ¿hay read replicas disponibles para descargar queries de lectura de la BD primaria?
   - ¿hay candidatos para CDN o caché de edge?
   - ¿la base de datos escala horizontalmente o necesita sharding?
   - ¿existe un plan de capacidad basado en crecimiento proyectado?

Entregables:
- informe de diagnóstico: síntoma, causa raíz identificada por capa, evidencia de trazas/logs,
- plan de optimización priorizado (tabla PERF-XXX con impacto, esfuerzo, riesgo),
- quick wins ejecutables en < 1 día,
- mejoras estructurales de largo plazo con estimado de impacto,
- métricas antes/después para validar cada optimización implementada.
```

---

## Fórmula estándar de uso

```text
Usa el prompt de performance en producción y adáptalo a:
- repositorio: [NOMBRE O URL]
- síntoma observado: [descripción de la degradación — métrica, magnitud, período]
- stack tecnológico: [lenguaje, framework, BD, caché, mensajería]
- infraestructura: [cloud / on-premise / contenedores]
- herramientas de observabilidad disponibles: [Grafana / Datadog / CloudWatch / ninguna]
- datos adjuntos: [exportación de trazas, logs del período afectado, resultados de EXPLAIN]
- SLO impactado: [descripción del SLO y estado del error budget]
- entorno de profiling disponible: [solo producción / staging / ninguno]
- documentos a revisar: diseño de performance 07-06, umbrales de 07-11, dashboards 10-04
- objetivo de salida específico: diagnóstico de causa raíz + plan de optimización priorizado
- nivel de profundidad: alto
```

---

## Resultado esperado

### Tabla de hallazgos de performance

| ID | Capa | Problema | Impacto estimado | Esfuerzo | Riesgo | Métrica de validación |
|---|---|---|---|---|---|---|
| PERF-001 | BD | N+1 queries en listado de pedidos (48 queries/request) | −85% latencia P95 | < 1h | bajo | P95 endpoint `/orders` |
| PERF-002 | Aplicación | Sin caché en endpoint de catálogo (100% cache miss) | −60% latencia, +3× throughput | Medio día | bajo | hit rate Redis, P95 `/catalog` |
| PERF-003 | BD | Índice faltante en `orders.customer_id` | −70% latencia de query | < 1h | bajo | EXPLAIN ANALYZE, P95 `/orders` |
| PERF-004 | Infraestructura | Auto-scaling con cooldown de 10 min en picos | Elimina saturación durante picos | < 1h | bajo | CPU peak, req/s durante pico |
