# 7.5 — Automatización en navegador con Google Antigravity

## Descripción

Prompt para diseñar y documentar una estrategia de pruebas automatizadas en navegador usando Google Antigravity: escenarios, navegación, selectors, datos de prueba, validaciones visuales y puntos frágiles del flujo.

**Cuándo usarlo:** para automatizar pruebas E2E o de regresión de flujos críticos impactados por el cambio. Usa este prompt en lugar de `07-03`+`07-09` cuando la automatización se ejecutará mediante el agente de navegador de Google Antigravity (verificación autónoma con capturas/video) en vez de un framework de scripting E2E tradicional.

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
