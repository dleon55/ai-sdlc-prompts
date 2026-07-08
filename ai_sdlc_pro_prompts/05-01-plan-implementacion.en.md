# 5.1 — Detailed implementation plan

## Description

Prompt to elaborate an executable and traceable implementation plan: previous activities, changes by component, migrations, tests, deployment, rollback and expected evidence per step.

**When to use it:** after approved design (`04-01`), before executing any change in the repository.

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
| Recommended next prompt | `05-02-riesgos-implementacion`, in parallel, before moving to `06-01-implementacion-multiagente` |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Elaborate a detailed, executable and traceable implementation plan for the proposed solution.

Include:
0. Start with a Task Metadata JSON Block (keys: status, task_count, impacted_components, estimated_hours).
1. previous activities,
2. changes by component,
3. data adjustments or migrations,
4. required tests,
5. environment validations,
6. branch integration,
7. deployment,
8. rollback,
9. expected evidence,
10. PSP/TSP Metrics Log (Estimated design time in minutes, estimated coding time in minutes, and projected defects count).

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
| JSON Metadata (0) | Structured and parser-friendly JSON block containing plan metadata | - | - | - | - |
| Steps 1 to 9 | Structured table listing implementation and rollback activities | - | - | - | - |
| PSP/TSP Metrics (10) | Logging block for estimated design/coding times and projected defect rate | - | - | - | - |
