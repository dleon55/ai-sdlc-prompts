# 7.2 — Integration test design

## Description

Prompt to define integration tests that validate the interaction between modules, services, APIs, database and integrations involved in the change.

**When to use it:** after unit tests (`07-01`), to validate that modules work correctly together.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | low — produces an integration test plan as a design artifact, does not run tests or modify the repository |
| Required inputs | API contracts, integration design, available test data, unit test matrix (`07-01`) if it exists |
| Allowed tools | read-only access to contracts, integration design, and code; does not run tests or write files, only produces the plan |
| Permitted autonomy | A1 — Propose (integration test plan without implementing it) |
| Stop criteria | stop if there are no reference API contracts or integration design; never use real production data as test data, only synthetic or anonymized data |
| Expected output | see `## Expected output` |
| Minimum evidence | each flow with explicit integrated components, test data, and error validation |
| Recommended next prompt | `07-08-implementacion-pruebas-integracion` to turn the plan into executable tests |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Define the integration tests necessary to validate the interaction between modules, services, APIs, database and integrations involved.

Include:
- flow,
- integrated components,
- test data,
- expected result,
- error validation.
```

---

## Use with standard formula

```text
Use the integration tests prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [TEST BRANCH]
- environment: [QA / STAGING]
- components: [MODULES AND INTEGRATIONS TO TEST]
- documents to review: API contracts, integration design, available test data
- specific output objective: integration test plan with error cases
- depth level: high
```

---

## Expected output

| Flow | Components | Test data | Expected result | Error cases |
|---|---|---|---|---|
