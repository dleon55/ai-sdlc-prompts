# Reglas de Negocio
## AI-SDLC Pro — Especificación Formal de Reglas

---

**Fecha:** 2026-04-12  
**Versión:** 1.0  
**Estándar:** RUP Business Modeling / PSP Process Definition  
**Clasificación:** Por dominio (Framework, Monetización, Técnica, Calidad)

---

## Tabla de Contenidos

1. [Reglas del Framework AI-SDLC](#1-reglas-del-framework-ai-sdlc)
2. [Reglas de Monetización](#2-reglas-de-monetización)
3. [Reglas Técnicas de Arquitectura](#3-reglas-técnicas-de-arquitectura)
4. [Reglas de Contribución y Calidad](#4-reglas-de-contribución-y-calidad)
5. [Reglas de Internacionalización](#5-reglas-de-internacionalización)
6. [Reglas de Persistencia de Datos](#6-reglas-de-persistencia-de-datos)
7. [Matriz de Cumplimiento](#7-matriz-de-cumplimiento)

---

## 1. Reglas del Framework AI-SDLC

### 1.1 Reglas Operativas Mandatorias

| ID | Nombre | Descripción | Severidad | Fuente |
|----|--------|-------------|-----------|--------|
| **FR-01** | Prepend Obligatorio | Todo prompt copiado DEBE incluir el bloque del framework `00-framework.md` antepuesto automáticamente | 🔴 Crítica | `00-framework.md` L1-37 |
| **FR-02** | Rol Multi-Agente | El framework define explícitamente el rol compuesto: Ingeniero de Software + Arquitecto + DBA + QA + DevSecOps | 🔴 Crítica | `00-framework.md` L14 |
| **FR-03** | 10 Mandamientos | Las 10 reglas obligatorias (L18-36) son innegociables y deben preceder todo trabajo | 🔴 Crítica | `00-framework.md` L18-36 |
| **FR-04** | Ciclo Forzado | Secuencia obligatoria: analiza → diseña → ejecuta → valida → documenta | 🔴 Crítica | Regla #9 |
| **FR-05** | Entregable Estructurado | Todo output debe distinguir: hechos confirmados, hallazgos, supuestos, riesgos, recomendaciones | 🟡 Alta | Regla #7 |
| **FR-06** | No Assumptions | "No asumas que el estado del repositorio es estático" — validación obligatoria pre-cambio | 🟡 Alta | Regla #2 |
| **FR-07** | Commits Atómicos | Todo trabajo debe ser controlado, trazable y con commits atómicos | 🟡 Alta | Regla #4 |
| **FR-08** | Análisis Previa | "No implementes primero y pienses después" — primero analiza, luego diseña | 🟡 Alta | Regla #9 |

### 1.2 Derivación de Reglas

```
FR-01 (Prepend Obligatorio)
  └── Implica: Tecnología JS copyPrompt() debe concatenar framework
  └── Implica: QA gate debe verificar que framework no esté "contaminado"
  └── Conflicta con: Ninguno — es regla fundacional

FR-04 (Ciclo Forzado)
  └── Implica: Prompts organizados secuencialmente (01 → 02 → ... → 12)
  └── Implica: No saltar fases (ej: no implementar sin diseño)
  └── Métrica: % de prompts usados en orden correcto
```

---

## 2. Reglas de Monetización

### 2.1 Modelo de Tiers

| ID | Nombre | Descripción | Severidad |
|----|--------|-------------|-----------|
| **MR-01** | Tier Free | 10 prompts básicos (análisis, diseño, implementación) sin costo | 🔴 Crítica |
| **MR-02** | Tier Pro Individual | $299 MXN/mes — acceso completo 44+ prompts, 00-B, 00-C, variables avanzadas | 🔴 Crítica |
| **MR-03** | Tier Pro Equipo | $799 MXN/mes — hasta 5 devs, proyectos compartidos, sync básico | 🟡 Alta |
| **MR-04** | Pack Único Gumroad | $499 MXN — compra única, versión del día, sin suscripción | 🟢 Media |
| **MR-05** | Enterprise | $5,000-15,000 MXN/mes — SSO, prompts privados, soporte prioritario | 🟢 Media |

### 2.2 Reglas de Gate de Conversión

| ID | Nombre | Condición | Acción |
|----|--------|-----------|--------|
| **MR-06** | Gate Framework Avanzado | Prompts 00-B (scaffolding) y 00-C (gobernanza) son PRO | Mostrar badge "🔒 Pro", botón "Upgrade para desbloquear" |
| **MR-07** | Gate Cantidad | Límite de 10 copias/mes en tier Free | Banner "Límite alcanzado — Upgrade a Pro" |
| **MR-08** | Gate Variables Avanzadas | Variables 7-12 requieren tier Pro | Input disabled con tooltip "Disponible en Pro" |

### 2.3 Reglas de Precios

| ID | Regla | Justificación |
|----|-------|---------------|
| **MR-09** | Precios en MXN | Mercado objetivo principal México/LATAM |
| **MR-10** | Sin descuentos automáticos | Valor percibido se mantiene, descuentos manuales por ventas |
| **MR-11** | Trial implícito | Tier Free actúa como trial ilimitado en tiempo, limitado en funcionalidad |

---

## 3. Reglas Técnicas de Arquitectura

### 3.1 Arquitectura de Generación

| ID | Nombre | Especificación | Severidad |
|----|--------|----------------|-----------|
| **TR-01** | Generador Estático | `build.py` debe producir único archivo `index.html` sin dependencias SSR | 🔴 Crítica |
| **TR-02** | Single Artifact | Output: un solo HTML (~255KB-1MB) conteniendo todo CSS, JS, contenido | 🔴 Crítica |
| **TR-03** | Zero CDN | Sin dependencias externas (fuentes, librerías, imágenes deben ser inline/data-uri) | 🟡 Alta |
| **TR-04** | GitHub Pages Compatible | No usar funcionalidades server-side (PHP, Node, etc.) | 🔴 Crítica |

### 3.2 Reglas de Datos y Estado

| ID | Nombre | Especificación |
|----|--------|----------------|
| **TR-05** | localStorage Only | Persistencia exclusiva en browser, sin backend database | 🔴 Crítica |
| **TR-06** | Schema Versionado | Claves `AI_SDLC_v1_*` permiten migraciones futuras | 🟡 Alta |
| **TR-07** | Límite LocalStorage | Asumir máximo 5MB disponible, comprimir datos si es necesario | 🟢 Media |

### 3.3 Reglas de Calidad y CI/CD

| ID | Nombre | Especificación |
|----|--------|----------------|
| **TR-08** | QA Gate Obligatorio | `verify_clean.py` debe reportar "0 prompts contaminados" antes de deploy | 🔴 Crítica |
| **TR-09** | Build Determinístico | Mismo input → mismo output (no timestamps en HTML) | 🟡 Alta |
| **TR-10** | Dual Deploy | Cada push a `main` despliega automáticamente a GitHub Pages y GCP | 🟡 Alta |

---

## 4. Reglas de Contribución y Calidad

### 4.1 Convenciones de Código

| ID | Nombre | Especificación | Penalización |
|----|--------|----------------|--------------|
| **CR-01** | Nomenclatura Archivos | `{sec}-{sub}-{nombre}.md` kebab-case, ceros a la izquierda | Build falla |
| **CR-02** | Variables Format | `{{NOMBRE_VARIABLE}}` MAYÚSCULAS con guiones bajos | QA gate falla |
| **CR-03** | Bloque Prompt | Contenido siempre dentro de ` ```text ``` ` | QA gate falla |
| **CR-04** | No Contaminación | Texto "Usa el prompt" NO debe aparecer dentro de bloques de código | QA gate falla |
| **CR-05** | Encoding UTF-8 LF | Sin BOM, saltos de línea Unix (\n) | Build warning |

### 4.2 Reglas de Commit (Conventional Commits)

| ID | Tipo | Cuándo Usar | Ejemplo |
|----|------|-------------|---------|
| **CC-01** | `feat(prompts)` | Nuevo prompt o grupo | `feat(prompts): agregar 04-05 patrones diseño` |
| **CC-02** | `fix(prompts)` | Corrección contenido prompt | `fix(prompts): corregir variable en 02-01` |
| **CC-03** | `fix(ux)` | Corrección interfaz de usuario | `fix(ux): scroll horizontal en mobile` |
| **CC-04** | `refactor` | Cambio build.py sin cambio comportamiento | `refactor: optimizar parseo markdown` |
| **CC-05** | `docs` | README, CHANGELOG, memoria técnica | `docs: agregar MT-003 despliegue` |

---

## 5. Reglas de Internacionalización (i18n)

### 5.1 Reglas de Idioma

| ID | Nombre | Especificación |
|----|--------|----------------|
| **IR-01** | Idioma Default | Español (`es`) es el idioma por defecto sin configuración previa | 🔴 Crítica |
| **IR-02** | Soporte Inglés | Inglés (`en`) debe estar disponible como alternativa | 🟡 Alta |
| **IR-03** | Detección Navegador | `navigator.language` determina idioma inicial si no hay preferencia | 🟡 Alta |
| **IR-04** | Persistencia Preferencia | `localStorage.AI_SDLC_language` almacena selección | 🟡 Alta |
| **IR-05** | Paridad Contenido | Todo prompt ES debe tener correspondiente EN (o fallback ES) | 🟡 Alta |

### 5.2 Reglas de UX Multi-idioma

| ID | Nombre | Especificación |
|----|--------|----------------|
| **IR-06** | Selector Visible | Botón de idioma visible en header siempre | 🟡 Alta |
| **IR-07** | Cambio Instantáneo | Switch de idioma debe completarse en < 300ms | 🟡 Alta |
| **IR-08** | SEO Hreflang | Meta tags `hreflang="es"` y `hreflang="en"` presentes | 🟢 Media |

---

## 6. Reglas de Persistencia de Datos

### 6.1 Schema de localStorage

| Clave | Tipo | Descripción | TTL |
|-------|------|-------------|-----|
| `AI_SDLC_language` | String | Idioma preferido ('es' o 'en') | Indefinido |
| `AI_SDLC_v1_projects` | JSON | Array de proyectos con sus variables | Indefinido |
| `AI_SDLC_sidebar` | String | '1' si colapsado | Indefinido |
| `AI_SDLC_fw_expanded` | String | '1' si framework expandido | Indefinido |
| `AI_SDLC_onboarding_done` | String | '1' si usuario completó onboarding | Indefinido |
| `AI_SDLC_email_collected` | String | Email capturado en onboarding | Indefinido |

### 6.2 Reglas de Variables de Proyecto

| ID | Variable | Tipo | Ejemplo | Requerida |
|----|----------|------|---------|-----------|
| **V-01** | `repositorio` | String | "urgemy-api" | Sí |
| **V-02** | `issue` | String | "#842" | No |
| **V-03** | `rama_actual` | String | "feature/payments" | No |
| **V-04** | `rama_destino` | String | "develop" | No |
| **V-05** | `ambiente` | Enum | "DEV/QA/PROD" | Sí |
| **V-06** | `componentes` | String[] | ["api", "postgres"] | No |
| **V-07** | `modulo` | String | "notificaciones" | No |
| **V-08** | `stack` | String | "Node.js, React, PostgreSQL" | No |
| **V-09** | `tipo_proyecto` | Enum | "Web/API/Mobile" | No |
| **V-10** | `metodologia` | Enum | "SCRUM/Kanban/Waterfall" | No |
| **V-11** | `agentes_ia` | String[] | ["Copilot", "Claude"] | No |
| **V-12** | `nivel_autonomia` | Enum | "alto/medio/bajo" | No |

---

## 7. Matriz de Cumplimiento

### 7.1 Métricas de Adherencia

| Dominio | Total Reglas | Críticas | Implementadas | Pendientes |
|---------|-------------|----------|---------------|------------|
| **Framework** | 8 | 4 | 8 | 0 |
| **Monetización** | 11 | 2 | 3 | 8 |
| **Técnica** | 10 | 4 | 9 | 1 (i18n prompts) |
| **Contribución** | 9 | 4 | 9 | 0 |
| **i18n** | 8 | 1 | 5 | 3 |
| **Persistencia** | 18 | 2 | 18 | 0 |
| **TOTAL** | **64** | **17** | **52** | **12** |

### 7.2 Definición de Hechos de Cumplimiento

| Estado | Definición PSP |
|--------|---------------|
| **Implementada** | Código existe, pasa QA gate, documentado |
| **Pendiente** | Especificada, no implementada o parcial |
| **Validada** | En producción, métricas confirman uso |

---

## 8. Glosario de Términos de Negocio

| Término | Definición en Contexto |
|---------|------------------------|
| **Prompt** | Instrucción estructurada que guía comportamiento de IA |
| **Framework** | Bloque de contexto obligatorio con reglas de ingeniería |
| **Contaminación** | Texto no deseado ("Usa el prompt") dentro de bloques de código |
| **Scaffolding** | Configuración inicial de repositorio (00-B) |
| **Gobernanza** | Reglas de coordinación multi-agente (00-C) |
| **Gate** | Punto de conversión que requiere upgrade de tier |
| **Auto-prepend** | Concatenación automática de framework al copiar |

---

## 9. Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-04-12 | Asistente IA | Documento inicial, 64 reglas identificadas |

---

**Trázabilidad PSP:**
- **Time Tracking:** 4 horas estimadas (documentación + revisión)
- **Defectos Inyectados:** 0
- **Defectos Removidos:** 0
- **Reusabilidad:** Plantilla aplicable a otros proyectos LionSystems

