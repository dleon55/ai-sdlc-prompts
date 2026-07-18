# 5.2 — Análisis de riesgos e impacto de implementación

## Descripción

Prompt para identificar y clasificar los riesgos de implementación: funcionales, técnicos, de datos, seguridad, operación, concurrencia de agentes, integración y despliegue. Genera una matriz de riesgos con probabilidad, impacto y plan de mitigación.

**Cuándo usarlo:** en paralelo al plan de implementación (`05-01`), antes de ejecutar cualquier cambio.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — no ejecuta cambios, pero un riesgo omitido o mal clasificado puede llegar sin mitigación a la fase de ejecución (`06-01`) |
| Entradas requeridas | diseño aprobado, arquitectura, historial de incidentes, plan de implementación (`05-01`) en curso o aprobado |
| Herramientas permitidas | solo lectura de diseño, arquitectura e historial de incidentes; no ejecuta comandos ni modifica el repositorio |
| Autonomía permitida | A0 — Analizar riesgos e impacto potencial; A1 — Proponer la matriz de riesgos con mitigación y contingencia |
| Criterios de detención | detener si no hay diseño o plan de referencia; escalar a revisión humana antes de continuar a `06-01` si algún riesgo queda clasificado como alto sin mitigación viable |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada riesgo con categoría, probabilidad, impacto, mitigación y contingencia explícitos; ningún riesgo alto sin plan de mitigación asociado |
| Siguiente prompt recomendado | `06-01-implementacion-multiagente`, una vez el plan (`05-01`) y esta matriz de riesgos estén aprobados |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Identifica y analiza los riesgos de implementación y el impacto potencial del cambio en otros módulos, procesos, servicios, pipelines, integraciones y usuarios, en paralelo al plan de implementación (`05-01`).

Entradas:
- diseño aprobado: [PEGAR O REFERENCIA]
- arquitectura: [REFERENCIA]
- historial de incidentes relacionados: [REFERENCIA O "ninguno conocido"]
- plan de implementación (`05-01`): [REFERENCIA]

Pasos:
1. Revisa el diseño aprobado, la arquitectura y el plan de implementación para identificar todos los puntos de cambio y sus dependencias.
2. Para cada punto de cambio, identifica riesgos en cada una de estas categorías cuando aplique: funcional, técnico, datos, seguridad, operación, concurrencia de agentes, integración, despliegue.
3. Para cada riesgo, estima probabilidad (baja/media/alta) e impacto (bajo/medio/alto) con base en el historial de incidentes o el diseño citado — no en intuición sin respaldo.
4. Define la mitigación propuesta y el plan de contingencia (qué hacer si la mitigación falla) para cada riesgo.
5. Si un riesgo queda clasificado como alto sin una mitigación viable, no lo minimices ni lo dejes implícito: decláralo explícitamente como bloqueante para `06-01`.

Restricciones:
- no clasifiques un riesgo como bajo solo porque falta evidencia en contra — si no hay información suficiente para evaluarlo, decláralo como "riesgo no evaluable con la información disponible" en vez de asumir que es bajo,
- ningún riesgo alto puede quedar sin mitigación o contingencia explícitas en la salida,
- no ejecutes comandos ni modifiques el repositorio o el ambiente — este prompt es de solo análisis y propuesta (A0/A1),
- distingue en cada fila de la matriz qué es un riesgo confirmado por evidencia citada (diseño, arquitectura, historial de incidentes) y qué es una inferencia propia — nunca los mezcles sin marcarlos,
- si no existe diseño o plan de implementación de referencia, detente y solicítalo en vez de construir la matriz sobre supuestos propios.

Salida:
- matriz de riesgos: categoría, probabilidad, impacto, mitigación, contingencia
- lista separada de riesgos altos sin mitigación viable (si existen), marcados como bloqueantes para `06-01`
```

---

## Uso con fórmula estándar

```text
Usa el prompt de análisis de riesgos de implementación y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA OBJETIVO]
- ambiente: [DEV / QA / PROD]
- componentes: [COMPONENTES A MODIFICAR]
- documentos a revisar: diseño aprobado, arquitectura, historial de incidentes
- objetivo puntual de salida: matriz de riesgos completa con plan de mitigación
- nivel de profundidad: alto
```

---

## Salida esperada

| Riesgo | Categoría | Probabilidad | Impacto | Mitigación | Contingencia |
|---|---|---|---|---|---|
