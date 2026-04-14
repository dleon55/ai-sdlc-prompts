# 🏗️ Arquitectura y Procesos - AI-SDLC Pro

## 1. Arquitectura de Archivos (Directory Map)
```text
WEB_PROMPTS/
├── ai_sdlc_pro_prompts/  # Fuentes: 44+ archivos Markdown segmentados por fase SDLC
├── docs/                # Documentación técnica, memorias y análisis
├── .github/workflows/   # CI/CD: Pipeline de despliegue a GitHub Pages y GCP
├── build.py             # Motor: Compilador Python que genera el sitio estático
├── verify_clean.py      # QA Gate: Script de validación de limpieza de prompts
├── index.html           # Artefacto Final: Aplicación SPA self-contained
└── nginx_prompts.conf   # Infra: Configuración de servidor para producción
```

## 2. Flujo de Generación (Compilation Pipeline)
El proceso de "compilación" del proyecto es unidireccional y se activa manualmente o vía CI:

1. **Raw Source:** Los ingenieros editan los prompts en archivos Markdown.
2. **Standardization:** `build.py` lee los archivos y los normaliza, extrayendo las variables `{{PLACEHOLDERS}}`.
3. **Template Composition:** Se utiliza un template de HTML Maestro (contenido en `build.py`) donde se inyectan los estilos CSS y la lógica JS.
4. **Interactivity Injection:** La metadata de los prompts se inyecta como una constante global de JavaScript (`PROMPT_INFO`).
5. **Output:** Se sobrescribe `index.html`.

## 3. Estratregia de Despliegue (CI/CD)
El proyecto utiliza GitHub Actions para automatizar el ciclo de vida:

- **Trigger:** Push a la rama `main`.
- **Jobs:**
    - **Build:** Ejecuta `python build.py`.
    - **Verify:** Ejecuta `python verify_clean.py`. Si este paso falla (prompt contaminado con fórmulas), el pipeline se aborta.
    - **Deploy Staging:** Sube el artefacto a **GitHub Pages**.
    - **Deploy Production:** Ejecuta un script de despliegue (`deploy-to-gcp.sh`) que transfiere el archivo al servidor GCP en `prompts.lionsystems.com.mx`.

## 4. Estándares de Ingeniería
- **Conventional Commits:** Uso obligatorio de prefijos `feat:`, `fix:`, `docs:`, `ci:` para el historial de versiones.
- **Atomic Commits:** Cada cambio funcional debe ir en su propio commit incluyendo la regeneración del `index.html`.
- **Zero Dependencies (Runtime):** La página web final no puede depender de CDNs externos ni de un backend para su funcionalidad core (Project Management y Variables).
