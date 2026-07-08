# 0-C.1 — Document an Issue Ready for AI Agent Execution

## Description

Prompt to write a high-quality GitHub issue that can be executed by an AI agent autonomously and in a controlled manner: with sufficient context, verifiable acceptance criteria, explicit restrictions, involved files, and human validation checklist post-execution.

**When to use:** before assigning any task to an AI agent (Copilot Agent, Claude, Codex, Windsurf), to ensure the agent operates with complete context and within safe limits.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | medium — this prompt executes nothing itself, but the issue it produces is the contract that will govern an executing agent afterward; a poorly written scope, restriction, or autonomy level here is inherited directly by the real execution |
| Required inputs | issue title and type, description of the problem/requirement, repository and target branch, environment, involved files/modules (if known), acceptance criteria, restrictions, assigned agent, expected observable result, authorized permissions/tools, budget |
| Allowed tools | read of the repository to verify that cited paths, current behavior, and context are real — must not invent paths or commands; does not create the issue on GitHub, only drafts the content and suggests the `gh issue create` command |
| Permitted autonomy | A1 — Propose (drafts the issue and the suggested command; publishing it on GitHub is an A3 action outside this prompt's scope) |
| Stop criteria | if available information does not allow the `## Execution contract` (autonomy mode, tools, scope) to be completed unambiguously, mark the issue "NOT suitable for an agent" in the readiness assessment instead of filling in invented values |
| Expected output | see `## Expected Output` |
| Minimum evidence | the generated issue includes all mandatory sections (Description, Technical context, Acceptance criteria, Restrictions, Execution contract, Required tests, Compliance evidence, Human validation checklist) and explicitly declares the A0-A3 autonomy mode |
| Recommended next prompt | `00-C-02-plan-mode-multiagente` so the assigned agent executes the task in plan mode before touching code |

---

## Mandatory Previous Context

> Include the block from file `00-framework.en.md` before this prompt.

---

## Complete Prompt

```text
Objective:
Write a complete GitHub issue ready to be executed by an AI agent, following best practices for documentation and agent governance.

Required inputs:
- issue title: [SHORT AND PRECISE TITLE]
- type: [feat / fix / refactor / chore / docs / test / security / infra]
- description of problem or requirement: [DESCRIPTION IN NATURAL LANGUAGE]
- repository and target branch: [REPO / BRANCH]
- environment: [dev / qa / staging]
- files or modules involved (if known): [LIST]
- acceptance criteria: [LIST OF VERIFIABLE CONDITIONS]
- restrictions: [WHAT THE AGENT CANNOT DO IN THIS ISSUE]
- assigned agent: [Copilot / Claude / Codex / Windsurf / Cursor / Antigravity]
- expected observable result: [EVIDENCE THAT PROVES SUCCESS]
- authorized permissions and tools: [READ / EDIT / SHELL / GITHUB / BROWSER / OTHERS]
- budget: [TIME / FILES / ATTEMPTS / COST, IF APPLICABLE]

Before drafting the issue:
1. Assess whether the problem is sufficiently defined.
2. Identify missing information, contradictions, and dependencies.
3. Classify the risk: low, medium, or high.
4. Determine whether the task is suitable for autonomous execution.
5. Do not invent paths, commands, criteria, or current behavior.

Constraints:
- don't invent acceptance criteria the requester hasn't explicitly given; if any are missing, mark them as pending in the readiness assessment instead of filling them in with your own assumptions,
- if the scope is ambiguous (affected files, expected behavior, target environment), flag the ambiguity and request clarification before drafting the final issue — don't proceed on an unconfirmed interpretation,
- don't assign an autonomy mode (A0-A3) in the `## Execution contract` higher than the task's real risk warrants; when in doubt, assign the more conservative level and explain why,
- don't create the issue on GitHub — this prompt only drafts the content and the suggested command; publishing it is an A3 action that requires explicit human approval outside this prompt.

Generate the issue with the following sections:

## Description
Clear and precise explanation of the problem or requirement. Without ambiguities.
- current behavior (if it's a fix)
- expected behavior
- relevant business context

## Technical context
- branch: [BRANCH]
- environment: [ENVIRONMENT]
- key files involved (with relative path)
- dependencies or related services
- related commits or PRs (if applicable)

## Acceptance criteria
Numbered list, each objectively verifiable by the agent and human reviewer:
- [ ] 1. [CONCRETE AND MEASURABLE CRITERION]
- [ ] 2. ...

## Restrictions for the agent
What the agent should NOT do in the context of this issue:
- do not modify [FILES/MODULES outside the scope]
- do not execute [HIGH-RISK ACTIONS]
- do not alter configurations of [CRITICAL AREA]
- stop and escalate if you find: [ESCALATION CONDITION]

## Execution contract
- authorized mode: [A0 analysis / A1 proposal / A2 controlled execution / A3 publication]
- authorized tools: [LIST]
- prohibited tools: [LIST]
- files or modules in scope: [LIST]
- files or modules out of scope: [LIST]
- actions requiring approval: [LIST]
- execution budget: [LIMITS]
- stop conditions: [LIST]

## Required tests
What tests should the agent write or update:
- test type (unit / integration / e2e / smoke)
- minimum expected coverage
- test file(s) to create or modify

## Compliance evidence
For every acceptance criterion define the expected test result, relevant path and line, screenshot/trace/log when applicable, and mandatory CI or remote validation. Code modification alone is not completion evidence.

## Human validation checklist (post-execution)
Review that the human must do before merging:
- [ ] The PR only touches files within the defined scope
- [ ] Acceptance criteria were satisfied with evidence
- [ ] There are no secrets, credentials, or tokens in the diff
- [ ] Tests pass in green (green CI)
- [ ] Code follows project conventions
- [ ] No new dependencies were installed without justification
- [ ] No unauthorized changes in workflows, migrations, or infrastructure files

## Readiness assessment
- objective clarity: [HIGH / MEDIUM / LOW]
- verifiable criteria: [YES / PARTIAL / NO]
- dependencies available: [YES / PARTIAL / NO]
- permissions defined: [YES / NO]
- risk: [LOW / MEDIUM / HIGH]
- suitable for an agent: [YES / YES WITH APPROVALS / NO]
- missing information: [LIST]

## Suggested labels
[type], [ai-agent], [environment], [priority]
```

---

## Usage with Standard Formula

```text
Use the AI agent issue prompt and adapt it to:
- repository: [NAME OR URL]
- issue title: [TITLE]
- type: [ISSUE TYPE]
- requirement description: [DESCRIPTION]
- involved files: [LIST]
- acceptance criteria: [CRITERIA]
- restrictions: [RESTRICTIONS]
- assigned agent: [AGENT]
- autonomy level: [AUTONOMY LEVEL]
- specific output goal: complete issue ready to create in GitHub with gh issue create
- depth level: high
```

---

## Expected Output

Issue drafted with all sections complete, plus the command to create it directly:

```bash
gh issue create \
  --repo [ORG/REPO] \
  --title "[ISSUE TYPE]: [TITLE]" \
  --body-file issue-draft.md \
  --label "[type],[ai-agent],[priority]" \
  --assignee "@me"
```

**Example applied to this project:**

```bash
gh issue create \
  --repo dleon/ai-sdlc-prompts \
  --title "fix: build.py does not validate that the ES/EN pair exists before generating the index" \
  --body-file issue-draft.md \
  --label "fix,ai-agent,high" \
  --assignee "@me"
```

With `## Execution contract` → authorized mode: A2 (controlled execution, scope limited to `build.py` and `tests/test_build.py`); and `## Readiness assessment` → clarity HIGH, verifiable criteria YES, risk MEDIUM, suitable for an agent YES WITH APPROVALS (requires human review of the CHANGELOG before merge).

---

## Antipatterns to Avoid

| Antipattern | Consequence | Solution |
|---|---|---|
| "Fix the login" without more context | Agent assumes incorrect path | Include involved files and expected behavior |
| Without acceptance criteria | Agent doesn't know when it's done | Numbered and verifiable criteria |
| Without restrictions | Agent touches files outside the scope | Explicit list of what should NOT be touched |
| Without human checklist | PR is merged without reviewing agent output | Mandatory human validation section |
| Autonomy level not defined | Agent assumes total autonomy | Always declare the `authorized mode` (A0-A3) in `## Execution contract` |
