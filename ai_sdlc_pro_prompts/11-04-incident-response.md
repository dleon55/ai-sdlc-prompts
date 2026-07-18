# 11.4 — Runbook de incident response en producción

## Descripción

Prompt para ejecutar el proceso completo de respuesta a incidentes en producción: detección, clasificación de severidad, activación del equipo, diagnóstico, contención, resolución, comunicación, post-mortem y lecciones aprendidas. Compatible con entornos multi-agente.

**Cuándo usarlo:** cuando se detecta un incidente activo en producción, para documentar el proceso de respuesta a posteriori, o para diseñar el runbook estándar del proyecto antes de que ocurra el primer incidente.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | operación |
| Riesgo esperado | alto — coordina acciones sobre producción activa, incluida contención con posible rollback |
| Entradas requeridas | síntoma/alerta, sistema afectado, ambiente, hora de detección, fuente de detección, stack |
| Herramientas permitidas | fases 1-3 y 6-7: solo lectura de logs/métricas; fase 4 (contención) puede requerir rollback o mitigación, siempre con aprobación |
| Autonomía permitida | A0 — Analizar en fases 1-3 y 6-7; A3 — Publicar en fase 4 (rollback, mitigación o mutación contra producción activa son despliegue/mutación remota según `00-framework.md`, no ejecución en workspace aislado), solo si el runbook ya autorizó la acción específica y con la aprobación explícita o política preautorizada que exige A3 |
| Criterios de detención | el propio prompt exige detener toda operación de agentes IA en el repositorio y no desplegar código mientras el incidente esté activo |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cronología con hora exacta de cada fase y actor responsable |
| Siguiente prompt recomendado | `03-02-causa-raiz` para el análisis formal si el post-mortem requiere profundidad adicional; `11-07-sre-postmortem-runbook` para consolidar lecciones aprendidas |

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
- sistema/servicio afectado: [SERVICIO]
- ambiente: PROD
- hora de detección: [HH:MM zona horaria]
- detectado por: [monitoreo automático / usuario / equipo / agente IA]
- stack del sistema: [STACK]

Restricciones:
- durante un incidente activo, prioriza la contención del impacto sobre la búsqueda de la causa raíz: estabilizar el sistema para los usuarios viene primero que entender por completo qué falló — la causa raíz profunda se investiga en el post-mortem (Fase 7), no a mitad de un SEV-1.
- ninguna acción de remediación destructiva (rollback, reinicio forzado, failover, modo mantenimiento, cambio de configuración en producción) se ejecuta sin aprobación explícita del responsable de turno, incluso en SEV-1 — la urgencia de contener no reemplaza la autorización, que puede darse en segundos por el canal de coordinación pero debe quedar registrada.
- define y respeta triggers claros de escalamiento y handoff: si el incidente supera el SLA de resolución de su severidad, si quien responde inicialmente no puede continuar, o si el diagnóstico revela que el sistema afectado no es el que se pensó originalmente, escala explícitamente a un responsable superior u otro equipo y documenta el traspaso (hora, de quién a quién, estado conocido hasta ese momento).
- respeta la pausa de agentes IA y de despliegues indicada en la Fase 2 durante toda la duración del incidente activo, no solo al momento de la detección.

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
Equipo respondiendo: [RESPONSABLE]
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

Esta fase produce un resumen inmediato del post-mortem. Para el documento formal con guía blameless detallada y un runbook on-call reutilizable, continúa con `11-07-sre-postmortem-runbook`.

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

### Ejemplo aplicado

| Campo | Valor |
|---|---|
| ID incidente | INC-20260312-014 |
| Severidad | SEV-2 |
| Sistema afectado | API de checkout |
| Hora detección | 14:32 UTC |
| Hora resolución | 15:10 UTC |
| Duración | 38 min |
| Afectados | ~2.400 usuarios (tasa de error 6.8%) |
| Causa raíz | pool de conexiones a la BD agotado tras un deploy que removió el límite de conexiones concurrentes |
| Fix | rollback del deploy `a1b2c3d` (PR #482) |
| Post-mortem | 2026-03-14 |
| Estado | resuelto |

| Hora | Fase | Evento | Actor |
|---|---|---|---|
| 14:32 | Detección | Alerta de tasa de error > 5% en API de checkout | Datadog (automático) |
| 14:36 | Activación | Equipo on-call notificado por PagerDuty, canal #inc-014 abierto | on-call SRE |
| 14:50 | Contención | Rollback del deploy `a1b2c3d` ejecutado | on-call SRE (con aprobación del tech lead) |
| 15:10 | Resolución | Tasa de error vuelve a < 0.1%, incidente cerrado | on-call SRE |
