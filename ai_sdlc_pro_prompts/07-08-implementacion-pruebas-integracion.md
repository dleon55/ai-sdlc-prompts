# 7.8 — Implementación de pruebas de integración

## Descripción

Prompt para generar el código ejecutable de las pruebas de integración a partir del diseño definido en `07-02`. Valida la interacción real entre módulos, servicios, APIs y base de datos usando el framework de pruebas del proyecto.

**Cuándo usarlo:** después de completar el diseño de pruebas de integración (`07-02`), cuando el entorno de pruebas (base de datos, servicios dependientes) está disponible o puede ser simulado con contenedores o stubs.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Adjunta el **Perfil de stack de pruebas** generado por `07-00` (ejecútalo una vez por proyecto si aún no existe).
> Adjunta o referencia el plan de pruebas de integración generado por `07-02`.

---

## Prompt completo

```text
Objetivo:
Implementa las pruebas de integración definidas en el plan de diseño adjunto usando el
framework de pruebas del proyecto.

Pasos:
1. Identifica el framework de pruebas y las herramientas de integración del repositorio
   (pytest + fixtures, Jest + supertest, Testcontainers, WireMock, etc.).
2. Por cada flujo del plan, genera el código de prueba correspondiente:
   - setup del estado inicial: base de datos, servicios externos o stubs necesarios,
   - ejecución del flujo de integración completo,
   - validación del resultado a través de todos los componentes involucrados,
   - teardown o limpieza del estado generado.
3. Implementa fixtures o helpers reutilizables para datos de prueba comunes.
4. Usa stubs o contenedores de prueba para dependencias externas no disponibles en CI.
5. Sigue las convenciones de estructura del proyecto para tests de integración.

Restricciones:
- Aísla el estado de cada test para evitar interferencia entre ejecuciones.
- No llames a servicios de producción reales; usa entornos de prueba o doubles.
- Incluye manejo explícito de errores y timeouts para llamadas a servicios.

Entrega:
- archivos de prueba de integración completos y ejecutables,
- instrucciones de setup del entorno de pruebas (variables de entorno, servicios requeridos),
- comando de ejecución verificado,
- notas sobre dependencias externas que requieren configuración adicional.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de implementación de pruebas de integración y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA DE TRABAJO]
- framework de pruebas: [AUTO-DETECTAR / pytest / Jest / Spring Test / etc.]
- herramientas de integración: [AUTO-DETECTAR / Testcontainers / WireMock / MSW / etc.]
- plan de integración: [ADJUNTA O REFERENCIA AL DOCUMENTO DE 07-02]
- documentos a revisar: contratos API, esquema de base de datos, configuración de servicios
- objetivo puntual de salida: pruebas de integración ejecutables con flujos críticos cubiertos
- nivel de profundidad: alto
```

---

## Salida esperada

Archivos de prueba en la estructura del proyecto, por ejemplo:

```
tests/integration/test_[flujo].[ext]
src/[modulo]/__tests__/[flujo].integration.test.[ext]
spec/integration/[flujo]_spec.[ext]
```

Con estructura interna:

```
[suite de integración para el flujo]
  setup: [inicialización del entorno]
  ✓ [flujo completo escenario positivo]
  ✓ [flujo con error en componente X]
  ✓ [flujo con datos límite]
  teardown: [limpieza del estado]
```
