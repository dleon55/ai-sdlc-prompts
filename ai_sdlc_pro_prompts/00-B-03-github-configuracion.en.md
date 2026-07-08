# 0-B.3 — GitHub Repository Configuration (Protections, Templates, and Settings)

## Description

Prompt to configure the GitHub repository completely and securely: branch protection, issue and PR templates, Dependabot, GitHub Actions permissions, Environments, secrets, and quality gates. Aligns the platform with the methodology and team maturity level.

**When to use:** when creating a new repository, when standardizing an existing one, or when the repo lacks formal protections and AI or multiple contributors will be incorporated.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | operation |
| Expected risk | medium — misconfigured branch protection, Actions permissions, or Environments can block the team or leave `main` without real protection; the prompt delivers commands and templates, it does not execute them |
| Required inputs | GitHub organization/user and repository name, branching methodology, branches to protect, team composition, deployment environments, CI stack |
| Allowed tools | read of the repository's current configuration (workflows, existing protections) — the prompt delivers `gh` CLI commands and template files as text; it does not run commands or modify GitHub configuration directly |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if the current state of branch protection, team roles, or real environments is not known with certainty, state the assumption explicitly instead of generating rules that could block the real team if applied |
| Expected output | see `## Expected Output` |
| Minimum evidence | the `gh` CLI commands cover every branch declared as protected; issue templates, PR template, `dependabot.yml`, and `CODEOWNERS` are complete with no unresolved placeholders |
| Recommended next prompt | `00-B-05-stack-calidad-codigo` to register the quality-gates workflow as a required check within the branch protection rules defined here |

---

## Mandatory Previous Context

> Include the block from file `00-framework.en.md` before this prompt.

---

## Complete Prompt

```text
Objective:
Generate the complete GitHub repository configuration, its protections, and work templates.

Required inputs:
- GitHub organization or user: [ORG/USER]
- repository name: [REPO]
- branching methodology: [GitFlow / GitHub Flow / Trunk-Based / other]
- protected branches: [e.g., main, develop, release/*]
- team: [roles and sizes, e.g., 3 devs + 2 QA + AI agents]
- deployment environments: [dev / staging / prod]
- CI stack: [GitHub Actions / CircleCI / other]

Deliver:

1. BRANCH PROTECTION (Branch Protection Rules)
   For each protected branch indicate:
   - requires pull request before merging: yes/no, number of reviewers
   - require status checks: what checks must pass (lint, tests, build)
   - require branches to be up to date: yes/no
   - require conversation resolution: yes/no
   - restrict who can push: list of roles
   - allow force push: never in main/develop
   - allow deletions: yes/no
   - require signed commits: recommendation
   Deliver the equivalent gh CLI command for each rule.

2. GITHUB ACTIONS PERMISSIONS
   - workflow permissions (read-only tokens by default)
   - environments with required reviewers for staging and prod
   - restriction of which workflows can use each secret
   - OIDC vs PAT: recommendation per environment

3. DEPENDABOT
   Generate the complete .github/dependabot.yml file with:
   - detected ecosystem according to the stack
   - update frequency
   - limit of open PRs
   - auto-merge for patch updates (only if tests are green)
   - ignore list for dependencies that should not be updated

4. ISSUE TEMPLATES (.github/ISSUE_TEMPLATE/)
   Generate the following files with complete content:
   a) bug_report.md:
      - bug description
      - steps to reproduce
      - expected vs actual behavior
      - environment (OS, version, stack)
      - logs or screenshots
      - acceptance criteria for considering the bug closed
   b) feature_request.md:
      - functional description
      - problem it solves
      - expected behavior
      - use cases
      - acceptance criteria
      - dependencies or impact on other modules
   c) ai_task.md (for tasks delegated to AI agents):
      - task description
      - relevant repository context
      - involved files
      - restrictions and rules
      - acceptance criteria verifiable by the agent
      - permitted autonomy level
      - human validation checklist post-execution

5. PULL REQUEST TEMPLATE (.github/PULL_REQUEST_TEMPLATE.md)
   - change description
   - related issue (#)
   - change type (feat / fix / docs / refactor / test / chore)
   - checklist: tests, docs, impact on other modules, no secrets, security review
   - instructions for the reviewer
   - deployment notes

6. CODEOWNERS (.github/CODEOWNERS or root)
   - map of responsible persons per directory/file type
   - special rule: mandatory human review for changes in /.github/, /workflows/, /migrations/

Output format:
- complete content of each file ready to copy
- gh CLI commands to configure branch protections
- summary table: area | configuration | priority | risk if omitted
```

---

## Usage with Standard Formula

```text
Use the GitHub repository configuration prompt and adapt it to:
- repository: [ORG/REPO]
- methodology: [BRANCHING STRATEGY]
- CI stack: [GITHUB ACTIONS / OTHER]
- environments: [DEV / STAGING / PROD]
- team: [COMPOSITION]
- documents to review: existing workflows, README, CONTRIBUTING
- specific output goal: ISSUE_TEMPLATE/, PR_TEMPLATE, dependabot.yml, CODEOWNERS files + gh CLI commands for branch protection
- depth level: high
```

---

## Expected Output

| Area | File/Configuration | Priority | Risk if Omitted |
|---|---|---|---|
| Branch protection | `gh api` rules for main | Mandatory | Direct commits, force push on history |
| PR template | `.github/PULL_REQUEST_TEMPLATE.md` | Mandatory | PRs without context, incomplete reviews |
| Bug template | `.github/ISSUE_TEMPLATE/bug_report.md` | Mandatory | Issues without sufficient data for reproduction |
| Feature template | `.github/ISSUE_TEMPLATE/feature_request.md` | Mandatory | Ambiguous requirements without acceptance criteria |
| AI task template | `.github/ISSUE_TEMPLATE/ai_task.md` | Mandatory if using agents | Agents operating without clear limits or criteria |
| CODEOWNERS | `.github/CODEOWNERS` | Recommended | PRs approved without area owner review |
| Dependabot | `.github/dependabot.yml` | Recommended | Vulnerable dependencies not automatically detected |
| Environments | GitHub Settings → Environments | Recommended | Deployments to prod without human approval |
