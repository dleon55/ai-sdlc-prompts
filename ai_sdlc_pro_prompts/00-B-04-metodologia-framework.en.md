# 0-B.4 — Methodology and Framework Selection and Configuration

## Description

Prompt to select, document, and operationally configure the project methodology and framework: workflow definition, ceremonies, roles, branching strategy, Definition of Ready, Definition of Done, and how AI agent work integrates into the process.

**When to use:** when starting a project, when formalizing an existing one that grew without methodology, or when AI agents are being incorporated and their place in the process needs to be defined.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | medium — a methodology poorly matched to the team's real maturity produces sustained operational friction (ceremonies that don't happen, ignored DoR/DoD), even though the prompt executes no technical change |
| Required inputs | project type, team size (people + AI agent types), expected delivery frequency, candidate or chosen methodology, third-party integrations/dependencies, current team maturity level |
| Allowed tools | read of README, CONTRIBUTING, current issues, and repository structure to contextualize the recommendation — no write or execution |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if the candidate methodology requires conditions the declared team does not meet (e.g., full SCRUM with a one-person team), state the alert explicitly instead of recommending it without reservations |
| Expected output | see `## Expected Output` |
| Minimum evidence | the branch flow diagram is consistent with the recommended methodology; the Definition of Ready and Definition of Done tables explicitly cover both human and AI agent work |
| Recommended next prompt | `00-B-01-scaffolding-repositorio` if no repository structure exists yet; `00-B-03-github-configuracion` to apply the branch strategy in real GitHub protections; `17-08-retrospectiva-equipo-sprint` at the close of the first sprint/iteration, to run the retrospective ceremony defined here |

---

## Mandatory Previous Context

> Include the block from file `00-framework.en.md` before this prompt.

---

## Complete Prompt

```text
Objective:
Select, document, and configure the project framework so it is operable by the human team and assigned AI agents.

Required inputs:
- project type: [product / service / library / internal tool / migration / other]
- team size: [number of people + types of AI agents]
- expected delivery frequency: [daily / weekly / per sprint / continuous]
- candidate or chosen methodology: [SCRUM / Kanban / Trunk-Based / GitFlow / GitHub Flow / RUP / no formal one yet]
- third-party integrations or dependencies: [external APIs, services, other teams]
- current team maturity level: [beginning / intermediate / mature]

Deliver:

1. METHODOLOGY RECOMMENDATION
   - selected methodology and justification
   - recommended variations or adaptations for this case
   - alerts if the methodology requires conditions the team doesn't yet meet

2. BRANCH STRATEGY
   Diagram and description of the branch flow:
   - permanent branches and their purpose
   - short-lived branches and naming convention (feat/, fix/, hotfix/, chore/, etc.)
   - merge rule: PR required / direct merge / squash / rebase
   - when to create a release branch
   - namespacing policy for AI agent branches (e.g., ai/codex/fix-login)

3. DEFINITION OF READY (DoR) — CRITERIA TO START AN ISSUE/TASK
   List of conditions a task must meet before being assigned to a developer or AI agent:
   - complete functional and technical description
   - measurable acceptance criteria
   - identified impact and involved files
   - documented restrictions and business rules
   - explicit dependencies
   - for AI agents: sufficient repository context attached

4. DEFINITION OF DONE (DoD) — CRITERIA TO CLOSE A TASK
   - code implemented and reviewed
   - unit tests written and passing
   - integration with destination branch without conflicts
   - documentation updated if there was interface change
   - basic security review completed
   - reviewer approval (human or automatic according to level)
   - for AI agents: human validation of output before merge

5. COMPLETE ISSUE FLOW
   Textual or Mermaid diagram of the lifecycle:
   Backlog → Ready → In progress (human or agent) → Code Review → QA → Accepted → Done

6. CEREMONIES AND CADENCE (if SCRUM/Kanban applies)
   - what meetings exist, who participates, expected duration
   - how AI agents participate or report in the process

7. OPERATIONAL DOCUMENTATION TO CREATE
   List of files to create in docs/ to formalize the framework:
   - docs/workflow.md: workflow and branching
   - docs/definition-of-ready.md
   - docs/definition-of-done.md
   - docs/team-conventions.md: code conventions, commits, PRs

Constraints:
- do not impose a complete formal methodology (e.g., full SCRUM with all its ceremonies) on a team that already has a different working process, even an informal one — if the current process works, propose targeted adjustments rather than a full replacement,
- if the declared team size, delivery cadence, or maturity level does not support the candidate methodology (e.g., full Scrum with a one-person team, or daily ceremonies with monthly releases), flag the alert explicitly in the recommendation instead of endorsing it without reservations,
- do not define ceremonies, roles, or artifacts the team has no real way to sustain over time — prioritize a minimal, sustainable process over a complete but unworkable one,
- the delivered branch strategy and DoR/DoD must be consistent with the recommended methodology, not with a generic template — if they contradict each other, fix it before delivering instead of leaving it for the team to resolve.

Output format:
- branch flow diagram (Mermaid or ASCII)
- DoR and DoD table with category and criterion
- instructions for registering the framework in the repo (what files to create and where)
```

---

## Usage with Standard Formula

```text
Use the methodology and framework prompt and adapt it to:
- project type: [PROJECT TYPE]
- team size: [NUMBER + AI AGENTS]
- delivery frequency: [CADENCE]
- candidate methodology: [METHODOLOGY OR "none"]
- maturity level: [LOW / MEDIUM / HIGH]
- documents to review: README, CONTRIBUTING, current issues, repository structure
- specific output goal: documented branch strategy + DoR + DoD + issue flow for humans and AI agents
- depth level: high
```

---

## Expected Output

```mermaid
gitGraph
   commit id: "init"
   branch develop
   checkout develop
   branch feat/login
   checkout feat/login
   commit id: "feat: add login"
   checkout develop
   merge feat/login
   branch ai/codex/fix-validation
   checkout ai/codex/fix-validation
   commit id: "fix: validate email"
   checkout develop
   merge ai/codex/fix-validation id: "PR #42 (reviewed)"
   checkout main
   merge develop id: "release v1.1"
```

| Criterion | DoR (to start) | DoD (to close) |
|---|---|---|
| Description | Clear functional and technical | Code implemented |
| Acceptance criteria | Defined and measurable | Verified and evidenced |
| Tests | Identified what to cover | Written and passing |
| Security | Risks identified | Basic review completed |
| Documentation | Impact identified | Updated if there was change |
| For AI agents | Repo context attached | Human validation completed |

### Applied example: `ai-sdlc-prompts` workflow

| Criterion | Applied to this repository |
|---|---|
| Branch in progress | `fix/prompts/reinforce-backlog-33` — `type/area/issue-description` convention, Trunk-Based with short-lived branches |
| DoR for an AI agent task | The `.md` file to modify and its `.en.md` counterpart are identified; each one's Editorial Contract is out of scope (preserved byte-identical) |
| DoD for an AI agent task | `python -m pytest tests/ -q --ignore=tests/e2e` passes green before the task is considered done |
