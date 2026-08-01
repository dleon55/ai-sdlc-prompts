# 5.1 — Detailed implementation plan

## Description

Prompt to elaborate an executable and traceable implementation plan: previous activities, changes by component, migrations, tests, deployment, rollback and expected evidence per step.

**When to use it:** after approved design (`04-01`), before executing any change in the repository.

**Fast path — low risk:** if the change is low risk, summarize the plan as a short list of 3-5 steps with their expected evidence, without the JSON metadata block or the PSP/TSP metrics log — reserve the detailed step-by-step plan for medium/high-risk changes or ones touching production, data, or infrastructure.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | medium — does not execute changes, but it is the basis on which real implementation will be authorized; an incomplete or overly optimistic plan can lead to execution without defined rollback or evidence |
| Required inputs | approved design (`04-01`), architecture, contracts, target branch, target environment, components to modify |
| Allowed tools | read-only access to design/architecture/contracts; does not execute commands or modify the repository, produces the plan as a document |
| Permitted autonomy | A1 — Propose (plan or artifact without applying it); does not by itself authorize executing, committing, or deploying |
| Stop criteria | stop if there is no approved design to start from; do not leave any step without defined expected evidence, dependency, or risk; explicitly flag any step that requires a production environment |
| Expected output | see `## Expected output` |
| Minimum evidence | parser-friendly JSON metadata block at the start, each step (1-9) with defined expected evidence, complete PSP/TSP metrics log |
| Recommended next prompt | `05-02-riesgos-implementacion`, in parallel, before moving to `06-01-implementacion-multiagente`; `07-00-deteccion-stack-pruebas` to detect the active test stack before defining the tests required per step (step 4) |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Elaborate a detailed, executable and traceable implementation plan for the proposed solution.

Steps:
0. Start with a parser-friendly JSON metadata block (keys: status, task_count, impacted_components, estimated_hours) — this lets orchestration tools or CI read the plan without re-interpreting free text.
1. List the previous activities needed before touching code (access grants, branch creation, backups, feature flags, stakeholder notice).
2. Detail the changes by component, at the same scope and granularity as the approved design (`04-01`) — if you add a component the design did not cover, flag it explicitly as a deviation instead of including it without comment.
3. Specify the required data adjustments or migrations, stating whether they are reversible and what happens to existing data during and after the migration.
4. Define the tests required per step (unit, integration, E2E, performance), prioritizing those that cover the change's critical path over peripheral cases if QA time is limited. If a test stack profile already exists (`07-00-deteccion-stack-pruebas`), reuse its commands and conventions instead of inventing your own test commands.
5. Define the validations to run in each environment (dev/QA/staging) before promoting the change to the next one, and what result gates the move to the following environment.
6. Describe the branch integration strategy: merge order, expected conflict resolution, and who approves each integration.
7. Detail the deployment: deployment order by component, maintenance windows if applicable, and who executes each step.
8. Detail the rollback per step — if a step has no possible rollback, state that explicitly instead of omitting it or assuming it won't be needed.
9. Define the expected evidence per step (logs, screenshots, test results, metrics) that verifiably demonstrates the step was completed.
10. Close with the PSP/TSP Metrics Log: estimated design time in minutes, estimated coding time in minutes, and projected defect count, to later compare against the actuals.

Constraints:
- do not execute commands or modify the repository or environment — this prompt produces the plan as a document; executing, committing, or deploying requires explicit approval and a separate prompt,
- do not leave any step (1 to 9) without a declared dependency, risk, or expected evidence; if one of those fields does not apply, say so explicitly instead of leaving it blank,
- if any step requires a production environment, flag it explicitly and do not mix it with dev/QA/staging steps,
- if there is no approved design (`04-01`) to start from, stop and request it — do not derive the plan from your own assumptions,
- the JSON metadata block must be valid and parser-friendly (no comments, no missing keys) — do not replace it with a free-text description.

Format for steps 1 to 9:
| Step | Activity | Component | Dependency | Risk | Expected evidence |
```

---

## Use with standard formula

```text
Use the implementation plan prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [TARGET BRANCH]
- environment: [DEV / QA / PROD]
- components: [COMPONENTS TO MODIFY]
- documents to review: approved design, architecture, contracts
- specific output objective: executable step-by-step implementation plan
- depth level: high
```

---

## Expected output

| Section / Step | Activity | Component | Dependency | Risk | Expected evidence |
|---|---|---|---|---|---|
| JSON Metadata (0) | `{"status":"planned","task_count":6,"impacted_components":["build.py","tests/test_i18n.py"],"estimated_hours":6}` | - | - | - | - |
| Step 2 — Changes by component | Add a `check_i18n_parity()` function in `build.py` that compares `##` headers between each `.md` file and its `.en.md` counterpart | `build.py` | Design approved in `04-01` | False positives from minor cross-language formatting differences | Passing unit test in `tests/test_i18n.py` + build log showing the check ran |
| Step 8 — Rollback | Revert the commit that adds the check; the build goes back to generating `index.html` without the parity validation | `build.py` | Step 2 completed | Low — isolated change in a single script, no data impact | Post-revert build run whose log no longer includes the validation step |
| PSP/TSP Metrics (10) | Design: 45 min · Coding: 180 min · Projected defects: 1 | - | - | - | - |
