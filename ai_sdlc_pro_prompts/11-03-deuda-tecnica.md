# 11.3 — Deuda técnica y mejora continua

## Descripción

Prompt para identificar la deuda técnica del repositorio y generar un backlog priorizado de mejoras clasificado por arquitectura, código, pruebas, documentación, seguridad, CI/CD, observabilidad, datos y performance.

**Cuándo usarlo:** al cierre de un sprint, en revisiones técnicas periódicas, o cuando se quiere planificar mejoras estructurales del proyecto.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Identifica deuda técnica en el repositorio y propón un backlog priorizado de mejoras.

Clasifica por:
- arquitectura,
- código,
- pruebas,
- documentación,
- seguridad,
- CI/CD,
- observabilidad,
- datos,
- performance.

Entrega:
- matriz de deuda técnica,
- prioridad,
- impacto,
- esfuerzo estimado,
- recomendación de atención.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de deuda técnica y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA PRINCIPAL]
- componentes: [MÓDULOS O ÁREAS A ANALIZAR]
- documentos a revisar: código fuente, tests, CI/CD, arquitectura, docs
- objetivo puntual de salida: backlog priorizado de deuda técnica con esfuerzo estimado
- nivel de profundidad: alto
```

---

## Salida esperada

| Ítem | Categoría | Descripción | Prioridad | Impacto | Esfuerzo | Recomendación |
|---|---|---|---|---|---|---|
