# 7.3 — E2E test design

## Description

Prompt to design end-to-end tests for the use cases impacted by the change: from actor to final result, including required evidence and related regressions.

**When to use it:** after integration tests (`07-02`), to validate the complete flow from the user perspective.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design — produces an E2E test plan as a table, not executable code |
| Expected risk | low — it is a planning document; it does not modify systems or execute tests |
| Required inputs | use case or requirement to cover, acceptance criteria, reference to the prior integration plan (`07-02`) |
| Allowed tools | read-only access to documentation (use cases, acceptance criteria, documented flows); no write access or execution required |
| Permitted autonomy | A1 — Propose (delivers a plan/artifact without applying it; execution happens in `07-09`) |
| Stop criteria | stop and request clarification if the use case or acceptance criteria are not defined in enough detail to derive steps, expected result, and evidence |
| Expected output | see `## Expected output` |
| Minimum evidence | each table row must specify actor, flow, preconditions, steps, expected result, required evidence, and related regressions |
| Recommended next prompt | `07-09-implementacion-pruebas-e2e` to turn this plan into executable E2E scripts |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design end-to-end tests for the use cases impacted by the change.

Include:
- actor,
- main flow,
- preconditions,
- steps,
- expected result,
- required evidence,
- related regressions.
```

---

## Use with standard formula

```text
Use the E2E tests prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [TEST BRANCH]
- environment: [QA / STAGING]
- components: [FLOWS AND MODULES TO TEST]
- documents to review: use cases, acceptance criteria, documented flows
- specific output objective: E2E test plan with required evidence per case
- depth level: high
```

---

## Expected output

| Actor | Flow | Preconditions | Steps | Expected result | Evidence | Regressions |
|---|---|---|---|---|---|---|
