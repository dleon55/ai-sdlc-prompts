# 10.2 — Technical memory of the change

## Description

Prompt to generate a clear and executive technical memory of the change made: context, problem, analysis, implemented solution, tests, risks, results and pending points.

**When to use it:** at the close of each issue or sprint, as a formal record of the work performed for audit and future reference.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | low — generates an audit/record document; does not act on the system, but as an input to formal audit, inaccuracies undermine traceability of the change |
| Required inputs | issue or requirement, integrated branch, environment, modified components, commits/PRs, approved design, executed test results |
| Allowed tools | read-only access (commits, PRs, approved design, test results); does not execute commands or modify the repository |
| Permitted autonomy | A1 — Propose: drafts the technical memory document; does not publish or archive it itself |
| Stop criteria | if test results are missing or the approved design is unavailable, it must flag that explicitly in the relevant section instead of inventing results |
| Expected output | see `## Expected output` |
| Minimum evidence | each section (root cause, executed tests, risks) is backed by a verifiable reference (commit, PR, or test result), not generic |
| Recommended next prompt | `10-03-release-changelog` if the change is grouped into a release; `11-03-deuda-tecnica` to record pending points as formal technical debt |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Generate a clear and executive technical memory of the change made.

Include:
1. context
2. problem or requirement
3. analysis
4. root cause if applicable
5. implemented solution
6. modified components
7. executed tests
8. risks
9. results
10. pending points
```

---

## Use with standard formula

```text
Use the technical memory prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [INTEGRATED BRANCH]
- environment: [PROD / STAGING]
- components: [MODIFIED COMPONENTS]
- documents to review: commits, PRs, approved design, test results
- specific output objective: complete technical memory for audit
- depth level: high
```

---

## Expected output

| Section | Content |
|---|---|
| Context | Change background |
| Problem / Requirement | What needed to be resolved |
| Analysis | Findings from previous analysis |
| Root cause | If applicable, confirmed cause |
| Implemented solution | What was done exactly |
| Modified components | List of files and modules |
| Executed tests | Test types and results |
| Risks | Residual or pending |
| Results | Final system state |
| Pending points | Derived tasks or new debt |
