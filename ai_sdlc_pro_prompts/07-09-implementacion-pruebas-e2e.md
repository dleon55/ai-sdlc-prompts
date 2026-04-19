# 7.9 — Implementación de pruebas E2E

## Descripción

Prompt para generar el código ejecutable de las pruebas end-to-end a partir del diseño definido en `07-03`. Produce scripts de automatización que validan flujos completos desde la interfaz de usuario hasta el resultado final, usando el framework E2E del proyecto.

**Cuándo usarlo:** después de completar el diseño de pruebas E2E (`07-03`), cuando la aplicación está desplegada en un entorno de pruebas accesible (QA o staging).

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Adjunta el **Perfil de stack de pruebas** generado por `07-00` (ejecútalo una vez por proyecto si aún no existe).
> Adjunta o referencia el plan de pruebas E2E generado por `07-03`.

---

## Prompt completo

```text
Objetivo:
Implementa las pruebas end-to-end definidas en el plan de diseño adjunto usando el
framework E2E del proyecto.

Pasos:
1. Identifica el framework E2E activo en el repositorio
   (Playwright, Cypress, Selenium, Puppeteer, Robot Framework, etc.).
2. Por cada flujo del plan, genera el script de prueba correspondiente:
   - configuración inicial: URL base, credenciales de prueba, estado previo requerido,
   - pasos de interacción con la UI en el orden definido en el plan,
   - aserciones de resultado esperado en cada paso crítico,
   - captura de evidencia: screenshots o video en pasos clave y en caso de fallo.
3. Implementa el patrón Page Object (u equivalente) para separar la lógica de interacción
   de los tests, si el proyecto ya lo usa o si hay más de 3 páginas involucradas.
4. Maneja esperas de forma explícita; evita sleeps fijos.
5. Cubre los flujos de regresión identificados en el plan.

Restricciones:
- Usa únicamente datos de prueba; nunca datos reales de producción.
- Los tests deben poder ejecutarse de forma independiente y en modo headless.
- Incluye cleanup del estado de la aplicación al finalizar cada test si el flujo
  lo requiere (por ejemplo, eliminar registros creados).

Entrega:
- scripts E2E completos y ejecutables,
- configuración necesaria del framework (variables de entorno, base URL, etc.),
- comando de ejecución verificado (headless y headed),
- directorio donde se guardan screenshots y reportes.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de implementación de pruebas E2E y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA DE TRABAJO]
- framework E2E: [AUTO-DETECTAR / Playwright / Cypress / Selenium / Robot Framework / etc.]
- URL del entorno de pruebas: [URL DE QA O STAGING]
- plan E2E: [ADJUNTA O REFERENCIA AL DOCUMENTO DE 07-03]
- documentos a revisar: casos de uso, flujos de pantalla, credenciales de prueba
- objetivo puntual de salida: scripts E2E ejecutables que cubran los flujos críticos del plan
- nivel de profundidad: alto
```

---

## Salida esperada

Scripts E2E en la estructura del proyecto, por ejemplo:

```
e2e/[flujo].spec.[ext]
cypress/e2e/[flujo].cy.[ext]
tests/e2e/test_[flujo].[ext]
```

Con estructura interna:

```
[suite del flujo de usuario]
  setup: [login, estado inicial]
  ✓ [flujo principal completo con aserciones por paso]
  ✓ [flujo alternativo o de error]
  ✓ [regresión relacionada]
  teardown: [limpieza de estado si aplica]
```
