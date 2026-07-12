# 0-B.1 — Scaffolding de repositorio nuevo

## Descripción

Prompt para diseñar y generar la estructura base de un repositorio nuevo: directorios, archivos de configuración, gobierno y estándares, a partir del tipo de proyecto, metodología y stack tecnológico seleccionados.

**Cuándo usarlo:** al iniciar un proyecto nuevo, al migrar un proyecto sin estructura formal, o al estandarizar un repositorio existente que creció sin guía.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | medio — la estructura de repositorio propuesta es costosa de rehacer una vez que el equipo empieza a construir sobre ella, aunque el prompt no escribe archivos por sí mismo |
| Entradas requeridas | tipo de proyecto, metodología, stack tecnológico, plataforma de hosting/CI, composición del equipo, tipo de licencia |
| Herramientas permitidas | lectura opcional de la estructura actual del repositorio si ya existe — no requiere escritura ni ejecución; el resultado es texto para que un humano lo aplique |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si el tipo de proyecto o el stack son ambiguos, o si ya existe una estructura en conflicto con la propuesta, declarar la ambigüedad y pedir confirmación antes de proponer una reestructuración completa |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | el árbol de directorios y la tabla de archivos son consistentes con el tipo de proyecto y stack declarados; cada archivo crítico (README, CONTRIBUTING, .gitignore, CODEOWNERS) incluye contenido base, no solo el nombre |
| Siguiente prompt recomendado | `00-B-03-github-configuracion` para las protecciones y plantillas de GitHub; `00-B-05-stack-calidad-codigo` para configurar linters, formatters y quality gates sobre la estructura ya creada; `00-B-02-gobernanza-ia-agentes` para definir la gobernanza de agentes IA sobre la estructura creada; `00-B-04-metodologia-framework` para formalizar la metodología y el flujo de branches |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña la estructura completa del repositorio para este proyecto nuevo (o a estandarizar).

Inputs requeridos:
- nombre del repositorio: [NOMBRE O URL]
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

Restricciones:
- si el repositorio ya tiene archivos de configuración existentes (package.json, pyproject.toml, .gitignore, workflows, etc.), no propongas sobrescribirlos sin señalar explícitamente el conflicto y pedir confirmación humana antes de reemplazar su contenido,
- no asumas versiones de lenguajes, frameworks o herramientas que no fueron declaradas como input — si el stack no especifica versión, decláralo como un vacío a confirmar en vez de inventar una versión "razonable",
- si la estructura actual del repositorio (carpetas, convenciones de nombres, archivos raíz ya presentes) entra en conflicto con la propuesta, señala el conflicto explícitamente en la sección de VACÍOS Y RIESGOS en vez de proponer una reestructuración silenciosa,
- este prompt entrega texto para que un humano lo aplique: no generes comandos de shell que creen o sobrescriban archivos directamente.

Formato de salida:
- árbol de directorios con comentarios en línea
- tabla de archivos: nombre | propósito | prioridad (obligatorio / recomendado / opcional)
- contenido base de los archivos críticos
```

---

## Uso con fórmula estándar

```text
Usa el prompt de scaffolding de repositorio y adáptalo a:
- nombre del repo: [NOMBRE O URL]
- tipo de proyecto: [TIPO DE PROYECTO]
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

### Ejemplo aplicado: estandarización de `ai-sdlc-prompts`

| Archivo | Contenido base propuesto (extracto) | Conflicto detectado |
|---|---|---|
| `.gitignore` | Agregar `__pycache__/`, `dist/`, `.pytest_cache/` — el repo es Python (`build.py`) + contenido Markdown | Ninguno — el archivo no existe todavía en la raíz |
| `CODEOWNERS` | `ai_sdlc_pro_prompts/*.md @equipo-contenido` y `build.py tests/ @equipo-plataforma` | El README ya asigna revisores informalmente en texto — declarar como vacío a confirmar antes de reemplazarlo por el archivo formal |
