# 3.1 — Review of incidents reported by tester against GitHub Issues

## Description

Prompt to normalize testing incidents, compare them against existing issues in GitHub, detect duplicates, incomplete or poorly documented ones, and draft those that do not exist with the project standard.

**When to use it:** when receiving a QA cycle report, before managing any defect in GitHub.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — misclassifying an incident as duplicate or "already exists" can hide a real, unreported defect |
| Required inputs | normalized QA incident report, read access to open and closed GitHub issues |
| Allowed tools | reading/searching GitHub issues — no creating, closing, commenting on, or modifying issues |
| Permitted autonomy | A1 — Propose (drafts issues and actions, does not execute them) |
| Stop criteria | the prompt itself explicitly restricts its scope to analysis and drafting; never run mutation actions on GitHub |
| Expected output | see `## Expected output` |
| Minimum evidence | each classified incident must reference the equivalent GitHub issue (or its confirmed absence) |
| Recommended next prompt | `03-02-causa-raiz` if a confirmed incident requires root cause investigation |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze the incidents reported by testing and compare them with existing issues in GitHub to determine if they already exist, if they are well documented and what their current status is.

Activities:
1. Normalize each incident:
   - title,
   - description,
   - steps to reproduce,
   - current result,
   - expected result,
   - severity,
   - environment,
   - module.
2. Search for equivalents in GitHub.
3. Classify each incident:
   - exists and is correct,
   - exists but is incomplete,
   - exists but is poorly documented,
   - is a duplicate of another already-reported incident,
   - does not exist.
4. Propose action:
   - comment,
   - update,
   - reopen,
   - create,
   - relate,
   - mark as duplicate.
5. If it does not exist, draft the complete issue with the project standard.

Restrictions:
This prompt is analysis and drafting only. Do not run commands that create, close, comment on, or modify issues in GitHub; deliver only the proposed actions and the drafted content for human review.

Output:
1. Executive summary
2. QA vs GitHub matrix
3. Issues to create
4. Issues to update
5. Issues with traceability problems
6. Recommendations for improvement to the QA → GH process
```

---

## Use with standard formula

```text
Use the incident review prompt and adapt it to:
- repository: [NAME OR URL]
- QA report: [PASTE LIST OF INCIDENTS]
- branch: [BRANCH IN TESTING]
- environment: [QA / STAGING]
- tested modules: [MODULES]
- documents to review: open and closed issues in GitHub, issue documentation standard
- specific output objective: QA vs GitHub matrix + drafted issues to create/update
- depth level: high
```

---

## Expected output

### Executive summary

| Metric | Value |
|---|---|
| Total reported incidents | 14 |
| Exist and are correct | 6 |
| Exist but incomplete | 3 |
| Do not exist | 4 |
| Duplicates | 1 |

### QA vs GitHub Matrix

| Incident | Severity | GH Issue | Current status | Proposed action |
|---|---|---|---|---|
| INC-014 — build.py doesn't validate ES/EN pair before publishing | high | none found | Does not exist | Create |
| INC-015 — intermittent timeout in test_build_unit | medium | #138 | Exists, incomplete (missing environment and steps) | Comment requesting missing data |
| INC-016 — same symptom as INC-014 reported by another tester | high | (same as INC-014, still no issue) | Duplicate of INC-014 | Mark duplicate, don't create a new issue |

### Issues to create

| Incident | Proposed title | Severity | Labels |
|---|---|---|---|
| INC-014 | fix: build.py doesn't validate ES/EN pair before publishing | high | bug, ai-agent |

### Issues to update / with traceability problems

| GH Issue | Detected problem | Proposed action |
|---|---|---|
| #138 | Missing environment and exact reproduction steps | Comment requesting the missing fields before closing |

### Recommendations for improvement to the QA → GH process

- Example: standardize that every QA report include the environment and version before normalizing it, to avoid the "comment requesting missing data" cycle on every round.
