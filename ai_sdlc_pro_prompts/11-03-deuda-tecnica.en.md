# 11.3 — Technical debt and continuous improvement

## Description

Prompt to identify the technical debt of the repository and generate a prioritized improvement backlog classified by architecture, code, tests, documentation, security, CI/CD, observability, data and performance.

**When to use it:** at the close of a sprint, in periodic technical reviews, or when planning structural project improvements.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | low — generates an inventory and prioritized backlog; does not modify code or systems |
| Required inputs | main branch, components or modules to analyze, access to source code, tests, CI/CD configuration, architecture and documentation |
| Allowed tools | read-only access to the repository (code, tests, CI/CD configuration, documentation) |
| Permitted autonomy | A0 — Analyze: inventory and recommendations, without applying changes |
| Stop criteria | if it cannot access an area declared as "to analyze" (nonexistent module or outside the repo), it must flag the omission instead of completing the matrix with assumptions |
| Expected output | see `## Expected output` |
| Minimum evidence | each matrix item references a real file, module, or configuration in the repository, with priority, impact, and effort justified |
| Recommended next prompt | `05-01-plan-implementacion` to plan the resolution of prioritized items; `11-06-gestion-parches-actualizaciones` if the identified debt is outdated dependencies |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Identify technical debt in the repository and propose a prioritized backlog of improvements.

Classify by:
- architecture,
- code,
- tests,
- documentation,
- security,
- CI/CD,
- observability,
- data,
- performance.

Deliver:
- technical debt matrix,
- priority,
- impact,
- estimated effort,
- attention recommendation.
```

---

## Use with standard formula

```text
Use the technical debt prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [MAIN BRANCH]
- components: [MODULES OR AREAS TO ANALYZE]
- documents to review: source code, tests, CI/CD, architecture, docs
- specific output objective: prioritized technical debt backlog with estimated effort
- depth level: high
```

---

## Expected output

| Item | Category | Description | Priority | Impact | Effort | Recommendation |
|---|---|---|---|---|---|---|
