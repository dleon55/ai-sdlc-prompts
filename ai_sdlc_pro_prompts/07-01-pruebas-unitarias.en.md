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

Steps:
1. Identify the function or unit under test: signature, input/output types, side effects, and external dependencies (I/O, network, time, randomness).
2. Enumerate scenarios per unit: positive cases (happy path), negative cases (invalid input or expected error), and edge cases (limits, empty, null, extreme values).
3. For each scenario, define the exact input and expected result (return value, thrown exception, or observable side effect).
4. Identify which external dependencies must be mocked or isolated so the test is deterministic and does not depend on network, a real database, or the file system.
5. Prioritize: if time is limited, cover business logic with branching (if/switch) and numeric edge cases first, before trivial getters/setters.
6. Recommend a target coverage level and explicitly flag what is out of scope for unit tests (belongs to integration `07-02` or E2E `07-03`).

Constraints:
- each test must be independent and must not depend on execution order or state shared with other tests,
- don't replicate private implementation details if an equivalent public API exists to test instead,
- don't use sleep or fixed delays to synchronize async tests — use time mocks or wait-for-condition instead,
- if the recommended coverage cannot be achieved with the available information, flag it instead of inventing scenarios.

Deliver:
- unit test matrix,
- coverage recommendation,
- list of dependencies to mock or isolate.
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
| calculateDiscount() | valid discount within range | price=100, percentage=10 | 90 | positive |
| calculateDiscount() | negative percentage | price=100, percentage=-5 | throws ValueError | negative |
| calculateDiscount() | percentage at upper bound (100%) | price=100, percentage=100 | 0 | edge |
