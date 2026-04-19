# 7.11 — Implementación de pruebas de performance y carga

## Descripción

Prompt para generar el código ejecutable de pruebas de performance, carga, stress y benchmark a partir del diseño definido en `07-06`. Produce scripts listos para ejecutar con la herramienta de carga del proyecto.

**Cuándo usarlo:** después de completar el diseño de pruebas de performance (`07-06`), cuando ya existe el ambiente de prueba levantado (QA / staging) y se necesita el script ejecutable para la herramienta seleccionada.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Adjunta el **Perfil de stack de pruebas** generado por `07-00` (ejecútalo una vez por proyecto si aún no existe).
> Adjunta el diseño de pruebas de performance generado por `07-06` con los escenarios, umbrales y herramienta seleccionada.

---

## Prompt completo

```text
Objetivo:
Implementa los scripts ejecutables de pruebas de performance y carga definidos en el diseño
adjunto de 07-06, usando la herramienta de carga del proyecto.

Pasos:

1. IDENTIFICACIÓN DEL CONTEXTO
   Del diseño 07-06 y el perfil 07-00, extrae:
   - herramienta de carga seleccionada (k6 / Locust / JMeter / Artillery / hey / wrk)
   - endpoints y operaciones a probar con sus parámetros exactos (URL, método, headers, payload)
   - tipos de prueba requeridos: load / stress / spike / soak / benchmark
   - umbrales de aceptación por escenario (P95, P99, tasa de error, throughput)
   - autenticación: ¿los endpoints requieren token? ¿cómo obtenerlo?
   - datos de prueba: ¿qué datos sintéticos o fixtures se necesitan?

2. ESTRUCTURA DEL SCRIPT
   Genera un script bien estructurado que incluya:
   
   a) Configuración global:
      - URL base del ambiente de prueba (variable de entorno — nunca hardcodeada)
      - timeouts de conexión y respuesta
      - umbrales de aceptación (thresholds) como código — el script debe fallar si no se cumplen
      - etiquetas para identificar escenarios en el reporte
   
   b) Autenticación (si aplica):
      - función de setup para obtener token antes de ejecutar las pruebas
      - manejo de renovación de token si el test es de larga duración (soak)
   
   c) Datos de prueba sintéticos:
      - generación de usuarios / IDs / payloads únicos por virtual user
      - evitar colisiones entre usuarios concurrentes
      - no usar datos reales de producción
   
   d) Escenarios de carga:
      Para cada escenario del diseño 07-06, implementar:
      - función de prueba con request HTTP + validación de respuesta
      - verificación de status code esperado
      - verificación de tiempo de respuesta dentro del umbral
      - manejo de errores: loggear y continuar, no detener el test completo
      - think time realista entre requests (simular comportamiento humano)

3. TIPOS DE PRUEBA A IMPLEMENTAR
   
   a) Load test (carga normal):
      ```
      Rampa: 0 → N usuarios en X minutos
      Sostenido: N usuarios durante Y minutos
      Rampa abajo: N → 0 en X minutos
      ```
      Implementar con la sintaxis de la herramienta seleccionada.
   
   b) Stress test (sobrecarga):
      ```
      Incrementar carga progresivamente hasta encontrar el punto de quiebre
      Registrar en qué nivel de carga empiezan a fallar los umbrales
      ```
   
   c) Spike test (pico súbito):
      ```
      Carga normal → pico súbito (10x) por 30 segundos → vuelta a carga normal
      Verificar que el sistema se recupera sin degradación persistente
      ```
   
   d) Soak test (resistencia):
      ```
      Carga sostenida al 70% del máximo durante período largo (1-8 horas)
      Detectar: memory leaks, degradación gradual de tiempos de respuesta,
      agotamiento de conexiones de BD, acumulación de sesiones
      ```
   
   e) Benchmark (línea base):
      ```
      Script de medición simple de un endpoint crítico — ejecutar antes y después del cambio
      Comparar P50, P95, P99 para detectar regresiones de rendimiento
      ```

4. THRESHOLDS Y CRITERIOS DE FALLO
   Codificar los umbrales directamente en el script:
   - el script debe retornar código de salida distinto de 0 si se viola cualquier umbral
   - thresholds mínimos recomendados si no se especifican en el diseño:
     * P95 de tiempo de respuesta < 500ms para APIs
     * P99 de tiempo de respuesta < 1s para APIs
     * tasa de error < 0.1%
     * throughput ≥ al esperado en producción

5. INTEGRACIÓN EN CI/CD
   Proporcionar el comando exacto para ejecutar cada tipo de prueba:
   - variable de entorno para URL base: `BASE_URL=https://staging.example.com`
   - flags de salida para integración en pipeline
   - comando para generar reporte en formato legible (HTML, JSON, InfluxDB)
   - instrucción de cuándo ejecutar qué tipo de prueba en CI/CD:
     * benchmark: en cada PR con cambios en endpoints críticos
     * load test: antes de cada release a producción
     * stress/spike/soak: periodicidad (semanal / mensual)

6. DATOS SINTÉTICOS Y FIXTURES
   Si el test requiere datos de entrada:
   - generar helpers para crear datos únicos por virtual user (evitar conflictos)
   - proporcionar script de setup de datos de prueba en el ambiente (si aplica)
   - proporcionar script de teardown para limpiar datos tras el test

RESTRICCIONES:
- usar exclusivamente datos sintéticos — nunca datos reales de producción
- los scripts deben ejecutarse sin intervención manual (headless)
- las URLs base deben ser configurables por variable de entorno
- el script debe ser idempotente: ejecutable múltiples veces sin efectos acumulativos no deseados
- no ejecutar stress/spike/soak contra producción sin ventana de mantenimiento

Entregables:
- scripts ejecutables por tipo de prueba (load, stress, spike, soak, benchmark),
- comando de ejecución para cada tipo con variables de entorno,
- integración propuesta en el pipeline CI/CD,
- guía de interpretación de resultados: qué métricas revisar y cómo leerlas.
```

---

## Fórmula estándar de uso

```text
Usa el prompt de implementación de pruebas de performance y adáptalo a:
- repositorio: [NOMBRE O URL]
- diseño de pruebas a implementar: [ADJUNTAR RESULTADO DE 07-06]
- perfil de stack de pruebas: [ADJUNTAR RESULTADO DE 07-00]
- herramienta de carga: [k6 / Locust / JMeter / Artillery / hey / wrk]
- ambientes disponibles: [staging URL / Docker local]
- autenticación de la API: [ninguna / Bearer token / API key / sesión]
- tipos de prueba requeridos: [load / stress / spike / soak / benchmark]
- integración en CI/CD: [GitHub Actions / GitLab CI / Jenkins / ninguna]
- documentos a revisar: diseño 07-06, perfil 07-00, endpoints documentados
- objetivo de salida específico: scripts ejecutables + comandos CI/CD
- nivel de profundidad: alto
```

---

## Resultado esperado

### Script de load test (ejemplo k6)

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const responseTime = new Trend('response_time', true);

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // rampa
    { duration: '5m', target: 50 },   // sostenido
    { duration: '2m', target: 0 },    // rampa abajo
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    errors: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export function setup() {
  const res = http.post(`${BASE_URL}/auth/token`, JSON.stringify({
    username: 'test_user',
    password: __ENV.TEST_PASSWORD,
  }), { headers: { 'Content-Type': 'application/json' } });
  return { token: res.json('access_token') };
}

export default function (data) {
  const params = { headers: { Authorization: `Bearer ${data.token}` } };
  const res = http.get(`${BASE_URL}/api/products`, params);

  const success = check(res, {
    'status 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  errorRate.add(!success);
  responseTime.add(res.timings.duration);
  sleep(1);
}
```

### Comandos de ejecución

```bash
# Load test
BASE_URL=https://staging.example.com TEST_PASSWORD=xxx k6 run --out json=results/load.json tests/performance/load-test.js

# Benchmark (antes y después del cambio)
BASE_URL=https://staging.example.com k6 run tests/performance/benchmark.js

# Stress test
BASE_URL=https://staging.example.com k6 run tests/performance/stress-test.js
```

### Integración GitHub Actions

```yaml
- name: Performance benchmark
  run: k6 run tests/performance/benchmark.js
  env:
    BASE_URL: ${{ secrets.STAGING_URL }}
    TEST_PASSWORD: ${{ secrets.PERF_TEST_PASSWORD }}
```
