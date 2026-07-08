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

Pasos:
1. Identifica el flujo a probar y los componentes que interactúan en él (servicios, APIs internas/externas, base de datos, colas, caché).
2. Define los datos de prueba necesarios para ejercitar el flujo completo — sintéticos o anonimizados, nunca datos reales de producción.
3. Para cada punto de integración, especifica el resultado esperado en el camino feliz y al menos un caso de fallo (timeout, respuesta de error, dato inconsistente).
4. Define cómo se valida el estado resultante (respuesta HTTP, registro en base de datos, evento emitido) y qué se debe limpiar después de la prueba.
5. Señala qué integraciones externas deben simularse (mocks/stubs/contract testing) porque no son controlables o estables en el entorno de prueba.
6. Prioriza los flujos críticos de negocio y las integraciones con mayor probabilidad de fallo (servicios de terceros, colas asíncronas) antes que integraciones internas estables.

Restricciones:
- nunca usar datos reales de producción como datos de prueba, solo datos sintéticos o anonimizados,
- cada prueba de integración debe poder ejecutarse de forma repetible sin dejar estado residual (idempotencia o limpieza explícita),
- si falta un contrato de API o diseño de integración de referencia, detente y señálalo en vez de asumir el comportamiento.

Entrega:
- plan de pruebas de integración,
- lista de integraciones externas a simular,
- estrategia de datos de prueba y limpieza.
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
| Registro de usuario | API auth, base de datos, servicio de email (mock) | usuario sintético con email único | usuario creado, email de bienvenida encolado | email duplicado devuelve 409 sin crear registro |
| Checkout de compra | API carrito, API pagos (stub), base de datos, cola de eventos | carrito con 2 ítems, tarjeta de prueba | orden creada, evento `order.created` emitido | pago rechazado revierte la orden y no emite el evento |
