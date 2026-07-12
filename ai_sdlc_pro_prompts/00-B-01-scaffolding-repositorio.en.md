# 0-B.1 — Repository Scaffolding for New Project

## Description

Prompt to design and generate the base structure of a new repository: directories, configuration files, governance and standards, based on the selected project type, methodology, and technology stack.

**When to use:** when starting a new project, when migrating a project without formal structure, or when standardizing an existing repository that grew without guidance.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | medium — the proposed repository structure is costly to redo once the team starts building on it, even though the prompt does not write any files itself |
| Required inputs | project type, methodology, technology stack, hosting/CI platform, team composition, license type |
| Allowed tools | optional read of the current repository structure if one already exists — no write or execution required; the output is text for a human to apply |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if project type or stack are ambiguous, or an existing structure conflicts with the proposal, state the ambiguity and request confirmation before proposing a full restructuring |
| Expected output | see `## Expected Output` |
| Minimum evidence | the directory tree and file table are consistent with the declared project type and stack; each critical file (README, CONTRIBUTING, .gitignore, CODEOWNERS) includes base content, not just a name |
| Recommended next prompt | `00-B-03-github-configuracion` for GitHub protections and templates; `00-B-05-stack-calidad-codigo` to configure linters, formatters, and quality gates on top of the structure just created; `00-B-02-gobernanza-ia-agentes` to define AI agent governance over the structure just created; `00-B-04-metodologia-framework` to formalize the methodology and branching flow |

---

## Mandatory Previous Context

> Include the block from file `00-framework.en.md` before this prompt.

---

## Complete Prompt

```text
Objective:
Design the complete repository structure for this new project (or to standardize).

Required inputs:
- repository name: [NAME OR URL]
- project type: [frontend SPA / API REST / full-stack / microservice / monorepo / library / data science / IaC / other]
- working methodology: [SCRUM / Kanban / Trunk-Based / GitFlow / GitHub Flow / RUP / other]
- main technology stack: [e.g., Python + FastAPI + PostgreSQL / Node + React + MongoDB / etc.]
- hosting/CI platform: [GitHub / GitLab / Bitbucket / Azure DevOps]
- team: [size and roles present: e.g., 2 devs + 1 QA + AI agents]
- license type: [MIT / Apache 2.0 / proprietary / internal]

Deliver:

1. DIRECTORY TREE
   - complete structure with purpose of each folder
   - naming convention applied

2. MANDATORY ROOT FILES
   For each file indicate: name, purpose, and suggested base content:
   - README.md (minimum structure: description, installation, usage, contribution, license)
   - .gitignore (adapted to the stack)
   - .editorconfig
   - CONTRIBUTING.md (aligned with chosen methodology)
   - CHANGELOG.md (Keep a Changelog format / semver)
   - LICENSE
   - CODEOWNERS

3. TOOL CONFIGURATION
   Base configuration files according to the stack:
   - dependency manager (package.json / pyproject.toml / pom.xml / go.mod)
   - linter and formatter
   - pre-commit hooks (.pre-commit-config.yaml)
   - environment variables (.env.example — never real .env)
   - Docker (Dockerfile + docker-compose.yml if applicable)

4. .github/ FOLDER
   - ISSUE_TEMPLATE/ (bug_report.md, feature_request.md)
   - PULL_REQUEST_TEMPLATE.md
   - workflows/ (basic CI according to the stack)
   - dependabot.yml

5. docs/ FOLDER
   - architecture.md (architecture template)
   - decisions/ (folder for ADRs)
   - runbooks/ (folder for operational runbooks)

6. GAPS AND RISKS
   - what files cannot be generated automatically and require team decision
   - risks of omitting each section

Constraints:
- if the repository already has existing configuration files (package.json, pyproject.toml, .gitignore, workflows, etc.), do not propose overwriting them without explicitly flagging the conflict and requesting human confirmation before replacing their content,
- do not assume language, framework, or tool versions that were not declared as input — if the stack does not specify a version, flag it as a gap to confirm instead of inventing a "reasonable" one,
- if the current repository structure (folders, naming conventions, root files already present) conflicts with the proposal, flag the conflict explicitly in the GAPS AND RISKS section instead of proposing a silent restructuring,
- this prompt delivers text for a human to apply: do not generate shell commands that create or overwrite files directly.

Output format:
- directory tree with inline comments
- file table: name | purpose | priority (mandatory / recommended / optional)
- base content of critical files
```

---

## Usage with Standard Formula

```text
Use the repository scaffolding prompt and adapt it to:
- repo name: [NAME OR URL]
- project type: [PROJECT TYPE]
- methodology: [METHODOLOGY]
- stack: [STACK]
- CI/hosting platform: [PLATFORM]
- team: [COMPOSITION]
- license: [LICENSE TYPE]
- specific output goal: directory tree + file table + base content for README, CONTRIBUTING, .gitignore, Dockerfile
- depth level: high
```

---

## Expected Output

```
my-project/
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
├── src/                    ← source code
├── tests/                  ← tests
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

| File | Purpose | Priority |
|---|---|---|
| README.md | Project entry point | Mandatory |
| CONTRIBUTING.md | Contribution and branching rules | Mandatory |
| CODEOWNERS | Reviewer assignment by area | Mandatory |
| .gitignore | VCS exclusions adapted to the stack | Mandatory |
| .env.example | Documented environment variables (without real values) | Mandatory |
| CHANGELOG.md | Versioned change history | Recommended |
| .editorconfig | Format consistency between IDEs | Recommended |
| .pre-commit-config.yaml | Automatic validations before commit | Recommended |
| docs/architecture.md | High-level architecture decisions | Recommended |
| docs/decisions/ | Numbered ADRs (Architecture Decision Records) | Recommended |
| docs/runbooks/ | Operational procedures | Optional |

### Applied example: standardizing `ai-sdlc-prompts`

| File | Proposed base content (excerpt) | Conflict detected |
|---|---|---|
| `.gitignore` | Add `__pycache__/`, `dist/`, `.pytest_cache/` — the repo is Python (`build.py`) + Markdown content | None — the file does not yet exist at the root |
| `CODEOWNERS` | `ai_sdlc_pro_prompts/*.md @content-team` and `build.py tests/ @platform-team` | The README already assigns reviewers informally in prose — flag as a gap to confirm before replacing it with the formal file |
