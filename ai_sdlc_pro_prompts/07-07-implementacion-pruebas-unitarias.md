# 7.7 — Implementación de pruebas unitarias

## Descripción

Prompt para generar el código ejecutable de las pruebas unitarias a partir del diseño definido en `07-01`. Produce archivos de prueba listos para ejecutar en el framework de pruebas del proyecto.

**Cuándo usarlo:** después de completar el diseño de pruebas unitarias (`07-01`), cuando el agente tiene acceso al código fuente y al framework de pruebas del proyecto.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Adjunta el **Perfil de stack de pruebas** generado por `07-00` (ejecútalo una vez por proyecto si aún no existe).
> Adjunta o referencia la matriz de pruebas generada por `07-01`.

---

## Prompt completo

```text
Objetivo:
Implementa las pruebas unitarias definidas en la matriz de diseño adjunta usando el framework
de pruebas del proyecto.

Pasos:
1. Identifica el framework de pruebas activo en el repositorio
   (package.json, pyproject.toml, Gemfile, pom.xml, etc.).
2. Por cada caso de la matriz, genera el código de prueba correspondiente:
   - nombre de test descriptivo según convención del proyecto,
   - arrange: setup de datos de entrada y mocks necesarios,
   - act: invocación de la unidad bajo prueba,
   - assert: validación del resultado esperado.
3. Agrupa los tests por unidad o módulo en el archivo de prueba correspondiente.
4. Sigue las convenciones de nombramiento y estructura de directorios del proyecto.
5. Incluye mocks o stubs donde la unidad dependa de servicios externos,
   base de datos o I/O.

Restricciones:
- No modifiques el código fuente, solo los archivos de prueba.
- Mantén cada test independiente y sin efectos secundarios entre ellos.
- Prioriza los casos marcados como críticos o de cobertura obligatoria.

Entrega:
- archivos de prueba completos y ejecutables,
- comando de ejecución verificado para el entorno del proyecto,
- estimación de cobertura alcanzada por los tests generados.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de implementación de pruebas unitarias y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA DE TRABAJO]
- framework de pruebas: [AUTO-DETECTAR / pytest / Jest / Vitest / JUnit / RSpec / etc.]
- matriz de pruebas: [ADJUNTA O REFERENCIA AL DOCUMENTO DE 07-01]
- documentos a revisar: código fuente de las unidades bajo prueba, configuración del framework
- objetivo puntual de salida: archivos de prueba ejecutables con cobertura ≥ 80%
- nivel de profundidad: alto
```

---

## Salida esperada

Archivos de prueba en la estructura del proyecto, por ejemplo:

```
tests/unit/test_[modulo].[ext]
src/[modulo]/[modulo].test.[ext]
spec/unit/[modulo]_spec.[ext]
```

Con estructura interna tipo AAA (Arrange / Act / Assert):

```
[clase o suite de test para la unidad]
  ✓ [escenario positivo principal]
  ✓ [escenario negativo esperado]
  ✓ [caso borde identificado]
```
