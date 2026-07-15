# 17.3 — Evaluación y decisión de adopción de herramienta/licencia

## Descripción

Prompt para producir una ficha de evaluación y decisión frente a un candidato de herramienta, librería paga o servicio SaaS a adoptar (ej: nuevo APM, nueva librería con licencia comercial, nuevo servicio cloud). Cubre costo total de propiedad (licencias + tiempo de integración + mantenimiento), alternativas consideradas —incluida la opción de no adoptar—, riesgos de vendor lock-in, seguridad/compliance de datos y dependencia de un solo proveedor, cerrando con una recomendación explícita de adoptar, rechazar o evaluar más. No compra, contrata ni firma nada: es un insumo de decisión para que quien aprueba presupuesto decida con criterio.

**Cuándo usarlo:** antes de adoptar formalmente una nueva herramienta, SaaS o librería paga que implique costo recurrente o dependencia de un proveedor externo. Diferencia con prompts relacionados: `11-08-finops-cloud-cost-audit` audita el gasto cloud **ya existente** de servicios que la organización ya contrató; este prompt evalúa la decisión de adoptar un servicio **todavía no contratado**, y su salida —si la herramienta involucra costo cloud recurrente— alimenta naturalmente una futura auditoría con `11-08-finops-cloud-cost-audit` una vez adoptada.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis/decisión — la ejecución de la compra, contratación o firma del contrato con el proveedor queda delegada a quien aprueba presupuesto; este prompt nunca ejecuta una adquisición |
| Riesgo esperado | medio — una ficha de evaluación mal hecha puede llevar a gasto innecesario, a un vendor lock-in no anticipado, o a exponer datos sensibles a un proveedor sin el debido análisis de compliance, pero el prompt en sí solo produce un documento de análisis y recomendación, nunca ejecuta la compra |
| Entradas requeridas | nombre de la herramienta/servicio candidato, problema o necesidad que resuelve, alternativas conocidas (o indicar que no se han identificado aún), presupuesto disponible si aplica, modelo de licenciamiento propuesto, tipo de datos que la herramienta tocará |
| Herramientas permitidas | lectura de documentación pública del proveedor, comparación de alternativas y cálculo de costo total estimado a partir de datos provistos o verificables; no ejecuta compras, no firma contratos, no ingresa datos reales de la empresa en la plataforma del proveedor para pruebas |
| Autonomía permitida | A1 — Proponer (ficha de evaluación con recomendación de adoptar/rechazar/evaluar más); nunca A2/A3 — este prompt no aprueba presupuesto ni contrata al proveedor |
| Criterios de detención | detener y escalar si no hay ningún precio de licencia verificable disponible — no fabricar cifras plausibles; detener si no se identificó ninguna alternativa (incluida la opción de no adoptar) para comparar |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada costo citado indica su fuente (documentación del proveedor, cotización, o "estimado" si no hay dato verificado), se listó al menos una alternativa además de "no adoptar", y los riesgos de vendor lock-in, seguridad/compliance y dependencia de proveedor único quedan explícitos con su severidad |
| Siguiente prompt recomendado | `11-08-finops-cloud-cost-audit` si la herramienta adoptada implica costo cloud recurrente que deba auditarse periódicamente una vez en producción |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como Analista de Procurement/FinOps especializado en evaluación de herramientas y licencias SaaS. Produce una ficha de evaluación y decisión sobre la herramienta candidata indicada, cubriendo costo total de propiedad, alternativas consideradas, riesgos y una recomendación explícita. No ejecutes ninguna compra, contratación ni registro con el proveedor: tu salida es un insumo de decisión para que un humano con autoridad de presupuesto decida.

Entradas:
- herramienta/servicio candidato: [NOMBRE DE LA HERRAMIENTA O SERVICIO]
- problema o necesidad que resuelve: [DESCRIPCIÓN DEL PROBLEMA]
- alternativas conocidas: [LISTA DE ALTERNATIVAS, INCLUYENDO "SEGUIR SIN HERRAMIENTA" — o "ninguna identificada aún" si aplica]
- presupuesto disponible (si aplica): [MONTO Y PERIODICIDAD, O "no definido"]
- modelo de licenciamiento propuesto: [POR USUARIO / POR USO O CONSUMO / SUSCRIPCIÓN FIJA / PERPETUA CON SOPORTE / OTRO]
- datos que la herramienta tocará o procesará: [TIPO DE DATOS — ej. datos de clientes, PII, código fuente, credenciales, "ninguno sensible"]
- equipo o rol que solicita la adopción: [EQUIPO/ROL]

Pasos:

1. COSTO TOTAL DE PROPIEDAD (TCO)
   Descompón el costo en:
   - costo de licencia (mensual y anual, según el modelo indicado)
   - tiempo de integración estimado (horas-persona necesarias multiplicadas por un costo-hora de referencia)
   - costo de mantenimiento continuo esperado (soporte, actualizaciones, tiempo de operación)
   - costo de salida/migración si en el futuro se descontinúa la herramienta
   Marca cada cifra como "verificada" (con fuente: cotización, documentación del proveedor, tarifa pública) o "estimada" si no hay dato confirmado — nunca presentes una cifra estimada como si fuera verificada.

2. ALTERNATIVAS CONSIDERADAS
   Lista las alternativas evaluadas, incluyendo siempre la opción de "no adoptar / mantener el status quo" como línea base de comparación. Para cada alternativa, resume costo aproximado, madurez del producto/proveedor y curva de adopción esperada.

3. RIESGOS
   Evalúa explícitamente:
   - vendor lock-in: qué tan reversible es la decisión, qué tan atado queda el sistema al formato/API propietario del proveedor, y cuál sería el costo de migrar fuera en el futuro.
   - seguridad y compliance de datos: qué datos verá o procesará el proveedor, si existe requisito normativo aplicable (ej. protección de datos, residencia de datos, certificaciones del proveedor), y si la herramienta pasaría una revisión de seguridad estándar de la organización.
   - dependencia de un solo proveedor: qué ocurre si el proveedor sube precios de forma unilateral, cambia los términos del servicio, es adquirido por otra empresa, o descontinúa el producto.
   - riesgo operativo: curva de aprendizaje del equipo, calidad del soporte del proveedor, existencia de SLA y sus garantías reales.
   Para cada riesgo, indica severidad (baja/media/alta) y si existe mitigación conocida.

4. BENEFICIO ESPERADO Y CRITERIO DE ÉXITO
   Describe el problema que la herramienta resolvería en términos concretos y cómo se mediría el éxito de la adopción si se aprueba (métrica u observación verificable), no en términos vagos de "mejora la productividad".

5. RECOMENDACIÓN
   Concluye con una de tres recomendaciones explícitas: ADOPTAR, RECHAZAR, o EVALUAR MÁS (ej. mediante una prueba piloto o POC acotada en tiempo y alcance). Justifica la recomendación citando los hallazgos de los pasos 1 a 4 — nunca la presentes sin justificación trazable.

6. RESUMEN EJECUTIVO
   Resume en pocas líneas la herramienta evaluada, el costo total estimado, el riesgo principal identificado y la recomendación final, en un formato que quien aprueba presupuesto pueda leer sin abrir el resto del documento.

Restricciones:
- nunca fabriques precios de licencia ni cifras de costo; si no están disponibles o verificadas, indícalo explícitamente como "no verificado / estimado" y refleja esa incertidumbre en el TCO final.
- este prompt no ejecuta la compra, no firma contratos, no crea cuentas de prueba con datos reales de la empresa, ni ingresa datos sensibles en la plataforma del proveedor para evaluarla.
- toda recomendación debe comparar contra al menos una alternativa real, incluida explícitamente la opción de no adoptar la herramienta.
- señala siempre y de forma explícita si la herramienta requeriría compartir datos sensibles o regulados con el proveedor, incluso si la recomendación final es adoptar.
- la decisión final de aprobar presupuesto y contratar al proveedor corresponde a un humano con autoridad de compra; este prompt únicamente produce la ficha de apoyo a esa decisión.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de evaluación de herramienta/licencia y adáptalo a:
- repositorio/contexto: [NOMBRE O URL DEL PROYECTO]
- herramienta/servicio candidato: [NOMBRE DE LA HERRAMIENTA]
- problema que resuelve: [DESCRIPCIÓN]
- alternativas conocidas: [LISTA O "ninguna identificada aún"]
- presupuesto disponible: [MONTO O "no definido"]
- modelo de licenciamiento: [POR USUARIO / POR USO / SUSCRIPCIÓN / OTRO]
- datos que tocará la herramienta: [TIPO DE DATOS]
- documentos a revisar: cotización o pricing público del proveedor, política de seguridad/compliance del proveedor si está disponible
- objetivo puntual de salida: ficha de evaluación con TCO, alternativas, riesgos y recomendación adoptar/rechazar/evaluar más
- nivel de profundidad: alto
```

---

## Salida esperada

| Criterio | Detalle |
|---|---|
| Herramienta candidata | Datadog APM (plan Pro) |
| Problema que resuelve | falta de trazabilidad distribuida entre microservicios; tiempo medio de diagnóstico de incidentes > 2h |
| Costo total estimado (año 1) | licencia: USD 31/host/mes × 12 hosts × 12 meses = ~USD 4,464/año (verificado, pricing público); integración: ~80 horas-persona × USD 45/h = USD 3,600 (estimado); mantenimiento continuo: ~4h/mes × USD 45/h × 12 = USD 2,160/año (estimado) → TCO año 1 ≈ USD 10,224 |
| Alternativas consideradas | (1) no adoptar / seguir con logs centralizados actuales — costo USD 0, pero no resuelve la trazabilidad distribuida; (2) OpenTelemetry + backend propio (Jaeger self-hosted) — costo de licencia USD 0 pero mayor tiempo de integración y mantenimiento operativo propio (estimado 160h iniciales + 8h/mes); (3) New Relic APM — pricing similar, madurez comparable, no evaluado en profundidad por falta de cotización |
| Riesgo de vendor lock-in | medio — instrumentación vía SDK propietario en el código de los servicios; migrar a otro APM requeriría reinstrumentar, mitigable adoptando estándar OpenTelemetry como capa de instrumentación |
| Riesgo de seguridad/compliance | bajo-medio — la herramienta procesará trazas de requests que pueden incluir metadata de usuarios (no PII directa si se configura correctamente el redactado); proveedor cuenta con certificación SOC 2 Type II (verificado en su documentación pública) |
| Riesgo de dependencia de proveedor único | medio — sin alternativa de failover; si el proveedor sube precios o cambia términos, la migración toma semanas, no días |
| Recomendación | EVALUAR MÁS — iniciar una prueba piloto de 30 días en 2 servicios no críticos, con criterio de éxito: reducir tiempo medio de diagnóstico de incidentes por debajo de 30 minutos, antes de comprometer el gasto anual completo |

> Nota: la tabla completa debe incluir todas las filas del análisis (TCO desglosado, cada alternativa considerada, cada riesgo evaluado por separado con severidad), marcando explícitamente cada cifra de costo como "verificada" o "estimada".

### Resumen ejecutivo

- **Herramienta evaluada:** [NOMBRE DE LA HERRAMIENTA] — resuelve [PROBLEMA] para el equipo [EQUIPO SOLICITANTE].
- **Costo total estimado (año 1):** [MONTO] — [VERIFICADO / ESTIMADO, con desglose de licencia + integración + mantenimiento].
- **Riesgo principal:** [RIESGO DE MAYOR SEVERIDAD] — mitigación propuesta: [MITIGACIÓN O "ninguna identificada"].
- **Recomendación:** [ADOPTAR / RECHAZAR / EVALUAR MÁS] — [JUSTIFICACIÓN EN UNA LÍNEA].
- **Decisión pendiente de:** aprobación de presupuesto por [ROL/PERSONA CON AUTORIDAD DE COMPRA] — este documento no autoriza ni ejecuta la contratación.
