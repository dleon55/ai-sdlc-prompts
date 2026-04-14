# 7.3 — E2E test design

## Description

Prompt to design end-to-end tests for the use cases impacted by the change: from actor to final result, including required evidence and related regressions.

**When to use it:** after integration tests (`07-02`), to validate the complete flow from the user perspective.

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

| Use case | Actor | Preconditions | Steps | Expected result | Evidence |
|---|---|---|---|---|---|
