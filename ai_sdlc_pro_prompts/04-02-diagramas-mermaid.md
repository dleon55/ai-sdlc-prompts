# 4.2 — Generar diagramas Mermaid

## Descripción

Prompt para generar diagramas Mermaid que documenten la solución: flujo actual y propuesto, secuencia, componentes y entidad-relación. Los diagramas deben ser consistentes con el código y la arquitectura real.

**Cuándo usarlo:** durante o después del diseño de la solución (`04-01`), para documentar y comunicar visualmente los cambios.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | bajo — genera artefactos de documentación visual, no modifica código ni configuración |
| Entradas requeridas | diseño aprobado (`04-01`), arquitectura real del sistema, código fuente o componentes involucrados en el cambio |
| Herramientas permitidas | solo lectura de código, diseño y arquitectura; no requiere ejecución ni escritura en el repositorio, únicamente genera bloques Mermaid como texto |
| Autonomía permitida | A0 — Analizar el diseño y código existente; A1 — Proponer los diagramas como artefacto de documentación |
| Criterios de detención | detener si no existe diseño aprobado (`04-01`) del cual derivar los diagramas; nunca inventar componentes, actores o flujos que no existan en el código o diseño real |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada diagrama corresponde a componentes/flujos verificables en el código o diseño citado; sintaxis Mermaid válida (caracteres especiales escapados, sin usar `end` sin comillas como texto de nodo) |
| Siguiente prompt recomendado | `04-03-casos-de-uso` para completar la documentación funcional de la solución |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Con base en el análisis y diseño del cambio, genera diagramas Mermaid claros y útiles para documentar la solución.

Necesito:
1. Diagrama de flujo del proceso actual y propuesto
2. Diagrama de secuencia
3. Diagrama de componentes
4. Si aplica, diagrama entidad-relación simplificado

Tipo de diagrama Mermaid a usar por cada uno:
- Flujo: usa `flowchart TD` o `flowchart LR`.
- Secuencia: usa `sequenceDiagram`.
- Componentes: Mermaid no tiene un tipo nativo de diagrama de componentes; usa `flowchart LR` con subgraphs por módulo.
- Entidad-relación: usa `erDiagram`.

Reglas:
- Los diagramas deben ser consistentes con el código y la arquitectura real.
- No inventes componentes inexistentes.
- Etiqueta claramente actores, servicios, módulos y datos.
- Regla de Sintaxis Estricta: Escapa siempre caracteres especiales (como paréntesis, corchetes o comas) en los nombres de los nodos envolviéndolos en comillas dobles (ej: id["Nombre Nodo (Detalle)"]). NUNCA utilices etiquetas HTML (como <br> o <b>) dentro de los textos de los nodos de Mermaid para evitar errores de renderizado.
- Nunca uses la palabra "end" como ID de nodo o como texto de nodo sin comillas: es palabra reservada y rompe el parseo de flowcharts.

Entrega:
- bloque Mermaid por diagrama,
- breve explicación de cada uno.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de diagramas Mermaid y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: diseño aprobado, arquitectura, código fuente
- objetivo puntual de salida: conjunto de diagramas Mermaid para documentación técnica
- nivel de profundidad: medio
```

---

## Salida esperada

Un bloque Mermaid por cada diagrama con su explicación:

| Diagrama | Descripción |
|---|---|
| Flujo actual | Cómo funciona el flujo hoy |
| Flujo propuesto | Cómo funcionará después del cambio |
| Secuencia | Interacción entre actores y servicios |
| Componentes | Relación entre módulos del sistema |
| ER (si aplica) | Entidades y relaciones de datos involucradas |
