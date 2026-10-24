# 0-C.3 — Configuration Specific to Each AI Agent Type

## Description

Prompt and reference for configuring the behavior, instructions, and restrictions of each AI agent type according to their capabilities and own mechanisms: GitHub Copilot (Agent / Chat / Edits), Claude via chat/API, Claude Code, OpenAI Codex, Windsurf, Cursor, and Google Antigravity. Ensures each agent operates with project context and within team rules.

**When to use:** when incorporating a new type of agent to the project, when detecting that an agent is not following conventions, or when configuring a multi-agent environment for the first time. Requires the baseline governance to already exist (see `00-B-02-gobernanza-ia-agentes`); this prompt configures agent-specific mechanisms, not the baseline.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | medium — if a mandatory common rule (no exposing secrets, no migrations without approval, no push to protected branches) is missing from an agent's own mechanism, that agent may operate with more autonomy than intended; the prompt only drafts content, it does not apply it |
| Required inputs | list of active agents (Copilot, Claude via chat/API, Claude Code, Codex, Windsurf, Cursor, Antigravity), project stack, methodology, project critical rules, general autonomy level; baseline governance already in place (`00-B-02`) |
| Allowed tools | read of the governance and configuration already existing in the repository to avoid duplication — no write or execution; the human decides whether to create the delivered files (`.github/copilot-instructions.md`, `.windsurfrules`, `.cursorrules`, `AGENTS.md`, `CLAUDE.md`, `docs/ai-agents/*.md`) |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if configuration is requested for an agent without baseline governance in place (`00-B-02`), or if the requested autonomy level for an agent conflicts with the mandatory common rules, flag the conflict before generating the agent-specific configuration |
| Expected output | this prompt has no standalone `## Expected Output` section — the output format is the per-agent configuration blocks and the "MECHANISMS COMPARATIVE TABLE" inside the prompt block |
| Minimum evidence | every agent declared active has a complete configuration block with file, mechanism, and content; the mandatory common rules appear in every generated mechanism |
| Recommended next prompt | `00-C-02-plan-mode-multiagente` to operate in plan mode and multi-agent coordination with the per-agent configuration already active |

---

## Mandatory Previous Context

> Include the block from file `00-framework.en.md` before this prompt.

---

## Complete Prompt

```text
Objective:
Generate the configuration instructions for each AI agent active in this project, according to their own control mechanisms and repository standards.

Required inputs:
- active agents: [list: Copilot / Claude (chat/API) / Claude Code / Codex / Windsurf / Cursor / Antigravity]
- project stack: [STACK]
- methodology: [METHODOLOGY]
- project critical rules: [RULES THAT ALL MUST FOLLOW]
- general autonomy level: [AUTONOMY LEVEL]

For each active agent, deliver:

─────────────────────────────────────
GITHUB COPILOT (Agent / Chat / Edits)
─────────────────────────────────────
File: .github/copilot-instructions.md
Content:
- agent role: Senior Software Engineer working on [PROJECT]
- stack: [exact versions of language, framework, DB, infra]
- code conventions: naming, structure, mandatory and prohibited patterns
- commit rules: Conventional Commits format, atomic commits
- what files NOT to modify without approval: workflows/, migrations/, .env, CODEOWNERS
- how to act when faced with ambiguity: pause and ask the human user
- QA rules: don't propose code without tests for new business logic
- plan mode: when user says "plan mode" or "just analyze", don't make changes

Additional Copilot files:
- .github/prompts/ → reusable prompts for frequent project tasks
- .github/instructions/ → instructions per file type (applyTo patterns):
  - *.py → Python conventions of the project
  - *.yml → rules for modifying workflows
  - *.sql / migrations/ → "never modify without explicit approval"

─────────────────────────────────────
CLAUDE — CHAT / API (Anthropic, no project tools)
─────────────────────────────────────
Mechanism: system prompt (first message of context)
System prompt base content:
- role, project, and stack
- behavior rules (same as 00-framework.md)
- instruction of plan mode by default if not indicated otherwise
- instruction to always report in structured format: facts / findings / assumptions / risks / recommendations
- instruction of branch prefix: claude/[issue]/[description]
- instruction of "do not execute until explicit human confirmation"

File to create: docs/ai-agents/claude-system-prompt.md
(template of the system prompt to paste manually into claude.ai or into each API call — this mechanism does not read repo files on its own)

─────────────────────────────────────
CLAUDE CODE (CLI/IDE — reads the repository directly)
─────────────────────────────────────
Mechanism: a CLAUDE.md file at the repository root (plus an optional one per subfolder for path-specific context), read automatically at the start of every session — unlike the chat/API mechanism above, nothing needs to be pasted manually.
CLAUDE.md content:
- agent role and purpose of the repository
- stack: [exact versions of language, framework, DB, infra]
- the project's build, test, and lint commands (so the agent uses them instead of guessing)
- code conventions and repo structure
- what files/folders NOT to modify without approval: workflows/, migrations/, .env, CODEOWNERS
- commit rules: Conventional Commits format, atomic commits
- instruction of branch prefix: claude/[issue]/[description] (same prefix as the chat/API mechanism, since both are Claude)
- how to act when faced with ambiguity: pause and ask the human user
- reference to skills/[capability]/SKILL.md for specialized procedures that shouldn't live in the main CLAUDE.md

File to create: CLAUDE.md (repository root) — not under docs/ai-agents/, because Claude Code only reads it automatically from the root (or the matching folder, for per-subfolder context)

─────────────────────────────────────
OPENAI CODEX (CLI / API — OpenAI's coding agent)
─────────────────────────────────────
Mechanism: instructions in the prompt + AGENTS.md in the repo
Configuration:
- AGENTS.md in root: defines Codex role, allowed and prohibited accesses
- Branch instructions: codex/[issue]/[description]
- Tool restrictions: what commands it can execute (tests, lint, build) and which not (deploy, migrate, push to main)
- Sandbox instruction: run tests in isolated environment, don't modify staging/prod data
- Approval mode: propose changes as diff for human review before applying

File to create: docs/ai-agents/codex-config.md

─────────────────────────────────────
WINDSURF (Codeium)
─────────────────────────────────────
Mechanism: .windsurfrules in root of the repository
Sections of the file:
- [context]: project description, stack, architecture
- [rules]: code conventions, prohibited patterns
- [security]: applicable OWASP, secrets, input validation
- [workflow]: always review before modifying, atomic commits, branch with windsurf/ prefix
- [restricted_files]: list of files that require explicit confirmation
- [escalation]: conditions where Windsurf should pause and show warning to user

─────────────────────────────────────
CURSOR
─────────────────────────────────────
Mechanism: .cursorrules in root of repository (or .cursor/rules/)
File structure:
- project and stack description in natural language
- code rules: what patterns to use, which to avoid
- security instructions: no hardcoded secrets, no eval(), no concatenated SQL
- testing rules: every business logic change requires a test
- branch with cursor/[issue]/[description] prefix
- plan mode available instruction: when "plan only" is indicated

─────────────────────────────────────
GOOGLE ANTIGRAVITY (usage scoped to E2E browser tests)
─────────────────────────────────────
Mechanism: instructions in the task prompt + configuration file
Specific scope: Antigravity is an agent-first platform (editor, terminal, and
browser) capable of generating, running, and testing code autonomously — it is not
limited to browser testing. This project deliberately scopes its usage to E2E
browser tests; it is not assigned source code modification tasks.
Configuration:
- base URL per environment: [DEV_URL / QA_URL / STAGING_URL]
- test credentials: use environment variables, never hardcode
- authorized flows: list of flows it can automate
- test data: use only datasets marked as "test data", never real data
- evidence capture: screenshots and video mandatory for each executed scenario
- report: project standard format (table: scenario | result | evidence)
- restriction: do not execute in production

File to create: docs/ai-agents/antigravity-config.md

─────────────────────────────────────
MECHANISMS COMPARATIVE TABLE
─────────────────────────────────────

| Agent | Instruction Mechanism | Repo File | Scope |
|---|---|---|---|
| GitHub Copilot | .github/copilot-instructions.md | Yes, in repo | Code + analysis |
| Claude (chat/API) | System prompt pasted manually | docs/ai-agents/claude-system-prompt.md | Analysis + code |
| Claude Code | CLAUDE.md, read automatically | Yes, in repo | Analysis + code |
| OpenAI Codex | AGENTS.md + prompt | AGENTS.md | Code + shell |
| Windsurf | .windsurfrules | Yes, in repo | Code |
| Cursor | .cursorrules | Yes, in repo | Code |
| Antigravity | Task prompt | docs/ai-agents/antigravity-config.md | Code + browser (scoped to E2E in this project) |

Rules that must be present in ALL agents:
- before proposing syntax changes or refactorings, verify the local runtime version (Node.js, Python, JDK) to prevent incompatibilities
- never push directly to protected branches
- never expose secrets, tokens, or credentials
- never execute migrations without human approval
- never modify CI/CD workflows without review
- in case of ambiguity or risk, pause and escalate
- all changes are traceable: branch named with agent prefix + issue ID
```

---

## Usage with Standard Formula

```text
Use the configuration by agent type prompt and adapt it to:
- repository: [NAME OR URL]
- active agents: [LIST]
- stack: [STACK]
- methodology: [METHODOLOGY]
- critical rules: [SPECIFIC PROJECT RULES]
- autonomy level: [AUTONOMY LEVEL]
- documents to review: README, CONTRIBUTING, existing AGENTS.md (if any), repository structure
- specific output goal: complete instruction files for each active agent + comparative table
- depth level: high
```

---

## Recommended docs/ai-agents/ Folder Structure

```
docs/ai-agents/
├── README.md                    ← index of configured agents and access level
├── claude-system-prompt.md      ← base system prompt for Claude chat/API sessions
├── codex-config.md              ← configuration and restrictions for Codex
└── antigravity-config.md        ← config of environments and authorized flows for Antigravity
```

`CLAUDE.md` is deliberately left out of this folder: Claude Code only reads
it automatically when it sits at the repository root (or in the matching
folder, for path-specific context) — moving it into `docs/ai-agents/` would
make it invisible to the very mechanism it's meant to feed.
