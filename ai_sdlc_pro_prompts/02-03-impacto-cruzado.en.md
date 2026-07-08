# 2.3 — Cross-impact analysis

## Description

Prompt to evaluate the impact of the change on all modules, processes, data, integrations, environments and pipelines of the system. Detects direct and indirect impacts and generates a severity matrix.

**When to use it:** after deep technical analysis (`02-02`) and before solution design (`04-01`).

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — although read-only, it has a wide blast radius (modules, data, integrations, environments, pipelines, semver); underestimating an impact can let a breaking change or an undetected production risk slip through |
| Required inputs | output of `02-02` (technical flow and dependencies), architecture, API contracts, database schema, involved components |
| Allowed tools | reading of code, architecture, contracts, and configuration — no execution or changes |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if there is not enough evidence to rule out impact on a critical component (security, data, production, semver), classify it as an unconfirmed high risk instead of omitting it from the matrix |
| Expected output | see `## Expected output` |
| Minimum evidence | every row of the impact matrix must cite the verified component or contract, not just one assumed by name or convention |
| Recommended next prompt | `04-01-diseno-solucion` |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze the impact of the requested change on other modules, processes, data, integrations, environments, pipelines, monorepo workspaces/subprojects, and versioning policies (semver).

Activities:
1. Evaluate impact on:
   - monorepo workspaces / subprojects (for example, shared dependencies, common utility packages),
   - API contracts and semantic versioning (semver) of local packages,
   - frontend,
   - backend,
   - database,
   - integrations,
   - infrastructure,
   - CI/CD (independent or shared build pipelines),
   - security and regulatory compliance (ISO, MAAGTICSI, etc.),
   - monitoring,
   - documentation.
2. Detect direct and indirect impacts.
3. Evaluate affectation to other use cases.

Output:
- impact matrix (including monorepo workspaces and packages),
- severity,
- affected component/workspace,
- impact type (direct/indirect, breaking changes in local dependencies),
- risk,
- mitigation recommendation.
```

---

## Use with standard formula

```text
Use the cross-impact analysis prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [CURRENT BRANCH]
- environment: [DEV / QA / PROD]
- components: [INVOLVED COMPONENTS]
- documents to review: architecture, API contracts, DB schema
- specific output objective: cross-impact matrix with severity by component
- depth level: high
```

---

## Expected output

| Component | Impact type | Severity | Risk | Recommendation |
|---|---|---|---|---|
| frontend | | | | |
| backend | | | | |
| database | | | | |
| integrations | | | | |
| infrastructure | | | | |
| CI/CD | | | | |
| security | | | | |
| monitoring | | | | |
| documentation | | | | |
