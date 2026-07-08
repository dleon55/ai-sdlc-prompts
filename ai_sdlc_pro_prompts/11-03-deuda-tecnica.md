# 11.3 — Deuda técnica y mejora continua

## Descripción

Prompt para identificar la deuda técnica del repositorio y generar un backlog priorizado de mejoras clasificado por arquitectura, código, pruebas, documentación, seguridad, CI/CD, observabilidad, datos y performance.

**Cuándo usarlo:** al cierre de un sprint, en revisiones técnicas periódicas, o cuando se quiere planificar mejoras estructurales del proyecto.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | bajo — genera un inventario y backlog priorizado; no modifica código ni sistemas |
| Entradas requeridas | rama principal, componentes o módulos a analizar, acceso a código fuente, tests, configuración CI/CD, arquitectura y documentación |
| Herramientas permitidas | solo lectura del repositorio (código, tests, configuración CI/CD, documentación) |
| Autonomía permitida | A0 — Analizar: inventario y recomendaciones, sin aplicar cambios |
| Criterios de detención | si no puede acceder a un área declarada como "a analizar" (módulo inexistente o fuera del repo), debe señalar la omisión en vez de completar la matriz con supuestos |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada ítem de la matriz referencia un archivo, módulo o configuración real del repositorio, con prioridad, impacto y esfuerzo justificados |
| Siguiente prompt recomendado | `05-01-plan-implementacion` para planificar la resolución de los ítems priorizados; `11-06-gestion-parches-actualizaciones` si la deuda identificada es de dependencias desactualizadas |

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
