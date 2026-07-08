# 7.3 — Diseño de pruebas E2E

## Descripción

Prompt para diseñar pruebas end-to-end de los casos de uso impactados por el cambio: desde el actor hasta el resultado final, incluyendo evidencia requerida y regresiones relacionadas.

**Cuándo usarlo:** después de las pruebas de integración (`07-02`), para validar el flujo completo desde la perspectiva del usuario.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño — produce un plan de pruebas E2E en formato tabla, no código ejecutable |
| Riesgo esperado | bajo — es un documento de planificación; no modifica sistemas ni ejecuta pruebas |
| Entradas requeridas | caso de uso o requerimiento a cubrir, criterios de aceptación, referencia al plan de integración previo (`07-02`) |
| Herramientas permitidas | solo lectura de documentación (casos de uso, criterios de aceptación, flujos documentados); no requiere acceso de escritura ni ejecución |
| Autonomía permitida | A1 — Proponer (entrega un plan/artefacto sin aplicar; la ejecución ocurre en `07-09`) |
| Criterios de detención | detener y pedir aclaración si el caso de uso o los criterios de aceptación no están definidos con suficiente detalle para derivar pasos, resultado esperado y evidencia |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada fila de la tabla debe especificar actor, flujo, precondiciones, pasos, resultado esperado, evidencia requerida y regresiones relacionadas |
| Siguiente prompt recomendado | `07-09-implementacion-pruebas-e2e` para convertir este plan en scripts E2E ejecutables |

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
