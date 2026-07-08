# 9.1 — Controlled integration with branches

## Description

Prompt to plan the integration of changes with other active branches: analysis of potential conflicts, recommended strategy (merge, rebase, cherry-pick) and concurrency risks with other agents or developers.

**When to use it:** before merging to any target branch, especially in environments with concurrent changes.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — does not execute the merge, but a poorly evaluated strategy can cause conflicts or overwrite changes from other agents or developers |
| Required inputs | commit history, list of active branches, related open PRs |
| Allowed tools | reading git history and state (`git log`, `git diff`, `git branch`) — no merge, rebase, cherry-pick or push execution |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if the local state is not synced with the remote (`git fetch` pending) or there are active branches from other agents with unverified changes, stop and request synchronization before recommending a definitive strategy |
| Expected output | see `## Expected output` |
| Minimum evidence | each potential conflict must cite the specific file or area and the branch it collides with |
| Recommended next prompt | `09-02-monitoreo-ci` once the integration has run, to validate the resulting pipeline status |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze how to integrate the changes with other active branches, avoiding conflicts and ensuring functional and technical consistency.

Include:
1. related branches,
2. potentially conflicting changes,
3. recommended strategy:
   - merge,
   - rebase,
   - cherry-pick,
   - controlled wait,
   - phased integration.
4. integration risks.
```

---

## Use with standard formula

```text
Use the controlled integration prompt and adapt it to:
- repository: [NAME OR URL]
- source branch: [BRANCH WITH CHANGES]
- target branch: [DEVELOP / MAIN / RELEASE]
- environment: [QA / STAGING / PROD]
- components: [MODIFIED COMPONENTS]
- documents to review: commit history, active branches, open PRs
- specific output objective: integration strategy with conflict resolution plan
- depth level: high
```

---

## Expected output

| Element | Detail |
|---|---|
| Related branches | List of active branches with concurrent changes |
| Potential conflicts | Files or areas with conflict risk |
| Recommended strategy | merge / rebase / cherry-pick with justification |
| Integration risks | What can break when integrating |
| Merge conditions | Criteria that must be met before integrating |
| Rollback | How to revert if integration fails |
