# 4.1 — Diseño funcional y técnico de solución

## Descripción

Prompt para diseñar la solución completa antes de implementar: objetivo, alcance, supuestos, restricciones, cambios por componente, riesgos, dependencias, estrategia de validación y rollback.

**Cuándo usarlo:** una vez completado el análisis funcional, técnico y de impacto, antes de planificar o ejecutar cualquier cambio.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | medio — el diseño resultante guía directamente la implementación; un diseño incompleto en riesgos o estrategia de rollback puede llevar a una implementación insegura o sin plan de reversión, aunque este prompt no ejecuta cambios |
| Entradas requeridas | análisis funcional, técnico y de impacto cruzado ya completados (`02-01`, `02-02`, `02-03`), arquitectura y contratos existentes |
| Herramientas permitidas | lectura de código, arquitectura y documentación — sin ejecución ni cambios; el resultado es un documento de diseño, no código |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si no existe una estrategia de rollback viable para un componente crítico, declararlo como riesgo abierto en el diseño en vez de omitirlo |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada cambio propuesto por componente debe estar vinculado a un riesgo y su mitigación, y a los hallazgos del análisis previo citado |
| Siguiente prompt recomendado | `05-01-plan-implementacion` |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña una solución completa, funcional y técnica, para el requerimiento o incidente analizado.

Incluye:
1. Objetivo de la solución
2. Alcance
3. Supuestos
4. Restricciones
5. Casos de uso impactados
6. Reglas de negocio
7. Cambios requeridos por componente
8. Riesgos
9. Dependencias
10. Estrategia de validación
11. Estrategia de rollback

Formato de salida:
1. Resumen de diseño
2. Diseño funcional
3. Diseño técnico
4. Componentes afectados
5. Riesgos y mitigaciones
6. Recomendación de implementación
```

---

## Uso con fórmula estándar

```text
Usa el prompt de diseño de solución y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA OBJETIVO]
- ambiente: [DEV / QA / PROD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: análisis previo, arquitectura, contratos
- objetivo puntual de salida: diseño completo con riesgos y estrategia de rollback
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Resumen de diseño | Descripción ejecutiva de la solución |
| Diseño funcional | Cambios en flujos, reglas y casos de uso |
| Diseño técnico | Componentes, contratos, cambios por módulo |
| Componentes afectados | Lista precisa con tipo de cambio |
| Riesgos y mitigaciones | Riesgos identificados con plan de mitigación |
| Recomendación | Orden y prioridad de implementación |
