# 🏗️ Arquitectura y Procesos - AI-SDLC Pro

## 1. Arquitectura de Archivos (Directory Map)
```text
WEB_PROMPTS/
├── ai_sdlc_pro_prompts/  # Fuentes: 112 prompts Markdown segmentados por fase SDLC
├── docs/                # Documentación técnica, memorias y análisis
├── .github/workflows/   # CI/CD: Pipeline de despliegue a GitHub Pages y GCP
├── build.py             # Motor: Compilador Python que genera el sitio estático
├── prompts-index.json   # Índice estructurado consumible por herramientas y MCP
├── verify_clean.py      # QA Gate: Script de validación de limpieza de prompts
├── extract_vars.py      # QA Gate: Contrato de placeholders y aliases
├── mcp-server/          # Servidor MCP para consulta y resolución de prompts
├── supabase/            # Esquema, migraciones y Edge Function del webhook Paddle
├── index.html           # Artefacto Final: Aplicación SPA self-contained
└── nginx_prompts.conf   # Infra: Configuración de servidor para producción
```

## 2. Flujo de Generación (Compilation Pipeline)
El proceso de "compilación" del proyecto es unidireccional y se activa manualmente o vía CI:

1. **Raw Source:** Los ingenieros editan los prompts ES/EN en archivos Markdown y mantienen su paridad funcional.
2. **Standardization:** `build.py` lee los archivos y los normaliza; `extract_vars.py` valida el contrato de placeholders, aliases y ejemplos ignorados.
3. **Template Composition:** Se utiliza un template de HTML Maestro (contenido en `build.py`) donde se inyectan los estilos CSS y la lógica JS.
4. **Interactivity Injection:** La metadata y el registro de variables se inyectan como constantes globales de JavaScript (`PROMPT_INFO` y `TOKEN_REGISTRY`).
5. **Output:** Se sobrescriben `index.html` y el índice estructurado `prompts-index.json`.

## 3. Estratregia de Despliegue (CI/CD)
El proyecto utiliza GitHub Actions para automatizar el ciclo de vida:

- **Trigger:** Pull request a `main`, push a `main` y ejecución manual.
- **Jobs:**
    - **Build y gates obligatorios:** ejecuta `build.py`, `verify_clean.py`, `extract_vars.py`, pruebas JavaScript de variables y `pytest`.
    - **PR:** usa configuración Paddle sandbox y valida sin desplegar.
    - **Main:** reconstruye con variables Live del Environment `production`, publica el artefacto en **GitHub Pages**, despliega GCP y la Edge Function de Supabase.
    - **E2E y MCP:** se ejecutan como señal informativa; un resultado fallido debe investigarse antes de declarar una liberación aceptada.

## 4. Estándares de Ingeniería
- **Conventional Commits:** Uso obligatorio de prefijos `feat:`, `fix:`, `docs:`, `ci:` para el historial de versiones.
- **Atomic Commits:** Cada cambio funcional debe ir en su propio commit incluyendo la regeneración del `index.html`.
- **Dependencias acotadas:** el catálogo y la experiencia anónima son autocontenidos; Supabase habilita autenticación/sincronización y Paddle.js sólo se usa para checkout configurado.
