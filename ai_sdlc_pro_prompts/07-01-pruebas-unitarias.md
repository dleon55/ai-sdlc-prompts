# 7.1 — Diseño de pruebas unitarias

## Descripción

Prompt para diseñar la suite de pruebas unitarias que valide los cambios propuestos o implementados: escenarios positivos, negativos y casos borde por cada función o unidad bajo prueba.

**Cuándo usarlo:** después de implementar cambios, en paralelo a la implementación, o como referencia antes de escribir código.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña las pruebas unitarias necesarias para validar los cambios propuestos o implementados.

Incluye:
- función o unidad bajo prueba,
- escenario,
- entrada,
- resultado esperado,
- casos positivos,
- casos negativos,
- casos borde.

Entrega:
- matriz de pruebas unitarias,
- recomendación de cobertura.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de pruebas unitarias y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA DE PRUEBAS]
- ambiente: [DEV / QA]
- componentes: [FUNCIONES O UNIDADES A PROBAR]
- documentos a revisar: código implementado, criterios de aceptación
- objetivo puntual de salida: matriz completa de pruebas unitarias con cobertura
- nivel de profundidad: alto
```

---

## Salida esperada

| Unidad | Escenario | Entrada | Resultado esperado | Tipo |
|---|---|---|---|---|
