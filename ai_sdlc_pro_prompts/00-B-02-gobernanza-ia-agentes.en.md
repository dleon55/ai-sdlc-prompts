# 0-B.2 — AI Agent Governance Configuration Files

## Description

Prompt to generate the configuration and governance files that control the behavior of AI agents over the repository: role instructions, coding rules, security restrictions, project context, and work protocol. Compatible with GitHub Copilot, Claude, Windsurf, Cursor, Codex, and other agents.

**When to use:** when starting a new repository, when incorporating AI agents into an existing project, or when agents are not following the project's conventions or framework.

---

## Mandatory Previous Context

> Include the block from file `00-framework.en.md` before this prompt.

---

## Complete Prompt

```text
Objective:
Generate the configuration and governance files that control the behavior of AI agents assigned to this repository.

Required inputs:
- project name: [NAME]
- technology stack: [e.g., Python 3.11 + FastAPI + PostgreSQL + Docker]
- working methodology: [SCRUM / Kanban / GitFlow / GitHub Flow / Trunk-Based]
- AI agent platform to use: [GitHub Copilot / Claude / Windsurf / Cursor / Codex / Antigravity / combination]
- permitted autonomy level: [analysis only / analysis + proposal / controlled execution / autonomous execution]
- project critical rules: [e.g., never edit main directly, don't regenerate already applied migrations, etc.]
- prohibited patterns: [e.g., don't use eval(), don't hardcode secrets, don't install dependencies without approval]

Deliver the following files with their complete content:

1. .github/copilot-instructions.md
   - agent role in this repository
   - stack and versions it should use
   - code conventions (naming, structure, preferred patterns)
   - what files/folders it should NOT modify without approval
   - commit format it should generate
   - QA rules (no merge without tests, minimum coverage, etc.)
   - how it should escalate if it detects ambiguity or risk

2. .windsurfrules (or .cursorrules if Cursor applies)
   - project context in natural language
   - active technologies and frameworks
   - preferred and prohibited code patterns
   - security rules (OWASP applicable to the stack)
   - instruction of "always review before modifying"
   - instruction of atomic commits

3. AGENTS.md (root of the repository)
   - purpose of the file
   - list of authorized agents and their role
   - access level per agent (read / proposal / execution)
   - escalation protocol and human approval
   - what decisions an agent should NEVER make alone

4. docs/ai-governance.md
   - AI usage policy in the project
   - environments where autonomous execution is permitted
   - security checklist before approving an AI-generated change
   - registry of AI decisions that require audit

Rules that must appear in ALL files:
- do not execute database migrations without explicit human approval
- do not modify CI/CD workflows without review
- do not expose or generate secrets, tokens, or credentials
- do not push directly to protected branches
- in case of ambiguity, pause and escalate — never assume
```

---

## Usage with Standard Formula

```text
Use the AI agent governance prompt and adapt it to:
- project name: [NAME]
- stack: [STACK]
- methodology: [METHODOLOGY]
- agents to configure: [LIST OF AGENTS]
- autonomy level: [LEVEL]
- project critical rules: [SPECIFIC RULES]
- documents to review: README, CONTRIBUTING, repository structure, existing workflows
- specific output goal: complete .github/copilot-instructions.md, .windsurfrules, AGENTS.md, docs/ai-governance.md files
- depth level: high
```

---

## Expected Output

| File | Purpose | Target Agent | Priority |
|---|---|---|---|
| `.github/copilot-instructions.md` | Role and context instructions for Copilot | GitHub Copilot (Chat, Edits, Agent) | Mandatory |
| `.windsurfrules` | Behavior rules for Windsurf | Windsurf | Mandatory if using Windsurf |
| `.cursorrules` | Behavior rules for Cursor | Cursor | Mandatory if using Cursor |
| `AGENTS.md` | Agent usage policy and protocol in the repo | All agents | Mandatory |
| `docs/ai-governance.md` | Formal AI governance policy | Human team + auditors | Recommended |
| `.github/prompts/` | Reusable prompts for repetitive tasks | GitHub Copilot workspace | Recommended |
| `.github/instructions/` | Instructions per file type (*.py, *.yml, etc.) | GitHub Copilot | Recommended |
