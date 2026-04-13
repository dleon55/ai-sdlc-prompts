# 8.3 — Static review remediation (master prompt)

## Description

Production-level master prompt to analyze a static review report with critical, medium and minor findings, and generate a comprehensive, controlled and safe correction plan for multi-agent environments.

**When to use it:** when a static review report is received and a structured correction plan is needed, not just superficial patches.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete master prompt

```text
Act as a Senior Software Engineer, Solutions Architect, QA Lead and DevOps Engineer with experience in PSP, RUP, DevSecOps, CI/CD and code review in productive systems.

Context:
I am working in a multi-agent environment with Open Agent Manager. Other agents may be modifying the repository in parallel.

Input:
I provide you with a static code review report with critical, medium, minor findings and technical debt.

Document:
[PASTE COMPLETE REPORT HERE]

Objective:
I want you to analyze this report and generate an integral, controlled and quality solution to correct the findings without affecting system stability.

---

CRITICAL RULES:
1. DO NOT implement directly.
2. First analyze, then design, then plan.
3. Consider impact on:
   - architecture
   - database
   - frontend/backend
   - integrations
   - CI/CD
   - other agents working in parallel
4. Do not propose changes without justification.
5. Detect dependencies between findings.
6. Prioritize system stability over speed.

---

PHASE 1 — REPORT ANALYSIS:
For each finding:
1. Validate if it really applies to the code
2. Classify: critical / medium / minor / technical debt
3. Identify: root cause, affected component, risk
4. Detect: duplications and dependencies between findings

---

PHASE 2 — SOLUTION DESIGN:
For each finding:
- proposed solution
- alternative (if applicable)
- technical impact
- impact on other modules
- implementation risks

Additionally:
1. Propose global refactorings if there are structural problems
2. Propose centralization (ex: duplicated constants)
3. Propose architecture improvements if applicable

---

PHASE 3 — QUALITY STRATEGY:
Define:
1. Necessary unit tests
2. Integration tests
3. E2E tests
4. Regression tests
5. Negative cases

Include: what to validate, how to validate, risk covered

---

PHASE 4 — CONTROLLED IMPLEMENTATION PLAN:
Generate detailed plan:
| Step | Change | File | Risk | Validation |

Consider:
- correct order of changes
- dependencies between fixes
- concurrency with other agents
- atomic commits
- rollback

---

PHASE 5 — INTEGRATION STRATEGY:
Define:
- branch strategy
- conflict handling
- CI validation
- PR validation
- merge conditions

---

PHASE 6 — RISK ANALYSIS:
Generate matrix:
| Risk | Probability | Impact | Mitigation |

---

MANDATORY OUTPUT FORMAT:
1. Executive summary
2. Report validation (what applies and what doesn't)
3. Analysis per finding
4. Root cause
5. Solution design
6. Quality strategy
7. Implementation plan
8. Integration strategy
9. Risks and mitigation
10. Final recommendation

QUALITY RULES:
- No superficial solutions
- No isolated changes without context
- Do not ignore impact on other modules
- Do not assume behavior without evidence
- If something is unclear → declare it
```

---

## Execution prompt (second step)

Once the above analysis is approved, use this prompt for execution:

```text
Based on the previously generated analysis and plan:

Objective:
Implement the changes in a controlled manner in a multi-agent environment.

Rules:
- minimal changes per commit
- one finding per commit
- do not modify outside the scope
- validate before each commit

For each change:
1. affected file
2. exact change
3. validation
4. suggested commit

If you detect conflict:
STOP execution and document the conflict before continuing.
```

---

## Use with standard formula

```text
Use the remediation master prompt and adapt it to:
- repository: [NAME OR URL]
- static review report: [PASTE REPORT]
- branch: [BRANCH WITH CHANGES]
- environment: [DEV / QA]
- components: [REVIEWED COMPONENTS]
- documents to review: source code, architecture, contracts
- specific output objective: executable and prioritized remediation plan
- depth level: high
```

---

## Expected output

### Report validation

| Finding | Applies | Classification | Component | Root cause |
|---|---|---|---|---|

### Remediation plan

| Step | Change | File | Risk | Validation | Suggested commit |
|---|---|---|---|---|---|

### Risk matrix

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
