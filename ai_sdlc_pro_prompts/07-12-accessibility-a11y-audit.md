# 7.12 — Auditoría de Accesibilidad (a11y) y UX Compliance

## Descripción

Prompt orientado a perfiles de QA Automation o Frontend Architect. Examina el código HTML, React, Vue o plantillas UI para verificar el cumplimiento de los estándares WCAG 2.2. Detecta problemas de contraste, navegabilidad por teclado, atributos ARIA faltantes y estructura semántica.

**Cuándo usarlo:** Antes de fusionar un Pull Request que introduce o modifica componentes visuales del Frontend, o al auditar un sistema existente para cumplir normativas de accesibilidad.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como un Auditor de Accesibilidad Web (a11y) experto en normativas WCAG 2.2 (Niveles A y AA). Analiza el código fuente del componente o vista de interfaz proporcionado para identificar barreras de accesibilidad y recomendar correcciones exactas.

Entradas:
- framework_ui: [React / Vue / HTML / Angular]
- codigo_frontend: [PEGA AQUÍ EL CÓDIGO DEL COMPONENTE O PÁGINA]

Actividades de Análisis:
1. SEMÁNTICA HTML: Verifica el uso correcto de etiquetas (`<nav>`, `<main>`, `<article>`, `<button>` vs `<div>` con `onClick`).
2. NAVEGACIÓN POR TECLADO: Asegura que todos los elementos interactivos sean accesibles mediante `Tab` y tengan estados `:focus-visible` claros. No debe haber "trampas de teclado" (keyboard traps).
3. LECTORES DE PANTALLA (Screen Readers): Revisa la presencia y correcto uso de etiquetas `aria-*`, `alt` en imágenes informativas, e ignorar (`aria-hidden="true"`) imágenes decorativas.
4. FORMULARIOS: Valida que los `<input>` estén correctamente enlazados a sus `<label>` (id/for) y que los mensajes de error sean anunciados por lectores de pantalla (`aria-describedby`, `aria-live`).

Salida Obligatoria:
1. INFORME WCAG: Listado de violaciones detectadas categorizadas por Severidad (Crítica, Alta, Media).
2. CÓDIGO CORREGIDO: El mismo componente refactorizado con las etiquetas semánticas y atributos ARIA aplicados.
3. CHECKLIST DE QA: Pasos manuales que un QA tester debe realizar (e.g., "Navegar el componente usando solo la tecla Tab").
```

---

## Uso con fórmula estándar

```text
Usa el prompt de auditoría de accesibilidad y adáptalo a:
- framework_ui: [FRAMEWORK]
- codigo_frontend: [CÓDIGO]
- objetivo puntual de salida: encontrar errores WCAG 2.2 AA y obtener código refactorizado.
- nivel de profundidad: exhaustivo
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Informe WCAG | Violaciones agrupadas por severidad y su impacto en usuarios |
| Código Corregido | Frontend refactorizado listo para copy-paste |
| QA Checklist | Pasos de pruebas manuales de accesibilidad |
