# Especificación de Casos de Uso
## AI-SDLC Pro — Modelo de Casos de Uso (RUP/UML)

---

**Fecha:** 2026-04-12  
**Versión:** 1.0  
**Metodología:** RUP Use-Case Driven Development  
**Notación:** UML 2.5 Use Case Diagrams + Especificación textual

---

## Diagrama de Casos de Uso (Resumen)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ACTORES                                            │
│                                                                             │
│   ┌──────────┐  ┌──────────────┐  ┌────────────┐  ┌────────────────┐        │
│   │ Usuario  │  │   Usuario    │  │   Admin    │  │   Sistema      │        │
│   │ Visitante│  │   Registrado │  │  LionSystems│  │   (Automated)  │        │
│   └────┬─────┘  └──────┬───────┘  └─────┬──────┘  └────────┬───────┘        │
└────────┼───────────────┼──────────────┼───────────────┼──────────────────────┘
         │               │              │               │
         │               │              │               │
         ▼               ▼              ▼               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CASOS DE USO                                         │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────┐     │
│  │                    SISTEMA DE PROMPTS                              │     │
│  │                                                                   │     │
│  │  UC-01: Explorar Landing Page        UC-06: Buscar Prompts       │     │
│  │  UC-02: Completar Onboarding         UC-07: Copiar Prompt        │     │
│  │  UC-03: Cambiar de Proyecto          UC-08: Ver Info Prompt      │     │
│  │  UC-04: Configurar Variables         UC-09: Multi-Select Copiar  │     │
│  │  UC-05: Crear Proyecto               UC-10: Colapsar/Expandir UI │     │
│  │                                                                   │     │
│  │  ┌─────────────────────────────────────────────────────────────┐  │     │
│  │  │              INTERNACIONALIZACIÓN (i18n)                    │  │     │
│  │  │                                                             │  │     │
│  │  │  UC-11: Detectar Idioma Automáticamente                   │  │     │
│  │  │  UC-12: Cambiar Idioma Manualmente                        │  │     │
│  │  │  UC-13: Persistir Preferencia Idioma                      │  │     │
│  │  └─────────────────────────────────────────────────────────────┘  │     │
│  │                                                                   │     │
│  │  ┌─────────────────────────────────────────────────────────────┐  │     │
│  │  │                 MONETIZACIÓN                                │  │     │
│  │  │                                                             │  │     │
│  │  │  UC-14: Acceder Tier Free     UC-16: Detectar Gate Pro    │  │     │
│  │  │  UC-15: Solicitar Upgrade     UC-17: Procesar Pago        │  │     │
│  │  └─────────────────────────────────────────────────────────────┘  │     │
│  │                                                                   │     │
│  └───────────────────────────────────────────────────────────────────┘     │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────┐     │
│  │              ADMINISTRACIÓN (LionSystems)                          │     │
│  │                                                                   │     │
│  │  UC-18: Desplegar Nuevo Prompt     UC-20: Monitorear Analytics  │     │
│  │  UC-19: Ejecutar QA Gate           UC-21: Gestionar Usuarios    │     │
│  └───────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Casos de Uso Detallados

### UC-01: Explorar Landing Page

| Campo | Descripción |
|-------|-------------|
| **ID** | UC-01 |
| **Nombre** | Explorar Landing Page |
| **Actor(es)** | Usuario Visitante |
| **Descripción** | El usuario visitante accede al sitio y explora la landing page para entender la propuesta de valor del producto |
| **Precondiciones** | Ninguna |
| **Postcondiciones** | Usuario informado sobre funcionalidades; posible conversión a tier Free |

**Flujo Principal:**
1. Usuario accede a URL raíz (`/`)
2. Sistema muestra landing page con hero section, features, CTA
3. Usuario explora secciones (scroll)
4. Usuario hace clic en "Probar gratis"
5. Sistema redirige a `/app` (aplicación principal)

**Flujos Alternativos:**
- **A1. Usuario ya visitó antes:** Si `localStorage.AI_SDLC_onboarding_done === '1'`, saltar directo a `/app`

**Reglas de Negocio:** BR-01, MR-11 (Trial implícito)

---

### UC-02: Completar Onboarding

| Campo | Descripción |
|-------|-------------|
| **ID** | UC-02 |
| **Nombre** | Completar Onboarding Guiado |
| **Actor(es)** | Usuario Nuevo |
| **Descripción** | Usuario primerizo recibe guía interactiva de primeros pasos |
| **Precondiciones** | `AI_SDLC_onboarding_done !== '1'` |
| **Postcondiciones** | `AI_SDLC_onboarding_done = '1'`; Email opcional capturado |

**Flujo Principal:**
1. Sistema detecta primera visita
2. Muestra welcome banner con mensaje introductorio
3. Muestra overlay modal con paso 1/4 de tutorial
4. Usuario navega pasos (Siguiente/Anterior)
5. Paso 4: Solicita email (opcional)
6. Usuario cierra o completa tutorial
7. Sistema marca onboarding como completado

**Flujos Alternativos:**
- **A1. Skip onboarding:** Usuario puede cerrar en cualquier paso

**Reglas de Negocio:** FR-03, MR-05

---

### UC-03: Cambiar de Proyecto Activo

| Campo | Descripción |
|-------|-------------|
| **ID** | UC-03 |
| **Nombre** | Cambiar Proyecto Activo |
| **Actor(es)** | Usuario Registrado |
| **Descripción** | Usuario selecciona otro proyecto de su lista, cargando sus variables asociadas |
| **Precondiciones** | Mínimo 2 proyectos creados |
| **Postcondiciones** | Proyecto seleccionado se vuelve activo; variables cargadas en contexto |

**Flujo Principal:**
1. Usuario hace clic en selector de proyecto (dropdown)
2. Sistema muestra lista de proyectos disponibles
3. Usuario selecciona proyecto destino
4. Sistema carga variables del proyecto seleccionado
5. UI actualiza: nombre de proyecto visible, variables aplicables

**Excepciones:**
- **E1. Solo un proyecto:** Selector muestra "Default" sin opción de cambio

**Reglas de Negocio:** TR-05, V-01 a V-12

---

### UC-04: Configurar Variables de Proyecto

| Campo | Descripción |
|-------|-------------|
| **ID** | UC-04 |
| **Nombre** | Configurar Variables de Contexto |
| **Actor(es)** | Usuario Registrado |
| **Descripción** | Usuario define las 12 variables de contexto que personalizarán los prompts |
| **Precondiciones** | Proyecto activo existente |
| **Postcondiciones** | Variables persistidas en `localStorage.AI_SDLC_v1_projects` |

**Flujo Principal:**
1. Usuario abre panel de variables (botón "Variables")
2. Sistema muestra formulario con 12 campos:
   - Globales: repositorio, ambiente, stack...
   - Por prompt: issue, rama, componentes...
3. Usuario completa campos relevantes
4. Usuario guarda cambios
5. Sistema actualiza `localStorage`
6. Sistema confirma: "Variables guardadas"

**Validaciones:**
- Campos requeridos (V-01, V-05) deben tener valor antes de copiar prompts

**Reglas de Negocio:** FR-05, TR-06

---

### UC-05: Crear Nuevo Proyecto

| Campo | Descripción |
|-------|-------------|
| **ID** | UC-05 |
| **Nombre** | Crear y Nombrar Proyecto |
| **Actor(es)** | Usuario Registrado |
| **Descripción** | Usuario crea proyecto nuevo con nombre descriptivo |
| **Precondiciones** | Ninguna (primer proyecto se crea automáticamente) |
| **Postcondiciones** | Nuevo proyecto en array `projects`; variables vacías inicializadas |

**Flujo Principal:**
1. Usuario abre modal "Proyectos"
2. Hace clic en "Nuevo proyecto"
3. Sistema solicita nombre del proyecto
4. Usuario ingresa nombre
5. Sistema crea proyecto con variables default vacías
6. Proyecto nuevo se convierte en activo automáticamente

**Excepciones:**
- **E1. Nombre duplicado:** "Ya existe un proyecto con ese nombre"

---

### UC-06: Buscar Prompts

| Campo | Descripción |
|-------|-------------|
| **ID** | UC-06 |
| **Nombre** | Buscar y Filtrar Prompts |
| **Actor(es)** | Usuario Registrado |
| **Descripción** | Usuario busca prompts por texto en título o contenido |
| **Precondiciones** | App cargada (sección /app) |
| **Postcondiciones** | Lista filtrada mostrando solo coincidencias |

**Flujo Principal:**
1. Usuario posiciona cursor en campo de búsqueda
2. Escribe término de búsqueda (ej: "incidente")
3. Sistema filtra en tiempo real (debounce 150ms)
4. Muestra contador: "3 de 44 prompts"
5. Cards no coincidentes ocultados
6. Usuario limpia búsqueda → restaura todos

**Flujos Alternativos:**
- **A1. Sin resultados:** Muestra estado vacío "Sin resultados. Intenta con otro término."

---

### UC-07: Copiar Prompt Individual

| Campo | Descripción |
|-------|-------------|
| **ID** | UC-07 |
| **Nombre** | Copiar Prompt al Portapapeles |
| **Actor(es)** | Usuario Registrado |
| **Descripción** | Usuario copia prompt específico con framework prepend y variables aplicadas |
| **Precondiciones** | Proyecto activo; prompt visible |
| **Postcondiciones** | Texto en clipboard listo para pegar en agente IA |

**Flujo Principal:**
1. Usuario localiza prompt deseado (ej: 02-01 Análisis de issue)
2. Expande card si está colapsado (clic en título o ▼)
3. Hace clic en botón "Copiar"
4. Sistema:
   a. Obtiene framework de `00-framework.md`
   b. Obtiene contenido del prompt
   c. Aplica sustitución de variables ({{REPO}} → valor proyecto)
   d. Concatena: framework + "\n\n" + prompt
5. Sistema copia a `navigator.clipboard`
6. Botón cambia a "✓ Copiado" por 3 segundos
7. Analytics: `gtag('event', 'copy_prompt', {id: '02-01'})`

**Reglas de Negocio:** FR-01 (Prepend obligatorio), FR-05

---

### UC-08: Ver Información de Prompt (Modal ⓘ)

| Campo | Descripción |
|-------|-------------|
| **ID** | UC-08 |
| **Nombre** | Consultar Info y Fórmulas de Uso |
| **Actor(es)** | Usuario Registrado |
| **Descripción** | Usuario ve descripción detallada, fórmulas de uso y variables sin copiar prompt |
| **Precondiciones** | Prompt en biblioteca |
| **Postcondiciones** | Modal informativo visible; prompt no copiado |

**Flujo Principal:**
1. Usuario identifica card de prompt
2. Hace clic en icono ⓘ (info)
3. Sistema muestra modal con:
   - Título del prompt
   - Descripción detallada
   - Fórmula de uso estándar
   - Lista de variables esperadas
4. Usuario cierra modal (X o Escape)

**Valor:** Evita contaminar clipboard con contenido informativo; sirve para entender antes de usar.

---

### UC-09: Multi-Selección y Copia en Bloque

| Campo | Descripción |
|-------|-------------|
| **ID** | UC-09 |
| **Nombre** | Seleccionar Múltiples Prompts |
| **Actor(es)** | Usuario Registrado |
| **Descripción** | Usuario selecciona varios prompts vía checkboxes y los copia en bloque |
| **Precondiciones** | Modo "Multi-select" activado |
| **Postcondiciones** | Múltiples prompts en clipboard separados por delimitador |

**Flujo Principal:**
1. Usuario activa modo "Multi-select" (toggle en header)
2. Checkboxes aparecen en cada card
3. Usuario marca prompts deseados (2, 3, n...)
4. Contador muestra "3 seleccionados"
5. Usuario hace clic en "Copiar seleccionados"
6. Sistema concatena: framework + prompt1 + "\n---\n" + prompt2 + ...
7. Copia a clipboard

**Reglas de Negocio:** FR-01 (framework prepend una sola vez al inicio)

---

### UC-10: Colapsar/Expandir Elementos UI

| Campo | Descripción |
|-------|-------------|
| **ID** | UC-10 |
| **Nombre** | Controlar Visibilidad de Componentes |
| **Actor(es)** | Usuario Registrado |
| **Descripción** | Usuario colapsa/expande sidebar, framework banner, o cards individuales |
| **Precondiciones** | Elemento UI presente |
| **Postcondiciones** | Estado persistido en localStorage |

**Elementos Controlables:**
- Sidebar (icono ≣)
- Framework banner (clic en header o ▼)
- Individual cards (clic en título o ▼)

**Persistencia:**
- Sidebar: `AI_SDLC_sidebar`
- Framework: `AI_SDLC_fw_expanded`
- Cards: no persisten (estado efímero)

---

### UC-11 a UC-13: Internacionalización

Ver documento `i18n-UseCases.md` para especificación detallada de:
- UC-11: Detectar Idioma Automáticamente
- UC-12: Cambiar Idioma Manualmente  
- UC-13: Persistir Preferencia Idioma

---

### UC-14 a UC-17: Monetización

Ver documento `Monetization-UseCases.md` para especificación detallada de:
- UC-14: Acceder Contenido Tier Free
- UC-15: Solicitar Upgrade a Pro
- UC-16: Detectar Gate de Conversión
- UC-17: Procesar Pago y Activar Pro

---

## Matriz de Trazabilidad

| Caso de Uso | Requerimientos | Componentes | Estimación PSP (horas) |
|-------------|----------------|-------------|----------------------|
| UC-01 | N-03 | Landing HTML | 8 |
| UC-02 | N-05 | Onboarding JS | 12 |
| UC-03 | N-02 | Projects JS | 4 |
| UC-04 | N-02 | VarPanel JS | 8 |
| UC-05 | N-02 | ProjectsModal JS | 6 |
| UC-06 | N-05 | Search JS | 4 |
| UC-07 | N-01, N-03 | copyPrompt() | 6 |
| UC-08 | N-05 | Info Modal | 4 |
| UC-09 | N-05 | MultiSelect JS | 6 |
| UC-10 | N-03 | Toggle UI | 4 |
| **Total** | | | **62 horas** |

---

## Especificación de Interfaces

### Interfaz de Usuario: Pantallas Principales

| Pantalla | Elementos | Navegación |
|----------|-----------|------------|
| **Landing** | Hero, Features, CTA, Footer | CTA → /app |
| **App/Main** | Header, Search, Sidebar, Content | Sidebar → #sec-XX |
| **Projects Modal** | Lista proyectos, CRUD, Import/Export | Modal overlay |
| **Var Panel** | Form 12 campos, Global/Per-prompt | Slide-in panel derecho |
| **Info Modal** | Descripción, Fórmulas, Variables | Modal centered |

---

**Trázabilidad PSP:**
- **Total Casos de Uso:** 21 identificados
- **Detallados:** 10 (prioridad alta)
- **Referenciados externos:** 11 (i18n, monetización)
- **Tiempo documentación:** 4 horas
- **Cobertura funcional:** ~95% del sistema

