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

Steps:
1. Identify the flow to test and the components that interact in it (services, internal/external APIs, database, queues, cache).
2. Define the test data needed to exercise the full flow — synthetic or anonymized, never real production data.
3. For each integration point, specify the expected result on the happy path and at least one failure case (timeout, error response, inconsistent data).
4. Define how the resulting state is validated (HTTP response, database record, emitted event) and what must be cleaned up after the test.
5. Flag which external integrations must be simulated (mocks/stubs/contract testing) because they are not controllable or stable in the test environment.
6. Prioritize critical business flows and integrations with the highest failure probability (third-party services, async queues) before stable internal integrations.

Constraints:
- never use real production data as test data, only synthetic or anonymized data,
- each integration test must be repeatable without leaving residual state (idempotency or explicit cleanup),
- if a reference API contract or integration design is missing, stop and flag it instead of assuming the behavior.

Deliver:
- integration test plan,
- list of external integrations to simulate,
- test data and cleanup strategy.
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
| User registration | auth API, database, email service (mock) | synthetic user with unique email | user created, welcome email queued | duplicate email returns 409 without creating the record |
| Purchase checkout | cart API, payments API (stub), database, event queue | cart with 2 items, test card | order created, `order.created` event emitted | rejected payment rolls back the order and does not emit the event |
