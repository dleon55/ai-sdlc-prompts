# 11.11 — Plan de decomiso de sistema o servicio legacy

## Descripción

Prompt para planificar el apagado completo y seguro de un sistema, servicio o base de datos que deja de operarse — distinto del versionado/deprecación parcial de una API (que cubre `04-05-versionado-deprecacion-api`). Incluye inventario de dependientes activos, obligaciones de retención o exportación de datos antes del apagado, plan de comunicación con ventana de gracia, y secuencia de apagado por fases con checkpoints de rollback si aparece un dependiente no detectado.

**Cuándo usarlo:** cuando se decide retirar por completo un sistema, servicio o base de datos, antes de ejecutar cualquier acción de apagado.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | operación |
| Riesgo esperado | alto — decomisar un sistema con dependientes no detectados puede romper servicios o reportes en producción sin aviso previo; perder datos sujetos a una obligación de retención (legal, fiscal, contractual) puede tener consecuencias legales |
| Entradas requeridas | sistema/servicio a decomisar, inventario conocido de consumidores/integraciones, obligaciones de retención de datos aplicables, fecha objetivo de apagado, disponibilidad de logs de acceso/tráfico reciente al sistema |
| Herramientas permitidas | lectura de logs de acceso/tráfico, código de integraciones conocidas, contratos de retención de datos y documentación de arquitectura; el diseño del plan es de solo análisis y propuesta — la ejecución del apagado real requiere aprobación explícita y ocurre fuera de este prompt |
| Autonomía permitida | A0 — Analizar (inventario de dependientes, obligaciones de retención); A1 — Proponer (plan de comunicación y secuencia de apagado); A3 — Publicar únicamente para ejecutar cada fase de apagado (deshabilitar escritura, pasar a solo lectura, apagado final) contra el sistema real, y solo con aprobación explícita antes de cada fase — no ejecuta ninguna fase de apagado por sí solo |
| Criterios de detención | detener si los logs de acceso/tráfico reciente no están disponibles o no cubren un periodo representativo — no asumir que "no hay tráfico visible" significa "no hay dependientes"; detener si existe una obligación de retención de datos sin plan de cumplimiento antes de la fecha de apagado |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada dependiente identificado cita la fuente que lo confirma (log de acceso, código de integración, documentación); cada fase de apagado tiene un checkpoint de verificación y un criterio de rollback explícito |
| Siguiente prompt recomendado | `04-05-versionado-deprecacion-api` si el decomiso es parcial (una versión de API, no el sistema completo) y este prompt no aplica; `11-09-runbook-rollback` si aparece un dependiente no detectado durante la ejecución y se requiere revertir una fase ya ejecutada |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña el plan completo de decomiso seguro de un sistema, servicio o base de datos que deja de operarse: inventario de dependientes, obligaciones de retención de datos, plan de comunicación, y secuencia de apagado por fases con checkpoints de rollback.

Entradas:
- sistema/servicio a decomisar: [NOMBRE O DESCRIPCIÓN]
- inventario conocido de consumidores/integraciones: [LISTA O "por determinar"]
- logs de acceso/tráfico reciente disponibles: [PERIODO CUBIERTO O "no disponibles"]
- obligaciones de retención de datos: [LEGAL / FISCAL / CONTRACTUAL / NINGUNA CONOCIDA]
- fecha objetivo de apagado: [FECHA]
- stack/infraestructura del sistema: [STACK]

Pasos:
1. INVENTARIO DE DEPENDIENTES ACTIVOS
   A partir de los logs de acceso/tráfico reciente y el código de integraciones conocidas, identifica todo consumidor activo del sistema (servicios, reportes, jobs batch, integraciones externas, usuarios directos). Si los logs no cubren un periodo representativo (ej. procesos que corren solo mensual o trimestralmente), señálalo explícitamente como brecha de visibilidad antes de concluir que no hay dependientes.

2. CLASIFICACIÓN DE DEPENDIENTES POR CRITICIDAD
   Para cada dependiente identificado, clasifica el impacto de que deje de funcionar (crítico para negocio, degradación aceptable, ya obsoleto) y si tiene una alternativa ya disponible o requiere migración antes del apagado.

3. OBLIGACIONES DE RETENCIÓN Y EXPORTACIÓN DE DATOS
   Verifica si existe una obligación de retención de datos (legal, fiscal, contractual) aplicable a la información del sistema. Si existe, define qué datos deben exportarse, en qué formato, a dónde, y por cuánto tiempo deben conservarse tras el apagado. Si no puedes confirmar si existe una obligación aplicable, decláralo como riesgo no resuelto en vez de asumir que no aplica.

4. PLAN DE COMUNICACIÓN Y VENTANA DE GRACIA
   Define a quién se debe notificar (dueños de los dependientes identificados, usuarios directos si aplica), con cuánta anticipación, y qué ventana de gracia se ofrece para que los dependientes migren o dejen de usar el sistema antes del apagado definitivo.

5. SECUENCIA DE APAGADO SEGURA (por fases)
   Diseña el apagado en fases con reversibilidad decreciente, nunca todo de una vez:
   a) Deshabilitar escritura nueva (el sistema sigue disponible en solo lectura) — fase reversible.
   b) Solo lectura durante la ventana de gracia acordada, monitoreando si aparece tráfico inesperado.
   c) Apagado final (el sistema deja de responder) — fase de menor reversibilidad, solo tras confirmar ausencia de tráfico en la fase anterior.
   Para cada fase, define el checkpoint de verificación (qué revisar antes de avanzar a la siguiente) y el criterio de rollback si aparece un dependiente no detectado.

6. PLAN DE ROLLBACK POR FASE
   Para cada fase de la secuencia, define explícitamente cómo revertir si aparece un dependiente no detectado (ej. reactivar escritura, restaurar el sistema desde el último backup) y el tiempo estimado de esa reversión.

Restricciones:
- no concluyas que un sistema no tiene dependientes solo porque los logs de tráfico reciente no muestran actividad — si el periodo cubierto no es representativo (procesos poco frecuentes, integraciones estacionales), decláralo como brecha de visibilidad y trata el riesgo como no resuelto,
- no propongas ni ejecutes el apagado final en una sola fase — el apagado debe ser progresivo (deshabilitar escritura → solo lectura → apagado final), con un checkpoint de verificación entre cada fase,
- si existe una obligación de retención de datos y no hay un plan de exportación o conservación confirmado, detente y no continúes con la secuencia de apagado hasta resolverlo,
- cada fase de apagado que efectivamente se ejecute contra el sistema real requiere aprobación explícita previa — este prompt diseña el plan, no lo ejecuta por sí mismo,
- si aparece un dependiente no detectado durante cualquier fase, el plan debe indicar explícitamente revertir esa fase antes de continuar, nunca "esperar a ver si se resuelve solo".

Salida:
- inventario de dependientes, con criticidad y fuente que lo confirma
- obligaciones de retención de datos y plan de exportación/conservación
- plan de comunicación y ventana de gracia
- secuencia de apagado por fases, con checkpoint y criterio de rollback por fase
- riesgos residuales (brechas de visibilidad, dependientes no confirmables)
```

---

## Uso con fórmula estándar

```text
Usa el prompt de plan de decomiso de sistema legacy y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- sistema/servicio a decomisar: [NOMBRE O DESCRIPCIÓN]
- inventario conocido de consumidores: [LISTA O "por determinar"]
- logs de acceso disponibles: [PERIODO CUBIERTO O "no disponibles"]
- obligaciones de retención: [LEGAL / FISCAL / CONTRACTUAL / NINGUNA CONOCIDA]
- fecha objetivo de apagado: [FECHA]
- documentos a revisar: logs de tráfico, código de integraciones, contratos de retención
- objetivo puntual de salida: plan de decomiso completo con secuencia segura de apagado
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Inventario de dependientes | Consumidor, criticidad, fuente que lo confirma |
| Retención de datos | Obligación aplicable, qué exportar, formato y tiempo de conservación |
| Plan de comunicación | A quién notificar, con cuánta anticipación, ventana de gracia |
| Secuencia de apagado | Fases con checkpoint de verificación y criterio de rollback |
| Riesgos residuales | Brechas de visibilidad o dependientes no confirmables |

### Ejemplo (fragmento)

| Dependiente | Criticidad | Fuente |
|---|---|---|
| Servicio de reportes financieros mensuales | Crítico — genera el cierre contable | Job programado detectado en el orquestador de tareas, corre el día 1 de cada mes (fuera del periodo de logs revisado inicialmente — se amplió la ventana de revisión a 60 días para capturarlo) |
| Integración con proveedor de logística (deprecada hace 8 meses) | Ya obsoleto | Sin tráfico en los últimos 90 días de logs; confirmado con el equipo de logística que migraron al nuevo proveedor |

**Secuencia de apagado, fase 1:** Deshabilitar escritura nueva. Checkpoint: monitorear 5 días hábiles buscando intentos de escritura rechazados en los logs. Rollback: reactivar escritura de inmediato si aparece un intento no anticipado; tiempo estimado de reversión: menor a 10 minutos (flag de configuración).
