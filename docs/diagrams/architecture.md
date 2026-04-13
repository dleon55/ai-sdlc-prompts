# Diagramas de Arquitectura
## AI-SDLC Pro — Documentación Visual del Sistema

---

## 1. Diagrama de Flujo: Proceso de Build (Actual vs Propuesto i18n)

### Flujo Actual (Monolenguaje ES)

```mermaid
flowchart TD
    A[Inicio: python build.py] --> B[Leer 00-framework.md]
    B --> C[Parsear: título, prompt, descripción]
    C --> D[Generar fw_block HTML]
    
    E[Iterar archivos *.md] --> F[Parsear prompt individual]
    F --> G[Generar card HTML]
    G --> H{¿Más archivos?}
    H -->|Sí| E
    H -->|No| I[Generar index.html completo]
    
    I --> J[Incrustar CSS + JS + HTML]
    J --> K[Output: index.html ~255KB]
    K --> L[Fin]
    
    D --> I
    
    style A fill:#e1f5e1
    style K fill:#fff4e1
    style L fill:#e1f5e1
```

### Flujo Propuesto (Bilingüe ES/EN)

```mermaid
flowchart TD
    A[Inicio: python build.py] --> B[Leer 00-framework.md]
    B --> C[Leer 00-framework.en.md]
    C --> D[Generar fw_block ES + EN]
    D --> D1[<div data-lang=es>...]
    D --> D2[<div data-lang=en style=display:none>...]
    
    E[Iterar archivos *.md] --> F[Buscar .en.md correspondiente]
    F --> G{¿.en.md existe?}
    G -->|Sí| H[Generar card ES + EN]
    G -->|No| I[Generar card ES + fallback ES]
    
    H --> H1[<div data-lang=es>...]
    H --> H2[<div data-lang=en style=display:none>...]
    I --> I1[<div data-lang=es>...]
    I --> I2[<div data-lang=en style=display:none>fallback ES...]
    
    H1 --> J
    H2 --> J
    I1 --> J
    I2 --> J
    
    J{¿Más archivos?} -->|Sí| E
    J -->|No| K[Generar index.html dual]
    
    K --> L[Incrustar CSS + JS + i18n functions]
    L --> M[Output: index.html ~520KB]
    M --> N[Fin]
    
    D1 --> K
    D2 --> K
    
    style A fill:#e1f5e1
    style M fill:#fff4e1
    style N fill:#e1f5e1
    style G fill:#fff4e1
```

**Explicación:**
- **Actual:** Build simple lee archivos `.md` y genera HTML monolenguaje (~255KB)
- **Propuesto:** Build dual lee tanto `.md` (ES) como `.en.md` (EN), genera ambos bloques con `data-lang` atributos (~520KB). El fallback muestra ES si EN no existe.

---

## 2. Diagrama de Secuencia: Cambio de Idioma (i18n)

```mermaid
sequenceDiagram
    actor U as Usuario
    participant B as Browser
    participant UI as LanguageSelector
    participant LS as localStorage
    participant D as DOM/data-lang
    participant GA as Google Analytics

    Note over U,GA: Flujo de Cambio de Idioma ES → EN
    
    U->>B: Clic en selector 🌐 ES
    B->>UI: toggleLanguageDropdown()
    UI->>B: Mostrar dropdown (🇪🇸 🇺🇸)
    
    U->>B: Selecciona "English"
    B->>UI: onLanguageSelect('en')
    
    UI->>LS: setItem('AI_SDLC_language', 'en')
    Note right of LS: Persistencia
    
    UI->>B: document.documentElement.lang = 'en'
    Note right of B: SEO + Accessibility
    
    UI->>D: updateFrameworkVisibility('en')
    D->>D: sec-00-es.style.display = 'none'
    D->>D: sec-00-en.style.display = 'block'
    Note right of D: < 300ms
    
    UI->>D: updateLanguageSelectorUI('en')
    D->>D: Marcar EN activo, ES inactivo
    
    UI->>D: updateMetaTags('en')
    D->>D: Actualizar og:description, etc.
    
    UI->>GA: gtag('event', 'language_change', {to: 'en'})
    Note right of GA: Métricas
    
    UI->>U: Feedback visual (label "EN")
    
    Note over U,GA: Sin recarga de página!
```

**Explicación:**
Muestra la interacción completa cuando usuario cambia idioma. El sistema persiste en localStorage, actualiza DOM con `data-lang` selectores, y trackea en GA. Críticamente: **sin recarga de página** para experiencia instantánea.

---

## 3. Diagrama de Componentes: Arquitectura del Sistema

```mermaid
graph TB
    subgraph "Generación (Build Time)"
        A1[ai_sdlc_pro_prompts/]
        A1 --> B1[00-framework.md]
        A1 --> B2[00-framework.en.md]
        A1 --> B3[01-01-*.md ... 44 archivos]
        
        C1[build.py] --> D1[Parser Markdown]
        C1 --> D2[Generador HTML]
        C1 --> D3[i18n_strings.py]
        
        D1 --> E1[index.html]
        D2 --> E1
        D3 --> E1
        
        F1[verify_clean.py] --> F2{QA Gate}
        F2 -->|Pass| G1[Deploy GitHub Pages]
        F2 -->|Pass| G2[Deploy GCP]
        F2 -->|Fail| H1[Error CI/CD]
        
        E1 --> F2
    end
    
    subgraph "Runtime (Browser)"
        I1[Usuario] --> I2[Navegador]
        I2 --> I3[index.html cargado]
        
        I3 --> J1[Router Client-Side]
        J1 -->|/| J2[Landing Page]
        J1 -->|/app| J3[App SPA]
        
        J3 --> K1[UI Components]
        K1 --> K2[LanguageSelector]
        K1 --> K3[ProjectManager]
        K1 --> K4[PromptCards]
        K1 --> K5[SearchFilter]
        K1 --> K6[VariablePanel]
        
        J3 --> L1[Core Logic]
        L1 --> L2[copyPrompt()]
        L1 --> L3[i18n Engine]
        L1 --> L4[LocalStorage Manager]
        
        J3 --> M1[Data Layer]
        M1 --> M2[localStorage API]
        M2 --> M3[Proyectos + Variables]
        M2 --> M4[Preferencias UI]
        M2 --> M5[Idioma]
        
        J3 --> N1[Analytics]
        N1 --> N2[Google Analytics 4]
    end
    
    G1 --> I2
    G2 --> I2
    
    style C1 fill:#e1f5e1
    style I3 fill:#fff4e1
    style K2 fill:#ffe1e1
```

**Explicación:**
Arquitectura de dos fases:
1. **Build Time:** Python genera HTML estático desde Markdown. QA gate valida antes de deploy dual (GitHub Pages + GCP).
2. **Runtime:** SPA vanilla JS sin backend. Componentes modulares (selector idioma, proyectos, prompts). Persistencia 100% localStorage. Analytics solo para métricas.

---

## 4. Diagrama Entidad-Relación: Datos de localStorage

```mermaid
erDiagram
    PROYECTO ||--o{ VARIABLE : contiene
    
    PROYECTO {
        string id PK "UUID o timestamp"
        string nombre "Nombre descriptivo"
        timestamp creado "Fecha creación"
        boolean activo "Proyecto actual"
    }
    
    VARIABLE {
        string clave PK "Nombre variable"
        string valor "Valor sustituible"
        string tipo "global|per_prompt"
        string proyecto_id FK "ID proyecto"
    }
    
    PREFERENCIA_USUARIO {
        string clave PK "AI_SDLC_*"
        string valor "Valor preferencia"
        string tipo "ui|idioma|onboarding"
    }
    
    PROYECTO ||--o{ PREFERENCIA_USUARIO : "configura visibilidad"
```

### Modelo de Datos localStorage (Schema v1)

```mermaid
classDiagram
    class LocalStorage {
        +String AI_SDLC_v1_projects
        +String AI_SDLC_language
        +String AI_SDLC_sidebar
        +String AI_SDLC_fw_expanded
        +String AI_SDLC_onboarding_done
        +String AI_SDLC_email_collected
    }
    
    class ProjectArray {
        +Array~Project~ projects
    }
    
    class Project {
        +String id
        +String name
        +Variables variables
        +Date created
    }
    
    class Variables {
        +String repositorio
        +String issue
        +String rama_actual
        +String rama_destino
        +String ambiente
        +Array componentes
        +String modulo
        +String stack
        +String tipo_proyecto
        +String metodologia
        +Array agentes_ia
        +String nivel_autonomia
    }
    
    LocalStorage --> ProjectArray : JSON.parse
    ProjectArray --> Project : contains
    Project --> Variables : has
```

**Explicación:**
Modelo de datos 100% client-side:
- **Proyectos:** Array JSON con ID, nombre, timestamp, y objeto variables
- **Variables:** 12 campos string/array según tipo (globales vs por-prompt)
- **Preferencias:** Claves sueltas para UI state (sidebar, idioma, onboarding)
- **Relaciones:** Uno-a-muchos (proyecto → variables). No hay relaciones complejas (normalizado en JSON).

---

## 5. Diagrama de Flujo: Copiado de Prompt (Core Functionality)

```mermaid
flowchart TD
    A[Usuario: Clic Copiar] --> B{¿Prompt regular o framework?}
    
    B -->|Regular| C[Obtener framework
    00-framework.md]
    B -->|Framework| D[Solo framework]
    
    C --> E[Obtener contenido prompt
    id=02-01]
    D --> F[Obtener contenido framework]
    
    E --> G[Concatenar:
    framework + "\n\n" + prompt]
    F --> H[Contenido framework puro]
    
    G --> I{Cargar variables
    proyecto activo}
    H --> J[No aplica variables]
    
    I --> K[localStorage.getItem
    AI_SDLC_v1_projects]
    K --> L[Encontrar proyecto activo]
    L --> M[Objeto variables:
    {repo, issue, ...}]
    
    M --> N[Reemplazar {{VAR}}]
    N --> N1["{{REPO}}" → "urgemy-api"]
    N --> N2["{{ISSUE}}" → "#842"]
    
    J --> O
    N --> O[Texto final listo]
    
    O --> P[navigator.clipboard
    .writeText]
    P --> Q{¿Éxito?}
    
    Q -->|Sí| R[Feedback visual:
    Botón "✓ Copiado"]
    Q -->|No| S[Alert error:
    "No se pudo copiar"]
    
    R --> T[gtag event:
    'copy_prompt']
    T --> U[Fin]
    S --> U
    
    style A fill:#e1f5e1
    style P fill:#fff4e1
    style R fill:#e1f5e1
    style S fill:#ffe1e1
```

**Explicación:**
Flujo crítico del sistema: usuario copia prompt → sistema antepone framework → aplica variables de proyecto → copia a clipboard. El framework nunca se copia solo (siempre prepend para prompts regulares).

---

## 6. Diagrama de Secuencia: Primer Uso (Onboarding)

```mermaid
sequenceDiagram
    actor U as Usuario Nuevo
    participant B as Browser
    participant LS as localStorage
    participant OB as Onboarding
    participant GA as Analytics

    Note over U,GA: Flujo de Primera Visita
    
    U->>B: Accede a /
    B->>LS: getItem('AI_SDLC_onboarding_done')
    LS-->>B: null / undefined
    
    B->>OB: initOnboarding()
    OB->>B: Mostrar Welcome Banner
    Note right of OB: "Bienvenido a AI-SDLC Pro..."
    
    OB->>B: Mostrar Overlay Modal Paso 1/4
    Note right of OB: Tutorial interactivo
    
    U->>B: Clic "Siguiente"
    B->>OB: Avanzar Paso 2/4
    
    U->>B: Clic "Siguiente"
    B->>OB: Avanzar Paso 3/4
    
    U->>B: Clic "Siguiente"
    B->>OB: Avanzar Paso 4/4
    OB->>B: Solicitar email (opcional)
    
    alt Usuario ingresa email
        U->>B: Input email
        B->>LS: setItem('AI_SDLC_email_collected', email)
    else Usuario omite
        B->>B: Continuar sin email
    end
    
    B->>LS: setItem('AI_SDLC_onboarding_done', '1')
    B->>OB: Cerrar onboarding
    
    B->>GA: gtag('event', 'onboarding_complete')
    
    U->>B: Ahora puede usar la app
    
    Note over U,B: Próximas visitas: onboarding saltado automáticamente
```

**Explicación:**
Flujo de primera experiencia: detección de nuevo usuario → tutorial paso a paso → captura opcional de email → flag de completado. Las visitas subsiguientes detectan el flag y omiten onboarding.

---

## Resumen de Diagramas

| Diagrama | Tipo | Propósito | Complejidad |
|----------|------|-----------|-------------|
| **Build Flow** | Flowchart | Proceso de generación actual vs i18n | Media |
| **Cambio Idioma** | Secuencia | Interacción i18n en runtime | Media |
| **Arquitectura** | Componentes | Vista global sistema build+runtime | Alta |
| **Datos localStorage** | ER + Class | Modelo de persistencia cliente | Baja |
| **Copiado Prompt** | Flowchart | Core functionality del producto | Media |
| **Onboarding** | Secuencia | Experiencia primer uso | Baja |

---

**Nota:** Todos los diagramas son consistentes con:
- Código actual de `build.py` (generación estática)
- Estructura real de archivos en `ai_sdlc_pro_prompts/`
- JavaScript implementado en `index.html` (SPA, localStorage)
- Arquitectura de deploy (GitHub Pages + GCP)

