# 12 — Master orchestrator prompt for complete cycle

## Description

Prompt that classifies an assignment and selects the minimum sufficient flow to complete it safely and with evidence. It can use one agent, a deterministic workflow, or a supervisor with subagents.

**When to use it:** when an assignment requires coordination across capabilities, phases, or agents. For simple tasks, use the specialized prompt directly.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | operation (routing meta-prompt — does not execute technical work directly) |
| Expected risk | variable — depends on the assignment being routed; the prompt itself requires declaring risk and reversibility as part of classification |
| Required inputs | issue/requirement, target branch, environment, components, permitted autonomy level, available tools, budget |
| Allowed tools | whatever the execution contract generated in Step 3 declares — assumes no tools by default |
| Permitted autonomy | dynamically defined by the prompt itself (Step 3, "Create contract"); must never exceed the declared input autonomy level |
| Stop criteria | "Do not execute all phases by default"; escalate to a human when risk or permission exceeds the generated contract |
| Expected output | see `## Patterns and expected deliverables` and the prompt's mandatory 8-point output format |
| Minimum evidence | explicit execution contract (scope, tools, checkpoints, stop condition) before delegating any subtask |
| Recommended next prompt | whatever the execution contract itself determines — this prompt is the entry point, not the exit |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Route and coordinate this assignment through the minimum flow that can satisfy it with verifiable evidence.

Input:
- issue/requirement/incident: [PASTE]
- target branch: [TARGET BRANCH]
- environment: [ENVIRONMENT]
- components: [INVOLVED COMPONENTS]
- permitted autonomy: [A0 / A1 / A2 / A3]
- available tools: [AVAILABLE TOOLS]
- budget: [TIME / CHANGES / ATTEMPTS / COST]

Step 1. CLASSIFY intent, complexity, risk, reversibility, and required evidence.

Step 2. SELECT A PATTERN
- single agent for a scoped, verifiable task
- sequential workflow for known dependencies
- parallel workflow for independent subtasks
- supervisor plus subagents for different specialties requiring reconciliation
- human-in-the-loop for ambiguity or high-risk actions

Do not execute every phase by default.

Step 3. CREATE THE CONTRACT
- scope, exclusions, tools, permissions, approvals, checkpoints, budget, stop conditions, success criteria, and evidence

Allowed states:
`discovered`, `planned`, `approved`, `executing`, `verifying`, `blocked`, `completed`, `rolled_back`.

Step 4. EXECUTE
- load only required capabilities
- delegate with explicit input, scope, and output
- preserve isolation and ownership
- record relevant decisions, tool calls, and evidence
- reconcile before integration

Step 5. VERIFY acceptance criteria, proportional tests, security, regressions, actual diff, and residual risks.

Step 6. CLOSE OR ESCALATE
- complete only with sufficient evidence
- block only for a real documented impediment
- use rolled_back when execution was reverted
- request human decisions when risk or permissions exceed the contract

Mandatory output format:
1. Classification and selected pattern
2. Current state
3. Execution contract
4. Plan or task graph
5. Executed actions
6. Evidence and validations
7. Residual risks
8. Pending human decisions
```

---

## Use with standard formula

```text
Use the master orchestrator prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [PASTE COMPLETE TEXT]
- target branch: [TARGET BRANCH]
- environment: [DEV / QA / STAGING / PROD]
- components: [INVOLVED COMPONENTS]
- documents to review: README, docs/, architecture, workflows, related issues
- specific output objective: documented complete cycle ready for execution
- depth level: high
```

---

## Patterns and expected deliverables

| Pattern | When to use | Deliverable |
|---|---|---|
| Single agent | Small scoped task | Verified change or analysis |
| Sequential | Strict dependencies | Checkpoints per stage |
| Parallel | Independent subtasks | Reconciled deliverables |
| Supervisor | Multiple specialties | Integrated and reviewed result |
| Human-in-the-loop | High risk or ambiguity | Approval and evidence |
