# 7.1 — Diseño de pruebas unitarias

## Descripción

Prompt para diseñar la suite de pruebas unitarias que valide los cambios propuestos o implementados: escenarios positivos, negativos y casos borde por cada función o unidad bajo prueba.

**Cuándo usarlo:** después de implementar cambios, en paralelo a la implementación, o como referencia antes de escribir código.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | bajo — produce una matriz de casos de prueba como diseño, no implementa ni ejecuta código de prueba |
| Entradas requeridas | código implementado o cambios propuestos, criterios de aceptación, perfil de stack de pruebas (`07-00`) si está disponible |
| Herramientas permitidas | solo lectura del código y de los criterios de aceptación; no ejecuta pruebas ni escribe archivos de test, únicamente produce la matriz de diseño |
| Autonomía permitida | A1 — Proponer (matriz de pruebas como artefacto, sin implementar el código de test) |
| Criterios de detención | detener si no hay código o criterios de aceptación de referencia; señalar explícitamente si la cobertura recomendada no puede alcanzarse con la información disponible en vez de inventar escenarios |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada unidad bajo prueba con al menos un caso positivo, un caso negativo y un caso borde documentados |
| Siguiente prompt recomendado | `07-07-implementacion-pruebas-unitarias` para convertir la matriz en código de prueba ejecutable |

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
