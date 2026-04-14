# 9.3 — GitHub Actions workflows review

## Description

Prompt to audit the repository workflows and verify if they adequately cover validation, tests, security, deployment and quality. Detects gaps, risks and proposes improvements.

**When to use it:** periodically as pipeline health review, or when incorporating new modules or environments.

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
