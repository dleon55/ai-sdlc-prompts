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

Steps:
1. Identify the actor (user role) and the main flow end-to-end, from user input to the observable result in the system.
2. Define the preconditions needed (data state, session, permissions) for the flow to be reproducible.
3. Detail the steps as the user would execute them, in exact order, without skipping relevant intermediate interactions.
4. Define the expected observable result (UI, response, persisted state) and the minimum evidence required to consider it validated (screenshot, log, database record).
5. Identify related regressions: what other flows could break because of this change and should be re-verified.
6. Prioritize critical business flows (those that generate revenue, affect security, or have the highest usage volume) before secondary or rarely used flows.

Constraints:
- always run against a QA/STAGING environment, never directly against production,
- if the use case or acceptance criteria are not defined in enough detail to derive steps and expected result, stop and ask for clarification instead of assuming the behavior,
- each case must be independent: it must not depend on state left by a previous E2E case.

Deliver:
- E2E test matrix,
- related regressions to re-verify.
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
| Authenticated user | Update shipping address in profile | active session, at least one saved address | 1. Go to Profile → Addresses. 2. Edit existing address. 3. Save changes. | address is updated and appears preselected on the next checkout | screenshot of updated profile + database record | checkout with default address |
