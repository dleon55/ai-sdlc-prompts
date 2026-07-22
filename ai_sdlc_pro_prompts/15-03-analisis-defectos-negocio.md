# 15.3 — Reporte y análisis de defectos con impacto en negocio

## Descripción

Prompt para testers manuales y analistas funcionales. Ayuda a estructurar reportes de bugs profesionales, traduciendo errores técnicos (mensajes de consola, respuestas HTTP fallidas) a consecuencias de negocio e impacto en el usuario, facilitando la priorización del equipo de desarrollo.

**Cuándo usarlo:** al reportar un fallo en el backlog de incidentes, asegurando que contenga toda la información necesaria para el desarrollador.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | bajo — redacta un reporte de bug, no ejecuta cambios ni acciones sobre el sistema |
| Entradas requeridas | descripción del error observado, pasos realizados, comportamiento esperado, evidencia técnica si existe (log, código HTTP, captura) |
| Herramientas permitidas | ninguna de ejecución — redacción de texto a partir de la evidencia proporcionada |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si la severidad técnica y la prioridad de negocio no pueden justificarse con la evidencia dada, declararlo en vez de asumir un nivel de impacto |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | pasos de reproducción concretos y comportamiento actual vs. esperado, ambos verificables por el desarrollador que reciba el reporte |
| Siguiente prompt recomendado | `03-01-incidentes-github` para comparar el defecto contra issues ya existentes antes de crearlo |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como un QA Defect Analyst. Ayuda al tester a documentar y analizar un defecto, traduciendo los síntomas visuales y posibles errores técnicos a impactos de negocio claros e instrucciones de reproducción precisas para desarrollo.

Entradas:
- descripción del error observado: [DESCRIPCION DEL ERROR]
- pasos que estabas realizando: [PASOS REALIZADOS]
- comportamiento esperado: [COMPORTAMIENTO ESPERADO]
- error técnico (pantallazo, log de consola o código HTTP si hay): [PEGAR SI APLICA]

Actividades:
1. Analiza el comportamiento anómalo reportado e identifica qué regla de negocio o flujo de usuario está fallando.
2. Traduce cualquier log o código de error técnico provisto a un lenguaje funcional comprensible (ej: "Error 500 al guardar" -> "Fallo crítico en persistencia al guardar datos de cliente").
3. Estructura el reporte de bug bajo las mejores prácticas de la industria:
   - título del defecto (claro e informativo),
   - severidad técnica vs prioridad de negocio,
   - pasos precisos de reproducción (repro steps),
   - comportamiento actual vs esperado,
   - datos de prueba usados,
   - impacto en el negocio (ej: impide que el usuario pague, degrada la experiencia visual, rompe la accesibilidad).

Restricciones:
- no asignes una severidad técnica ni una prioridad de negocio si la evidencia proporcionada no la sustenta; en ese caso decláralo como "impacto no determinado" en vez de estimarlo a partir de la intuición,
- distingue explícitamente entre impacto confirmado (observado y reproducible con los pasos dados) e impacto sospechado (inferido del síntoma pero no verificado) — no los presentes con el mismo nivel de certeza,
- el diagnóstico técnico es una traducción funcional de la evidencia disponible (logs, código HTTP, capturas); si esa evidencia no indica la causa raíz, dilo explícitamente en vez de inventar una explicación técnica plausible,
- este prompt solo documenta y analiza el defecto — no propongas ni apliques una corrección de código, y no ejecutes los pasos de reproducción sobre ningún ambiente real.

Salida:
Genera una ficha de reporte de defecto estructurada con los siguientes apartados:
1. Título del Defecto
2. Severidad (Bloqueante / Crítico / Mayor / Menor) e Impacto en Negocio
3. Pasos de Reproducción
4. Comportamiento Actual vs Esperado
5. Datos y Entorno de Prueba
6. Diagnóstico Técnico para Desarrolladores (traducción funcional de logs)
```

---

## Uso con fórmula estándar

```text
Usa el prompt de análisis de defectos y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [LOG O DESCRIPCIÓN DEL INCIDENTE]
- rama: main
- ambiente: QA
- componentes: pasarela de pagos
- documentos a revisar: políticas de pago, captura de pantalla de consola
- objetivo puntual de salida: reporte de bug estructurado con impacto de negocio
- nivel de profundidad: alto
```

---

## Salida esperada

Una ficha organizada lista para copiar en Jira o GitHub Issues:

### 1. Título del Defecto
`[ERROR] El botón de finalizar compra se queda colgado y no envía la orden`

### 2. Severidad e Impacto en Negocio
*   **Severidad:** Bloqueante (Blocker).
*   **Impacto:** El cliente no puede completar compras. Afecta directamente la conversión de ventas y detiene el flujo operativo de facturación.

### 3. Pasos de Reproducción
1. Agregar cualquier producto al carrito de compras.
2. Ir a la pantalla de checkout.
3. Rellenar campos de envío válidos.
4. Presionar el botón "Finalizar compra".

### 4. Comportamiento Actual vs Esperado
*   **Comportamiento Actual:** El botón muestra un spinner infinito, se observa un error `POST /api/orders 500` en consola y no avanza a la confirmación.
*   **Comportamiento Esperado:** La orden debe procesarse, redirigir a la pantalla de agradecimiento y limpiar el carrito.

### 5. Datos y Entorno de Prueba
*   **Entorno:** QA (https://qa.prompts.lionsystems.com.mx/)
*   **Navegador:** Chrome v120 / Windows 11
*   **Datos:** Cuenta de usuario de prueba `test_buyer@lionsystems.com`

### 6. Diagnóstico Técnico para Desarrolladores
*   **Origen:** El servidor retorna `HTTP 500 (Internal Server Error)` al llamar al endpoint de creación de orden. La evidencia disponible (código HTTP y captura de consola) no incluye el log del servidor ni el stack trace, por lo que **la causa raíz no puede determinarse con esta evidencia — impacto no determinado en el origen técnico**. Se requiere el log del servidor (request id, timestamp) para diagnosticar la causa exacta.
