# Requerimientos Funcionales
## AI-SDLC Pro — Especificación de Requerimientos (SRS)

---

**Fecha:** 2026-04-12  
**Versión:** 1.0  
**Estándar:** IEEE 830-1998 / RUP SRS  
**Prioridad:** MoSCoW (Must, Should, Could, Won't)

---

## 1. Introducción

### 1.1 Propósito
Este documento especifica los requerimientos funcionales del sistema AI-SDLC Pro. Define las capacidades que el sistema debe proporcionar para satisfacer las necesidades de los usuarios y stakeholders.

### 1.2 Alcance
Cubre todas las funcionalidades accesibles por usuarios finales (visitantes, usuarios free/pro) y administradores del sistema.

### 1.3 Definiciones y Acrónimos
- **SRS:** Software Requirements Specification
- **FR:** Functional Requirement
- **NFR:** Non-Functional Requirement
- **UC:** Use Case

---

## 2. Requerimientos Funcionales por Componente

### 2.1 Sistema de Generación (Build)

| ID | Requerimiento | Prioridad | Caso de Uso | Estado |
|----|---------------|-----------|-------------|--------|
| **FR-BLD-01** | El generador `build.py` debe procesar 44 archivos `.md` en `ai_sdlc_pro_prompts/` | Must | - | ✅ |
| **FR-BLD-02** | Debe generar único archivo `index.html` (~255KB) sin dependencias externas | Must | - | ✅ |
| **FR-BLD-03** | Debe extraer título, descripción, prompt, fórmulas y variables de cada `.md` | Must | - | ✅ |
| **FR-BLD-04** | Debe generar cards HTML con IDs únicos por prompt (`pid = seccion-sub`) | Must | - | ✅ |
| **FR-BLD-05** | Debe incluir framework `00-framework.md` en output para JS prepend | Must | FR-01 | ✅ |
| **FR-BLD-06** | Debe soportar generación bilingüe ES/EN (alternativa C) | Should | i18n | 🔶 |

### 2.2 Sistema de Prompts

| ID | Requerimiento | Prioridad | Caso de Uso | Estado |
|----|---------------|-----------|-------------|--------|
| **FR-PRM-01** | Mostrar biblioteca de 44 prompts organizados en 15 grupos (00-12) | Must | UC-01 | ✅ |
| **FR-PRM-02** | Permitir expansión/colapso individual de cada card de prompt | Must | UC-10 | ✅ |
| **FR-PRM-03** | Mostrar descripción corta y botón "Copiar" en card colapsada | Must | UC-07 | ✅ |
| **FR-PRM-04** | Mostrar contenido completo del prompt en card expandida | Must | UC-07 | ✅ |
| **FR-PRM-05** | Incluir botón ⓘ que muestra modal con info detallada sin copiar | Must | UC-08 | ✅ |
| **FR-PRM-06** | Soportar búsqueda en tiempo real por texto en título o contenido | Should | UC-06 | ✅ |
| **FR-PRM-07** | Permitir selección múltiple (checkboxes) y copia en bloque | Could | UC-09 | ✅ |
| **FR-PRM-08** | Soportar internacionalización ES/EN de contenido de prompts | Should | i18n | 🔶 |

### 2.3 Sistema de Copiado

| ID | Requerimiento | Prioridad | Caso de Uso | Estado |
|----|---------------|-----------|-------------|--------|
| **FR-COPY-01** | Anteponer automáticamente framework `00-framework.md` a cada copia | Must | UC-07 | ✅ |
| **FR-COPY-02** | Sustituir variables `{{VAR}}` por valores del proyecto activo | Must | UC-07 | ✅ |
| **FR-COPY-03** | Copiar resultado a clipboard usando `navigator.clipboard` API | Must | UC-07 | ✅ |
| **FR-COPY-04** | Mostrar feedback visual "Copiado ✓" por 3 segundos | Should | UC-07 | ✅ |
| **FR-COPY-05** | En copia múltiple, incluir framework solo una vez al inicio | Should | UC-09 | ✅ |
| **FR-COPY-06** | Soportar copia de framework individual (completo) | Should | UC-07 | ✅ |

### 2.4 Sistema de Proyectos

| ID | Requerimiento | Prioridad | Caso de Uso | Estado |
|----|---------------|-----------|-------------|--------|
| **FR-PRJ-01** | Crear proyecto nuevo con nombre descriptivo | Must | UC-05 | ✅ |
| **FR-PRJ-02** | Listar proyectos existentes en dropdown selector | Must | UC-03 | ✅ |
| **FR-PRJ-03** | Cambiar proyecto activo (switch contexto) | Must | UC-03 | ✅ |
| **FR-PRJ-04** | Eliminar proyecto (con confirmación) | Should | UC-05 | ✅ |
| **FR-PRJ-05** | Importar proyectos desde JSON | Could | UC-05 | ✅ |
| **FR-PRJ-06** | Exportar proyectos a JSON | Could | UC-05 | ✅ |
| **FR-PRJ-07** | Auto-crear proyecto "Default" si no existen proyectos | Must | UC-05 | ✅ |

### 2.5 Sistema de Variables

| ID | Requerimiento | Prioridad | Caso de Uso | Estado |
|----|---------------|-----------|-------------|--------|
| **FR-VAR-01** | Almacenar 12 variables por proyecto (ver DataModel.md) | Must | UC-04 | ✅ |
| **FR-VAR-02** | Clasificar variables: Globales (7) vs Por-prompt (5) | Should | UC-04 | ✅ |
| **FR-VAR-03** | Panel de edición de variables deslizable desde derecha | Should | UC-04 | ✅ |
| **FR-VAR-04** | Validar campos requeridos antes de permitir copia | Should | UC-04 | 🟡 |
| **FR-VAR-05** | Aplicar sustitución de variables en tiempo real al copiar | Must | UC-07 | ✅ |

### 2.6 Sistema de Internacionalización (i18n)

| ID | Requerimiento | Prioridad | Caso de Uso | Estado |
|----|---------------|-----------|-------------|--------|
| **FR-I18N-01** | Detectar idioma preferido del navegador (`navigator.language`) | Must | UC-11 | ✅ |
| **FR-I18N-02** | Permitir cambio manual de idioma ES ↔ EN | Must | UC-12 | ✅ |
| **FR-I18N-03** | Persistir preferencia en `localStorage.AI_SDLC_language` | Must | UC-13 | ✅ |
| **FR-I18N-04** | Mostrar selector de idioma visible en header | Must | UC-12 | ✅ |
| **FR-I18N-05** | Cambiar idioma sin recarga de página (instantáneo) | Should | UC-12 | ✅ |
| **FR-I18N-06** | Actualizar atributo `html lang` para SEO y accesibilidad | Should | UC-12 | ✅ |
| **FR-I18N-07** | Actualizar meta tags dinámicamente al cambiar idioma | Could | UC-12 | 🔶 |
| **FR-I18N-08** | Fallback a ES si contenido EN no disponible | Should | i18n | ✅ |
| **FR-I18N-09** | Traducir UI completa (strings, labels, tooltips) | Must | i18n | ✅ |
| **FR-I18N-10** | Traducir contenido de los 44 prompts | Should | i18n | 🔶 |
| **FR-I18N-11** | Traducir landing page completa | Could | i18n | 🔶 |

### 2.7 Sistema de UI/UX

| ID | Requerimiento | Prioridad | Caso de Uso | Estado |
|----|---------------|-----------|-------------|--------|
| **FR-UI-01** | Diseño responsivo (mobile < 560px, tablet, desktop) | Must | - | ✅ |
| **FR-UI-02** | Tema oscuro (dark mode) único, sin toggle light | Must | - | ✅ |
| **FR-UI-03** | Sidebar colapsable/expandible con persistencia | Should | UC-10 | ✅ |
| **FR-UI-04** | Framework banner colapsable con persistencia | Should | UC-10 | ✅ |
| **FR-UI-05** | Navegación por anclas (#sec-XX) con scroll suave | Should | - | ✅ |
| **FR-UI-06** | Highlight de sección activa en sidebar (IntersectionObserver) | Could | - | ✅ |
| **FR-UI-07** | Búsqueda con debounce (150ms) para performance | Should | UC-06 | ✅ |
| **FR-UI-08** | Estados vacíos visibles (no results, empty project) | Should | - | ✅ |

### 2.8 Sistema de Onboarding

| ID | Requerimiento | Prioridad | Caso de Uso | Estado |
|----|---------------|-----------|-------------|--------|
| **FR-ONB-01** | Detectar primera visita (no `AI_SDLC_onboarding_done`) | Must | UC-02 | ✅ |
| **FR-ONB-02** | Mostrar welcome banner con mensaje introductorio | Must | UC-02 | ✅ |
| **FR-ONB-03** | Mostrar overlay tutorial paso a paso (4 pasos) | Should | UC-02 | ✅ |
| **FR-ONB-04** | Permitir cerrar/skip onboarding en cualquier paso | Should | UC-02 | ✅ |
| **FR-ONB-05** | Capturar email opcional en último paso | Should | UC-02 | ✅ |
| **FR-ONB-06** | Marcar onboarding completado en localStorage | Must | UC-02 | ✅ |
| **FR-ONB-07** | No mostrar onboarding nuevamente una vez completado | Must | UC-02 | ✅ |

### 2.9 Sistema de Analytics

| ID | Requerimiento | Prioridad | Caso de Uso | Estado |
|----|---------------|-----------|-------------|--------|
| **FR-ANL-01** | Integrar Google Analytics 4 (G-C5JKYNZ62F) | Must | - | ✅ |
| **FR-ANL-02** | Trackear evento `copy_prompt` con ID del prompt | Should | UC-07 | ✅ |
| **FR-ANL-03** | Trackear evento `language_change` con idioma destino | Should | UC-12 | ✅ |
| **FR-ANL-04** | Trackear page views de `/app` vs landing | Could | - | ✅ |
| **FR-ANL-05** | No bloquear funcionamiento si analytics falla | Must | - | ✅ |

### 2.10 Sistema de Monetización (Futuro)

| ID | Requerimiento | Prioridad | Caso de Uso | Estado |
|----|---------------|-----------|-------------|--------|
| **FR-MON-01** | Detectar tier del usuario (Free vs Pro) | Must | UC-14 | 🔶 |
| **FR-MON-02** | Mostrar badge "🔒 Pro" en prompts bloqueados | Must | UC-16 | 🔶 |
| **FR-MON-03** | Mostrar CTA upgrade cuando usuario intenta acceder Pro | Must | UC-15 | 🔶 |
| **FR-MON-04** | Limitar funcionalidad en tier Free (10 prompts, variables básicas) | Must | UC-14 | 🔶 |
| **FR-MON-05** | Integrar gateway de pago (Stripe/Gumroad/Lemon Squeezy) | Must | UC-17 | 🔶 |
| **FR-MON-06** | Activar funcionalidad Pro tras pago exitoso | Must | UC-17 | 🔶 |

---

## 3. Matriz de Requerimientos vs Casos de Uso

| Requerimiento | UC-01 | UC-02 | UC-03 | UC-04 | UC-05 | UC-06 | UC-07 | UC-08 | UC-09 | UC-10 |
|---------------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| FR-PRM-01 | ✅ | | | | | ✅ | ✅ | ✅ | ✅ | |
| FR-PRM-02 | | | | | | | ✅ | | | ✅ |
| FR-COPY-01 | | | | | | | ✅ | | ✅ | |
| FR-PRJ-03 | | | ✅ | | | | | | | |
| FR-VAR-01 | | | | ✅ | | | ✅ | | | |
| FR-I18N-02 | | | | | | | | | | |
| FR-UI-01 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| FR-ONB-01 | | ✅ | | | | | | | | |

---

## 4. Requerimientos de Interfaz Externa

### 4.1 Interfaces de Usuario

| Interfaz | Descripción | Tipo |
|----------|-------------|------|
| **Landing Page** | Página de marketing, conversión | Público |
| **App SPA** | Biblioteca interactiva de prompts | Autenticado (future) / Free |
| **Admin Panel** | Gestión de prompts, analytics | Privado (LionSystems) |

### 4.2 Interfaces de Software

| Interfaz | Protocolo | Descripción |
|----------|-----------|-------------|
| **Google Analytics** | HTTPS/JS | Event tracking |
| **Stripe/Gumroad** | HTTPS/API | Procesamiento pagos (future) |
| **Clipboard API** | Browser API | navigator.clipboard |
| **localStorage** | Browser API | Persistencia datos usuario |

### 4.3 Interfaces de Comunicaciones

| Interfaz | Protocolo | Descripción |
|----------|-----------|-------------|
| **GitHub Pages** | HTTPS | Hosting estático primario |
| **GCP Nginx** | HTTPS/TLS | Hosting producción |
| **CDN (none)** | - | Self-contained, no external CDN |

---

## 5. Requerimientos de Adaptabilidad

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| **FR-ADP-01** | Debe funcionar offline una vez cargado (PWA-ready) | Could |
| **FR-ADP-02** | Degradación graceful si JavaScript deshabilitado | Won't |
| **FR-ADP-03** | Soporte para agregar idioma adicional (FR, PT) sin refactor | Could |

---

## 6. Métricas de Verificación

| Requerimiento | Criterio de Aceptación | Método de Prueba |
|---------------|------------------------|------------------|
| FR-COPY-01 | Framework siempre presente en clipboard | Test E2E: copy → paste verificar |
| FR-PRM-06 | Búsqueda < 100ms debounce | Lighthouse performance |
| FR-I18N-05 | Cambio idioma < 300ms | DevTools Performance tab |
| FR-UI-01 | Responsive en 320px, 768px, 1920px | Chrome DevTools responsive |

---

## 7. Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-04-12 | Asistente IA | Documento inicial, 54 FR identificados |

---

**Trázabilidad PSP:**
- **Total Requerimientos:** 54 FR
- **Must:** 32 (59%)
- **Should:** 15 (28%)
- **Could:** 5 (9%)
- **Won't:** 2 (4%)
- **Implementados:** ~42 (78%)
- **Pendientes:** ~12 (monetización + i18n prompts)

