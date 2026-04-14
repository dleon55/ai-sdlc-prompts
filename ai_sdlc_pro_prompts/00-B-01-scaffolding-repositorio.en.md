# 0-B.1 — Repository Scaffolding for New Project

## Description

Prompt to design and generate the base structure of a new repository: directories, configuration files, governance and standards, based on the selected project type, methodology, and technology stack.

**When to use:** when starting a new project, when migrating a project without formal structure, or when standardizing an existing repository that grew without guidance.

---

## Mandatory Previous Context

> Include the block from file `00-framework.en.md` before this prompt.

---

## Complete Prompt

```text
Objective:
Design the complete repository structure for this new project (or to standardize).

Required inputs:
- repository name: [NAME]
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

Output format:
- directory tree with inline comments
- file table: name | purpose | priority (mandatory / recommended / optional)
- base content of critical files
```

---

## Usage with Standard Formula

```text
Use the repository scaffolding prompt and adapt it to:
- repo name: [NAME]
- project type: [TYPE]
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
