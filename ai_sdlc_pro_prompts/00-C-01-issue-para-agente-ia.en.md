# 0-C.1 — Document an Issue Ready for AI Agent Execution

## Description

Prompt to write a high-quality GitHub issue that can be executed by an AI agent autonomously and in a controlled manner: with sufficient context, verifiable acceptance criteria, explicit restrictions, involved files, and human validation checklist post-execution.

**When to use:** before assigning any task to an AI agent (Copilot Agent, Claude, Codex, Windsurf), to ensure the agent operates with complete context and within safe limits.

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
- autonomy level: [LEVEL]

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

## Required tests
What tests should the agent write or update:
- test type (unit / integration / e2e / smoke)
- minimum expected coverage
- test file(s) to create or modify

## Human validation checklist (post-execution)
Review that the human must do before merging:
- [ ] The PR only touches files within the defined scope
- [ ] Acceptance criteria were satisfied with evidence
- [ ] There are no secrets, credentials, or tokens in the diff
- [ ] Tests pass in green (green CI)
- [ ] Code follows project conventions
- [ ] No new dependencies were installed without justification
- [ ] No unauthorized changes in workflows, migrations, or infrastructure files

## Authorized autonomy level
[ ] Analysis and proposal only (agent makes no commits)
[ ] Proposal with draft PR (agent creates PR in draft)
[ ] Controlled execution (agent can make commits in feature branch)
[ ] Autonomous execution (agent can complete and request merge)

## Suggested labels
[type], [ai-agent], [environment], [priority]
```

---

## Usage with Standard Formula

```text
Use the AI agent issue prompt and adapt it to:
- repository: [NAME OR URL]
- issue title: [TITLE]
- type: [TYPE]
- requirement description: [DESCRIPTION]
- involved files: [LIST]
- acceptance criteria: [CRITERIA]
- restrictions: [RESTRICTIONS]
- assigned agent: [AGENT]
- autonomy level: [LEVEL]
- specific output goal: complete issue ready to create in GitHub with gh issue create
- depth level: high
```

---

## Expected Output

Issue drafted with all sections complete, plus the command to create it directly:

```bash
gh issue create \
  --repo [ORG/REPO] \
  --title "[TYPE]: [TITLE]" \
  --body-file issue-draft.md \
  --label "[type],[ai-agent],[priority]" \
  --assignee "@me"
```

---

## Antipatterns to Avoid

| Antipattern | Consequence | Solution |
|---|---|---|
| "Fix the login" without more context | Agent assumes incorrect path | Include involved files and expected behavior |
| Without acceptance criteria | Agent doesn't know when it's done | Numbered and verifiable criteria |
| Without restrictions | Agent touches files outside the scope | Explicit list of what should NOT be touched |
| Without human checklist | PR is merged without reviewing agent output | Mandatory human validation section |
| Autonomy level not defined | Agent assumes total autonomy | Always declare the authorized level |
