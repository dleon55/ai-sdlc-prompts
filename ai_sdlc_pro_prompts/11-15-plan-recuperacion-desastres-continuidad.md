# 11.15 — Plan de recuperación ante desastres y continuidad de negocio (DR/BCP)

## Descripción

Prompt para diseñar el plan de recuperación ante desastres (Disaster Recovery) y continuidad de negocio de un sistema: validación de objetivos de RTO/RPO, secuenciación de recuperación de dependencias, procedimiento de failover, cadencia de pruebas de backup-restore, y criterios de activación del plan ante una pérdida catastrófica (pérdida de centro de datos/región, ransomware, corrupción masiva de datos). Distinto de `11-04-incident-response`, que atiende un incidente ya en curso de alcance acotado, y de `11-09-runbook-rollback`, que revierte un solo despliegue reciente — este prompt prepara y valida la capacidad de recuperación completa del sistema ante un escenario de pérdida total, antes de que ocurra.

**Cuándo usarlo:** al definir la arquitectura inicial de un sistema crítico (después de `00-D-02`, donde se declaran los objetivos de RPO/RTO), periódicamente para validar que la capacidad real de recuperación sigue cumpliendo esos objetivos, o al preparar la primera prueba formal de recuperación (drill) de un sistema que nunca ha sido probado.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | alto — un plan de DR no probado o con objetivos de RTO/RPO no validados against la capacidad real de recuperación da una falsa sensación de resiliencia hasta que ocurre el desastre real; el prompt no ejecuta ninguna restauración, failover ni prueba de recuperación por sí mismo |
| Entradas requeridas | objetivos de RTO/RPO declarados (`00-D-02` u otra fuente), arquitectura del sistema y sus dependencias críticas, mecanismo de backup actual (si existe), última prueba de restauración realizada (si alguna) |
| Herramientas permitidas | ninguna de ejecución — lectura de documentación y arquitectura existentes; produce un documento de plan y un procedimiento de prueba, no ejecuta ninguna restauración ni failover real |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si no puede confirmarse que el RTO/RPO objetivo es alcanzable con el mecanismo de backup/replicación actual, no declarar el sistema "recuperable" — marcarlo como brecha de capacidad y reportar el RTO/RPO real estimado en su lugar |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada dependencia crítica del sistema aparece en la secuencia de recuperación con su propio RTO/RPO estimado; toda brecha entre el objetivo declarado y la capacidad real de recuperación se reporta explícitamente, no se asume cerrada |
| Siguiente prompt recomendado | `11-07-sre-postmortem-runbook` si un drill o una activación real del plan revela fallas que requieren postmortem; `00-D-04-registro-riesgos-proyecto` para registrar como riesgo abierto cualquier brecha de capacidad de recuperación no cerrada |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña el plan de recuperación ante desastres y continuidad de negocio del sistema: validación de RTO/RPO, secuencia de recuperación de dependencias, procedimiento de failover, cadencia de pruebas de backup-restore y criterios de activación.

Entradas:
- objetivos de RTO/RPO declarados: [PEGAR O REFERENCIA A 00-D-02, O "no declarados aún"]
- arquitectura del sistema y dependencias críticas: [PEGAR O REFERENCIA A 04-01]
- mecanismo de backup/replicación actual: [DESCRIPCIÓN, O "no existe backup formal"]
- última prueba de restauración realizada: [FECHA Y RESULTADO, O "nunca probado"]

Actividades:
1. ESCENARIOS DE DESASTRE EN ALCANCE
   Define los escenarios catastróficos cubiertos por este plan (pérdida de centro de datos/región, ransomware/corrupción masiva de datos, pérdida del proveedor de nube, borrado accidental irreversible) — no asumas que todos los escenarios se recuperan igual; distingue si alguno queda explícitamente fuera de alcance y por qué.

2. VALIDACIÓN DE RTO/RPO
   Para cada escenario, estima el RTO (tiempo de recuperación) y RPO (pérdida de datos máxima tolerable) *reales* alcanzables con el mecanismo de backup/replicación actual, comparándolos contra el objetivo declarado — no repitas el objetivo declarado como si fuera la capacidad real sin verificarlo. Si existe una brecha entre el objetivo y la capacidad real, repórtala explícitamente con el tamaño de la brecha.

3. SECUENCIA DE RECUPERACIÓN DE DEPENDENCIAS
   Lista las dependencias críticas del sistema (bases de datos, colas, servicios externos, secretos/credenciales, DNS) y define el orden en que deben recuperarse — no asumas que todas se recuperan en paralelo sin conflicto; señala qué dependencia bloquea a cuáles.

4. PROCEDIMIENTO DE FAILOVER
   Define los pasos concretos para activar el sitio/región/entorno de recuperación, incluyendo quién tiene autoridad para declarar el desastre y activar el plan, y cómo se redirige el tráfico real de usuarios.

5. CADENCIA DE PRUEBAS (DRILLS)
   Define con qué frecuencia se debe probar la restauración real de backups y, si aplica, un failover completo simulado (tabletop o técnico) — un plan de DR nunca probado se reporta como "no validado", no como "listo".

6. CRITERIOS DE ACTIVACIÓN Y DESACTIVACIÓN
   Define qué condición objetiva activa formalmente el plan (vs. tratarlo como un incidente normal de `11-04`) y qué condición confirma que la operación normal puede retomarse (failback).

7. COMUNICACIÓN DE CRISIS
   Define qué stakeholders deben ser notificados al activar el plan, por qué canal, y con qué cadencia de actualización mientras dura la recuperación.

Restricciones:
- nunca declares un RTO/RPO como "cumplido" sin verificar la capacidad real del mecanismo de backup/replicación actual — un objetivo sin verificación se reporta como no validado, no como alcanzado,
- toda dependencia crítica debe aparecer en la secuencia de recuperación con su propio RTO/RPO estimado — no agrupes dependencias distintas bajo una sola estimación genérica,
- si el sistema nunca ha tenido una prueba real de restauración, decláralo explícitamente como riesgo abierto de alta severidad, no lo omitas ni asumas que el backup funciona porque existe,
- este prompt diseña el plan y el procedimiento de prueba; no ejecuta ninguna restauración, failover ni prueba de recuperación real,
- si no se conocen los objetivos de RTO/RPO ni la arquitectura de dependencias del sistema, detente y solicítalos antes de proponer el plan.

Salida:
0. Bloque JSON de metadatos (claves: status, scenarios_covered_count, rto_rpo_gaps_count, never_tested, confidence_score [0.0 a 1.0]).
1. Escenarios de desastre en alcance (y explícitamente fuera de alcance).
2. RTO/RPO objetivo vs. capacidad real estimada, por escenario, con brechas señaladas.
3. Secuencia de recuperación de dependencias críticas, con orden y bloqueos.
4. Procedimiento de failover: pasos, autoridad de activación, redirección de tráfico.
5. Cadencia de pruebas de backup-restore y de failover simulado.
6. Criterios de activación y de failback (retorno a operación normal).
7. Plan de comunicación de crisis.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de plan de recuperación ante desastres y continuidad de negocio y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- objetivos de RTO/RPO: [REFERENCIA A 00-D-02, O "no declarados aún"]
- arquitectura y dependencias críticas: [REFERENCIA A 04-01]
- documentos a revisar: mecanismo de backup actual, resultado de la última prueba de restauración
- objetivo puntual de salida: plan de DR/BCP con RTO/RPO validado y cadencia de pruebas
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen del plan |
| Escenarios en alcance (1) | Escenarios catastróficos cubiertos y explícitamente excluidos |
| RTO/RPO objetivo vs. real (2) | Comparación por escenario, con brechas de capacidad señaladas |
| Secuencia de dependencias (3) | Orden de recuperación de dependencias críticas y sus bloqueos |
| Procedimiento de failover (4) | Pasos, autoridad de activación, redirección de tráfico |
| Cadencia de pruebas (5) | Frecuencia de pruebas de restauración y de failover simulado |
| Criterios de activación/failback (6) | Condición objetiva de activación y de retorno a operación normal |
| Comunicación de crisis (7) | Stakeholders a notificar, canal y cadencia |

### Ejemplo (fragmento)

```json
{
  "status": "plan_definido_con_brecha_abierta",
  "scenarios_covered_count": 3,
  "rto_rpo_gaps_count": 1,
  "never_tested": true,
  "confidence_score": 0.68
}
```

| Escenario | RTO objetivo | RTO real estimado | RPO objetivo | RPO real estimado | Brecha |
|---|---|---|---|---|---|
| Pérdida de región completa | 4 horas | ~9 horas (restauración manual desde backup diario en otra región) | 1 hora | 24 horas (backup solo diario, sin replicación continua) | **[BRECHA ABIERTA]** ni el RTO ni el RPO objetivo son alcanzables con el backup diario actual; requiere replicación continua entre regiones para cerrar |
| Ransomware/corrupción masiva de datos | 8 horas | ~8 horas (restauración desde el backup inmutable más reciente no afectado) | 24 horas | 24 horas | Cumplido — backups inmutables verificados en la última prueba |

| Sección | Contenido de ejemplo |
|---|---|
| Cadencia de pruebas (5) | Nunca se ha ejecutado una restauración real desde backup — se reporta como riesgo abierto de alta severidad; se recomienda una primera prueba de restauración en ambiente aislado dentro de las próximas 2 semanas, seguida de una cadencia trimestral |
