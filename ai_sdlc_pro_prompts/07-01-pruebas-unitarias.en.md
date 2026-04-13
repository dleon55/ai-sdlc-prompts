# 7.1 — Unit test design

## Description

Prompt to design the unit test suite that validates the proposed or implemented changes: positive, negative and edge cases for each function or unit under test.

**When to use it:** after implementing changes, in parallel with implementation, or as reference before writing code.

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
