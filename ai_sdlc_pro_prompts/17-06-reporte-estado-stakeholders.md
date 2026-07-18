# 17.6 — Reporte de estado a stakeholders

## Descripción

Prompt para generar un reporte periódico de avance de un proyecto o iniciativa dirigido a stakeholders no técnicos (patrocinadores, dirección, clientes internos), a partir de fuentes reales (issues/PRs del periodo, estado de CI/CD, hitos del project charter, riesgos activos), traducido a lenguaje de negocio, sin inventar avance no verificado ni ocultar bloqueos o riesgos.

**Cuándo usarlo:** al cierre de un sprint o hito, o en la cadencia periódica de comunicación acordada con los stakeholders (semanal/quincenal).

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | reporte |
| Riesgo esperado | medio — un reporte que sobreestime el avance real o minimice un riesgo puede llevar a los stakeholders a tomar decisiones de negocio (compromisos con clientes, inversión adicional) sobre una base falsa; el prompt solo reporta y traduce a lenguaje de negocio, no decide ni ejecuta nada |
| Entradas requeridas | hitos comprometidos (de `00-D-01` o el roadmap vigente), issues/PRs cerrados y abiertos en el periodo, estado de CI/CD del periodo, riesgos activos (de `05-02` o el registro vigente), periodo a reportar, audiencia (nivel de detalle técnico esperado) |
| Herramientas permitidas | lectura del gestor de tareas/issues, historial de PRs, resultados de CI y documentos de riesgos/hitos existentes; la salida es un documento de reporte — no reasigna tareas, no cierra issues, no modifica el roadmap |
| Autonomía permitida | A0 — Analizar (recopilar avance real de las fuentes); A1 — Proponer (redacción del reporte en lenguaje de negocio); nunca A2/A3 — este prompt no comunica directamente a los stakeholders, produce el documento para que un humano lo revise y envíe |
| Criterios de detención | detener y señalar explícitamente si un hito reportado como "en progreso" no tiene ningún issue/PR asociado verificable — no reportar avance que no pueda trazarse a una fuente real; detener si el periodo a reportar no está definido |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada hito reportado como completado o en progreso cita el issue, PR o resultado de CI que lo sustenta; cada riesgo mencionado se traza al registro de riesgos de origen |
| Siguiente prompt recomendado | `05-02-riesgos-implementacion` si aparece un riesgo nuevo no registrado que deba formalizarse; `17-04-reporte-capacidad-equipo` si el reporte revela que el atraso se debe a sobrecarga del equipo |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Genera el reporte de estado del periodo para stakeholders no técnicos, traduciendo el avance real (verificable en las fuentes provistas) a lenguaje de negocio, sin inventar progreso ni ocultar bloqueos o riesgos.

Entradas:
- hitos comprometidos: [PEGAR O REFERENCIA A 00-D-01/ROADMAP]
- issues/PRs del periodo: [PEGAR O ENLACE AL GESTOR DE TAREAS]
- estado de CI/CD del periodo: [RESUMEN O ENLACE]
- riesgos activos: [PEGAR O REFERENCIA A 05-02/REGISTRO DE RIESGOS]
- periodo a reportar: [ej. SPRINT ACTUAL / ÚLTIMAS 2 SEMANAS]
- audiencia: [PATROCINADOR EJECUTIVO / CLIENTE INTERNO / DIRECCIÓN — nivel de detalle técnico esperado]

Pasos:
1. RECOPILACIÓN DE AVANCE VERIFICABLE
   Para cada hito comprometido, determina su estado real (completado/en progreso/bloqueado/no iniciado) citando el issue, PR o resultado de CI concreto que lo sustenta. Si un hito no tiene evidencia verificable de avance, no lo reportes como "en progreso" — repórtalo como "sin evidencia de avance en el periodo" en vez de asumir optimismo.

2. TRADUCCIÓN A LENGUAJE DE NEGOCIO
   Reescribe cada hito y bloqueo técnico en términos que un stakeholder no técnico pueda entender sin conocer la arquitectura o el stack (evita jerga técnica salvo que la audiencia declarada la requiera); conecta cada ítem con el impacto de negocio relevante (fecha comprometida, valor entregado, riesgo para el cliente).

3. RIESGOS Y BLOQUEOS
   Incorpora los riesgos activos del registro provisto, traduciendo su impacto técnico a impacto de negocio (qué pasa si el riesgo se materializa, en términos de fecha, alcance o costo). No omitas un riesgo alto solo porque no tiene aún mitigación confirmada — repórtalo igual, señalando que la mitigación está pendiente.

4. DECISIONES PENDIENTES
   Señala explícitamente qué decisiones de negocio (no técnicas) están bloqueando el avance y requieren una respuesta de los stakeholders (ej. aprobación de alcance, presupuesto adicional, priorización entre ítems en conflicto).

5. PRÓXIMOS HITOS
   Lista los próximos hitos comprometidos para el siguiente periodo, con su fecha objetivo y el nivel de confianza (alto/medio/bajo) basado en el avance real observado, no en el plan original si ya diverge de la realidad.

6. RESUMEN EJECUTIVO
   Cierra con un resumen de una pantalla: estado general del proyecto (en curso / en riesgo / bloqueado), 2-3 logros del periodo, 2-3 riesgos o bloqueos principales, y la(s) decisión(es) que se necesita(n) de los stakeholders.

Restricciones:
- nunca reportes un hito como "completado" o "en progreso" sin poder citar el issue, PR o resultado de CI que lo sustenta — si no hay evidencia, repórtalo explícitamente como sin evidencia de avance,
- no minimices ni omitas un riesgo o bloqueo activo para que el reporte luzca mejor — el objetivo es informar con precisión, no gestionar la percepción del stakeholder,
- no tomes ni insinúes decisiones de negocio en este prompt (priorización, aprobación de presupuesto) — señala que se requieren, pero la decisión la toma el stakeholder humano,
- adapta el nivel de detalle técnico a la audiencia declarada, pero nunca sacrifiques precisión por simplicidad — si simplificar un término técnico pierde un matiz importante para la decisión, consérvalo con una breve aclaración en vez de omitirlo.

Salida:
- resumen ejecutivo: estado general, logros, riesgos principales, decisiones requeridas
- tabla de hitos: hito, estado, evidencia citada, fecha objetivo
- riesgos y bloqueos activos, en lenguaje de negocio
- decisiones pendientes de los stakeholders
- próximos hitos con nivel de confianza
```

---

## Uso con fórmula estándar

```text
Usa el prompt de reporte de estado a stakeholders y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- hitos comprometidos: [REFERENCIA A 00-D-01/ROADMAP]
- issues/PRs del periodo: [ENLACE AL GESTOR DE TAREAS]
- estado de CI/CD: [RESUMEN O ENLACE]
- riesgos activos: [REFERENCIA A 05-02/REGISTRO DE RIESGOS]
- periodo a reportar: [SPRINT ACTUAL / ÚLTIMAS 2 SEMANAS]
- audiencia: [PATROCINADOR EJECUTIVO / CLIENTE INTERNO]
- documentos a revisar: roadmap, gestor de tareas, registro de riesgos
- objetivo puntual de salida: reporte de estado listo para enviar a stakeholders
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Resumen ejecutivo | Estado general, logros, riesgos principales, decisiones requeridas — una pantalla |
| Tabla de hitos | Hito, estado, evidencia citada, fecha objetivo |
| Riesgos y bloqueos | Impacto técnico traducido a impacto de negocio |
| Decisiones pendientes | Qué decisión de negocio se necesita y de quién |
| Próximos hitos | Fecha objetivo y nivel de confianza basado en avance real |

### Ejemplo (fragmento)

**Resumen ejecutivo:** Estado general: **en riesgo**. Logros del periodo: migración de autenticación completada y en producción (PR #214); cobertura de pruebas del módulo de pagos subió de 40% a 78%. Riesgo principal: la integración con el proveedor de facturación externo lleva 2 semanas bloqueada por falta de credenciales de sandbox del proveedor — sin mitigación confirmada. Decisión requerida: aprobar extender el hito de "facturación automática" 1 semana, o desalcanzar esa funcionalidad del release actual.

| Hito | Estado | Evidencia | Fecha objetivo |
|---|---|---|---|
| Migración de autenticación | Completado | PR #214, mergeado y desplegado (deploy-gcp run #189, smoke test OK) | Cumplida |
| Integración de facturación externa | Bloqueado | Sin PRs nuevos desde hace 9 días; issue #231 señala bloqueo por credenciales del proveedor | En riesgo — depende de decisión de negocio |
