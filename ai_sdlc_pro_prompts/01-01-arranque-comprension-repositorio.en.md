# 1.1 — Repository technical inventory

## Description

Starter prompt to build an initial technical inventory of the repository: structure, workspaces/sub-modules, detected technologies, engineering-cycle artifacts, and relevant gaps. This is the recommended first step before any analysis or implementation on a new or unfamiliar repository.

**When to use it:** when starting work on a repository with no prior context, or to refresh the inventory after significant structural changes.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | low — this is a read-only inventory; a gap or inaccuracy is corrected in later iterations and does not produce repository changes |
| Required inputs | read access to the complete repository (source code, configuration, existing documentation); no reference issue or incident required |
| Allowed tools | reading of folder structure, code, configuration, and documentation — no execution or changes |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if parts of the repository are inaccessible or the monorepo has unresolved workspaces, state the covered scope and gaps instead of inferring unverified structure |
| Expected output | see `## Expected output` |
| Minimum evidence | every folder, technology, or artifact listed in the inventory must correspond to a verifiable path or file in the repository |
| Recommended next prompt | `01-02-analisis-procesos` to map project governance; `02-01-analisis-issue` if a concrete issue or requirement already exists to address |

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
