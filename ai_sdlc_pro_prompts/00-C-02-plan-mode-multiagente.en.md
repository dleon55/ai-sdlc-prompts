# 0-C.2 — Safe Plan Mode and Multi-Agent Coordination

## Description

Prompt to execute any task in **plan mode** before implementing: the agent analyzes, designs, and proposes without touching the code. Includes the coordination protocol for environments where multiple agents (Copilot, Claude, Codex, Windsurf, Antigravity) operate in parallel on the same repository, preventing conflicts, overwrites, and work loss.

**When to use:** always before executing high-impact tasks, when there is more than one active agent in the repo, or when working in `mode:plan` in Agent Manager or GitHub Copilot Agent.

---

## Mandatory Previous Context

> Include the block from file `00-framework.en.md` before this prompt.

---

## Complete Prompt — PLAN MODE

```text
Objective:
Operate in PLAN MODE. Do not modify any file. Do not make commits. Do not execute commands that alter the repository or environment state.

Your work in this mode is:
1. Analyze the current state of the repository related to the task.
2. Map what files would be modified and why.
3. Identify risks, potential conflicts, and dependencies.
4. Propose the detailed implementation plan.
5. Estimate the scope of the change (lines, files, modules).
6. Signal what requires human approval before executing.

Input:
- issue/task: [REFERENCE OR DESCRIPTION]
- target branch: [BRANCH]
- active agents in parallel (if known): [LIST OR "none known"]

Deliver in PLAN MODE:

## Implementation plan
### 1. Files that would be modified
| File | Type of change | Risk | Requires approval |
|---|---|---|---|

### 2. Files that should NOT be touched in this task
(Explicit list to avoid scope creep)

### 3. Potential conflicts with work in parallel
- active branches that touch the same files
- recent changes (last 48h) in scope files
- open issues or PRs related

### 4. Dependencies and preconditions
- what must be ready before executing
- environment variables or secrets needed
- migrations or data required

### 5. Proposed implementation steps
Numbered, atomic, with what file changes at each step.

### 6. Commit strategy
- estimated number of commits
- message for each commit (project convention)
- recommended order

### 7. Test plan
- tests to write or update
- how to verify that acceptance criteria are met

### 8. High signals that stop execution
List of conditions where the agent must pause and escalate to the human:
- finding [condition A]
- finding [condition B]

Do you approve this plan? Confirm to proceed to controlled execution.
```

---

## Complete Prompt — MULTI-AGENT PROTOCOL

```text
Objective:
Before starting any work, execute the multi-agent coordination protocol for this repository.

Step 1. STATE VERIFICATION
- git fetch origin && git log --oneline -10 origin/[BRANCH]
- git branch -r | grep -v HEAD
- gh pr list --repo [ORG/REPO] --state open

Step 2. POTENTIAL CONFLICT DETECTION
- list the files you would modify in this task
- verify if any were modified in recent commits
- verify if there are open PRs that touch the same files
- if there is conflict: STOP and report before continuing

Step 3. WORK AREA RESERVATION
- create your branch with agent prefix: [agent-type]/[issue-id]/[short-description]
  Examples:
  - copilot/42/fix-login-validation
  - claude/43/refactor-auth-service
  - codex/44/add-unit-tests
  - windsurf/45/update-nginx-config
  - antigravity/46/e2e-checkout-flow
- make an initial empty commit to mark the area:
  git commit --allow-empty -m "wip([agent]): reserve branch for issue #[N]"

Step 4. AGENT COEXISTENCE RULES
- one agent = one branch = one issue at a time
- if two agents need the same file, the second waits or works in a separate copy
- no agent merges to main/develop without human approval
- atomic commits — one logical change per commit
- if you detect work from another agent in the same area: pause, report, wait for instruction

Step 5. STATUS REPORT
At the end of the plan or execution, report:
- branch created: [NAME]
- modified files: [LIST]
- tests updated: [YES/NO]
- PR opened: [URL or "pending approval to create"]
- conflicts detected: [NONE / DESCRIPTION]
- pending human review: [LIST]
```

---

## Usage with Standard Formula

```text
Use the plan mode and multi-agent coordination prompt and adapt it to:
- repository: [NAME OR URL]
- task or issue: [REFERENCE]
- target branch: [BRANCH]
- active agents in parallel: [LIST OR "none known"]
- mode: [PLAN ONLY / PLAN + CONTROLLED EXECUTION]
- documents to review: recent git log, open PRs, AGENTS.md
- specific output goal: implementation plan with file table + conflict detection + branch reservation
- depth level: high
```

---

## Branch Naming Convention by Agent

| Agent | Branch prefix | Example |
|---|---|---|
| GitHub Copilot | `copilot/` | `copilot/42/fix-login` |
| Claude (Anthropic) | `claude/` | `claude/43/refactor-auth` |
| OpenAI Codex | `codex/` | `codex/44/add-tests` |
| Windsurf | `windsurf/` | `windsurf/45/update-nginx` |
| Cursor | `cursor/` | `cursor/46/style-cleanup` |
| Antigravity | `antigravity/` | `antigravity/47/e2e-flow` |
| Human / mixed | `feat/`, `fix/`, etc. | `feat/user-profile` |

---

## Execution Traffic Light

| State | Color | Description | Agent action |
|---|---|---|---|
| No conflicts, plan approved | 🟢 Green | Area free, clear plan | Proceed with controlled execution |
| Potential conflict detected | 🟡 Yellow | Another agent modified nearby files | Report, wait for human confirmation |
| Active conflict confirmed | 🔴 Red | Same file modified in active work | Stop, make no commits, escalate |
| Critical area (infra/cicd/db) | 🔴 Red | workflows/, migrations/, docker-compose | Always requires explicit human approval |
