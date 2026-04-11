# 11.4 — Runbook de incident response en producción

## Descripción

Prompt para ejecutar el proceso completo de respuesta a incidentes en producción: detección, clasificación de severidad, activación del equipo, diagnóstico, contención, resolución, comunicación, post-mortem y lecciones aprendidas. Compatible con entornos multi-agente.

**Cuándo usarlo:** cuando se detecta un incidente activo en producción, para documentar el proceso de respuesta a posteriori, o para diseñar el runbook estándar del proyecto antes de que ocurra el primer incidente.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Ejecuta o diseña el proceso completo de incident response para este sistema en producción.

Inputs requeridos:
- síntoma o alerta detectada: [DESCRIPCIÓN]
- sistema/servicio afectado: [NOMBRE]
- ambiente: PROD
- hora de detección: [HH:MM zona horaria]
- detectado por: [monitoreo automático / usuario / equipo / agente IA]
- stack del sistema: [STACK]

## FASE 1 — DETECCIÓN Y CLASIFICACIÓN (0–5 min)

### Clasificación de severidad
Clasifica el incidente según su impacto:

| Severidad | Criterio | SLA respuesta | SLA resolución | Ejemplo |
|---|---|---|---|---|
| SEV-1 (Crítico) | Sistema no disponible o datos comprometidos | 5 min | 1 hora | Sitio caído, breach de datos |
| SEV-2 (Alto) | Funcionalidad crítica degradada | 15 min | 4 horas | Login lento, API con errores > 5% |
| SEV-3 (Medio) | Funcionalidad no crítica afectada | 1 hora | 24 horas | Feature secundaria rota |
| SEV-4 (Bajo) | Impacto mínimo o cosmético | 4 horas | 72 horas | Texto incorrecto, warning en logs |

Responde:
- ¿Cuál es la severidad de este incidente y por qué?
- ¿Cuántos usuarios o procesos están afectados?
- ¿Hay riesgo de pérdida o corrupción de datos?

## FASE 2 — ACTIVACIÓN (0–10 min)

### Protocolo de notificación
Indica quién debe ser notificado según la severidad:
- SEV-1/2: responsable técnico + stakeholder de negocio inmediatamente
- SEV-3/4: responsable técnico en horario laboral

### Canal de coordinación
- Canal principal de incidente: [CANAL]
- Frecuencia de updates: cada [N] minutos
- Formato de update: [HH:MM] Estado: [activo/contenido/resuelto] | Impacto: [...] | Próximo update: [HH:MM]

### Para agentes IA activos en el repositorio durante el incidente
- DETENER todas las operaciones de agentes IA en el repositorio
- No hacer merge de PRs abiertos hasta resolver el incidente
- No desplegar código durante el incidente

## FASE 3 — DIAGNÓSTICO (5–30 min)

Ejecuta los siguientes pasos de diagnóstico ordenados por probabilidad e impacto:

### 3.1 Verificación de salud inmediata
Comandos o acciones para confirmar el alcance del problema:
- estado de servicios
- últimos logs de error
- métricas clave (CPU, memoria, latencia, tasa de error)
- cambios recientes (últimos deploys, cambios de config)

### 3.2 Hipótesis ordenadas
Genera hipótesis por orden de probabilidad:
1. [Hipótesis 1] → Cómo validarla → Comando o evidencia
2. [Hipótesis 2] → Cómo validarla → Comando o evidencia
3. ...

### 3.3 Correlación temporal
- ¿Coincide el inicio del incidente con algún deploy reciente?
- ¿Coincide con un pico de carga o evento externo?
- ¿Otros servicios también están afectados?

## FASE 4 — CONTENCIÓN (inmediata si es SEV-1/2)

Acciones para limitar el impacto MIENTRAS se busca la causa raíz:
- rollback del último deploy (si el incidente comenzó después de un deploy)
- increased logging / debug mode
- rate limiting o circuit breaker si hay sobrecarga
- desvío de tráfico a instancia sana
- modo mantenimiento si es necesario

Indica el comando exacto y la estimación de tiempo para cada acción de contención.

## FASE 5 — RESOLUCIÓN

Una vez identificada la causa raíz:
- descripción de la causa raíz confirmada
- fix aplicado: descripción + commit + PR
- prueba de que el fix resuelve el problema
- validación post-fix: smoke test mínimo

## FASE 6 — COMUNICACIÓN

### Comunicación durante el incidente
Genera los templates de comunicación para cada momento:
- Notificación inicial (cuando se detecta)
- Update de progreso (cada N min para SEV-1/2)
- Notificación de resolución

### Template de notificación inicial
```
🔴 [INCIDENTE ACTIVO] [SISTEMA] — SEV-[N]
Hora detección: [HH:MM]
Síntoma: [DESCRIPCIÓN]
Impacto: [USUARIOS/PROCESOS AFECTADOS]
Equipo respondiendo: [NOMBRE]
Próximo update: [HH:MM]
```

### Template de resolución
```
✅ [INCIDENTE RESUELTO] [SISTEMA]
Hora resolución: [HH:MM]
Duración total: [X horas Y minutos]
Causa raíz: [DESCRIPCIÓN BREVE]
Fix aplicado: [DESCRIPCIÓN]
Post-mortem: [FECHA PROGRAMADA]
```

## FASE 7 — POST-MORTEM (dentro de 48–72h)

Documenta el incidente completo en un post-mortem sin blame (blameless):

### Cronología
| Hora | Evento |
|---|---|
| HH:MM | Primer síntoma detectado |
| HH:MM | Alerta activada |
| HH:MM | Equipo notificado |
| HH:MM | Causa raíz identificada |
| HH:MM | Fix desplegado |
| HH:MM | Incidente resuelto |

### Análisis de causa raíz (5 Whys)
Por qué ocurrió el incidente → por qué esa causa → hasta llegar a la causa raíz sistémica.

### Lecciones aprendidas y acciones correctivas
| Lección | Acción correctiva | Responsable | Fecha límite | Issue creado |
|---|---|---|---|---|
```

---

## Uso con fórmula estándar

```text
Usa el prompt de incident response y adáptalo a:
- repositorio: [NOMBRE O URL]
- síntoma: [DESCRIPCIÓN DEL INCIDENTE]
- sistema afectado: [SERVICIO]
- ambiente: PROD
- hora de detección: [HH:MM]
- detectado por: [FUENTE]
- stack: [STACK]
- documentos a revisar: logs de producción, últimos deploys, runbooks/, métricas
- objetivo puntual de salida: clasificación de severidad + pasos de diagnóstico + template de comunicación
- nivel de profundidad: alto
```

---

## Salida esperada

### Ficha del incidente

| Campo | Valor |
|---|---|
| ID incidente | INC-[YYYYMMDD]-[NNN] |
| Severidad | SEV-[N] |
| Sistema afectado | [SISTEMA] |
| Hora detección | [HH:MM TZ] |
| Hora resolución | [HH:MM TZ] |
| Duración | [X horas Y min] |
| Afectados | [N usuarios / procesos] |
| Causa raíz | [DESCRIPCIÓN] |
| Fix | [COMMIT / PR] |
| Post-mortem | [FECHA] |
| Estado | activo / contenido / resuelto |

### Cronología del incidente

| Hora | Fase | Evento | Actor |
|---|---|---|---|
| HH:MM | Detección | | |
| HH:MM | Activación | | |
| HH:MM | Diagnóstico | | |
| HH:MM | Contención | | |
| HH:MM | Resolución | | |
