# 11.10 — Capacity planning y proyección de escalamiento

## Descripción

Prompt para proyectar las necesidades futuras de capacidad (cómputo, base de datos, cache, almacenamiento, límites de rate de APIs de terceros) frente a una hipótesis de crecimiento, identificar el primer componente que llegará a su techo, y definir umbrales de escalamiento y el lead time necesario para actuar antes de que el cuello de botella ocurra. No mide el rendimiento actual bajo carga ni provisiona infraestructura: proyecta a futuro a partir de datos y supuestos explícitos.

**Cuándo usarlo:** al planificar un crecimiento esperado (tráfico, volumen de datos, base de usuarios) antes de que ocurra, o después de que `07-06-pruebas-performance-carga` revele un techo de capacidad bajo carga actual que requiere un plan de proyección hacia adelante. Diferencia con prompts relacionados: `07-06-pruebas-performance-carga` mide la capacidad actual bajo carga mediante pruebas ejecutadas; este prompt proyecta las necesidades de capacidad **futuras** frente a una curva de crecimiento, usando los resultados de pruebas de carga como una entrada más entre varias. `11-08-finops-cloud-cost-audit` audita el gasto cloud **actual**; este prompt proyecta cuánto costará y cuándo será necesario escalar a futuro, lo cual alimenta naturalmente una futura auditoría de costos.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis/planificación |
| Riesgo esperado | medio — una proyección de capacidad equivocada puede llevar a sobre-aprovisionar (desperdicio de presupuesto) o a sub-aprovisionar (caída de servicio al alcanzar el techo), pero el prompt en sí solo analiza y recomienda, nunca aprovisiona infraestructura |
| Entradas requeridas | métricas de utilización actual por capa (cómputo, conexiones/almacenamiento de BD, cache, rate limits de APIs de terceros, profundidad de colas), hipótesis de crecimiento esperado y su fuente (proyección de negocio real o supuesto), resultados de pruebas de carga si existen (`07-06`) |
| Herramientas permitidas | lectura de métricas, dashboards, resultados de pruebas de carga y proyecciones de negocio; la salida es un documento de análisis y recomendación de texto — no ejecuta cambios de infraestructura ni configura autoscaling |
| Autonomía permitida | A0 — Analizar (lectura de métricas y proyección); A1 — Proponer (plan de escalamiento y umbrales); nunca A2/A3 — este prompt no aprovisiona, redimensiona ni modifica infraestructura |
| Criterios de detención | detener y escalar si no hay ninguna métrica de utilización real disponible para el componente crítico — no fabricar cifras plausibles; señalar como proyección de baja confianza si la hipótesis de crecimiento es un supuesto sin respaldo de negocio |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada proyección cita la métrica base real (o indica explícitamente que es estimada), el supuesto de crecimiento usado y su fuente, y el modelo de proyección aplicado (lineal u otro, con justificación) |
| Siguiente prompt recomendado | `07-06-pruebas-performance-carga` para validar el techo proyectado con una prueba de carga real antes de comprometerse con el plan; `11-08-finops-cloud-cost-audit` para validar el impacto en costos del plan de escalamiento propuesto |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como Arquitecto de Infraestructura especializado en capacity planning. Proyecta las necesidades de capacidad de cada capa del sistema frente a la hipótesis de crecimiento indicada, identifica el primer componente que alcanzará su techo actual y define un plan de escalamiento con umbrales concretos y lead time de ejecución.

Entradas:
- componentes/capas a evaluar: [CÓMPUTO / BASE DE DATOS (conexiones, storage, IOPS) / CACHE / COLAS / RATE LIMITS DE APIS DE TERCEROS / CDN / OTRO]
- métricas de utilización actual disponibles: [DASHBOARD, EXPORT DE MÉTRICAS, RESULTADOS DE 07-06 U OTRA FUENTE — o "no disponibles" si aplica]
- hipótesis de crecimiento a planificar: [ej: 3x usuarios activos en 6 meses / +40% volumen de transacciones en Q1]
- fuente de la hipótesis de crecimiento: [PROYECCIÓN DE NEGOCIO FORMAL / SUPUESTO DEL EQUIPO / EXTRAPOLACIÓN DE TENDENCIA HISTÓRICA]
- horizonte de planificación: [ej: 6 MESES / 12 MESES]

Pasos:

1. LÍNEA BASE DE UTILIZACIÓN ACTUAL
   Para cada capa (cómputo, conexiones y almacenamiento de BD, cache, profundidad de colas, rate limits de APIs de terceros), reúne la utilización real actual (P50/P95, pico, promedio) a partir de métricas existentes.
   - si una capa no tiene métricas disponibles, indícalo explícitamente y márcala como "sin datos — proyección de baja confianza" en vez de asumir un valor.

2. HIPÓTESIS DE CRECIMIENTO Y SU FUENTE
   Documenta la hipótesis de crecimiento a usar (ej: 3x usuarios en 6 meses) y clasifica su origen: proyección de negocio formal, supuesto del equipo, o extrapolación de tendencia histórica. Señala el nivel de confianza de cada clasificación.

3. PROYECCIÓN POR CAPA
   Para cada componente, proyecta cuándo alcanzará su techo actual bajo la hipótesis de crecimiento, usando el modelo más simple defendible (extrapolación lineal por defecto). Si hay razón para esperar crecimiento no lineal (viral, estacional, efecto de red), usa ese modelo y justifica por qué.

4. IDENTIFICACIÓN DEL CUELLO DE BOTELLA PRINCIPAL
   De todas las capas proyectadas, identifica cuál será la PRIMERA en alcanzar su techo (la restricción vinculante). No trates todas las capas como igualmente urgentes: prioriza por fecha de saturación estimada, no por severidad percibida.

5. OPCIONES DE ESCALAMIENTO PARA EL CUELLO DE BOTELLA
   Para el componente identificado como restricción vinculante, evalúa opciones (escalamiento vertical, escalamiento horizontal, cache adicional, read replicas, particionamiento, cambio arquitectónico) con tradeoffs aproximados de costo, complejidad y tiempo de implementación.

6. UMBRALES Y TRIGGERS DE ESCALAMIENTO
   Define umbrales concretos y accionables (ej: "escalar horizontalmente cuando CPU P95 > 70% sostenido durante 10 minutos", "agregar réplica de lectura cuando conexiones activas > 80% del pool durante 15 minutos"). Evita recomendaciones vagas tipo "monitorear y reaccionar".

7. LEAD TIME DE EJECUCIÓN
   Estima cuánto tiempo toma ejecutar la acción de escalamiento recomendada (aprovisionamiento, aprobación de presupuesto, migración, cambio de contrato con proveedor de API) y verifica que ese lead time quepa antes de la fecha proyectada de saturación. Si no alcanza, señálalo como riesgo urgente.

8. RESUMEN EJECUTIVO Y PRÓXIMOS PASOS
   Resume el cuello de botella principal, la fecha estimada de saturación, la acción recomendada y cuándo debe iniciarse para no comprometer el servicio.

Restricciones:
- nunca presentes una proyección de capacidad sin indicar la hipótesis de crecimiento subyacente y su nivel de confianza — toda proyección depende de un supuesto que debe quedar explícito.
- distingue siempre datos de utilización real (con fuente citada) de cifras estimadas o supuestas; marca cada número en la salida como "real" o "estimado".
- este prompt analiza y recomienda; nunca aprovisiona, redimensiona ni modifica infraestructura, ni ejecuta comandos de despliegue o scaling (`terraform apply`, `kubectl scale`, cambios de tier en el proveedor cloud, etc.).
- si las métricas de utilización base no están disponibles para una capa, dilo explícitamente y marca toda la proyección de esa capa como de baja confianza en vez de fabricar cifras plausibles.
- si el lead time de ejecución de la acción recomendada excede el tiempo restante hasta la fecha proyectada de saturación, señálalo como riesgo crítico que requiere decisión y priorización humana inmediata.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de capacity planning y adáptalo a:
- repositorio: [NOMBRE O URL]
- componentes/capas a evaluar: [CÓMPUTO / BD / CACHE / COLAS / RATE LIMITS]
- métricas de utilización actual disponibles: [FUENTE O "no disponibles"]
- hipótesis de crecimiento: [ej: 3x usuarios en 6 meses]
- fuente de la hipótesis: [PROYECCIÓN DE NEGOCIO / SUPUESTO / TENDENCIA HISTÓRICA]
- horizonte de planificación: [6 MESES / 12 MESES]
- documentos a revisar: dashboards de métricas, resultados de pruebas de carga (07-06), proyecciones de negocio
- objetivo puntual de salida: identificar el cuello de botella principal y un plan de escalamiento con umbrales y lead time
- nivel de profundidad: alto
```

---

## Salida esperada

| Componente | Utilización actual | Proyección a [N meses] | Techo actual | Fecha estimada de saturación | Acción recomendada |
|---|---|---|---|---|---|
| Pool de conexiones BD (Postgres primario) | 65% promedio, 82% P95 (real, últimos 30 días) | +3x tráfico en 6 meses (proyección de negocio, confianza alta) → P95 supera 100% en el mes 3 | 100 conexiones máx. configuradas | mes 3 del horizonte (extrapolación lineal sobre P95) | agregar pgBouncer en modo transaction + read replica para lecturas; lead time estimado 3-4 semanas — iniciar en el mes 1 para no comprometer el servicio |

> Nota: la tabla completa debe incluir una fila por cada capa evaluada (cómputo, BD, cache, colas, rate limits de terceros, etc.), señalando cuál es el cuello de botella principal (primera fecha de saturación) y separando explícitamente utilización "real" de "estimada" en cada celda.

### Resumen ejecutivo

- **Cuello de botella principal:** [COMPONENTE] — primero en alcanzar su techo, en [FECHA ESTIMADA].
- **Hipótesis de crecimiento usada:** [DESCRIPCIÓN] — fuente: [PROYECCIÓN DE NEGOCIO / SUPUESTO] — confianza: [ALTA / MEDIA / BAJA].
- **Acción recomendada y lead time:** [ACCIÓN] — debe iniciarse antes de [FECHA LÍMITE] para no comprometer el servicio.
- **Riesgos residuales:** [capas sin datos de utilización, supuestos de crecimiento no validados por negocio, lead time ajustado o insuficiente].
