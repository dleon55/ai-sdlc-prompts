# 0-B.5 — Configuración de stack y herramientas de calidad de código

## Descripción

Prompt para seleccionar y configurar las herramientas de calidad de código según el stack del proyecto: linters, formatters, analizadores estáticos, pre-commit hooks, coverage mínimo y quality gates en CI. Genera los archivos de configuración listos para usar.

**Cuándo usarlo:** al iniciar un proyecto, al estandarizar calidad en uno existente, o cuando se incorporan agentes IA que deben respetar las convenciones del stack.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Selecciona y configura las herramientas de calidad de código para el stack de este proyecto.

Inputs requeridos:
- lenguaje(s) principal(es): [Python / JavaScript / TypeScript / Java / Go / otro]
- framework(s): [FastAPI / Django / React / Vue / Spring / otro]
- plataforma CI: [GitHub Actions / GitLab CI / otro]
- cobertura mínima deseada: [ej: 80%]
- nivel de restricción: [permisivo / balanceado / estricto]

Entrega:

1. HERRAMIENTAS RECOMENDADAS POR CAPA
   Por cada lenguaje detectado, indicar:
   - linter: herramienta + versión recomendada + justificación
   - formatter: herramienta + configuración base
   - analizador estático de seguridad (SAST): herramienta recomendada
   - análisis de dependencias vulnerables: herramienta recomendada
   - framework de pruebas: herramienta + runner recomendado
   - medición de cobertura: herramienta + configuración de umbral mínimo

2. ARCHIVOS DE CONFIGURACIÓN (contenido completo listo para copiar)
   Según el stack, genera los que apliquen:
   - .eslintrc.json / eslint.config.js (JavaScript/TypeScript)
   - .prettierrc (JavaScript/TypeScript)
   - pyproject.toml con [tool.ruff], [tool.black], [tool.pytest.ini_options] (Python)
   - .flake8 o ruff.toml (Python alternativo)
   - .editorconfig (todos los lenguajes)
   - sonar-project.properties (si se usa SonarQube/SonarCloud)

3. PRE-COMMIT HOOKS (.pre-commit-config.yaml)
   Hooks mínimos recomendados:
   - trailing-whitespace
   - end-of-file-fixer
   - check-yaml / check-json
   - linter del stack (en modo fast)
   - formatter del stack
   - detección de secretos (detect-secrets o gitleaks)
   - check-added-large-files
   Incluir el archivo .pre-commit-config.yaml completo y el comando de instalación.

4. QUALITY GATES EN CI (.github/workflows/quality.yml)
   Workflow que ejecute:
   - lint
   - format check (fail si hay cambios pendientes de formatear)
   - SAST
   - tests + coverage con umbral mínimo (fail si no se alcanza)
   - análisis de dependencias vulnerables
   Configurar como required check en branch protection.

5. REGLAS PARA AGENTES IA
   Instrucciones que deben agregarse a .github/copilot-instructions.md y .windsurfrules:
   - "siempre ejecutar [formatter] antes de proponer cambios"
   - "no desactivar reglas del linter con comentarios inline sin justificación"
   - "cobertura mínima de [X]% para el código nuevo"
   - "no agregar dependencias sin verificar CVEs en [herramienta]"

6. COMANDOS DE BOOTSTRAP
   Secuencia de comandos para dejar el entorno listo desde cero:
   - instalación de herramientas de desarrollo
   - instalación de pre-commit hooks
   - ejecución inicial de todos los checks
   - verificación de que el pipeline CI pasa en verde

Formato de salida:
- tabla de herramientas por capa
- archivos de configuración completos
- workflow CI completo
- comandos de bootstrap en orden
```

---

## Uso con fórmula estándar

```text
Usa el prompt de configuración de stack y calidad de código y adáptalo a:
- lenguaje(s): [LENGUAJES]
- frameworks: [FRAMEWORKS]
- plataforma CI: [CI]
- cobertura mínima: [PORCENTAJE]
- nivel de restricción: [PERMISIVO / BALANCEADO / ESTRICTO]
- objetivo puntual de salida: archivos de configuración completos + workflow CI quality gates + comandos de bootstrap
- nivel de profundidad: alto
```

---

## Salida esperada

| Capa | Herramienta | Archivo de config | En CI | En pre-commit |
|---|---|---|---|---|
| Linter (Python) | Ruff | `pyproject.toml [tool.ruff]` | ✅ | ✅ |
| Formatter (Python) | Black | `pyproject.toml [tool.black]` | ✅ (check) | ✅ |
| Tests (Python) | Pytest | `pyproject.toml [tool.pytest]` | ✅ | ❌ |
| Coverage | pytest-cov | `pyproject.toml` | ✅ (umbral 80%) | ❌ |
| SAST | Bandit | `pyproject.toml` | ✅ | opcional |
| Secretos | detect-secrets | `.pre-commit-config.yaml` | ✅ | ✅ |
| Dependencias | Safety / pip-audit | workflow | ✅ | ❌ |
