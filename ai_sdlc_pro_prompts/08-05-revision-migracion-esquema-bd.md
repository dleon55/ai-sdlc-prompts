# 8.5 — Revisión de migración de esquema de base de datos

## Descripción

Prompt para revisar una migración de esquema de base de datos ANTES de aplicarla: qué hace exactamente el DDL, qué bloqueos adquiere y por cuánto tiempo, si es compatible con el código actualmente desplegado durante un rolling deploy, si requiere un patrón expand-contract, si existe una ruta de rollback verificada y si hay riesgo de pérdida de datos.

**Cuándo usarlo:** antes de ejecutar una migración de esquema contra staging o producción — como parte del PR que introduce el archivo de migración, o como último control antes del `migrate up` en el pipeline de despliegue. No lo confundas con `08-04-sql-query-profiling`: ese prompt analiza el plan de ejecución de una CONSULTA sobre un esquema que ya existe (`EXPLAIN ANALYZE`, N+1, índices faltantes); este prompt evalúa la SEGURIDAD del propio CAMBIO de esquema — bloqueos de tabla, compatibilidad con el código desplegado, patrón expand-contract y reversibilidad — antes de que ese cambio se ejecute.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis / validación |
| Riesgo esperado | alto — una migración de esquema mal evaluada y aplicada a ciegas puede bloquear tablas de alto tráfico, romper el código actualmente desplegado durante un rolling deploy o causar pérdida irreversible de datos; el prompt en sí es de solo lectura, pero el costo de un diagnóstico incompleto se paga en producción |
| Entradas requeridas | script o archivo de migración (DDL exacto, up y down si existen), motor de base de datos y versión, tamaño aproximado y tráfico de la(s) tabla(s) afectada(s), fragmento relevante del código actualmente desplegado que lee o escribe esas columnas/tablas, estrategia de despliegue (rolling / blue-green / con downtime permitido) |
| Herramientas permitidas | lectura del script de migración, del esquema actual y del código proporcionado; sin acceso a la base de datos real, sin ejecutar la migración ni ningún DDL/DML contra ningún ambiente |
| Autonomía permitida | A0 — Analizar (diagnóstico de riesgo); A1 — Proponer (versión corregida de la migración, plan expand-contract, script de rollback, como propuesta); nunca A2/A3 — este prompt no ejecuta ni aplica la migración bajo ninguna circunstancia |
| Criterios de detención | detener y escalar a aprobación humana explícita si la migración toma un lock de tabla completo sobre una tabla de alto tráfico sin plan de ventana de mantenimiento; detener si no se puede confirmar compatibilidad con el código actualmente desplegado; nunca dar por aceptable una operación con pérdida de datos irreversible solo porque quien la solicita dice que "está bien" — señalarla explícitamente igual |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada riesgo señalado debe citar la sentencia DDL exacta responsable (ADD COLUMN, DROP COLUMN, ALTER TYPE, CREATE INDEX, etc.) y, cuando aplique, el fragmento de código actualmente desplegado que quedaría incompatible |
| Siguiente prompt recomendado | `11-09-runbook-rollback` para documentar y preparar el procedimiento de rollback en caso de que la migración deba revertirse después de aplicada |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como un Database Reliability Engineer / DBA Senior. Revisa la migración de esquema propuesta y determina si es segura para aplicar, identificando bloqueos, incompatibilidades con el código desplegado, riesgo de pérdida de datos y necesidad de un patrón expand-contract, ANTES de que se ejecute contra cualquier ambiente compartido.

Entradas:
- motor_bd_y_version: [PostgreSQL 15 / MySQL 8 / SQL Server / etc.]
- migracion: [PEGA EL DDL COMPLETO DE LA MIGRACIÓN — UP Y DOWN SI EXISTEN]
- tabla_afectada_volumetria: [FILAS APROXIMADAS, TRÁFICO DE LECTURA/ESCRITURA POR SEGUNDO EN PRODUCCIÓN]
- codigo_desplegado_relevante: [FRAGMENTOS DE CÓDIGO/ORM QUE LEEN O ESCRIBEN LAS COLUMNAS/TABLAS AFECTADAS]
- estrategia_despliegue: [ROLLING / BLUE-GREEN / VENTANA DE MANTENIMIENTO PERMITIDA]

Pasos:

1. IDENTIFICA QUÉ HACE LA MIGRACIÓN
   Descompón el DDL en operaciones atómicas: ADD COLUMN, DROP COLUMN, RENAME COLUMN, ALTER COLUMN TYPE,
   ADD/DROP CONSTRAINT (NOT NULL, FK, UNIQUE, CHECK), CREATE/DROP INDEX, RENAME TABLE, etc.
   Para cada operación indica si es aditiva (segura por naturaleza) o destructiva/bloqueante (requiere análisis).

2. EVALÚA EL COMPORTAMIENTO DE BLOQUEO PARA EL MOTOR INDICADO
   Para cada operación: ¿adquiere un lock a nivel de tabla o de fila? ¿Es un lock exclusivo que bloquea
   lecturas y escrituras, o admite concurrencia (ej. `CREATE INDEX CONCURRENTLY` en PostgreSQL,
   `ALGORITHM=INPLACE, LOCK=NONE` en MySQL)? Estima cuánto tiempo se mantendría ese lock dado el volumen
   de filas declarado — no asumas una tabla de desarrollo con pocas filas.

3. VERIFICA COMPATIBILIDAD CON EL CÓDIGO ACTUALMENTE DESPLEGADO
   Con base en `codigo_desplegado_relevante`, determina si el código que sigue corriendo DURANTE el
   rolling deploy (antes de que la nueva versión esté 100% desplegada) seguiría funcionando contra el
   esquema resultante. Casos típicos de ruptura: DROP de una columna que el código viejo todavía lee o
   escribe, RENAME sin vista/alias de compatibilidad, cambio de tipo que el código viejo no puede
   deserializar, nueva columna NOT NULL sin default que el código viejo no popula al insertar.

4. DETERMINA SI SE REQUIERE UN PATRÓN EXPAND-CONTRACT
   Si el paso 3 detecta incompatibilidad, propone la secuencia expand-contract en migraciones separadas:
   (a) expandir — agregar la columna/tabla nueva sin tocar la vieja; (b) desplegar código que escribe en
   ambas; (c) backfill de datos históricos; (d) desplegar código que lee solo de la nueva; (e) contraer —
   eliminar la columna/tabla vieja en una migración POSTERIOR, solo cuando ya no la referencia ningún
   código desplegado. Indica en qué paso de esa secuencia se ubica la migración bajo revisión.

5. EVALÚA EL RIESGO DE PÉRDIDA DE DATOS
   Señala explícitamente cualquier operación irreversible: DROP COLUMN, DROP TABLE, TRUNCATE, cambio de
   tipo que trunca o pierde precisión, downgrade de constraint que descarta filas existentes. Indica si
   hay un respaldo o snapshot verificado antes de ejecutar. No aceptes como válida la afirmación de que
   "los datos no importan" sin que quede documentada como decisión explícita del solicitante.

6. VERIFICA LA RUTA DE ROLLBACK
   Revisa si existe un script `down`/reversa para esta migración específica y si es simétrico y seguro de
   ejecutar (ej. un rollback que reintente recrear una columna eliminada no puede recuperar los datos ya
   perdidos). Si no hay rollback definido o el rollback es incompleto, señálalo como bloqueante.

7. VERIFICA IDEMPOTENCIA Y SEGURIDAD DE RE-EJECUCIÓN
   Determina qué ocurre si la migración se ejecuta dos veces (ej. por reintento de pipeline) o si falla a
   mitad de camino: ¿deja el esquema en un estado intermedio inconsistente? ¿el DDL usa
   `IF NOT EXISTS`/`IF EXISTS` o falla ruidosamente en un re-run seguro?

8. ESTIMA EL TIEMPO DE EJECUCIÓN Y CLASIFICA COMO ONLINE O CON VENTANA DE MANTENIMIENTO
   Proyecta el tiempo de aplicación contra la volumetría real de producción declarada (no contra una BD
   de desarrollo). Clasifica la migración como segura para ejecutar en caliente o como dependiente de una
   ventana de mantenimiento, y justifica con la evidencia de los pasos 2 y 8.

Restricciones:
- nunca apruebes una migración que adquiera un lock de tabla completo y prolongado sobre una tabla de alto tráfico sin un plan explícito de ventana de mantenimiento o sin una alternativa online equivalente,
- nunca asumas compatibilidad hacia atrás con el código desplegado sin haber revisado el fragmento de código real proporcionado; si no se proporcionó código relevante, dilo explícitamente y marca la compatibilidad como no verificada en lugar de asumirla,
- señala toda operación con pérdida de datos irreversible de forma explícita y destacada, incluso si quien solicita la revisión afirma que es aceptable — la aceptación debe quedar registrada como decisión humana, no absorbida silenciosamente en la aprobación,
- este prompt revisa y recomienda; nunca ejecuta la migración, ni el DDL de corrección propuesto, ni ningún comando contra una base de datos real,
- si se desconoce la volumetría o el patrón de tráfico de producción de la tabla afectada, dilo explícitamente y no asumas un escenario de tabla pequeña o de bajo tráfico para calificar la migración como segura.

Entrega:
1. RESUMEN DE LA MIGRACIÓN — qué hace, sentencia por sentencia.
2. RIESGO DE BLOQUEO — tipo de lock, duración estimada, tablas/filas afectadas.
3. COMPATIBILIDAD CON CÓDIGO DESPLEGADO — compatible / incompatible y por qué, con cita del código.
4. ESTRATEGIA RECOMENDADA — aplicación directa o secuencia expand-contract detallada.
5. RIESGO DE PÉRDIDA DE DATOS — operaciones irreversibles señaladas explícitamente.
6. RUTA DE ROLLBACK — existente/verificada, incompleta o ausente.
7. VEREDICTO — apto para ejecución online / requiere ventana de mantenimiento / bloqueado hasta corregir, con la lista de cambios requeridos antes de aprobar.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de revisión de migración de esquema de base de datos y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- motor_bd_y_version: [MOTOR Y VERSIÓN]
- migracion: [ARCHIVO O DDL]
- ambiente: [STAGING / PROD]
- tabla_afectada_volumetria: [FILAS Y TRÁFICO]
- documentos a revisar: código desplegado relevante, migraciones previas, runbook de despliegue
- objetivo puntual de salida: veredicto de seguridad de la migración + estrategia recomendada
- nivel de profundidad: alto
```

---

## Salida esperada

| Migración | Tipo de cambio | Riesgo de lock | Compatible con código actual | Estrategia (directa/expand-contract) | Rollback verificado |
|---|---|---|---|---|---|
| `0042_add_status_not_null_orders.sql` | `ADD COLUMN status VARCHAR(20) NOT NULL` sin default sobre `orders` (18M filas, ~400 writes/s) | Alto — en la mayoría de motores, un `ADD COLUMN NOT NULL` sin default reescribe la tabla completa y toma lock exclusivo durante toda la operación; a este volumen puede tomar varios minutos | No — el código actualmente desplegado inserta filas en `orders` sin enviar `status`, por lo que fallaría contra la nueva restricción NOT NULL de inmediato | Expand-contract: (1) agregar columna nullable con DEFAULT, (2) desplegar código que escriba `status` explícito, (3) backfill de filas históricas, (4) migración posterior que agrega el NOT NULL solo cuando el 100% de escrituras ya envían el valor | No — la migración no incluye script `down`; se requiere antes de aprobar |
