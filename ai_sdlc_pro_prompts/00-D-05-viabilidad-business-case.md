# 0-D.5 — Estudio de viabilidad y business case: ¿deberíamos hacer este proyecto?

## Descripción

Prompt para evaluar si una idea o iniciativa **vale la pena formalizarse como proyecto**, antes de invertir tiempo en redactar el Project Charter: viabilidad técnica, económica, operativa y legal/regulatoria, alternativas consideradas (incluyendo no hacer nada) y una recomendación explícita de go/no-go.

**Cuándo usarlo:** al recibir una idea de proyecto o iniciativa de negocio, **antes** de `00-D-01-project-charter` — este prompt determina si el proyecto debería formalizarse; el Charter asume que ya se decidió que sí.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | alto — la recomendación de go/no-go de este análisis condiciona si se invierte presupuesto y tiempo del equipo en formalizar el proyecto; un análisis optimista o sesgado puede justificar proyectos que no debieron aprobarse, aunque el prompt no ejecuta ni compromete nada por sí mismo |
| Entradas requeridas | idea o iniciativa en bruto, contexto de negocio, restricciones conocidas (presupuesto máximo, plazo, recursos disponibles), alternativas ya consideradas si existen |
| Herramientas permitidas | ninguna de ejecución — lectura de contexto y documentación existente; produce un documento de análisis, no ejecuta ni aprueba nada |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si no puede estimarse ni el costo ni el beneficio con un mínimo de confianza, no forzar una recomendación go/no-go — declarar "viabilidad no determinable con la información disponible" en vez de inventar una cifra |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada dimensión de viabilidad (técnica, económica, operativa, legal/regulatoria) tiene un veredicto explícito con justificación citada; las alternativas descartadas, incluida "no hacer nada", están documentadas |
| Siguiente prompt recomendado | `00-D-01-project-charter` si el veredicto es GO o GO condicionado |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Evalúa si la idea o iniciativa descrita justifica formalizarse como proyecto: viabilidad técnica, económica, operativa y legal/regulatoria, alternativas consideradas y una recomendación explícita de go/no-go.

Entradas:
- idea o iniciativa: [DESCRIPCIÓN EN BRUTO]
- contexto de negocio: [POR QUÉ SURGE ESTA IDEA, QUÉ PROBLEMA RESUELVE]
- restricciones conocidas: [PRESUPUESTO MÁXIMO, PLAZO, RECURSOS DISPONIBLES, O "no declaradas aún"]
- alternativas ya consideradas: [PEGAR O "ninguna considerada aún"]

Actividades:
1. VIABILIDAD TÉCNICA
   Evalúa si existe la tecnología y la capacidad del equipo (actual o adquirible) para ejecutar esta idea. Identifica los riesgos técnicos mayores que podrían hacerla inviable.

2. VIABILIDAD ECONÓMICA
   Estima el costo aproximado (orden de magnitud, con el método de estimación declarado) y el beneficio esperado (cuantificado si es posible, cualitativo si no). Calcula ROI aproximado o payback period si hay suficiente información; si no la hay, decláralo explícitamente en vez de inventar una cifra.

3. VIABILIDAD OPERATIVA
   Evalúa si la organización puede operar y mantener el resultado una vez construido: impacto en procesos existentes, capacidad del equipo para sostenerlo en el tiempo, dependencias operativas nuevas que introduce.

4. VIABILIDAD LEGAL/REGULATORIA
   Identifica restricciones de compliance (regulación de la industria, protección de datos, licenciamiento) que podrían bloquear o encarecer significativamente el proyecto.

5. ALTERNATIVAS CONSIDERADAS
   Compara al menos: construir (build), comprar/adoptar una solución existente (buy), y no hacer nada — con pros y contras de cada una. "No hacer nada" siempre debe evaluarse explícitamente, nunca omitirse por obvio.

6. RECOMENDACIÓN
   Emite un veredicto: GO / NO-GO / GO CONDICIONADO (con las condiciones específicas que deben cumplirse). Nunca emitas una recomendación sin justificarla contra las 4 dimensiones de viabilidad evaluadas.

Restricciones:
- nunca declares viabilidad económica sin declarar el método de estimación de costo/beneficio usado — una cifra sin método se reporta como no verificable, no como estimación válida,
- siempre incluye "no hacer nada" como alternativa explícita a comparar, nunca la omitas por parecer obvio,
- no recomiendes GO si alguna dimensión de viabilidad tiene un riesgo crítico sin mitigación identificada — en ese caso, la recomendación debe ser NO-GO o GO CONDICIONADO a resolver ese riesgo primero,
- distingue siempre una estimación basada en datos reales de una basada en supuestos — nunca las presentes con el mismo nivel de certeza.

Salida:
0. Bloque JSON de metadatos (claves: status, feasibility_verdict ["go", "no_go", "go_conditional", "not_determinable"], dimensions_evaluated, confidence_score [0.0 a 1.0]).
1. Viabilidad técnica: capacidad, tecnología, riesgos mayores.
2. Viabilidad económica: costo estimado, beneficio esperado, ROI/payback si aplica, método de estimación.
3. Viabilidad operativa: impacto en procesos, capacidad de sostener el resultado.
4. Viabilidad legal/regulatoria: restricciones identificadas.
5. Alternativas consideradas: build / buy / no hacer nada, con pros y contras.
6. Recomendación final: GO / NO-GO / GO CONDICIONADO, con condiciones si aplica.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de estudio de viabilidad y business case y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL, SI YA EXISTE]
- idea o iniciativa: [DESCRIPCIÓN EN BRUTO]
- contexto de negocio: [POR QUÉ SURGE ESTA IDEA]
- documentos a revisar: contexto de negocio, restricciones presupuestales conocidas
- objetivo puntual de salida: recomendación de go/no-go con las 4 dimensiones de viabilidad
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el veredicto de viabilidad |
| Viabilidad técnica (1) | Capacidad y riesgos técnicos mayores |
| Viabilidad económica (2) | Costo, beneficio, ROI/payback con método de estimación declarado |
| Viabilidad operativa (3) | Impacto en procesos y capacidad de sostenimiento |
| Viabilidad legal/regulatoria (4) | Restricciones de compliance identificadas |
| Alternativas (5) | Build / buy / no hacer nada, comparadas |
| Recomendación (6) | Veredicto go/no-go/condicionado, justificado |

### Ejemplo (fragmento)

```json
{
  "status": "evaluado",
  "feasibility_verdict": "go_conditional",
  "dimensions_evaluated": 4,
  "confidence_score": 0.68
}
```

| Sección | Ejemplo de contenido |
|---|---|
| Viabilidad económica (2) | Costo estimado: $80,000-120,000 USD (analogía con proyecto similar de integración de pagos, ver 00-D-01 anterior) \| Beneficio esperado: reducción de 15% en abandono de checkout (estimación cualitativa, sin dato histórico propio) \| ROI no calculable con confianza — falta dato real de conversión actual |
| Recomendación (6) | GO CONDICIONADO: proceder solo si se instrumenta la tasa de abandono de checkout actual durante 4 semanas antes de aprobar el presupuesto completo, para validar el supuesto de beneficio con datos reales en vez de una estimación cualitativa |
