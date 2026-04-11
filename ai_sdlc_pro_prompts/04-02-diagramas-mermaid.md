# 4.2 — Generar diagramas Mermaid

## Descripción

Prompt para generar diagramas Mermaid que documenten la solución: flujo actual y propuesto, secuencia, componentes y entidad-relación. Los diagramas deben ser consistentes con el código y la arquitectura real.

**Cuándo usarlo:** durante o después del diseño de la solución (`04-01`), para documentar y comunicar visualmente los cambios.

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

Reglas:
- Los diagramas deben ser consistentes con el código y la arquitectura real.
- No inventes componentes inexistentes.
- Etiqueta claramente actores, servicios, módulos y datos.

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
