# 8.3 — Static review remediation (master prompt)

## Description

Production-level master prompt to analyze a static review report with critical, medium and minor findings, and generate a comprehensive, controlled and safe correction plan for multi-agent environments.

**When to use it:** when a static review report is received and a structured correction plan is needed, not just superficial patches.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis (block 1) and execution (block 2) — explicit two-phase prompt |
| Expected risk | high — the execution block modifies code, potentially in production |
| Required inputs | static review report with critical, medium, and minor findings |
| Allowed tools | block 1: reading code and documentation; block 2: editing files and running local tests, no push/deploy without approval |
| Permitted autonomy | A1 — Propose (block 1); A2 — Execute controlled (block 2, only after human approval of block 1's plan) |
| Stop criteria | do not start the execution block without explicit approval of the analysis plan; stop if a proposed change affects system stability without a clear mitigation |
| Expected output | see `## Expected output` |
| Minimum evidence | each step of the remediation plan must list file, risk, and associated validation |
| Recommended next prompt | `07-01-pruebas-unitarias` / `07-02-pruebas-integracion` to validate the applied remediation |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete master prompt

```text
PHASE 1 OF 2 — ANALYSIS ONLY. Do not implement changes in this phase; the output is a plan that requires human approval before moving to Phase 2 (execution, next block).

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

CONSTRAINTS:
- this phase is analysis-only: don't edit files, don't run build/test commands beyond reading, and don't create commits or branches in this block,
- any finding from the original report that you decide to discard must be explicitly justified; don't silently drop it from the plan,
- the Phase 4 plan must precisely bound the scope of each change (file and component) — any work that falls outside that scope requires a new analysis-and-approval cycle, it is not executed as part of the same plan,
- don't mark any finding as resolved or imply implementation already happened; the output of this phase is a proposal pending human approval.
```

---

## Execution prompt (second step)

Once the above analysis is approved, use this prompt for execution:

```text
PHASE 2 OF 2 — EXECUTION. Use this block ONLY after Phase 1 (analysis) has been reviewed and approved by a human. If you are reading this block without explicit approval of Phase 1, STOP and request it before continuing.

Based on the previously generated analysis and plan:

Objective:
Implement the changes in a controlled manner in a multi-agent environment.

Rules:
- minimal changes per commit
- one finding per commit
- do not modify outside the scope
- validate before each commit

Constraints:
- apply only the changes that were explicitly described and approved in the Phase 1 plan — if you identify additional necessary work during execution, don't implement it: stop, document it, and request a new analysis cycle,
- don't reinterpret or "improve" the approved plan on the fly; any deviation from the original plan requires human approval before being applied,
- don't push or deploy without additional explicit approval, even if local commits pass validation,
- if an approved change no longer applies (e.g. the code changed since the analysis), stop and report it instead of silently adapting it.

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
| `parse_editorial_contract` doesn't validate required fields before indexing them | Yes | Critical | `build.py` | Missing explicit schema validation when parsing the Editorial Contract table |

### Remediation plan

| Step | Change | File | Risk | Validation | Suggested commit |
|---|---|---|---|---|---|
| 1 | Add validation of required fields with a clear error message before indexing the contract dictionary | `build.py` | Low — change scoped to a pure function, no side effects | `python -m pytest tests/test_parse_md_contract.py` | `fix(build): validate required contract fields before indexing` |

### Risk matrix

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| The build silently fails for a new prompt with an incomplete contract table | Medium | High — blocks static site generation | Add a regression test covering an incomplete contract that fails with a clear message in CI |
