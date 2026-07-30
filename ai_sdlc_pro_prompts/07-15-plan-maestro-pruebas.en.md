# 7.15 — Master test plan: project QA strategy

## Description

Prompt to define the whole project or release's testing strategy: scope and quality objectives, test levels with their target coverage, environments and data, roles and responsibilities, test-cycle entry/exit criteria, and defect handling during the cycle. Ties together the overall QA approach before designing individual per-type tests.

**When to use it:** at the start of a project (after `07-00`, test-stack detection) or when planning a major release/milestone, before designing individual per-type tests (`07-01` through `07-06`). Distinct from `07-00` (which only detects the technical test stack) and from the `07-01`-`07-14` prompts (which design/implement **one** specific type of test): this prompt defines the overall approach — what gets tested, at what depth, in which environment, and when a release is considered ready from a QA standpoint.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | medium — an incomplete test strategy (no clear exit criteria, no defined per-level coverage) doesn't block anything by itself, but lets features reach production with no objective "done" criterion, silently propagating quality risk until it materializes in production |
| Required inputs | test-stack profile (`07-00`) if it exists, project or release scope, relevant non-functional requirements (`02-06`) if they exist, QA time/resource constraints, available environments |
| Allowed tools | reading existing documentation and configuration — no test execution or changes; produces the strategy document |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if an objective, verifiable exit criterion cannot be defined for at least the critical levels (unit, integration, E2E of the core flows), do not declare the strategy complete — report it as a pending gap instead of filling it with a subjective criterion |
| Expected output | see `## Expected output` |
| Minimum evidence | each test level (unit/integration/E2E/smoke/performance/security/accessibility) declares target coverage, an owner, and its point in the pipeline; the test-cycle entry and exit criteria are explicitly defined and verifiable |
| Recommended next prompt | `07-01-pruebas-unitarias` (and the corresponding `07-02` through `07-06` prompts) to design each test type according to this strategy |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Define the testing strategy for the whole project or release: scope, test levels with target coverage, environments, roles, entry/exit criteria, and defect handling during the cycle.

Inputs:
- test-stack profile: [PASTE OR REFERENCE TO 07-00, OR "not yet detected"]
- project or release scope: [DESCRIPTION]
- relevant non-functional requirements: [PASTE OR REFERENCE TO 02-06, OR "not yet defined"]
- QA time/resource constraints: [DESCRIPTION OR "none declared"]
- available environments: [DEV / QA / STAGING / PROD, AND WHICH ONES ACTUALLY EXIST]

Activities:
1. SCOPE AND QUALITY OBJECTIVES
   Define what will be tested (critical components or flows) and what is explicitly out of scope for this cycle, with the reason — never leave an area out of scope without an explicit justification.

2. TEST LEVELS AND TARGET COVERAGE
   For each applicable level (unit, integration, E2E, smoke, performance/load, security, accessibility), define the coverage target (percentage or qualitative scope), whether it's manual or automated, and why that choice for that specific level. Justify the target coverage against the component's risk: a business-critical component cannot have the same target as a cosmetic one without saying so explicitly.

3. ENVIRONMENTS AND DATA
   Define which environment corresponds to each test level and the test-data strategy (reference `07-14-gestion-datos-prueba` if applicable).

4. ROLES AND RESPONSIBILITIES
   Define who designs, implements, and maintains each test level (developer, dedicated QA, AI agent) — no level may be left without an assigned owner.

5. ENTRY AND EXIT CRITERIA
   Define what must be true before starting a release's test cycle (entry) and what must be true to consider it ready for production (exit). Every criterion must be objectively verifiable (metric, checklist, pipeline result) — never a subjective criterion like "it looks fine" or "seems stable".

6. DEFECT MANAGEMENT DURING THE CYCLE
   Define which defect severity blocks a release and which can be postponed, and who has the authority to make that call.

7. TOOLS AND PIPELINE
   Define at which point in the CI/CD pipeline each test level runs (local, PR, pre-merge, pre-deploy, post-deploy), referencing the stack detected in `07-00`.

Constraints:
- do not declare a target coverage without justifying it against the component's risk — any difference in rigor between components must be explicit, never implicit,
- every entry or exit criterion must be objectively verifiable (metric, checklist, pipeline result) — never accept a subjective criterion with no way to confirm it,
- if the test-stack profile (`07-00`) or the project/release scope is missing, stop and request it before proposing the strategy,
- explicitly distinguish which test levels already exist (and with what real coverage, if verifiable) from those proposed from scratch — never present them as already implemented.

Output:
0. JSON metadata block (keys: status, test_levels_covered, entry_criteria_count, exit_criteria_count, confidence_score [0.0 to 1.0]).
1. Scope and quality objectives, with justified exclusions.
2. Test levels and target coverage: Level | Target coverage | Manual/Automated | Owner | Environment | Pipeline stage
3. Test-cycle entry criteria.
4. Exit criteria (QA Definition of Done).
5. Defect management during the cycle: severity that blocks vs. severity that can be postponed, and who decides.
6. Gaps and pending next steps.
```

---

## Usage with standard formula

```text
Use the master test plan prompt and adapt it to:
- repository/project: [NAME OR URL]
- project or release scope: [DESCRIPTION]
- test-stack profile: [REFERENCE TO 07-00]
- documents to review: stack profile (07-00), non-functional requirements (02-06)
- specific output objective: complete QA strategy with levels, coverage, and entry/exit criteria
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the strategy summary |
| Scope and objectives (1) | What's tested and what's out of scope, with justification |
| Test levels (2) | Complete table with target coverage, owner, and pipeline location |
| Entry criteria (3) | Verifiable conditions to start the test cycle |
| Exit criteria (4) | QA Definition of Done, objectively verifiable |
| Defect management (5) | Severity that blocks vs. postpones, and who decides |
| Gaps (6) | Information pending confirmation before approving the strategy |

### Example (excerpt)

```json
{
  "status": "strategy_defined_with_gaps",
  "test_levels_covered": 6,
  "entry_criteria_count": 3,
  "exit_criteria_count": 4,
  "confidence_score": 0.73
}
```

| Level | Target coverage | Manual/Automated | Owner | Environment | Pipeline stage |
|---|---|---|---|---|---|
| Unit | ≥80% in critical business modules (payments, auth); ≥50% elsewhere | Automated | Developer implementing the change | Local + CI | Every push, mandatory gate for merge |
| E2E | The 5 core flows declared in the Charter (signup, checkout, cancellation, refund, export) | Automated | Dedicated QA | Staging | Pre-deploy to production, mandatory gate |

| Section | Example content |
|---|---|
| Exit criteria (4) | 100% of unit and integration tests green · 0 open critical- or high-severity defects · performance tests within the `02-06` thresholds · smoke tests passed in staging after the latest deploy |
