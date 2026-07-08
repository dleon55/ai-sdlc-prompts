# 7.5 — Automatización en navegador con Google Antigravity

## Descripción

Prompt para diseñar y documentar una estrategia de pruebas automatizadas en navegador usando Google Antigravity: escenarios, navegación, selectors, datos de prueba, validaciones visuales y puntos frágiles del flujo.

**Cuándo usarlo:** para automatizar pruebas E2E o de regresión de flujos críticos impactados por el cambio. Usa este prompt en lugar de `07-03`+`07-09` cuando la automatización se ejecutará mediante el agente de navegador de Google Antigravity (verificación autónoma con capturas/video) en vez de un framework de scripting E2E tradicional.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño/documentación — produce una estrategia de automatización en navegador, no la ejecuta directamente |
| Riesgo esperado | medio — aunque el prompt solo documenta la estrategia, esta se entrega tal cual al agente de navegador de Google Antigravity para ejecución autónoma contra QA/staging, sin una revisión de código intermedia como en `07-03`+`07-09` |
| Entradas requeridas | casos de uso o flujos críticos a automatizar, plan E2E previo si existe, diseño de UI, URL base del ambiente QA/STAGING |
| Herramientas permitidas | lectura de documentación y diseño de UI; no incluye acceso al navegador ni ejecución — la ejecución real ocurre fuera de este prompt, a cargo del agente de Google Antigravity |
| Autonomía permitida | A1 — Proponer (entrega la estrategia como artefacto; la ejecución autónoma por Google Antigravity es un paso externo posterior que requiere ambiente y credenciales de prueba ya autorizados) |
| Criterios de detención | detener si el ambiente de destino no es QA/STAGING (nunca automatizar directamente contra producción); detener si faltan selectors o datos de prueba estables, ya que produciría una automatización frágil |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada escenario debe listar navegación, selector clave, datos de prueba, validación esperada, evidencia (captura/video) y punto frágil identificado |
| Siguiente prompt recomendado | ninguno en la biblioteca — la estrategia se entrega directamente al agente de navegador de Google Antigravity para su ejecución autónoma (alternativa a `07-03`+`07-09`) |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña y documenta una estrategia de pruebas automatizadas en navegador usando Google Antigravity para validar los flujos impactados.

Incluye:
- escenario,
- navegación,
- selectors esperados,
- datos de prueba,
- validaciones visuales y funcionales,
- capturas o evidencia esperada,
- posibles puntos frágiles del flujo.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de automatización con Antigravity y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- flujos a automatizar: [FLUJOS CRÍTICOS A CUBRIR]
- ambiente: [QA / STAGING]
- URL base: [URL DEL AMBIENTE]
- documentos a revisar: casos de uso, plan E2E, diseño de UI
- objetivo puntual de salida: estrategia de automatización con pasos, selectors y validaciones
- nivel de profundidad: alto
```

---

## Salida esperada

| Escenario | Navegación | Selector clave | Datos de prueba | Validación | Evidencia | Punto frágil |
|---|---|---|---|---|---|---|
