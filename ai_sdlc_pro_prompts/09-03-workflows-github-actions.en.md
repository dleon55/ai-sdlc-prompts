# 9.3 — GitHub Actions workflows review

## Description

Prompt to audit the repository workflows and verify if they adequately cover validation, tests, security, deployment and quality. Detects gaps, risks and proposes improvements.

**When to use it:** periodically as pipeline health review, or when incorporating new modules or environments.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — does not modify workflows directly, only audits and recommends |
| Required inputs | contents of `.github/workflows/`, CI/CD README |
| Allowed tools | reading workflow files — no job execution or pipeline changes |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if a workflow references secrets or permissions that cannot be inspected without access to the repository configuration, document it as a visibility gap instead of assuming its state |
| Expected output | see `## Expected output` |
| Minimum evidence | each reported gap must cite the workflow file and the specific job |
| Recommended next prompt | `11-02-hardening-seguridad` if security gaps are detected in the pipeline |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze the repository workflows and determine if they adequately cover validation, tests, security, deployment and quality.

Include:
- workflow inventory,
- triggers,
- jobs,
- existing validations,
- missing ones,
- risks,
- recommended improvements.
```

---

## Use with standard formula

```text
Use the workflows review prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [MAIN BRANCH]
- documents to review: .github/workflows/, CI/CD README
- specific output objective: workflows inventory with gaps and recommended improvements
- depth level: medium
```

---

## Expected output

### Workflow inventory

| Workflow | File | Trigger | Jobs | Purpose |
|---|---|---|---|---|

### Coverage analysis

| Area | Covered | Workflow | Missing | Risk | Recommendation |
|---|---|---|---|---|---|
| validation / lint | | | | | |
| build | | | | | |
| unit tests | | | | | |
| integration tests | | | | | |
| security analysis | | | | | |
| DEV deploy | | | | | |
| QA deploy | | | | | |
| PROD deploy | | | | | |
| notifications | | | | | |
