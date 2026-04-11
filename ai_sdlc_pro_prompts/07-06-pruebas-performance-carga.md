# 7.6 — Pruebas de performance y carga

## Descripción

Prompt para diseñar una estrategia de pruebas de performance, carga, stress y benchmark para los componentes impactados por un cambio: escenarios, umbrales de aceptación, herramientas, datos de prueba y criterios de fallo.

**Cuándo usarlo:** antes de desplegar a producción cambios que afecten APIs, consultas de base de datos, procesos batch, generación de archivos o cualquier componente con requerimientos de rendimiento. También como revisión periódica de salud del sistema.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña la estrategia de pruebas de performance y carga para los componentes afectados por este cambio.

Inputs requeridos:
- componentes a probar: [LISTA]
- ambiente de prueba: [QA / STAGING — nunca PROD para pruebas de carga]
- usuarios concurrentes esperados en producción: [NÚMERO]
- SLA o tiempo de respuesta aceptable: [ej: P95 < 500ms, P99 < 1s]
- herramienta disponible: [k6 / Locust / JMeter / Artillery / hey / wrk / otro]

Entrega:

1. TIPOS DE PRUEBA A EJECUTAR
   Para cada tipo, indica objetivo, duración, carga y criterio de fallo:
   a) Load test — carga normal esperada en producción
   b) Stress test — carga que supera el máximo esperado (1.5x - 2x)
   c) Spike test — pico súbito de tráfico (10x por 30s)
   d) Soak test — carga sostenida durante período largo (detecta memory leaks)
   e) Benchmark — medir línea base antes y después del cambio

2. ESCENARIOS DE PRUEBA
   Por cada endpoint/operación crítica:
   - nombre del escenario
   - ruta / operación
   - método HTTP o tipo de operación
   - payload de prueba (sin datos reales — usar datos sintéticos)
   - usuarios concurrentes
   - duración
   - umbral de aceptación: tiempo de respuesta P50, P95, P99
   - umbral de aceptación: tasa de error máxima permitida (ej: < 0.1%)
   - umbral de aceptación: throughput mínimo (req/s)

3. DATOS DE PRUEBA
   - cómo generar datos sintéticos para la prueba
   - volumen de datos en BD necesario para que los resultados sean representativos
   - limpieza post-prueba

4. SCRIPT BASE (según herramienta elegida)
   Genera el script de prueba base listo para ejecutar y adaptar.

5. UMBRALES DE FALLO (fail criteria)
   Lista los criterios que hacen que la prueba falle automáticamente:
   - tiempo de respuesta P95 > [X]ms
   - tasa de error > [Y]%
   - throughput < [Z] req/s

6. INTERPRETACIÓN DE RESULTADOS
   - qué métricas revisar primero
   - cómo detectar cuellos de botella (CPU, memoria, BD, red, locks)
   - qué investigar si el P99 > P95 * 3 (distribución anormal)

7. COMPARATIVA ANTES / DESPUÉS
   Tabla para registrar métricas pre y post cambio:
   | Escenario | P50 antes | P95 antes | P99 antes | P50 después | P95 después | P99 después | Delta |
```

---

## Uso con fórmula estándar

```text
Usa el prompt de pruebas de performance y carga y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- componentes a probar: [LISTA]
- ambiente: [QA / STAGING]
- SLA objetivo: [TIEMPOS DE RESPUESTA ACEPTABLES]
- usuarios concurrentes esperados: [NÚMERO]
- herramienta: [k6 / Locust / JMeter / Artillery]
- documentos a revisar: arquitectura, contratos de API, requerimientos de performance
- objetivo puntual de salida: estrategia completa + script base + tabla de umbrales
- nivel de profundidad: alto
```

---

## Salida esperada

### Escenarios de prueba

| Escenario | Ruta | Concurrentes | Duración | P95 máx | Error máx | Tipo |
|---|---|---|---|---|---|---|
| Listado de prompts | GET /api/prompts | 100 | 5m | 300ms | 0.1% | Load |
| Filtrado por categoría | GET /api/prompts?cat=07 | 100 | 5m | 300ms | 0.1% | Load |
| Stress general | GET /* | 300 | 3m | 800ms | 1% | Stress |
| Spike homepage | GET / | 1000 | 30s | 1500ms | 2% | Spike |
| Soak API | GET /api/prompts | 50 | 60m | 400ms | 0.1% | Soak |

### Script base k6

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 100 },   // ramp-up
    { duration: '3m', target: 100 },   // carga sostenida
    { duration: '1m', target: 0 },     // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<300'],   // P95 < 300ms
    http_req_failed: ['rate<0.001'],    // < 0.1% errores
  },
};

export default function () {
  const res = http.get('[URL_BASE]/');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

### Comparativa antes/después

| Escenario | P50 antes | P95 antes | P99 antes | P50 después | P95 después | P99 después | Δ P95 |
|---|---|---|---|---|---|---|---|
