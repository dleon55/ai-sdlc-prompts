# 7.1 — Unit test design

## Description

Prompt to design the unit test suite that validates the proposed or implemented changes: positive, negative and edge cases for each function or unit under test.

**When to use it:** after implementing changes, in parallel with implementation, or as reference before writing code.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | low — produces a test case matrix as a design artifact, does not implement or run test code |
| Required inputs | implemented code or proposed changes, acceptance criteria, test stack profile (`07-00`) if available |
| Allowed tools | read-only access to code and acceptance criteria; does not run tests or write test files, only produces the design matrix |
| Permitted autonomy | A1 — Propose (test matrix as an artifact, without implementing the test code) |
| Stop criteria | stop if there is no reference code or acceptance criteria; explicitly flag if the recommended coverage cannot be achieved with the available information instead of inventing scenarios |
| Expected output | see `## Expected output` |
| Minimum evidence | each function/unit under test documented with at least one positive, one negative, and one edge case |
| Recommended next prompt | `07-07-implementacion-pruebas-unitarias` to turn the matrix into executable test code |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design the unit tests necessary to validate the proposed or implemented changes.

Include:
- function or unit under test,
- scenario,
- input,
- expected result,
- positive cases,
- negative cases,
- edge cases.

Deliver:
- unit test matrix,
- coverage recommendation.
```

---

## Use with standard formula

```text
Use the unit tests prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [TEST BRANCH]
- environment: [DEV / QA]
- components: [FUNCTIONS OR UNITS TO TEST]
- documents to review: implemented code, acceptance criteria
- specific output objective: complete unit test matrix with coverage
- depth level: high
```

---

## Expected output

| Function/Unit | Scenario | Input | Expected | Type |
|---|---|---|---|---|
