# 7.2 — Diseño de pruebas de integración

## Descripción

Prompt para definir las pruebas de integración que validen la interacción entre módulos, servicios, APIs, base de datos e integraciones involucradas en el cambio.

**Cuándo usarlo:** después de las pruebas unitarias (`07-01`), para validar que los módulos funcionan correctamente en conjunto.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | bajo — produce un plan de pruebas de integración como diseño, no ejecuta pruebas ni modifica el repositorio |
| Entradas requeridas | contratos de API, diseño de integración, datos de prueba disponibles, matriz de pruebas unitarias (`07-01`) si existe |
| Herramientas permitidas | solo lectura de contratos, diseño de integración y código; no ejecuta pruebas ni escribe archivos, únicamente produce el plan |
| Autonomía permitida | A1 — Proponer (plan de pruebas de integración sin implementar) |
| Criterios de detención | detener si faltan contratos de API o diseño de integración de referencia; nunca usar datos reales de producción como datos de prueba, solo datos sintéticos o anonimizados |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada flujo con componentes integrados, datos de prueba y validación de errores explícitos |
| Siguiente prompt recomendado | `07-08-implementacion-pruebas-integracion` para convertir el plan en pruebas ejecutables |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Define las pruebas de integración necesarias para validar la interacción entre módulos, servicios, APIs, base de datos e integraciones involucradas.

Incluye:
- flujo,
- componentes integrados,
- datos de prueba,
- resultado esperado,
- validación de errores.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de pruebas de integración y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA DE PRUEBAS]
- ambiente: [QA / STAGING]
- componentes: [MÓDULOS E INTEGRACIONES A PROBAR]
- documentos a revisar: contratos API, diseño de integración, datos de prueba disponibles
- objetivo puntual de salida: plan de pruebas de integración con casos de error
- nivel de profundidad: alto
```

---

## Salida esperada

| Flujo | Componentes integrados | Datos de prueba | Resultado esperado | Validación de error |
|---|---|---|---|---|
