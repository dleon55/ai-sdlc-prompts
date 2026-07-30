# 0-D.4 — Registro de riesgos del proyecto (RAID): riesgos, supuestos, incidentes y dependencias

## Descripción

Prompt para construir y mantener el **registro de riesgos de todo el proyecto** siguiendo el formato RAID (Risks, Assumptions, Issues, Dependencies): riesgos potenciales con probabilidad/impacto, supuestos sobre los que se apoya el plan, incidentes ya materializados que requieren resolución, y dependencias externas que pueden bloquear el cronograma. Es el registro a nivel de todo el proyecto — distinto de `05-02-riesgos-implementacion`, que analiza los riesgos de un cambio o feature puntual ya diseñado.

**Cuándo usarlo:** junto con el Project Charter (`00-D-01`) y el plan de trabajo (`00-D-03`), al inicio del proyecto, y revisado periódicamente (cada hito o cada sprint) durante toda la ejecución — un registro de riesgos que solo se llena una vez al inicio pierde su valor.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | alto — este registro es el insumo que el patrocinador usa para decisiones de go/no-go y de inversión en mitigación; un riesgo alto omitido o mal clasificado a nivel de proyecto completo puede materializarse sin que nadie lo haya visto venir, con impacto en fecha, presupuesto o alcance, aunque el prompt no ejecuta ni compromete nada por sí mismo |
| Entradas requeridas | Project Charter (`00-D-01`), stack/arquitectura inicial (`00-D-02`) si existe, plan de trabajo (`00-D-03`) si existe, restricciones de negocio conocidas, historial de riesgos materializados en proyectos similares si existe |
| Herramientas permitidas | ninguna de ejecución — lectura de documentación existente; produce un documento de registro (RAID log), no aplica ninguna mitigación por sí mismo |
| Autonomía permitida | A0 — Analizar (riesgos, supuestos, incidentes y dependencias ya declarados o evidentes en el contexto); A1 — Proponer (mitigaciones, riesgos inferidos no declarados explícitamente por el negocio, siempre marcados como propuesta) |
| Criterios de detención | si un riesgo queda clasificado como alto (probabilidad alta o impacto alto) sin una mitigación viable, no lo minimices ni lo dejes implícito — decláralo explícitamente como bloqueante para aprobar el Charter o el plan de trabajo |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada riesgo (R-XXX) declara categoría, probabilidad, impacto, mitigación y contingencia; cada supuesto (A-XXX) declara qué pasa si resulta falso y cómo se validará; cada incidente (I-XXX) y dependencia (D-XXX) declara responsable y estado |
| Siguiente prompt recomendado | `05-02-riesgos-implementacion` cuando cada feature o cambio individual del proyecto entre a su fase de diseño/implementación — ese prompt cubre el riesgo específico de ESE cambio, no reemplaza este registro de proyecto |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Construye el registro de riesgos de todo el proyecto en formato RAID: riesgos, supuestos, incidentes ya materializados y dependencias externas, con clasificación, responsable y plan de acción para cada uno.

Entradas:
- Project Charter: [PEGAR O REFERENCIA A 00-D-01]
- stack/arquitectura inicial: [PEGAR O REFERENCIA A 00-D-02, O "no definida aún"]
- plan de trabajo: [PEGAR O REFERENCIA A 00-D-03, O "no definido aún"]
- restricciones de negocio conocidas: [PRESUPUESTO, PLAZO, COMPLIANCE, U "ninguna declarada"]
- historial de riesgos materializados en proyectos similares: [DESCRIPCIÓN O "no disponible"]

Actividades:
1. RIESGOS (R)
   Identifica riesgos potenciales del proyecto por categoría: técnico, de negocio, de recursos/personal, de cronograma, de terceros/proveedores, regulatorio/compliance, financiero. Para cada uno: identificador (R-XXX), categoría, descripción, probabilidad (baja/media/alta), impacto (bajo/medio/alto), responsable (owner), mitigación, contingencia, y estado (abierto/mitigado/cerrado/materializado). Basa probabilidad e impacto en evidencia citada (historial, Charter, restricciones) — si no hay evidencia suficiente, decláralo como "riesgo no evaluable con la información disponible" en vez de asumir que es bajo.

2. SUPUESTOS (A)
   Identifica los supuestos sobre los que se apoya el Charter y el plan de trabajo (técnicos, de negocio, de recursos, de mercado). Para cada uno: identificador (A-XXX), descripción, qué pasa si resulta falso (impacto de la invalidación), cómo y cuándo se validará, y estado (validado/pendiente de validar/invalidado).

3. INCIDENTES (I)
   Registra problemas ya materializados (no hipotéticos) que requieren resolución activa ahora mismo — a diferencia de los riesgos, que son potenciales. Para cada uno: identificador (I-XXX), descripción, impacto actual, responsable, fecha límite de resolución, y estado.

4. DEPENDENCIAS (D)
   Identifica dependencias externas al control directo del equipo del proyecto: otros equipos, proveedores, aprobaciones regulatorias o de negocio, infraestructura compartida. Para cada una: identificador (D-XXX), descripción, tipo (interna/externa), a qué actividad o hito bloquea, fecha en que se necesita resuelta, y estado.

5. PRIORIZACIÓN Y ESCALAMIENTO
   Prioriza los riesgos por severidad (probabilidad × impacto) y señala explícitamente cuáles requieren decisión o escalamiento del patrocinador antes de continuar. Nunca resuelvas por tu cuenta un riesgo alto sin mitigación viable — repórtalo como decisión pendiente.

6. CADENCIA DE REVISIÓN
   Propón una cadencia de revisión de este registro (semanal/quincenal/por hito) proporcional al riesgo esperado del proyecto declarado en el Charter.

Restricciones:
- nunca clasifiques un riesgo como bajo solo porque falta evidencia en contra — si no hay información suficiente para evaluarlo, decláralo como "riesgo no evaluable con la información disponible",
- ningún riesgo alto puede quedar sin mitigación o contingencia explícitas en la salida — si no existe una mitigación viable, decláralo bloqueante en vez de omitirlo o minimizarlo,
- distingue siempre un riesgo, supuesto, incidente o dependencia declarado explícitamente por el negocio/Charter de uno que tú infieres — nunca los presentes con el mismo nivel de certeza,
- no confundas este registro de proyecto con el análisis de riesgos de una implementación puntual (`05-02`) — si detectas un riesgo que aplica solo a un cambio específico ya en diseño, señala que corresponde a `05-02` en vez de mezclarlo aquí,
- si no existe Project Charter de referencia, detente y solicítalo antes de construir el registro sobre supuestos propios.

Salida:
0. Bloque JSON de metadatos (claves: status, risk_count, high_risk_unmitigated_count, open_issues_count, confidence_score [0.0 a 1.0]).
1. Riesgos (R): ID | Categoría | Descripción | Probabilidad | Impacto | Responsable | Mitigación | Contingencia | Estado
2. Supuestos (A): ID | Descripción | Impacto si resulta falso | Cómo/cuándo se valida | Estado
3. Incidentes (I): ID | Descripción | Impacto actual | Responsable | Fecha límite | Estado
4. Dependencias (D): ID | Descripción | Tipo | Bloquea a | Fecha necesaria | Estado
5. Riesgos altos sin mitigación viable — bloqueantes para el patrocinador.
6. Cadencia de revisión recomendada.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de registro de riesgos del proyecto (RAID) y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- Project Charter: [REFERENCIA A 00-D-01]
- plan de trabajo: [REFERENCIA A 00-D-03, O "no definido aún"]
- documentos a revisar: Project Charter, arquitectura inicial (00-D-02), plan de trabajo (00-D-03)
- objetivo puntual de salida: registro RAID completo con riesgos altos priorizados
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen del registro |
| Riesgos (1) | Tabla completa de riesgos con probabilidad, impacto, mitigación y contingencia |
| Supuestos (2) | Tabla de supuestos con impacto de invalidación y plan de validación |
| Incidentes (3) | Problemas ya materializados con responsable y fecha límite |
| Dependencias (4) | Dependencias externas con fecha en que se necesitan resueltas |
| Riesgos altos sin mitigar (5) | Lista de bloqueantes que requieren decisión del patrocinador |
| Cadencia de revisión (6) | Frecuencia recomendada para revisar el registro |

### Ejemplo (fragmento)

```json
{
  "status": "registrado_con_bloqueantes",
  "risk_count": 11,
  "high_risk_unmitigated_count": 1,
  "open_issues_count": 2,
  "confidence_score": 0.7
}
```

| Sección | Ejemplo de contenido |
|---|---|
| Riesgos (1) | R-004 \| Terceros/proveedores \| El proveedor de pasarela de pagos no ha confirmado disponibilidad de sandbox para la fecha de inicio de integración \| Media \| Alto \| Líder técnico \| Escalar contacto con el proveedor esta semana; explorar proveedor alterno como plan B \| Si no hay sandbox en 2 semanas, mover la integración de pagos a la fase 2 del cronograma \| Abierto |
| Riesgos altos sin mitigar (5) | R-004 no tiene mitigación confirmada — depende de una respuesta externa fuera del control del equipo; requiere decisión del patrocinador sobre si mover la fecha de integración de pagos antes de aprobar el cronograma final |
