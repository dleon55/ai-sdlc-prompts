# 11.9 — Runbook de ejecución de rollback

## Descripción

Prompt para decidir si un cambio recién desplegado debe revertirse o corregirse hacia adelante, y para diseñar (y, cuando esté autorizado, guiar) la ejecución del rollback: mecánica exacta según el tipo de cambio (deploy de código, migración de base de datos, config/feature flag, infraestructura), manejo de datos escritos en la versión nueva y verificación de que el rollback realmente restauró un estado sano.

**Cuándo usarlo:** cuando un cambio desplegado recientemente está causando problemas y se está considerando o ejecutando un rollback. Si esto es un incidente activo que aún no fue triado, usa primero `11-04-incident-response` para clasificar severidad, contener y decidir el curso de acción — este prompt se invoca una vez que el rollback ya es la vía elegida (por ejemplo, desde la Fase 4 de contención de ese runbook). Después de ejecutar el rollback, continúa con `11-07-sre-postmortem-runbook` para documentar qué pasó y por qué.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | operación |
| Riesgo esperado | alto — la decisión de rollback ocurre bajo presión de tiempo durante un problema activo; un rollback mal ejecutado (que pierda datos escritos en la versión nueva, o que asuma reversible una migración de base de datos que no lo es) puede empeorar la situación en vez de resolverla |
| Entradas requeridas | síntoma que motiva el rollback, componente(s) afectados y su tipo de cambio (código / migración de BD / config o feature flag / infraestructura), versión o estado objetivo al que revertir, indicación de si hubo escrituras de datos en la versión nueva, ambiente |
| Herramientas permitidas | diseño del plan de rollback y del criterio de decisión: solo lectura de logs, métricas, historial de deploys y definición de migraciones; la ejecución real contra un ambiente vivo está limitada por la autonomía indicada abajo |
| Autonomía permitida | A1 — Proponer para todo el diseño del criterio de decisión y del runbook de rollback; A2 — Ejecutar controlado solo para la ejecución en un ambiente aislado (staging/QA) con las precondiciones explícitas ya verificadas (versión previa confirmada desplegable, reversibilidad de la migración confirmada); A3 — Publicar para ejecutar el rollback contra producción, y en particular cualquier rollback que toque una migración de base de datos o datos de producción — es despliegue/mutación remota según `00-framework.md`, no ejecución en workspace aislado, y requiere la aprobación explícita o política preautorizada que exige A3 antes de cada acción — este prompt no se autoconcede permiso para ejecutarlo sin esa aprobación |
| Criterios de detención | detener y escalar si la reversibilidad de una migración de base de datos no puede confirmarse; detener si no se puede confirmar que la versión previa es desplegable (dependencias, configuración); detener si el rollback implicaría pérdida de datos no aceptada explícitamente por el responsable del sistema; no ejecutar ninguna acción contra producción sin la aprobación explícita que exige este contrato |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada componente a revertir con su reversibilidad evaluada explícitamente, pasos de ejecución en orden con comando o acción concreta, y verificación post-rollback contra el síntoma original, no solo contra el éxito técnico del despliegue |
| Siguiente prompt recomendado | `11-07-sre-postmortem-runbook` para documentar el incidente y el rollback ejecutado |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Decide si corresponde hacer rollback o corregir hacia adelante, y diseña (o guía, si ya está autorizado) la ejecución del rollback de este cambio.

Inputs requeridos:
- síntoma que motiva el rollback: [DESCRIPCIÓN]
- componente(s) afectados: [LISTA]
- tipo(s) de cambio involucrado: [código / migración de BD / config o feature flag / infraestructura — puede ser más de uno]
- versión o estado objetivo al que revertir: [REFERENCIA — commit, tag, versión de migración, valor de config previo]
- ¿hubo escrituras de datos en la versión nueva desde que se desplegó?: [SÍ / NO / DESCONOCIDO]
- ambiente: [DEV / QA / STAGING / PROD]
- ¿hay un incidente activo coordinado en otro canal/runbook?: [SÍ, referencia / NO]

Pasos:

1. CONFIRMAR EL CRITERIO DE DECISIÓN (rollback vs. roll-forward)
   No asumas que revertir es siempre la opción correcta. Para este problema específico, evalúa:
   - ¿un hotfix acotado resolvería el síntoma más rápido y con menos riesgo que un rollback completo?
   - ¿el rollback es técnicamente más simple porque el cambio es aislado (una sola imagen de contenedor, un solo flag), o es complejo porque toca varios componentes acoplados?
   - ¿cuánto tiempo lleva cada opción, con quién se ejecuta y qué tan reversible es el propio rollback si algo sale mal?
   Declara explícitamente la decisión (rollback / roll-forward) y la razón.

2. IDENTIFICAR EXACTAMENTE QUÉ DEBE REVERTIRSE
   Descompón el cambio desplegado en sus partes y clasifica cada una:
   - código de aplicación (deploy de una imagen/artefacto anterior)
   - migración de base de datos (esquema y/o datos)
   - configuración o feature flag
   - cambio de infraestructura (IaC, recursos cloud, red)
   Cada tipo tiene mecánica y riesgo distintos — no trates el rollback como una sola acción genérica.

3. VALIDAR QUE LA VERSIÓN PREVIA ES REALMENTE DESPLEGABLE (si hay rollback de código)
   - ¿la versión previa estaba funcionando de forma confirmada antes del deploy actual (no era ya una versión rota)?
   - ¿sus dependencias externas (APIs, esquema de BD, formato de mensajes) siguen siendo compatibles con el estado actual del sistema, o el sistema ya avanzó de forma incompatible?
   - si no se puede confirmar alguno de estos puntos, decláralo explícitamente como bloqueo antes de continuar.

4. EVALUAR REVERSIBILIDAD DE LA MIGRACIÓN DE BASE DE DATOS (si aplica)
   Antes de proponer cualquier paso de ejecución, determina explícitamente:
   - ¿la migración es reversible sin pérdida de datos (ej. agregar una columna nullable) o implica pérdida potencial (ej. columnas eliminadas, transformaciones de datos, particiones fusionadas)?
   - si no es reversible sin pérdida, ¿qué datos exactamente se perderían y quién debe aprobar esa pérdida?
   - ¿existe un script de rollback probado (down migration) o habría que reconstruirlo desde un backup?
   Muchas migraciones NO son reversibles de forma segura — este análisis debe completarse y quedar documentado antes de ejecutar nada, no descubrirse a mitad del rollback.

5. MANEJAR LOS DATOS ESCRITOS EN LA VERSIÓN NUEVA
   Si hubo escrituras (transacciones, registros, eventos) desde que se desplegó la versión que se va a revertir:
   - ¿esos datos se pierden al revertir, se preservan tal cual, o necesitan una migración de vuelta a un formato compatible con la versión anterior?
   - ¿existe una ventana de incompatibilidad entre el formato de datos nuevo y el que la versión anterior sabe leer?
   - si hay pérdida de datos inevitable, cuantifícala (cuántos registros, qué usuarios o procesos) y quién debe aceptarla explícitamente.

6. DEFINIR LOS PASOS DE EJECUCIÓN EN ORDEN
   Para cada paso indica: descripción de la acción, comando o procedimiento exacto, resultado esperado, y cómo verificar que ese paso específico fue exitoso antes de continuar al siguiente. Ordena los pasos considerando dependencias entre componentes (por ejemplo, revertir código antes o después de revertir la migración según cuál rompe la compatibilidad).

7. DEFINIR LA VERIFICACIÓN POST-ROLLBACK
   No te límites a confirmar que el despliegue de la versión anterior tuvo éxito técnico. Verifica específicamente que el síntoma original que motivó el rollback esté resuelto:
   - métrica o comportamiento que disparó la decisión, medida después del rollback
   - flujos críticos funcionando end-to-end
   - ausencia de errores nuevos introducidos por el propio rollback (por ejemplo, incompatibilidad entre código viejo y datos ya migrados)

8. COMUNICAR EL ESTADO DEL ROLLBACK
   Si hay un incidente activo coordinado (`11-04-incident-response`), sigue su canal y formato de comunicación. Si no lo hay, define de todas formas: a quién notificar antes de ejecutar, a quién notificar al completar, y qué información mínima debe incluir cada notificación (componente revertido, estado, impacto residual conocido).

Restricciones:
- nunca ejecutes un rollback de una migración de base de datos sin antes confirmar explícitamente si es reversible y qué datos, si los hay, se perderán — esto se declara antes de proponer los pasos de ejecución, no se descubre durante la ejecución.
- la ejecución de un rollback contra un ambiente vivo o de producción requiere la autonomía y aprobación explícita indicadas para este prompt; no te autoconcedas derechos de ejecución más amplios que los definidos.
- si no puedes confirmar que la versión previa es desplegable o que una migración es reversible, dilo explícitamente y trátalo como condición de detención, no como un supuesto razonable para seguir adelante.
- documenta todo rollback ejecutado, incluso los exitosos, porque son eventos operativamente significativos que alimentan el post-mortem y las métricas de confiabilidad.
- no propongas un rollback parcial (revertir el código pero dejar la migración aplicada, o viceversa) sin señalar explícitamente el riesgo de dejar el sistema en un estado inconsistente.

Entrega:
1. Decisión rollback vs. roll-forward con justificación.
2. Descomposición del cambio en componentes a revertir, con reversibilidad evaluada por componente.
3. Plan de manejo de datos escritos en la versión nueva.
4. Pasos de ejecución ordenados con comando/acción y verificación por paso.
5. Plan de verificación post-rollback contra el síntoma original.
6. Plan de comunicación del estado del rollback.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de runbook de rollback y adáptalo a:
- repositorio: [NOMBRE O URL]
- síntoma que motiva el rollback: [DESCRIPCIÓN]
- componente(s) afectados: [LISTA]
- tipo(s) de cambio: [código / migración de BD / config-flag / infraestructura]
- versión objetivo de rollback: [REFERENCIA]
- escrituras en la versión nueva: [SÍ / NO / DESCONOCIDO]
- ambiente: [DEV / QA / STAGING / PROD]
- incidente activo asociado: [REFERENCIA O NO]
- documentos a revisar: historial de deploys, migraciones aplicadas, runbooks/, dashboards de métricas
- objetivo puntual de salida: decisión rollback/roll-forward + plan de ejecución + verificación post-rollback
- nivel de profundidad: alto
```

---

## Salida esperada

| Componente a revertir | Reversible | Pasos de ejecución | Riesgo de pérdida de datos | Verificación post-rollback |
|---|---|---|---|---|
| [código / migración BD / config-flag / infra] | Sí / No / Parcial | [Secuencia de comandos/acciones] | [Ninguno / Descripción cuantificada] | [Qué se mide y umbral esperado] |

### Ejemplo aplicado

| Componente a revertir | Reversible | Pasos de ejecución | Riesgo de pérdida de datos | Verificación post-rollback |
|---|---|---|---|---|
| Deploy de código: API de checkout `v2.14.0` → `v2.13.2` | Sí — versión previa confirmada estable en producción durante 3 semanas, sin cambios de esquema pendientes | 1. `kubectl set image deploy/checkout-api checkout-api=registry/checkout-api:2.13.2` 2. `kubectl rollout status deploy/checkout-api` 3. Verificar 0 pods en `CrashLoopBackOff` | Ninguno — la versión `2.13.2` lee el mismo esquema de BD, no se agregaron columnas nuevas en `v2.14.0` | Tasa de error de `POST /checkout` vuelve a < 0.1% en 5 min; P95 de latencia < 300ms; 20 checkouts de smoke test end-to-end exitosos |
| Migración de BD: `add_loyalty_points_column` (v2.14.0) | Parcial — la columna `loyalty_points` es reversible (`DROP COLUMN`) sin pérdida de datos porque no hubo escritura de otros procesos sobre ella todavía, pero **requiere aprobación explícita del DBA de guardia antes de ejecutar** | 1. Confirmar `SELECT count(*) FROM orders WHERE loyalty_points IS NOT NULL;` = 0 (nadie escribió aún) 2. Ejecutar `down` migration `2026071201_add_loyalty_points_column` 3. Verificar `\d orders` sin la columna | Ninguno si el conteo del paso 1 es 0; si es mayor a 0, DETENER y escalar — esos registros se perderían al hacer `DROP COLUMN` | `SELECT * FROM orders LIMIT 5;` retorna sin error; suite de integración de `orders` en verde |
