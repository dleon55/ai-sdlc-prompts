# Análisis de Incidente y Causa Raíz (RCA) - Portal AI-SDLC Pro

**Fecha del reporte:** 2026-04-14
**Ingeniero Analista:** Antigravity (Senior Full-Stack & DevSecOps)

---

### 1. Síntoma Observado
1. **Falla Funcional:** Los prompts copiados mediante el modo de selección múltiple ("Multi-select") no están reemplazando las variables (ej: `[REPOSITORIO]`, `[REFERENCIA]`), pegando el texto original con placeholders.
2. **Error Crítico en Consola:** `Uncaught ReferenceError: closeLanguageDropdown is not defined` en `app:5787`.
3. **Violación de Seguridad (CSP):** El navegador bloquea la carga de un píxel de rastreo (`ga-audiences`) por violar la política de `img-src`.

---

### 2. Evidencia

#### **Logs de Navegador (Hechos Confirmados):**
* `app:5787 Uncaught ReferenceError: closeLanguageDropdown is not defined`
* `violates the following Content Security Policy directive: "img-src 'self' data: https://lionsystems.com.mx https://www.googletagmanager.com"`

#### **Código Fuente (`build.py`):**
* **Línea 1861/1879:** Se llama a `closeLanguageDropdown()` en el listener global de clic y en el listener de teclado (tecla Escape).
* **Línea 1639 (`copySelected`):**  `var el = document.getElementById('code-' + pid);`
  * **Hallazgo:** Tras la refactorización bilingüe, los IDs cambiaron a `code-[pid]-es` y `code-[pid]-en`. El selector actual devuelve `null`.

#### **Configuración (`nginx_prompts.conf`):**
* **Línea 22:** La directiva `img-src` no incluye `https://www.google.com.mx`, bloqueando los servicios de audiencias de Google.

---

### 3. Hipótesis
1. **Referencia Perdida:** Durante la integración de la navegación unificada, la función `closeLanguageDropdown` fue omitida por error o renombrada indebidamente, dejando llamadas huérfanas que detienen la ejecución de scripts.
2. **Desajuste de Selectores:** La lógica de selección múltiple no fue actualizada tras segmentar los prompts por idioma, lo que causa el fallo silencioso al no encontrar el elemento que contiene el texto para procesar `applyVars`.
3. **CSP Incompleto:** La configuración de Nginx es demasiado restrictiva para las dependencias externas de análisis/marketing empleadas en producción.

---

### 4. Causa Raíz Confirmada
1. **JS Runtime Break:** Inexistencia de la función `closeLanguageDropdown` en el scope global.
2. **Selector ID Obsoleto:** Hard-coding del prefijo `code-` en `copySelected` sin contemplar el sufijo de idioma (`-es` / `-en`).
3. **Misconfiguration de DNS/Domain en CSP:** Omisión de dominios asociados a Google Analytics/Ads.

---

### 5. Factores Contribuyentes
* **Alta Deuda Técnica en Refactor de UI:** La migración a bilingüe impactó múltiples selectores de IDs que no fueron auditados completamente en todas las funciones (especialmente en `Multi-select`).
* **Falta de Pruebas Automatizadas (E2E):** No se ejecutaron pruebas en modo multi-select tras el último cambio.
* **Entorno Multi-agente:** Posible conflicto/omisión durante una sustitución de bloques grandes de código.

---

### 6. Riesgo Asociado
* **Crítico:** La inutilidad funcional de la biblioteca (no reemplaza variables) degrada severamente la propuesta de valor del producto.
* **Reputacional:** Errores de consola visibles y advertencias de CSP dan imagen de inestabilidad técnica.

---

### 7. Recomendación de Remediación

1. **[FIX JS]** Implementar la función `closeLanguageDropdown()` faltante para limpiar el estado de la UI.
2. **[FIX LOGIC]** Actualizar `copySelected` para usar `getCurrentLanguage()` y construir el ID dinámicamente (`'code-' + pid + '-' + lang`).
3. **[HARDENING CSP]** Actualizar `nginx_prompts.conf` para incluir wildcards o dominios específicos de Google Ads/Analytics en `img-src`.

---
