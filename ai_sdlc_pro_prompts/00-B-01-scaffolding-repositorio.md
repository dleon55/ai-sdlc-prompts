# 0-B.1 — Scaffolding de repositorio nuevo

## Descripción

Prompt para diseñar y generar la estructura base de un repositorio nuevo: directorios, archivos de configuración, gobierno y estándares, a partir del tipo de proyecto, metodología y stack tecnológico seleccionados.

**Cuándo usarlo:** al iniciar un proyecto nuevo, al migrar un proyecto sin estructura formal, o al estandarizar un repositorio existente que creció sin guía.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña la estructura completa del repositorio para este proyecto nuevo (o a estandarizar).

Inputs requeridos:
- nombre del repositorio: [NOMBRE]
- tipo de proyecto: [frontend SPA / API REST / full-stack / microservicio / monorepo / librería / data science / IaC / otro]
- metodología de trabajo: [SCRUM / Kanban / Trunk-Based / GitFlow / GitHub Flow / RUP / otro]
- stack tecnológico principal: [ej: Python + FastAPI + PostgreSQL / Node + React + MongoDB / etc.]
- plataforma de hosting/CI: [GitHub / GitLab / Bitbucket / Azure DevOps]
- equipo: [tamaño y roles presentes: ej. 2 devs + 1 QA + AI agents]
- tipo de licencia: [MIT / Apache 2.0 / propietaria / interna]

Entrega:

1. ÁRBOL DE DIRECTORIOS
   - estructura completa con propósito de cada carpeta
   - convención de nombres aplicada

2. ARCHIVOS RAÍZ OBLIGATORIOS
   Por cada archivo indica: nombre, propósito y contenido base sugerido:
   - README.md (estructura mínima: descripción, instalación, uso, contribución, licencia)
   - .gitignore (adaptado al stack)
   - .editorconfig
   - CONTRIBUTING.md (alineado a la metodología elegida)
   - CHANGELOG.md (formato Keep a Changelog / semver)
   - LICENSE
   - CODEOWNERS

3. CONFIGURACIÓN DE HERRAMIENTAS
   Archivos de configuración base según el stack:
   - gestor de dependencias (package.json / pyproject.toml / pom.xml / go.mod)
   - linter y formatter
   - pre-commit hooks (.pre-commit-config.yaml)
   - variables de entorno (.env.example — nunca .env real)
   - Docker (Dockerfile + docker-compose.yml si aplica)

4. CARPETA .github/
   - ISSUE_TEMPLATE/ (bug_report.md, feature_request.md)
   - PULL_REQUEST_TEMPLATE.md
   - workflows/ (CI básico según el stack)
   - dependabot.yml

5. CARPETA docs/
   - architecture.md (plantilla de arquitectura)
   - decisions/ (carpeta para ADRs)
   - runbooks/ (carpeta para runbooks operativos)

6. VACÍOS Y RIESGOS
   - qué archivos no pueden generarse automáticamente y requieren decisión del equipo
   - riesgos de omitir cada sección

Formato de salida:
- árbol de directorios con comentarios en línea
- tabla de archivos: nombre | propósito | prioridad (obligatorio / recomendado / opcional)
- contenido base de los archivos críticos
```

---

## Uso con fórmula estándar

```text
Usa el prompt de scaffolding de repositorio y adáptalo a:
- nombre del repo: [NOMBRE]
- tipo de proyecto: [TIPO]
- metodología: [METODOLOGÍA]
- stack: [STACK]
- plataforma CI/hosting: [PLATAFORMA]
- equipo: [COMPOSICIÓN]
- licencia: [TIPO DE LICENCIA]
- objetivo puntual de salida: árbol de directorios + tabla de archivos + contenido base de README, CONTRIBUTING, .gitignore, Dockerfile
- nivel de profundidad: alto
```

---

## Salida esperada

```
mi-proyecto/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── workflows/
│   │   └── ci.yml
│   └── dependabot.yml
├── docs/
│   ├── architecture.md
│   ├── decisions/          ← ADRs
│   └── runbooks/
├── src/                    ← código fuente
├── tests/                  ← pruebas
├── .editorconfig
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── CODEOWNERS
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

| Archivo | Propósito | Prioridad |
|---|---|---|
| README.md | Punto de entrada del proyecto | Obligatorio |
| CONTRIBUTING.md | Reglas de contribución y branching | Obligatorio |
| CODEOWNERS | Asignación de revisores por área | Obligatorio |
| .gitignore | Exclusiones de VCS adaptadas al stack | Obligatorio |
| .env.example | Variables de entorno documentadas (sin valores reales) | Obligatorio |
| CHANGELOG.md | Historial de cambios versionado | Recomendado |
| .editorconfig | Consistencia de formato entre IDEs | Recomendado |
| .pre-commit-config.yaml | Validaciones automáticas antes de commit | Recomendado |
| docs/architecture.md | Decisiones de arquitectura de alto nivel | Recomendado |
| docs/decisions/ | ADRs numerados (Architecture Decision Records) | Recomendado |
| docs/runbooks/ | Procedimientos operativos | Opcional |
