# Documento de Visión del Proyecto
## AI-SDLC Pro — Biblioteca de Prompts de Ingeniería de Software

---

**Fecha:** 2026-04-12  
**Versión:** 1.2  
**Estado:** Aprobado  
**Autor:** LionSystems — dleon55  
**Estándar:** RUP / PSP v3.0

---

## 1. Introducción

### 1.1 Propósito del Documento
Este documento establece la visión estratégica, alcance y posicionamiento del producto **AI-SDLC Pro**. Define los objetivos de negocio, usuarios objetivo y diferenciadores competitivos que guiarán el desarrollo y evolución del sistema.

### 1.2 Alcance del Producto
AI-SDLC Pro es una biblioteca interactiva web de prompts estructurados para dirigir agentes de inteligencia artificial (GitHub Copilot, Claude, Cursor, Windsurf, Codex, Antigravity) a través del ciclo completo de ingeniería de software.

### 1.3 Definiciones y Acrónimos

| Término | Definición |
|---------|------------|
| **AI-SDLC** | Artificial Intelligence - Software Development Life Cycle |
| **Prompt** | Instrucción estructurada en lenguaje natural para dirigir comportamiento de IA |
| **Framework** | Bloque de contexto obligatorio que antecede a todo prompt |
| **SPA** | Single Page Application — aplicación de página única |
| **PSP** | Personal Software Process — metodología de desarrollo individual |
| **RUP** | Rational Unified Process — marco de proceso de software |

---

## 2. Posicionamiento del Producto

### 2.1 Oportunidad de Negocio

| Aspecto | Descripción |
|---------|-------------|
| **Problema** | Desarrolladores obtienen outputs inconsistentes de IA por falta de contexto estructurado y metodología SDLC |
| **Solución** | Biblioteca de 44 prompts profesionales con framework multi-agente obligatorio |
| **Mercado** | 26.9M desarrolladores globales, crecimiento IA-assisted coding al 35% anual |

### 2.2 Definición del Problema

| Elemento | Descripción |
|----------|-------------|
| **Quién** | Desarrolladores individuales, tech leads, CTOs, equipos de ingeniería |
| **Qué** | Dificultad para obtener outputs consistentes y trazables de agentes IA |
| **Dónde** | Repositorios de software, IDEs, plataformas de desarrollo |
| **Cuándo** | Durante todo el ciclo SDLC: análisis, diseño, implementación, pruebas, despliegue |
| **Por qué** | Falta de framework estandarizado, contexto inconsistente entre devs, brecha de madurez IA |
| **Cómo** | Mediante prompts estructurados con variables de contexto y reglas de gobernanza |

### 2.3 Posicionamiento en el Mercado

**Para:** Equipos de desarrollo de software (3-50 personas)  
**Que:** Necesitan estandarizar la calidad de outputs de IA  
**AI-SDLC Pro** es una: Biblioteca de prompts estructurados  
**Que:** Proporciona contexto SDLC completo con gobernanza multi-agente  
**A diferencia de:** PromptBase, FlowGPT, recursos sueltos de Udemy  
**Nuestro producto:** Ofrece framework obligatorio, variables de proyecto persistentes, y ciclo SDLC end-to-end en español

---

## 3. Descripción de Stakeholders

| Stakeholder | Rol | Interés | Prioridad |
|-------------|-----|---------|-----------|
| **Desarrollador Individual** | Usuario final | Productividad, consistencia de outputs | 🔴 Alta |
| **Tech Lead** | Influencer | Estandarización equipo, calidad | 🔴 Alta |
| **CTO / Engineering Manager** | Decision de compra | ROI, madurez equipo, métricas | 🔴 Alta |
| **LionSystems** | Propietario producto | Monetización, posicionamiento marca | 🔴 Alta |
| **Traductores Técnicos** | Proveedor | Calidad i18n | 🟡 Media |
| **GitHub / Google** | Infraestructura | Uso APIs, analytics | 🟢 Baja |

---

## 4. Descripción de Usuarios

### 4.1 Buyer Personas

#### Persona 1: Dev Sr / Tech Lead
- **Demográfico:** 5-10 años exp, 28-38 años, México/Colombia/Argentina
- **Comportamiento:** Usa Copilot/Claude diario, lidera equipo 3-8 devs
- **Necesidades:** Contexto repetitivo automatizado, outputs consistentes entre equipo
- **Dolor principal:** Cada dev estructura prompts diferente, inconsistencia de calidad
- **Disposición a pagar:** Alta ($299-799 MXN/mes)

#### Persona 2: CTO / Engineering Manager
- **Demográfico:** 10+ años exp, 35-50 años, responsable de equipo 10-30 devs
- **Comportamiento:** Define estándares, evalúa herramientas, reporta a CEO
- **Necesidades:** Estandarización de prácticas AI, brecha de madurez entre devs
- **Dolor principal:** Juniors usan IA ineficientemente, seniors gastan tiempo en contexto básico
- **Disposición a pagar:** Muy alta ($5K-15K MXN/mes enterprise)

#### Persona 3: Dev Jr / Bootcamp Grad
- **Demográfico:** 1-3 años exp, 22-28 años, primer trabajo tech
- **Comportamiento:** Aprende con IA, necesita guía estructurada
- **Necesidades:** Prompts probados, metodología clara, ramp-up rápido
- **Dolor principal:** No sabe estructurar prompts para tareas reales de ingeniería
- **Disposición a pagar:** Media (prefiere tier Free)

### 4.2 Perfiles de Usuario (RUP)

| Actor | Descripción | Responsabilidad |
|-------|-------------|-----------------|
| **Usuario Visitante** | Accede por primera vez | Explorar landing, entender propuesta de valor |
| **Usuario Free** | Registrado, tier gratuito | Usar 10 prompts básicos, evaluar producto |
| **Usuario Pro** | Suscriptor pagado | Acceso completo 44+ prompts, variables avanzadas |
| **Administrador** | LionSystems | Deploys, analytics, gestión de contenido |

---

## 5. Necesidades y Características Clave

### 5.1 Necesidades Priorizadas (MoSCoW)

| ID | Necesidad | Prioridad | Solución Propuesta |
|----|-----------|-----------|-------------------|
| **N-01** | Contexto obligatorio consistente | **Must** | Framework auto-prepend |
| **N-02** | Variables de proyecto persistentes | **Must** | Sistema de proyectos con 12 variables |
| **N-03** | Biblioteca estructurada SDLC | **Must** | 44 prompts en 15 grupos |
| **N-04** | Copiar prompts fácilmente | **Must** | Botón copiar con framework + variables |
| **N-05** | Buscar prompts rápidamente | **Should** | Búsqueda en tiempo real |
| **N-06** | Soporte multi-idioma | **Should** | i18n ES/EN (implementado parcial) |
| **N-07** | Multi-selección de prompts | **Could** | Checkboxes + copia en bloque |
| **N-08** | Sincronización cloud | **Won't** | Fuera de alcance (localStorage only) |

### 5.2 Características del Producto

| Característica | Prioridad | Esfuerzo Estimado (PSP) |
|----------------|-----------|------------------------|
| Framework auto-prepend | 🔴 Crítica | 8 horas |
| Sistema de proyectos | 🔴 Crítica | 16 horas |
| Biblioteca 44 prompts | 🔴 Crítica | 80 horas (contenido) |
| Búsqueda en tiempo real | 🟡 Alta | 4 horas |
| i18n ES/EN completo | 🟡 Alta | 60 horas |
| Onboarding guiado | 🟢 Media | 8 horas |
| Analytics GA4 | 🟢 Media | 4 horas |
| Monetización tiers | 🟢 Media | 20 horas |

---

## 6. Alternativas Competitivas

| Competidor | Debilidad que AI-SDLC Pro resuelve |
|------------|-------------------------------------|
| **PromptBase** | Prompts individuales sin estructura SDLC, sin multi-agente, en inglés |
| **FlowGPT / PromptHero** | Sin framework, sin variables, sin proyectos, prompts sueltos |
| **Recursos Udemy/Gumroad** | Estáticos, no interactivos, no adaptables al proyecto real |
| **GitHub Copilot DIY** | Requiere experiencia, sin guía SDLC, sin estructura |

---

## 7. Alcance de Versiones (Roadmap)

### v1.0 (Actual — 2026-04)
- ✅ 44 prompts estructurados
- ✅ Framework auto-prepend
- ✅ Sistema de proyectos (12 variables)
- ✅ SPA responsive, diseño oscuro
- ✅ CI/CD dual (GitHub Pages + GCP)

### v1.1 (In Progress)
- 🔶 i18n ES/EN (framework listo, prompts pendientes)
- 🔶 Gate de monetización Free/Pro
- 🔶 Landing page de conversión optimizada

### v1.2 (Q2 2026)
- ⏳ Proyectos compartidos (equipo)
- ⏳ SSO Enterprise
- ⏳ Prompts privados por organización

### v2.0 (Q3 2026)
- ⏳ Integración API (OpenAI, Anthropic)
- ⏳ Extensiones IDE (VS Code plugin)
- ⏳ Analytics de uso por prompt

---

## 8. Métricas de Éxito (PSP)

| Métrica | Línea Base | Objetivo | Medición |
|---------|-----------|----------|----------|
| **Adopción** | 0 usuarios | 1,000 usuarios activos mensuales | Google Analytics |
| **Conversión** | 0% | 5% Free → Pro | Funnel GA4 |
| **Retención** | N/A | 60% retención mensual | Cohort analysis |
| **Satisfacción** | N/A | NPS > 40 | Encuestas in-app |
| **Calidad prompts** | N/A | 0 contaminaciones detectadas | `verify_clean.py` |
| **Build time** | 2s | < 5s | CI/CD logs |

---

## 9. Riesgos del Producto

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| **R-01** | Competidor grande copia concepto | Media | 🔴 Alto | Diferenciación i18n español, velocidad de iteración |
| **R-02** | Traducciones técnicas incorrectas | Media | 🟡 Medio | Glosario validado, revisión peer |
| **R-03** | Low adoption por falta de awareness | Alta | 🔴 Alto | Marketing LinkedIn, casos de uso reales |
| **R-04** | Dependencia de plataformas IA (Copilot, Claude) | Baja | 🟡 Medio | Agnosticismo de agente, soporte multi-agente |

---

## 10. Aprobaciones

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **Product Owner** | LionSystems | [Pendiente] | 2026-04-12 |
| **Arquitecto Soluciones** | [Asistente IA] | [Automated] | 2026-04-12 |

---

**Trázabilidad PSP:**
- **Tamaño estimado:** 140 líneas documento
- **Tiempo desarrollo:** Aplicable a fases de Elaboración/Construcción RUP
- **Defectos documento:** 0 (primera versión)
- **Reusabilidad:** Plantilla para futuros productos LionSystems

