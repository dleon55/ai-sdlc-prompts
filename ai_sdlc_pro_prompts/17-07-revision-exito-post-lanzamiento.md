# 17.7 — Revisión de éxito post-lanzamiento: realización de beneficios contra el Project Charter

## Descripción

Prompt para evaluar, semanas o meses después del lanzamiento de un proyecto o feature significativa, si se cumplieron los objetivos y KPIs declarados originalmente en el Project Charter (`00-D-01`) — cierra el círculo entre lo que se prometió y lo que realmente se logró. Distinto de `11-07-sre-postmortem-runbook` (postmortem de un incidente puntual) y de `17-06-reporte-estado-stakeholders` (reporte de estado en vivo durante la ejecución, no una retrospectiva de beneficios).

**Cuándo usarlo:** semanas o meses después del lanzamiento, cuando ya hay datos reales de uso o de negocio disponibles — como cierre formal de un proyecto o como revisión periódica de iniciativas ya lanzadas.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — una revisión de éxito sesgada u omitida deja a la organización sin aprendizaje real sobre si sus inversiones de proyecto generan el valor prometido, repitiendo los mismos errores de estimación de beneficios en futuros proyectos; el prompt no ejecuta ni recolecta datos nuevos |
| Entradas requeridas | Project Charter original con objetivos/KPIs declarados (`00-D-01`), datos reales de uso/adopción/negocio desde el lanzamiento, ventana de tiempo transcurrida |
| Herramientas permitidas | lectura de documentación y datos ya recolectados — sin ejecutar análisis de datos en vivo ni instrumentación nueva |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si un KPI del Charter no puede medirse con los datos disponibles, no inventes un valor aproximado — repórtalo como "no medible" y señala qué instrumentación faltaría para poder medirlo la próxima vez |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada objetivo/KPI declarado en el Charter aparece en la revisión con su valor real medido (o "no medible" con la razón) y un veredicto de cumplido/parcial/no cumplido |
| Siguiente prompt recomendado | `11-03-deuda-tecnica` si la revisión revela deuda técnica que quedó pendiente del proyecto original |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Evalúa si el proyecto o feature lanzada cumplió los objetivos y KPIs declarados en su Project Charter original, con datos reales medidos, identificando beneficios no previstos y aprendizajes para futuras estimaciones.

Entradas:
- Project Charter original: [PEGAR O REFERENCIA A 00-D-01]
- datos reales de uso/adopción/negocio: [PEGAR O REFERENCIA A LAS FUENTES DE DATOS DISPONIBLES]
- ventana de tiempo transcurrida desde el lanzamiento: [EJ. "6 semanas", "3 meses"]

Actividades:
1. RECUPERACIÓN DE OBJETIVOS ORIGINALES
   Cita textualmente los objetivos y KPIs declarados en el Project Charter original — no los reinterpretes con el conocimiento actual del proyecto.

2. MEDICIÓN REAL
   Para cada objetivo/KPI, mide el valor real alcanzado con los datos disponibles y compáralo contra la meta declarada originalmente.

3. VEREDICTO POR OBJETIVO
   Clasifica cada uno: cumplido / parcialmente cumplido / no cumplido / no medible (con la razón específica de por qué no es medible).

4. BENEFICIOS NO PREVISTOS
   Identifica beneficios (positivos o negativos) que se materializaron pero que no estaban en el Charter original.

5. SUPUESTOS INVALIDADOS
   Identifica qué supuestos del Charter original resultaron falsos en retrospectiva, y qué se aprende de eso para mejorar futuras estimaciones de beneficios.

6. RECOMENDACIÓN DE SEGUIMIENTO
   Recomienda si se requiere una acción de seguimiento: inversión adicional para cerrar una brecha detectada, instrumentación nueva para poder medir mejor la próxima vez, o cierre del proyecto como exitoso sin acción adicional.

Restricciones:
- nunca declares un KPI como "cumplido" sin un valor medido real citado — si no hay dato disponible, es "no medible", nunca un supuesto optimista disfrazado de medición,
- cita los objetivos originales del Charter textualmente antes de evaluarlos — no los reformules de una manera que facilite declararlos cumplidos,
- distingue explícitamente un beneficio realmente causado por este proyecto de una mejora coincidente por otra causa — si no puedes atribuir causalidad con confianza razonable, decláralo explícitamente en vez de atribuirlo,
- no ejecutes ni recolectes datos nuevos — esta revisión es de solo lectura sobre evidencia ya disponible; si falta instrumentación para medir un KPI, repórtalo como hallazgo, no inventes el dato faltante.

Salida:
0. Bloque JSON de metadatos (claves: status, kpis_evaluated, kpis_met_count, kpis_not_measurable_count, confidence_score [0.0 a 1.0]).
1. Objetivos/KPIs originales del Charter (cita textual).
2. Valor real medido por KPI, con la fuente de datos citada.
3. Veredicto por KPI: cumplido / parcial / no cumplido / no medible.
4. Beneficios no previstos (positivos y negativos).
5. Supuestos del Charter que resultaron falsos — aprendizaje para el futuro.
6. Recomendación de seguimiento.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de revisión de éxito post-lanzamiento y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- Project Charter original: [REFERENCIA A 00-D-01]
- ventana de tiempo transcurrida: [EJ. "6 semanas"]
- documentos a revisar: Project Charter, datos de uso/adopción/negocio disponibles
- objetivo puntual de salida: revisión de KPIs cumplidos/no cumplidos con aprendizajes
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen de cumplimiento |
| Objetivos originales (1) | Cita textual de los KPIs del Charter |
| Valor real medido (2) | Dato real por KPI, con fuente citada |
| Veredicto (3) | Cumplido/parcial/no cumplido/no medible por KPI |
| Beneficios no previstos (4) | Efectos positivos o negativos no anticipados |
| Supuestos invalidados (5) | Qué se asumió que resultó falso, y el aprendizaje |
| Recomendación (6) | Acción de seguimiento sugerida |

### Ejemplo (fragmento)

```json
{
  "status": "revisado_con_hallazgos",
  "kpis_evaluated": 4,
  "kpis_met_count": 2,
  "kpis_not_measurable_count": 1,
  "confidence_score": 0.71
}
```

| KPI original (Charter) | Meta declarada | Valor real medido | Fuente | Veredicto |
|---|---|---|---|---|
| Reducción de abandono en checkout | -15% en 8 semanas | -9% en 8 semanas | Dashboard de analítica de conversión | Parcialmente cumplido |
| Reducción de tickets de soporte relacionados | -20% | No medible | No se etiquetó la categoría de ticket antes del lanzamiento para poder aislar este efecto | No medible — falta instrumentación |

| Sección | Ejemplo de contenido |
|---|---|
| Supuestos invalidados (5) | El Charter asumía que el 80% de los usuarios completarían el nuevo flujo sin ayuda; los datos muestran que el 35% abandona en el paso 2 — el supuesto de facilidad de uso fue optimista; para el próximo proyecto similar, incluir una prueba de usabilidad con usuarios reales antes de comprometer una meta de conversión |
