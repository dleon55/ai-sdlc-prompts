# 10.2 — Technical memory of the change

## Description

Prompt to generate a clear and executive technical memory of the change made: context, problem, analysis, implemented solution, tests, risks, results and pending points.

**When to use it:** at the close of each issue or sprint, as a formal record of the work performed for audit and future reference.

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
