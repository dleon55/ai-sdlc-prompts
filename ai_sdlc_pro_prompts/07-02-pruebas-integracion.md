# 7.2 — Diseño de pruebas de integración

## Descripción

Prompt para definir las pruebas de integración que validen la interacción entre módulos, servicios, APIs, base de datos e integraciones involucradas en el cambio.

**Cuándo usarlo:** después de las pruebas unitarias (`07-01`), para validar que los módulos funcionan correctamente en conjunto.

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
