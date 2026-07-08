# 8.2 — Requirement compliance review

## Description

Prompt to validate if the implementation really complies with the issue, requirement, use case and acceptance criteria. Compares what was requested, what was designed, what was implemented and what was tested.

**When to use it:** before closing an issue or opening a PR for merge, as a quality closure step.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | validation |
| Expected risk | medium — the verdict determines whether an issue can be closed; a false "compliant" can close incomplete work and a false "non-compliant" blocks unnecessarily |
| Required inputs | original issue or requirement, approved design, implemented code, test results |
| Allowed tools | reading the issue, design, code and existing test results — no new test execution or code modification |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if any of the four inputs to compare is missing (requested, designed, implemented or tested), stop and report it as an evidence gap before issuing a compliance verdict |
| Expected output | see `## Expected output` |
| Minimum evidence | each acceptance criterion must be marked as fully met, partial or not met, with the specific gap cited in the matrix |
| Recommended next prompt | `09-01-integracion-ramas` if compliance is total and the change is ready to integrate |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Validate if the implementation really complies with the issue, requirement, use case and acceptance criteria.

Compare:
- what was requested,
- what was designed,
- what was implemented,
- what was tested.

Deliver:
- total/partial/non compliance,
- detected differences,
- risks for non-compliance,
- required actions.
```

---

## Use with standard formula

```text
Use the requirement compliance prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [BRANCH WITH CHANGES]
- documents to review: original issue, approved design, implemented code, test results
- specific output objective: compliance matrix with gaps and required actions
- depth level: high
```

---

## Expected output

| Acceptance criteria | Requested | Designed | Implemented | Tested | Status | Gap |
|---|---|---|---|---|---|---|

### Compliance result

| Item | Status | Differences | Risk | Required action |
|---|---|---|---|---|
