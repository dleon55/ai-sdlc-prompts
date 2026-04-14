# Plan de Implementación Integral - Remediación AI-SDLC Pro

Este plan detalla la solución a los hallazgos críticos detectados en el portal, estructurado para un entorno multi-agente y con un enfoque de ingeniería de alta calidad.

## 1. Resumen Ejecutivo
Se han validado tres hallazgos críticos: un `ReferenceError` que rompe el runtime de JS, una falla lógica en el copiado multi-select que impide el reemplazo de variables, y una restricción de CSP que bloquea el rastreo de analíticas. La solución propuesta restaura la funcionalidad bilingüe y de variables sin comprometer la seguridad.

## 2. Validación y Análisis por Hallazgo

### [H1] Crítico - ReferenceError: closeLanguageDropdown is not defined
*   **Validación:** Aplica. El código llama a la función en las líneas 1861 y 1879 de `build.py` pero no existe la definición.
*   **Causa Raíz:** Omisión durante el refactor bilingüe.
*   **Riesgo:** Inestabilidad global del frontend; los eventos posteriores al error pueden no dispararse.

### [H2] Crítico - Falla en Reemplazo de Variables (Multi-select)
*   **Validación:** Aplica. La función `copySelected` usa IDs obsoletos (`code-[pid]`) en lugar de los segmentados por idioma (`code-[pid]-[lang]`).
*   **Causa Raíz:** Falta de actualización de selectores en la lógica de multi-selección tras el cambio a i18n.
*   **Riesgo:** Degradación total del valor del producto (prompts inservibles con placeholders).

### [H3] Medio - Violación de CSP (ga-audiences)
*   **Validación:** Aplica. `nginx_prompts.conf` bloquea dominios de Google necesarios para la operación comercial definida.
*   **Causa Raíz:** Política de `img-src` excesivamente restrictiva.
*   **Riesgo:** Pérdida de datos de analítica y audiencias.

---

## 3. Diseño de Solución

| Hallazgo | Solución Propuesta | Impacto Técnico |
| :--- | :--- | :--- |
| **H1 (JS)** | Implementar `closeLanguageDropdown()` que remueva la clase `.open` del elemento `#lang-dropdown`. | Mínimo. Mejora la robustez visual. |
| **H2 (i18n)** | Modificar `copySelected` para usar `getCurrentLanguage()` y concatenar el sufijo `-es` o `-en` al buscar el elemento por ID. | Medio. Asegura que `applyVars` reciba el contenido correcto. |
| **H3 (CSP)** | Actualizar `nginx_prompts.conf` añadiendo `https://www.google.com.mx` a la directiva `img-src`. | Bajo. Mejora compatibilidad sin abrir brechas críticas. |

---

## 4. Estrategia de Calidad
1.  **Validación Cruzada:** Verificar que al cambiar de idioma, el copiado múltiple extraiga los prompts en el idioma activo.
2.  **Smoke Test (Console):** Abrir el inspector y confirmar que al presionar 'Escape' o hacer clic fuera del menú de idioma no se generan errores.
3.  **Test de Regresión:** Validar que el copiado individual sigue funcionando correctamente.

---

## 5. Plan de Implementación Controlado

| Paso | Cambio | Archivo | Riesgo | Validación |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Definir `closeLanguageDropdown()` | `build.py` | Bajo | Clic fuera del menú no lanza error. |
| 2 | Refactorizar `copySelected` (IDs dinámicos) | `build.py` | Medio | Copiar 2 prompts y verificar variables. |
| 3 | Actualizar cabeceras CSP | `nginx_prompts.conf` | Bajo | Desaparición de error CSP en consola. |
| 4 | Ejecutar build final | `build.py` | N/A | Generación de `index.html` v1.2.1. |

---

## 6. Riesgos y Mitigación
*   **Riesgo:** Conflicto de fusión con otro agente en `build.py`.
*   **Mitigación:** Usar `multi_replace_file_content` con bloques pequeños y específicos, validando el contenido antes de cada escritura.

---

## Recomendación Final
Proceder con la implementación inmediata del Paso 1 y 2 en `build.py` para restaurar la funcionalidad principal, seguido del ajuste de infraestructura en Nginx.

render_diffs(file:///c:/Users/dleon/OneDrive/Documentos/GitHub/www-lionsystems-odoo/WEB_PROMPTS/build.py)
render_diffs(file:///c:/Users/dleon/OneDrive/Documentos/GitHub/www-lionsystems-odoo/WEB_PROMPTS/nginx_prompts.conf)
