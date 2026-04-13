# 8.2 — Requirement compliance review

## Description

Prompt to validate if the implementation really complies with the issue, requirement, use case and acceptance criteria. Compares what was requested, what was designed, what was implemented and what was tested.

**When to use it:** before closing an issue or opening a PR for merge, as a quality closure step.

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
