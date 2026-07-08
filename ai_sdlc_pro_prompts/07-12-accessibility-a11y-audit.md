# 7.12 — Auditoría de Accesibilidad (a11y) y UX Compliance

## Descripción

Prompt orientado a perfiles de QA Automation o Frontend Architect. Examina el código HTML, React, Vue o plantillas UI para verificar el cumplimiento de los estándares WCAG 2.2. Detecta problemas de contraste, navegabilidad por teclado, atributos ARIA faltantes y estructura semántica.

**Cuándo usarlo:** Antes de fusionar un Pull Request que introduce o modifica componentes visuales del Frontend, o al auditar un sistema existente para cumplir normativas de accesibilidad.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | validación |
| Riesgo esperado | medio — no aplica cambios directamente, pero un veredicto de cumplimiento incorrecto puede dejar pasar barreras de accesibilidad a producción |
| Entradas requeridas | código fuente del componente o vista (`codigo_frontend`) y el framework UI usado (`framework_ui`) |
| Herramientas permitidas | lectura del fragmento de código proporcionado — sin acceso a otros archivos del repositorio, sin ejecutar el componente ni herramientas automatizadas de a11y (axe, Lighthouse) |
| Autonomía permitida | A1 — Proponer (entrega informe y código corregido como propuesta; no aplica el cambio directamente al repositorio) |
| Criterios de detención | si el fragmento de código no incluye suficiente contexto para evaluar un criterio (p. ej. contraste de color definido en una hoja de estilos externa no provista, o comportamiento dinámico no visible en el snippet), documentarlo como limitación de evidencia en vez de asumir cumplimiento o incumplimiento |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada violación reportada debe citar el elemento o línea del código y el criterio WCAG 2.2 específico incumplido |
| Siguiente prompt recomendado | `08-01-revision-estatica` para incluir el código corregido en la revisión estática previa al merge |

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

Restricciones:
- cita el criterio de éxito WCAG 2.2 específico (p. ej. 2.1.1, 4.1.2) que respalda cada violación reportada, nunca una referencia genérica al estándar,
- no declares que un criterio "cumple" o "no cumple" si el fragmento de código no incluye evidencia suficiente (p. ej. contraste definido en una hoja de estilos externa no provista) — documenta la limitación en vez de asumir,
- distingue explícitamente los hallazgos verificables de forma automática (contraste calculable, atributos ausentes, estructura semántica) de aquellos que requieren verificación manual con tecnología de asistencia real (lector de pantalla, navegación solo con teclado) — no sustituyas esa verificación manual con tu propio análisis estático,
- no ejecutes el componente ni simules su comportamiento dinámico; si el comportamiento depende de JavaScript no visible en el snippet, señálalo como limitación de evidencia en el informe.

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

### Ejemplo de hallazgo

| Elemento | Criterio WCAG 2.2 | Severidad | Descripción | Corrección |
|---|---|---|---|---|
| `<div onClick={handleSubmit}>Enviar</div>` (línea 42) | 2.1.1 Keyboard | Crítica | El control no es alcanzable ni operable por teclado y no expone el rol semántico de botón a lectores de pantalla | Reemplazar por `<button type="button" onClick={handleSubmit}>Enviar</button>` |
| `<img src="banner-promo.png">` sin atributo `alt` (línea 10) | 1.1.1 Non-text Content | Alta | El lector de pantalla no puede describir una imagen informativa, dejando al usuario sin contexto | Agregar `alt="Descripción del contenido del banner"`, o `alt=""` si la imagen es puramente decorativa |
