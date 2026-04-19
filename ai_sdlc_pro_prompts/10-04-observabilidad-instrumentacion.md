# 10.4 — Observabilidad: Instrumentación y Monitoreo

## Descripción

Prompt para diseñar e implementar la estrategia de observabilidad de una aplicación: pilares de métricas, logs estructurados y trazas distribuidas; alertas, dashboards, SLOs/SLAs y correlación de señales para detectar y diagnosticar problemas en producción.

**Cuándo usarlo:** al incorporar observabilidad a un sistema nuevo, al revisar la cobertura de monitoreo antes de un despliegue mayor, o cuando se identifican puntos ciegos en la detección de fallos en producción.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Si existe un resultado de `13-04` (Threat Modeling), adjúntalo para identificar componentes críticos que requieren mayor cobertura de observabilidad.

---

## Prompt completo

```text
Objetivo:
Diseñar e implementar la estrategia de observabilidad completa para la aplicación,
cubriendo los tres pilares (métricas, logs, trazas), definiendo SLOs, alertas accionables
y dashboards para detectar y diagnosticar problemas antes de que impacten a los usuarios.

Pasos:

1. INVENTARIO DE COMPONENTES A INSTRUMENTAR
   Mapear todos los componentes del sistema que requieren observabilidad:
   - servicios backend y APIs (nombres, lenguaje, framework)
   - bases de datos y caches (tipo, motor, cómo se accede)
   - colas de mensajes o workers asíncronos
   - servicios externos y terceros (con SLA propio)
   - infraestructura: contenedores, nodos, balanceadores de carga
   - frontend (si aplica): Core Web Vitals, errores JS, experiencia de usuario real

2. PILAR 1 — MÉTRICAS
   Para cada servicio, definir las métricas RED + USE:
   
   RED (para servicios orientados a solicitudes):
   - Rate: solicitudes por segundo (req/s)
   - Errors: tasa de error (% de respuestas 4xx/5xx)
   - Duration: distribución de latencia (P50, P95, P99)
   
   USE (para recursos de infraestructura):
   - Utilization: % de CPU, memoria, disco, conexiones de red
   - Saturation: tamaño de colas, tiempo de espera
   - Errors: errores de sistema, fallos de hardware
   
   Métricas de negocio (Golden Signals de dominio):
   - métricas que reflejan salud del negocio: pedidos procesados/min, usuarios activos, conversiones
   - métricas que alertan antes de que el usuario lo note: tasa de reintentos, errores de validación
   
   Para cada métrica, especificar:
   - nombre y unit (ej: `http_request_duration_seconds`, `gauge` / `counter` / `histogram`)
   - labels/dimensiones para segmentar (endpoint, método, status_code, región)
   - instrucción de instrumentación: código o configuración necesaria para exponerla

3. PILAR 2 — LOGS ESTRUCTURADOS
   Definir la estrategia de logging:
   
   a) Formato y estructura:
      - usar JSON estructurado (no texto plano) — permite búsqueda y filtrado eficiente
      - campos obligatorios en cada log: timestamp (ISO 8601), level, service, trace_id, span_id, message
      - campos contextuales: request_id, user_id (anonimizado si aplica GDPR), endpoint, duration_ms
   
   b) Niveles de log y cuándo usarlos:
      - ERROR: fallo que requiere atención inmediata
      - WARN: condición anómala recuperable que puede escalar
      - INFO: eventos de negocio relevantes (request completado, job ejecutado)
      - DEBUG: detalle de diagnóstico (solo habilitado en entornos no-prod)
   
   c) Qué NO loggear (seguridad y privacidad):
      - contraseñas, tokens, API keys, números de tarjeta
      - PII sin anonimización (nombres completos, emails, IPs de usuarios en GDPR)
      - stack traces completos en respuestas al cliente (solo en logs internos)
   
   d) Retención y costos:
      - definir período de retención por nivel: ERROR 90d, INFO 30d, DEBUG 7d
      - configurar sampling para logs de alto volumen (ej: 10% de requests exitosos)

4. PILAR 3 — TRAZAS DISTRIBUIDAS
   Si el sistema tiene más de un servicio o componente:
   
   a) Propagación de contexto:
      - implementar W3C Trace Context (`traceparent` header) entre servicios
      - propagar trace_id y span_id en todas las llamadas HTTP, mensajes de cola, jobs
   
   b) Spans instrumentados:
      - span por cada operación de negocio (endpoint, query de BD, llamada a servicio externo)
      - atributos en cada span: nombre de operación, status, duración, error (si aplica)
      - sampling: 100% de trazas con error, 10% de trazas exitosas (ajustar por volumen)
   
   c) Correlación:
      - asegurar que trace_id aparece también en logs y métricas para correlacionar señales
      - configurar el stack de observabilidad para navegar de alerta → traza → logs

5. DEFINICIÓN DE SLOs Y ALERTAS
   
   a) SLOs (Service Level Objectives):
      Para cada servicio crítico, definir:
      - SLI (indicador): ej. "% de requests con latencia < 500ms en P95"
      - SLO objetivo: ej. 99.5% en ventana de 30 días
      - Error budget: (100% - SLO)% — cuánto margen de fallo existe
      - Burn rate: velocidad a la que se consume el error budget
   
   b) Alertas accionables (evitar alert fatigue):
      Para cada alerta, definir:
      - condición de disparo con threshold preciso
      - severidad: page (madrugada) / ticket (horario laboral) / info (solo log)
      - ventana de evaluación y período de "no disparar de nuevo" (cooldown)
      - playbook adjunto: qué hacer cuando se dispara (enlace a runbook 11-04)
      - destinatario: equipo, canal Slack, PagerDuty, OpsGenie
      
      Alertas mínimas recomendadas:
      - tasa de error > 1% en 5 min → page
      - P99 de latencia > umbral × 2 en 5 min → page
      - CPU o memoria > 85% sostenido 10 min → ticket
      - error budget < 10% restante → ticket
      - servicio externo con > 5% de errores → ticket

6. DASHBOARDS
   Diseñar la estructura de dashboards operacionales:
   
   a) Dashboard de salud del sistema (overview):
      - tasa de error global y por servicio
      - latencia P95 y P99 por servicio
      - throughput (req/s) por servicio
      - estado de SLOs (% cumplimiento, error budget restante)
      - incidentes activos
   
   b) Dashboard por servicio (drill-down):
      - RED metrics del servicio
      - distribución de latencia por endpoint
      - top 10 endpoints por error
      - trazas lentas o con error
      - logs relacionados (integración directa desde dashboard)
   
   c) Dashboard de infraestructura:
      - CPU, memoria, disco por nodo/contenedor
      - conexiones activas de BD, pool usage
      - tamaño de colas de mensajes

7. STACK DE OBSERVABILIDAD RECOMENDADO
   Proponer el stack según la infraestructura del proyecto:
   
   Opción cloud-native:
   - Métricas: Prometheus + Grafana / CloudWatch / Datadog
   - Logs: Loki + Grafana / CloudWatch Logs / Datadog Logs
   - Trazas: Tempo + Grafana / X-Ray / Datadog APM
   - Alertas: Alertmanager / CloudWatch Alarms / PagerDuty
   
   Opción OSS autoalojada:
   - Prometheus (métricas) + Loki (logs) + Tempo (trazas) + Grafana (visualización)
   - OpenTelemetry Collector como agente universal de exportación
   
   Para cada componente del stack seleccionado, proporcionar:
   - instrucción de instalación o configuración básica
   - configuración de exportación desde la aplicación (SDK, agente, sidecar)

Entregables:
- mapa de instrumentación por componente (métricas, logs, trazas definidas),
- catálogo de SLOs con SLI, objetivo y error budget,
- catálogo de alertas con condición, severidad y playbook,
- estructura de dashboards recomendada,
- stack de observabilidad propuesto con configuración inicial.
```

---

## Fórmula estándar de uso

```text
Usa el prompt de observabilidad e instrumentación y adáptalo a:
- repositorio: [NOMBRE O URL]
- stack tecnológico: [lenguaje, framework, base de datos, mensajería]
- infraestructura: [cloud provider / on-premise / contenedores / serverless]
- stack de observabilidad actual: [ninguno / Prometheus+Grafana / Datadog / CloudWatch / otro]
- número de servicios: [monolito / N microservicios]
- SLAs comprometidos con clientes: [tiempo de respuesta, disponibilidad]
- entorno objetivo: [producción / staging / ambos]
- documentos a revisar: arquitectura del sistema, runbooks existentes, modelo de amenazas 13-04
- objetivo de salida específico: catálogo de SLOs + alertas + estructura de dashboards
- nivel de profundidad: alto
```

---

## Resultado esperado

### Catálogo de SLOs

| Servicio | SLI | SLO | Ventana | Error budget |
|---|---|---|---|---|
| API Gateway | % requests con P95 < 500ms | 99.5% | 30 días | 0.5% ≈ 3.6 h/mes |
| Auth Service | % logins exitosos / total intentos válidos | 99.9% | 30 días | 0.1% ≈ 44 min/mes |
| Worker de pagos | % jobs procesados sin error | 99.95% | 30 días | 0.05% ≈ 22 min/mes |

### Catálogo de alertas

| Alerta | Condición | Severidad | Playbook | Destinatario |
|---|---|---|---|---|
| High error rate | tasa de error > 1% durante 5 min | Page | Runbook 11-04 § Error rate | #oncall + PagerDuty |
| High latency | P99 > 1s durante 5 min | Page | Runbook 11-04 § Latencia | #oncall |
| Error budget < 10% | burn rate > 14.4× en 1h | Ticket | Ver dashboard SLO | #tech-lead |
| DB pool exhaustion | conexiones activas > 90% del pool | Ticket | Runbook 11-04 § BD | #backend |
