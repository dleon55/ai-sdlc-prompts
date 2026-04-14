# 3.1 — Review of incidents reported by tester against GitHub Issues

## Description

Prompt to normalize testing incidents, compare them against existing issues in GitHub, detect duplicates, incomplete or poorly documented ones, and draft those that do not exist with the project standard.

**When to use it:** when receiving a QA cycle report, before managing any defect in GitHub.

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
   - does not exist.
4. Propose action:
   - comment,
   - update,
   - reopen,
   - create,
   - relate,
   - mark as duplicate.
5. If it does not exist, draft the complete issue with the project standard.

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
| Total reported incidents | |
| Exist and are correct | |
| Exist but incomplete | |
| Do not exist | |
| Duplicates | |

### QA vs GitHub Matrix

| Incident | Severity | GH Issue | Current status | Proposed action |
|---|---|---|---|---|
