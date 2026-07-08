# 1.1 — Repository technical inventory

## Description

Starter prompt to build an initial technical inventory of the repository: structure, workspaces/sub-modules, detected technologies, engineering-cycle artifacts, and relevant gaps. This is the recommended first step before any analysis or implementation on a new or unfamiliar repository.

**When to use it:** when starting work on a repository with no prior context, or to refresh the inventory after significant structural changes.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
I want you to comprehensively analyze this repository and build an initial technical inventory of the project.

Activities:
1. Review the complete structure of the repository (detecting if it is a monorepo or modular project).
2. Identify:
   - workspaces / subprojects / sub-modules,
   - dependencies and boundaries between internal packages,
   - components,
   - modules,
   - layers,
   - services,
   - internal libraries,
   - scripts,
   - pipelines,
   - tests,
   - documentation,
   - configuration files,
   - containers,
   - migrations,
   - environment variables.
3. Detect technologies used:
   - frontend,
   - backend,
   - database,
   - infrastructure,
   - messaging,
   - authentication,
   - observability.
4. Locate engineering cycle artifacts and compliance standards (PSP, ISO, etc.):
   - analysis,
   - design,
   - use cases,
   - diagrams,
   - implementation,
   - tests,
   - CI/CD,
   - documentation.
5. Detect relevant gaps or absences.

Output format:
1. Executive summary
2. Inventory of folders and purpose
3. Detected architecture
4. Technologies and versions found
5. Processes/documentation located
6. Risks or gaps
7. Recommended review order
```

---

## Use with standard formula

```text
Use the repository technical inventory prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [MAIN BRANCH]
- documents to review: complete source code, configuration, existing documentation
- specific output objective: initial technical inventory with detected risks and gaps
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Executive summary | High-level overview of the repository in a few lines |
| Folder inventory | Structure and purpose of each main folder |
| Detected architecture | Monorepo/modular, layers, components, and services identified |
| Technologies | Frontend, backend, DB, infrastructure, messaging, auth, observability stack |
| Processes/documentation | Engineering-cycle artifacts already present |
| Risks or gaps | Relevant absences detected |
| Review order | Recommendation on where to continue the analysis |
