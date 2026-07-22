# 17.5 — Auditoría de renovación de vendors y contratos tecnológicos

## Descripción

Prompt para auditar un contrato de vendor, SaaS o licencia tecnológica antes de su fecha de renovación: compara el uso real observado contra lo licenciado/contratado (¿se está pagando de más?), contrasta la solución actual contra alternativas vigentes del mercado, sopesa los riesgos de continuar (vendor lock-in, calidad de soporte, postura de seguridad del proveedor) frente a los riesgos y el costo/esfuerzo de migrar, y entrega una recomendación explícita de renovar, renegociar, migrar o cancelar. No ejecuta la renovación ni negocia con el vendor: es la ficha de auditoría que sustenta la decisión de quien administra el contrato.

**Cuándo usarlo:** en el ciclo previo a la fecha de renovación de cualquier contrato de vendor tecnológico, SaaS o licencia (idealmente con suficiente antelación para dejar margen de negociación o migración antes del vencimiento). Diferencia con prompts relacionados: `17-03-evaluacion-herramienta-licencia` se usa para **adoptar** una herramienta nueva que aún no se tiene contratada, evaluando si conviene incorporarla; este prompt se usa para decidir sobre una herramienta que **ya está en producción**, en su punto de renovación, con datos reales de uso y costo acumulados. `11-08-finops-cloud-cost-audit` audita el gasto **agregado** de infraestructura cloud en curso (cómputo, storage, redes de múltiples proveedores); este prompt audita un **contrato o licencia específico** en su ciclo de renovación, con foco en la decisión binaria de continuar o no con ese vendor puntual.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis/auditoría — la ejecución de la renovación, renegociación, migración o cancelación queda delegada a quien administra el contrato (procurement, finanzas o el responsable técnico del vendor), nunca a este prompt |
| Riesgo esperado | medio — una recomendación de renovación equivocada puede implicar sobre-pago sostenido, lock-in innecesario o migrar sin justificación suficiente, con impacto de costo y continuidad operativa; el prompt en sí solo analiza y recomienda, nunca ejecuta la renovación ni negocia con el vendor |
| Entradas requeridas | contrato o términos de licencia vigentes (costo, volumen/asientos contratados, fecha de renovación, cláusulas de cancelación o penalización), datos reales de uso (asientos activos, volumen consumido, frecuencia de uso por equipo/feature), alternativas de mercado conocidas o a investigar, historial de incidentes de soporte o seguridad del vendor si existe, lead time disponible antes de la fecha de renovación |
| Herramientas permitidas | lectura de contratos, facturas, dashboards de uso/analytics del propio vendor, documentación pública de alternativas de mercado; investigación de mercado (búsqueda web) para comparar alternativas vigentes; la salida es un documento de auditoría y recomendación de texto — no ejecuta renovaciones, cancelaciones, migraciones ni negociaciones con el vendor |
| Autonomía permitida | A0 — Analizar (uso real vs. contratado, comparación de alternativas); A1 — Proponer (recomendación de renovar/renegociar/migrar/cancelar); nunca A2/A3 — este prompt no renueva, cancela, firma ni negocia contratos, ni ejecuta la migración a una alternativa |
| Criterios de detención | detener y escalar si no hay datos reales de uso disponibles para calcular la relación uso vs. contratado — no fabricar cifras de utilización plausibles; marcar como recomendación de baja confianza si la comparación con alternativas de mercado se basa en información desactualizada o no verificada; escalar como urgente si la fecha de renovación está a menos del lead time mínimo necesario para negociar o migrar |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | la cifra de uso real cita su fuente (dashboard del vendor, reporte de accesos, métricas internas) y su fecha de corte; el costo actual y las condiciones de renovación citan el contrato o la factura correspondiente; cada alternativa de mercado mencionada indica su fuente y fecha de consulta |
| Siguiente prompt recomendado | `17-03-evaluacion-herramienta-licencia` si la recomendación es migrar a una alternativa — se re-evalúa esa alternativa como si fuera una adopción nueva, con su propio análisis de encaje |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como Analista de Procurement Tecnológico especializado en auditoría de renovación de contratos de vendors y SaaS. Antes de la fecha de renovación indicada, evalúa si el uso real justifica el costo contratado, si la solución actual sigue siendo la mejor opción frente a alternativas vigentes del mercado, y los riesgos de continuar frente a los riesgos y esfuerzo de migrar. Entrega una recomendación explícita: renovar, renegociar, migrar o cancelar.

Entradas:
- vendor/contrato a auditar: [NOMBRE DEL VENDOR / PRODUCTO / SERVICIO]
- fecha de renovación: [FECHA]
- costo actual: [MONTO Y PERIODICIDAD — ej. USD 2,400/mes, facturación anual]
- volumen/plan contratado: [ej. 50 ASIENTOS / TIER ENTERPRISE / X REQUESTS-MES]
- uso real observado: [DATOS DE USO DISPONIBLES — dashboard de analytics del vendor, reporte de accesos, métricas internas — o "no disponibles" si aplica]
- alternativas conocidas en el mercado: [NOMBRES DE COMPETIDORES CONOCIDOS, o "ninguna identificada — requiere investigación"]
- cláusulas relevantes del contrato: [PLAZO DE CANCELACIÓN, PENALIZACIONES, AUTO-RENOVACIÓN, PORTABILIDAD DE DATOS]
- lead time disponible antes de la fecha de renovación: [ej. 60 DÍAS]

Pasos:

1. USO REAL VS. CONTRATADO
   Calcula la relación entre lo efectivamente usado (asientos activos, volumen consumido, frecuencia de uso por equipo o feature) y lo contratado/licenciado. Identifica sobre-aprovisionamiento (pagando por capacidad no usada) o sub-aprovisionamiento (uso cerca del límite, riesgo de fricción operativa).
   - si no hay datos reales de uso disponibles, indícalo explícitamente y marca esta sección como "sin datos — auditoría de baja confianza" en vez de asumir un nivel de uso.

2. COSTO ACTUAL Y SU TENDENCIA
   Documenta el costo actual, su periodicidad, y cómo ha evolucionado en renovaciones anteriores si hay historial disponible (incrementos de precio, cambios de tier). Calcula el costo por unidad real de uso (ej. costo por asiento activo, no por asiento contratado) para exponer el sobre-pago si existe.

3. COMPARACIÓN CON ALTERNATIVAS DE MERCADO
   Identifica y compara al menos 2-3 alternativas vigentes en el mercado (o usa las indicadas en las entradas), evaluando funcionalidad equivalente, costo aproximado, y madurez del proveedor. Cita la fuente y fecha de consulta de cada alternativa. Si no se identifican alternativas viables, decláralo explícitamente en vez de inventar competidores.

4. RIESGOS DE CONTINUAR CON EL VENDOR ACTUAL
   Evalúa vendor lock-in (dificultad y costo de salir más adelante), calidad y tiempos de respuesta del soporte, postura de seguridad del proveedor (certificaciones, incidentes conocidos, políticas de datos), y dependencia crítica del negocio en esa herramienta.

5. RIESGOS Y COSTO/ESFUERZO DE MIGRAR
   Si existe una alternativa viable, estima el esfuerzo de migración (tiempo, personas, downtime esperado, riesgo de pérdida o transformación de datos), el costo de transición (doble pago durante el periodo de transición, capacitación del equipo), y el riesgo de que la alternativa no cumpla con requisitos no evidentes hoy.

6. CLÁUSULAS CONTRACTUALES RELEVANTES
   Revisa plazos de cancelación, penalizaciones por salida anticipada, condiciones de auto-renovación y portabilidad de datos. Señala si alguna cláusula impone una fecha límite de decisión anterior a la fecha de renovación misma.

7. RECOMENDACIÓN EXPLÍCITA
   Con base en los pasos anteriores, entrega una recomendación única y explícita entre: RENOVAR (sin cambios), RENEGOCIAR (renovar con cambios de precio/plan/condiciones), MIGRAR (a una alternativa identificada), o CANCELAR (sin reemplazo). Justifica la recomendación citando la evidencia de uso, costo, riesgo y alternativas recabada en los pasos previos.

8. RESUMEN EJECUTIVO Y PRÓXIMOS PASOS
   Resume la recomendación, el ahorro o costo estimado de seguirla, la fecha límite para actuar (considerando el lead time y las cláusulas contractuales), y quién debe tomar la decisión final.

Restricciones:
- nunca presentes una cifra de uso real sin citar su fuente y fecha de corte; si no hay datos de uso disponibles, dilo explícitamente y marca la auditoría como de baja confianza en vez de fabricar cifras plausibles.
- distingue siempre datos verificados (contrato, factura, dashboard de uso) de estimaciones o supuestos; marca cada cifra en la salida como "real" o "estimada".
- este prompt analiza y recomienda; nunca ejecuta la renovación, la cancelación, la firma de un nuevo contrato, la negociación con el vendor, ni la migración técnica a una alternativa.
- si el lead time disponible antes de la fecha de renovación es insuficiente para ejecutar la recomendación (negociar, evaluar migración, tramitar cancelación), señálalo como riesgo urgente que requiere decisión humana inmediata.
- si no se identifican alternativas viables de mercado, decláralo explícitamente en vez de inventar competidores o comparaciones no verificadas.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de auditoría de renovación de vendors y adáptalo a:
- repositorio/organización: [NOMBRE O URL]
- vendor/contrato a auditar: [NOMBRE DEL VENDOR / PRODUCTO]
- fecha de renovación: [FECHA]
- costo actual: [MONTO Y PERIODICIDAD]
- volumen/plan contratado: [ASIENTOS / TIER / CUOTA]
- uso real observado: [FUENTE DE DATOS O "no disponible"]
- alternativas conocidas: [NOMBRES O "ninguna identificada"]
- lead time disponible: [ej. 60 DÍAS]
- documentos a revisar: contrato vigente, facturas recientes, dashboard de uso del vendor
- objetivo puntual de salida: recomendación explícita de renovar/renegociar/migrar/cancelar con evidencia de uso, costo y alternativas
- nivel de profundidad: alto
```

---

## Salida esperada

| Dimensión | Hallazgo | Fuente / evidencia |
|---|---|---|
| Uso real vs. contratado | 32 de 50 asientos activos en los últimos 90 días (64% de utilización) — sobre-aprovisionamiento de 18 asientos | dashboard de analytics del vendor, corte al 2026-07-10 (real) |
| Costo actual | USD 2,400/mes (facturación anual), sin incremento desde la renovación anterior | factura de julio 2026 y contrato vigente (real) |
| Costo por unidad real de uso | USD 75/asiento activo (vs. USD 48/asiento si se ajustara el plan a 32 asientos) | cálculo derivado (estimado) |
| Alternativas de mercado | 2 alternativas con funcionalidad equivalente y costo 15-20% menor; 1 con integración más limitada al stack actual | investigación de mercado, consultada 2026-07-14 (real, sujeto a cambios de pricing) |
| Riesgos de continuar | lock-in moderado (exportación de datos posible pero manual); soporte con SLA de 24h cumplido en el último año; sin incidentes de seguridad reportados | historial de tickets de soporte interno (real) |
| Riesgos/costo de migrar | esfuerzo estimado 3-4 semanas de ingeniería, doble pago durante 1 mes de transición, riesgo medio de fricción en el equipo por curva de aprendizaje | estimación del equipo técnico (estimado) |
| Cláusulas relevantes | auto-renovación con 30 días de aviso previo para cancelar sin penalización | contrato vigente, cláusula 8.2 (real) |
| Recomendación | RENEGOCIAR: ajustar el plan a 35 asientos (con margen de crecimiento) antes de la renovación; si el vendor no ajusta precio, evaluar migración en el siguiente ciclo | síntesis de los hallazgos anteriores |

> Nota: la tabla completa debe cubrir cada dimensión evaluada (uso, costo, alternativas, riesgos de continuar, riesgos de migrar, cláusulas contractuales), separando explícitamente evidencia "real" de estimaciones, y terminar siempre en una recomendación única y explícita entre RENOVAR / RENEGOCIAR / MIGRAR / CANCELAR.

### Resumen ejecutivo

- **Recomendación:** [RENOVAR / RENEGOCIAR / MIGRAR / CANCELAR] — justificación en una línea.
- **Ahorro o costo estimado de seguir la recomendación:** [MONTO O RANGO] frente al costo actual de renovación sin cambios.
- **Fecha límite para actuar:** [FECHA], considerando el lead time disponible y las cláusulas de cancelación/auto-renovación del contrato.
- **Riesgos residuales:** [datos de uso no disponibles, comparación de mercado desactualizada, lead time ajustado o insuficiente para ejecutar la recomendación].
- **Responsable de la decisión final:** [ROL/PERSONA] — este prompt entrega la ficha de auditoría, no ejecuta la renovación, renegociación, migración o cancelación.
