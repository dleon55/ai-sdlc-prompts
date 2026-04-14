# 0-B.5 — Stack and Code Quality Tools Configuration

## Description

Prompt to select and configure code quality tools according to the project stack: linters, formatters, static analyzers, pre-commit hooks, minimum coverage, and quality gates in CI. Generates ready-to-use configuration files.

**When to use:** when starting a project, when standardizing quality in an existing one, or when AI agents are being incorporated that must respect the stack conventions.

---

## Mandatory Previous Context

> Include the block from file `00-framework.en.md` before this prompt.

---

## Complete Prompt

```text
Objective:
Select and configure code quality tools for this project's stack.

Required inputs:
- main language(s): [Python / JavaScript / TypeScript / Java / Go / other]
- framework(s): [FastAPI / Django / React / Vue / Spring / other]
- CI platform: [GitHub Actions / GitLab CI / other]
- desired minimum coverage: [e.g., 80%]
- restriction level: [permissive / balanced / strict]

Deliver:

1. RECOMMENDED TOOLS BY LAYER
   For each detected language, indicate:
   - linter: tool + recommended version + justification
   - formatter: tool + base configuration
   - static security analyzer (SAST): recommended tool
   - vulnerable dependency analyzer: recommended tool
   - testing framework: tool + recommended runner
   - coverage measurement: tool + minimum threshold configuration

2. CONFIGURATION FILES (complete content ready to copy)
   According to the stack, generate those that apply:
   - .eslintrc.json / eslint.config.js (JavaScript/TypeScript)
   - .prettierrc (JavaScript/TypeScript)
   - pyproject.toml with [tool.ruff], [tool.black], [tool.pytest.ini_options] (Python)
   - .flake8 or ruff.toml (Python alternative)
   - .editorconfig (all languages)
   - sonar-project.properties (if using SonarQube/SonarCloud)

3. PRE-COMMIT HOOKS (.pre-commit-config.yaml)
   Minimum recommended hooks:
   - trailing-whitespace
   - end-of-file-fixer
   - check-yaml / check-json
   - stack linter (in fast mode)
   - stack formatter
   - secret detection (detect-secrets or gitleaks)
   - check-added-large-files
   Include the complete .pre-commit-config.yaml file and installation command.

4. QUALITY GATES IN CI (.github/workflows/quality.yml)
   Workflow that runs:
   - lint
   - format check (fail if there are pending formatting changes)
   - SAST
   - tests + coverage with minimum threshold (fail if not reached)
   - vulnerable dependency analysis
   Configure as required check in branch protection.

5. RULES FOR AI AGENTS
   Instructions that should be added to .github/copilot-instructions.md and .windsurfrules:
   - "always run [formatter] before proposing changes"
   - "don't disable linter rules with inline comments without justification"
   - "minimum coverage of [X]% for new code"
   - "don't add dependencies without verifying CVEs in [tool]"

6. BOOTSTRAP COMMANDS
   Sequence of commands to set up the environment from scratch:
   - installation of development tools
   - installation of pre-commit hooks
   - initial execution of all checks
   - verification that the CI pipeline passes in green

Output format:
- tools table by layer
- complete configuration files
- complete CI workflow
- bootstrap commands in order
```

---

## Usage with Standard Formula

```text
Use the stack and code quality configuration prompt and adapt it to:
- language(s): [LANGUAGES]
- frameworks: [FRAMEWORKS]
- CI platform: [CI]
- minimum coverage: [PERCENTAGE]
- restriction level: [PERMISSIVE / BALANCED / STRICT]
- specific output goal: complete configuration files + CI quality gates workflow + bootstrap commands
- depth level: high
```

---

## Expected Output

| Layer | Tool | Config File | In CI | In pre-commit |
|---|---|---|---|---|
| Linter (Python) | Ruff | `pyproject.toml [tool.ruff]` | ✅ | ✅ |
| Formatter (Python) | Black | `pyproject.toml [tool.black]` | ✅ (check) | ✅ |
| Tests (Python) | Pytest | `pyproject.toml [tool.pytest]` | ✅ | ❌ |
| Coverage | pytest-cov | `pyproject.toml` | ✅ (threshold 80%) | ❌ |
| SAST | Bandit | `pyproject.toml` | ✅ | optional |
| Secrets | detect-secrets | `.pre-commit-config.yaml` | ✅ | ✅ |
| Dependencies | Safety / pip-audit | workflow | ✅ | ❌ |
