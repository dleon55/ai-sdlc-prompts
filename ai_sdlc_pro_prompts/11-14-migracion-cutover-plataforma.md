# 11.14 — Plan de migración y cutover de plataforma o sistema legacy

## Descripción

Prompt para diseñar el plan de migración de una plataforma, sistema o stack antiguo a uno nuevo: estrategia de migración de datos (big-bang vs. incremental, dual-write, backfill), secuenciación del cutover de tráfico (todo-o-nada vs. progresivo), verificación de consistencia entre el sistema origen y el destino, y plan de rollback específico de la migración. Es el paso que ocurre **antes** de poder decomisionar el sistema origen con `11-11-plan-decomiso-sistema-legacy`, y es distinto de `08-05-revision-migracion-esquema-bd`, que solo revisa la seguridad de un cambio de esquema de base de datos ya escrito — este prompt diseña el movimiento completo de una aplicación, sus datos y su tráfico entre dos sistemas.

**Cuándo usarlo:** cuando se decide mover una aplicación, sus datos o su tráfico de un sistema/stack/nube antiguo a uno nuevo (upgrade mayor de stack, migración de nube, consolidación de sistemas, monolito→microservicios) — antes de ejecutar cualquier cutover real, y como paso previo obligatorio a `11-11` si el objetivo final es apagar el sistema origen.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | alto — una migración mal secuenciada puede causar pérdida de datos, downtime no planeado o inconsistencia entre sistemas si el corte de tráfico ocurre antes de que el backfill o la verificación estén completos; el prompt no ejecuta ninguna migración de datos ni mueve tráfico real por sí mismo |
| Entradas requeridas | sistema origen y destino (descripción, stack, volumen de datos), arquitectura de destino si existe (`00-D-02`/`04-01`), restricciones de downtime tolerable, dependientes conocidos del sistema origen (inventario de `11-11` si existe) |
| Herramientas permitidas | ninguna de ejecución — lectura de documentación y arquitectura existentes; produce un documento de plan, no ejecuta ninguna migración de datos ni corte de tráfico |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si no puede confirmarse una estrategia de verificación de consistencia de datos entre origen y destino, no declarar el plan de cutover como listo para ejecutar — marcarlo como bloqueante en vez de asumir consistencia |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada etapa del cutover declara criterio de avance verificable y plan de rollback específico; la estrategia de migración de datos declara el método de verificación de consistencia usado |
| Siguiente prompt recomendado | `11-11-plan-decomiso-sistema-legacy` una vez el cutover se completó y el sistema origen ya no recibe tráfico; `11-09-runbook-rollback` para el rollback de un solo despliegue puntual dentro del plan de cutover, si aplica |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña el plan de migración y cutover de un sistema, plataforma o stack antiguo a uno nuevo, con estrategia de migración de datos, secuenciación del corte de tráfico, verificación de consistencia y plan de rollback específico de la migración.

Entradas:
- sistema origen: [DESCRIPCIÓN, STACK, VOLUMEN DE DATOS APROXIMADO]
- sistema destino: [DESCRIPCIÓN, STACK, O REFERENCIA A 00-D-02/04-01]
- razón de la migración: [UPGRADE DE STACK / MIGRACIÓN DE NUBE / CONSOLIDACIÓN / MONOLITO→MICROSERVICIOS / OTRO]
- downtime tolerable: [VENTANA MÁXIMA ACEPTABLE, O "cero downtime requerido"]
- dependientes conocidos del sistema origen: [PEGAR O REFERENCIA AL INVENTARIO DE 11-11, O "no inventariados aún"]

Actividades:
1. INVENTARIO DE ALCANCE
   Define qué migra (datos, funcionalidad, integraciones, usuarios/tenants) y qué queda explícitamente fuera de esta fase de migración, con la razón — no dejes ningún componente del sistema origen sin una decisión explícita de si migra o no.

2. ESTRATEGIA DE MIGRACIÓN DE DATOS
   Define big-bang (corte único de todos los datos) vs. incremental (por lotes, por tenant, por región); si es incremental, define el orden. Si el sistema debe seguir operando durante la migración, define la estrategia de dual-write (escribir a ambos sistemas simultáneamente) o de sincronización continua, y el mecanismo de backfill de datos históricos previos al inicio de la migración.

3. VERIFICACIÓN DE CONSISTENCIA
   Define cómo se confirmará, con evidencia concreta (conteo de registros, checksums, muestreo, reconciliación), que los datos en el sistema destino son consistentes con el origen antes de cortar tráfico. Nunca declares consistencia lograda sin un método de verificación citado; define también el umbral de discrepancia aceptable, si alguno.

4. ESTRATEGIA DE CUTOVER
   Define todo-o-nada vs. progresivo (canary por segmento de usuario, tenant o región). Si es progresivo, define el criterio de avance objetivo entre etapas y quién tiene autoridad para decidir avanzar a la siguiente etapa.

5. PLAN DE ROLLBACK ESPECÍFICO DE LA MIGRACIÓN
   Distinto de un rollback de un solo despliegue: define cómo revertir el corte de tráfico hacia el sistema origen si el destino falla después del cutover, incluyendo qué pasa con los datos escritos en el destino durante la ventana en que estuvo activo (se pierden, se reconcilían hacia el origen, u otro). Si no existe una estrategia de rollback viable para alguna etapa, decláralo como riesgo abierto en vez de omitirlo.

6. CRITERIOS DE ÉXITO Y CIERRE
   Define qué confirma que la migración está completa (sistema destino sirviendo el 100% del tráfico de forma estable, sin errores de reconciliación pendientes). Este es el punto en el que el sistema origen queda candidato para `11-11-plan-decomiso-sistema-legacy`.

7. COMUNICACIÓN
   Define qué stakeholders o equipos deben ser notificados antes, durante y después del cutover, y por qué canal.

Restricciones:
- nunca declares "migración completa" sin un criterio de verificación de consistencia de datos citado y confirmado — una migración sin verificación se reporta como no verificable, no como exitosa,
- toda etapa del cutover progresivo debe declarar su propio criterio de avance y su propio plan de rollback — no asumas que el rollback de la última etapa cubre a las etapas anteriores,
- no propongas cortar tráfico al 100% en un solo paso si el downtime tolerable declarado es "cero" y no existe estrategia de dual-write o sincronización continua — señala esa contradicción explícitamente en vez de ignorarla,
- este prompt diseña el plan; no ejecuta ninguna migración de datos, no corta tráfico real ni modifica configuración de infraestructura,
- si faltan datos de dependientes del sistema origen (usuarios, integraciones, otros servicios), detente y solicita el inventario — o ejecuta primero la fase de inventario de `11-11` — antes de proponer el plan.

Salida:
0. Bloque JSON de metadatos (claves: status, migration_strategy, cutover_stages_count, unmitigated_rollback_risks_count, confidence_score [0.0 a 1.0]).
1. Inventario de alcance: qué migra, qué no, y por qué.
2. Estrategia de migración de datos: método, backfill, dual-write si aplica.
3. Plan de verificación de consistencia: método, umbral aceptable de discrepancia.
4. Plan de cutover: etapas, criterio de avance por etapa, responsable de la decisión.
5. Plan de rollback por etapa.
6. Criterios de éxito y cierre (listo para `11-11`).
7. Plan de comunicación.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de migración y cutover de plataforma y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- sistema origen: [DESCRIPCIÓN Y STACK]
- sistema destino: [DESCRIPCIÓN Y STACK, O REFERENCIA A 00-D-02/04-01]
- downtime tolerable: [VENTANA MÁXIMA ACEPTABLE]
- documentos a revisar: arquitectura destino, inventario de dependientes (11-11) si existe
- objetivo puntual de salida: plan de migración y cutover con verificación de consistencia y rollback por etapa
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen del plan |
| Inventario de alcance (1) | Qué migra y qué no, con justificación |
| Estrategia de migración de datos (2) | Método (big-bang/incremental), backfill, dual-write si aplica |
| Verificación de consistencia (3) | Método concreto y umbral de discrepancia aceptable |
| Plan de cutover (4) | Etapas con criterio de avance y responsable de la decisión |
| Plan de rollback (5) | Estrategia de reversión específica por cada etapa del cutover |
| Criterios de éxito y cierre (6) | Condición objetiva para considerar la migración completa |
| Comunicación (7) | Stakeholders a notificar, momento y canal |

### Ejemplo (fragmento)

```json
{
  "status": "plan_definido_con_riesgo_abierto",
  "migration_strategy": "incremental_por_tenant_con_dual_write",
  "cutover_stages_count": 4,
  "unmitigated_rollback_risks_count": 1,
  "confidence_score": 0.71
}
```

| Etapa | Alcance | Criterio de avance | Responsable | Rollback |
|---|---|---|---|---|
| 1 — Canary | 2% de tenants (cuentas internas de prueba) | 0 errores de reconciliación en 48h, latencia P95 dentro de ±10% del sistema origen | Líder técnico de migración | Revertir DNS/routing al sistema origen; datos escritos en destino durante la ventana se descartan (no hubo escritura de usuarios reales) |
| 2 — 10% de tenants | Tenants de bajo volumen, sin SLA contractual estricto | 0 errores de reconciliación en 72h | Líder técnico + aprobación de Producto | Revertir routing; reconciliar hacia el origen los datos escritos en destino durante la ventana (ventana corta, volumen bajo) |
| 4 — 100% | Todos los tenants | Sistema destino estable 7 días sin incidentes de severidad alta | Patrocinador del proyecto | **[RIESGO ABIERTO]** no existe estrategia de reconciliación viable para revertir 100% del tráfico después de 7 días de escritura en destino — requiere decisión del patrocinador sobre tolerancia a pérdida de datos en caso de rollback tardío |
