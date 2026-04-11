# 7.3 — Diseño de pruebas E2E

## Descripción

Prompt para diseñar pruebas end-to-end de los casos de uso impactados por el cambio: desde el actor hasta el resultado final, incluyendo evidencia requerida y regresiones relacionadas.

**Cuándo usarlo:** después de las pruebas de integración (`07-02`), para validar el flujo completo desde la perspectiva del usuario.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña pruebas end-to-end para los casos de uso impactados por el cambio.

Incluye:
- actor,
- flujo principal,
- precondiciones,
- pasos,
- resultado esperado,
- evidencia requerida,
- regresiones relacionadas.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de pruebas E2E y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA DE PRUEBAS]
- ambiente: [QA / STAGING]
- componentes: [FLUJOS Y MÓDULOS A PROBAR]
- documentos a revisar: casos de uso, criterios de aceptación, flujos documentados
- objetivo puntual de salida: plan de pruebas E2E con evidencia requerida por caso
- nivel de profundidad: alto
```

---

## Salida esperada

| Actor | Flujo | Precondiciones | Pasos | Resultado esperado | Evidencia | Regresiones |
|---|---|---|---|---|---|---|
