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

Steps:
1. Verify the local state is synced with the remote (`git fetch`) before analyzing anything; analysis based on stale information can recommend a strategy that no longer applies.
2. Identify related active branches: same areas of the code, same functional module, or same issue/epic, and who is working on them (agent or developer).
3. Compare the commit history and diff of each related branch against the source branch to detect potentially conflicting changes: same files, same functions, concurrent schema migrations.
4. Evaluate the most suitable integration strategy based on the type of conflict and the state of the branches:
   - merge — when history must be preserved and there are no relevant conflicts,
   - rebase — when a linear history is desired and the source branch has not been shared with other agents,
   - cherry-pick — when only a subset of commits is needed,
   - controlled wait — when another active branch is about to merge and its result would change the analysis,
   - phased integration — when the change is large and splitting it into verifiable steps is safer.
5. Document the integration risks: what can break, which tests must be re-run after integrating, and what state each component is left in if the integration stops halfway through.
6. Define the conditions that must be met before running the merge (green CI, approved code review, no active branches with unverified changes) and a rollback plan if the integration fails.

Constraints:
- don't execute merge, rebase, cherry-pick, or push — this prompt only produces the analysis and recommendation, execution requires explicit human approval,
- if the local state is not synced with the remote or there are active branches from other agents with unverified changes, stop and request synchronization before recommending a definitive strategy,
- don't assume the contents of a branch you haven't been able to inspect directly; if access is limited, flag it as a visibility gap instead of inferring its state,
- every reported potential conflict must cite the specific file or area and the branch it collides with — don't generalize "there may be conflicts" without concrete evidence.

Deliver:
- recommended integration strategy with justification,
- conflict resolution plan,
- merge conditions and rollback plan.
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
| Related branches | `feature/checkout-refactor` (source branch), `feature/payment-retry` (touches `PaymentService`, PR #482 in review, CI green), `hotfix/payment-timeout` (merged 2 days ago, already integrated into `develop`) |
| Potential conflicts | `src/services/PaymentService.ts` — both branches modify `processPayment()`; `migrations/024_add_retry_column.sql` vs `migrations/025_add_payment_status.sql` — concurrent migrations on the same table |
| Recommended strategy | controlled wait: wait for `feature/payment-retry` (PR #482) to merge into `develop` first, then rebase `feature/checkout-refactor` onto `develop` — avoids resolving the same conflict twice and reduces the risk of rewriting shared history |
| Integration risks | if `PaymentService.processPayment()`'s signature changes in `feature/payment-retry`, checkout integration tests may fail silently until the next CI run; possible breaking change for internal consumers of the `/api/payments` endpoint |
| Merge conditions | green CI on both branches, approved code review, `feature/payment-retry` merged into `develop` before starting the rebase, no other active branches touching `PaymentService` |
| Rollback | revert the merge commit on `develop` (`git revert -m 1 <sha>`) + re-run the payments integration suite before retrying the integration |
