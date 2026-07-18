# 11.9 — Rollback Execution Runbook

## Description

Prompt to decide whether a recently deployed change should be rolled back or fixed forward, and to design (and, when authorized, guide) the rollback execution: the exact mechanics per change type (code deploy, database migration, config/feature flag, infrastructure), how to handle data written on the new version, and verification that the rollback actually restored a healthy state.

**When to use it:** when a recently shipped change is causing problems and a rollback is being considered or executed. If this is an active incident that hasn't been triaged yet, use `11-04-incident-response` first to classify severity, contain, and decide the course of action — this prompt is invoked once rollback is already the chosen path (for example, from that runbook's Phase 4 containment). After executing the rollback, continue with `11-07-sre-postmortem-runbook` to document what happened and why.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | operation |
| Expected risk | high — rollback decisions happen under time pressure during an active problem; a poorly executed rollback (one that loses data written on the new version, or that assumes a database migration is reversible when it isn't) can make things worse instead of resolving them |
| Required inputs | symptom driving the rollback, affected component(s) and their change type (code / DB migration / config or feature flag / infrastructure), target version or state to revert to, whether data was written on the new version, environment |
| Allowed tools | design of the rollback plan and decision criteria: read-only access to logs, metrics, deploy history, and migration definitions; actual execution against a live environment is limited by the autonomy below |
| Permitted autonomy | A1 — Propose for the entire design of the decision criteria and the rollback runbook; A2 — Execute controlled only in an isolated environment (staging/QA) once the explicit preconditions are already verified (previous version confirmed deployable, migration reversibility confirmed); A3 — Publish to execute the rollback against production, and in particular any rollback touching a database migration or production data — this is a deployment/remote mutation per `00-framework.md`, not execution in an isolated workspace, and requires the explicit or pre-authorized-policy approval that A3 requires before each action — this prompt does not grant itself broader execution rights than that |
| Stop criteria | stop and escalate if a database migration's reversibility cannot be confirmed; stop if it cannot be confirmed that the previous version is deployable (dependencies, configuration); stop if the rollback would imply data loss not explicitly accepted by the system's responsible party; do not execute any action against production without the explicit approval this contract requires |
| Expected output | see `## Expected output` |
| Minimum evidence | each component to revert with its reversibility explicitly assessed, execution steps in order with a concrete command or action, and post-rollback verification against the original symptom, not just against deployment technical success |
| Recommended next prompt | `11-07-sre-postmortem-runbook` to document the incident and the rollback that was executed |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Decide whether to roll back or fix forward, and design (or guide, if already authorized) the rollback execution for this change.

Required inputs:
- symptom driving the rollback: [DESCRIPTION]
- affected component(s): [LIST]
- change type(s) involved: [code / DB migration / config or feature flag / infrastructure — can be more than one]
- target version or state to revert to: [REFERENCE — commit, tag, migration version, previous config value]
- was data written on the new version since it was deployed?: [YES / NO / UNKNOWN]
- environment: [DEV / QA / STAGING / PROD]
- is there an active incident coordinated in another channel/runbook?: [YES, reference / NO]

Steps:

1. CONFIRM THE DECISION CRITERIA (rollback vs. roll-forward)
   Do not assume reverting is always the right call. For this specific problem, evaluate:
   - would a scoped hotfix resolve the symptom faster and with less risk than a full rollback?
   - is the rollback technically simple because the change is isolated (a single container image, a single flag), or complex because it touches several coupled components?
   - how long does each option take, who executes it, and how reversible is the rollback itself if something goes wrong?
   Explicitly state the decision (rollback / roll-forward) and the reasoning.

2. IDENTIFY EXACTLY WHAT NEEDS TO ROLL BACK
   Break the deployed change into its parts and classify each one:
   - application code (deploy of a previous image/artifact)
   - database migration (schema and/or data)
   - configuration or feature flag
   - infrastructure change (IaC, cloud resources, network)
   Each type has different mechanics and risk — don't treat rollback as a single generic action.

3. CONFIRM THE PREVIOUS VERSION IS ACTUALLY DEPLOYABLE (if rolling back code)
   - was the previous version confirmed working before the current deploy (not already a broken version)?
   - are its external dependencies (APIs, DB schema, message format) still compatible with the system's current state, or has the system already moved forward incompatibly?
   - if either point can't be confirmed, explicitly declare it a blocker before continuing.

4. ASSESS DATABASE MIGRATION REVERSIBILITY (if applicable)
   Before proposing any execution steps, explicitly determine:
   - is the migration reversible without data loss (e.g., adding a nullable column) or does it carry potential loss (e.g., dropped columns, data transformations, merged partitions)?
   - if not safely reversible, exactly what data would be lost and who must approve that loss?
   - is there a tested rollback script (down migration), or would it need to be rebuilt from a backup?
   Many migrations are NOT safely reversible — this analysis must be completed and documented before executing anything, not discovered mid-rollback.

5. HANDLE DATA WRITTEN ON THE NEW VERSION
   If writes (transactions, records, events) happened since the version being rolled back was deployed:
   - will that data be lost when reverting, preserved as-is, or does it need migrating back to a format the previous version can read?
   - is there an incompatibility window between the new data format and what the previous version knows how to read?
   - if data loss is unavoidable, quantify it (how many records, which users or processes) and identify who must explicitly accept it.

6. DEFINE THE EXECUTION STEPS IN ORDER
   For each step indicate: description of the action, exact command or procedure, expected result, and how to verify that specific step succeeded before moving to the next one. Order the steps considering dependencies between components (for example, whether to revert code before or after reverting the migration depending on which one breaks compatibility).

7. DEFINE POST-ROLLBACK VERIFICATION
   Don't stop at confirming the previous version's deploy technically succeeded. Specifically verify that the original symptom that triggered the rollback is resolved:
   - the metric or behavior that triggered the decision, measured after the rollback
   - critical flows working end-to-end
   - absence of new errors introduced by the rollback itself (for example, incompatibility between old code and already-migrated data)

8. COMMUNICATE ROLLBACK STATUS
   If there's an active coordinated incident (`11-04-incident-response`), follow its channel and communication format. If not, define it anyway: who to notify before executing, who to notify upon completion, and what minimum information each notification must include (component reverted, status, known residual impact).

Constraints:
- never execute a rollback of a database migration without first explicitly confirming whether it's reversible and what data, if any, will be lost — this is declared before proposing execution steps, not discovered during execution.
- executing a rollback against a live or production environment requires the autonomy and explicit approval indicated for this prompt; do not grant yourself broader execution rights than what is defined.
- if you cannot confirm that the previous version is deployable or that a migration is reversible, say so explicitly and treat that as a stop condition, not a reasonable assumption to proceed on.
- document every rollback executed, even successful ones, since they are operationally significant events that feed into the post-mortem and reliability metrics.
- do not propose a partial rollback (reverting the code but leaving the migration applied, or vice versa) without explicitly flagging the risk of leaving the system in an inconsistent state.

Deliver:
1. Rollback vs. roll-forward decision with justification.
2. Breakdown of the change into components to revert, with reversibility assessed per component.
3. Plan for handling data written on the new version.
4. Ordered execution steps with command/action and verification per step.
5. Post-rollback verification plan against the original symptom.
6. Communication plan for rollback status.
```

---

## Use with standard formula

```text
Use the rollback runbook prompt and adapt it to:
- repository: [NAME OR URL]
- symptom driving the rollback: [DESCRIPTION]
- affected component(s): [LIST]
- change type(s): [code / DB migration / config-flag / infrastructure]
- rollback target version: [REFERENCE]
- writes on the new version: [YES / NO / UNKNOWN]
- environment: [DEV / QA / STAGING / PROD]
- associated active incident: [REFERENCE OR NONE]
- documents to review: deploy history, applied migrations, runbooks/, metrics dashboards
- specific output objective: rollback/roll-forward decision + execution plan + post-rollback verification
- depth level: high
```

---

## Expected output

| Component to revert | Reversible | Execution steps | Data loss risk | Post-rollback verification |
|---|---|---|---|---|
| [code / DB migration / config-flag / infra] | Yes / No / Partial | [Sequence of commands/actions] | [None / Quantified description] | [What is measured and expected threshold] |

### Example applied

| Component to revert | Reversible | Execution steps | Data loss risk | Post-rollback verification |
|---|---|---|---|---|
| Code deploy: checkout API `v2.14.0` → `v2.13.2` | Yes — previous version confirmed stable in production for 3 weeks, no pending schema changes | 1. `kubectl set image deploy/checkout-api checkout-api=registry/checkout-api:2.13.2` 2. `kubectl rollout status deploy/checkout-api` 3. Verify 0 pods in `CrashLoopBackOff` | None — version `2.13.2` reads the same DB schema, no new columns were added in `v2.14.0` | `POST /checkout` error rate back to < 0.1% within 5 min; P95 latency < 300ms; 20 end-to-end smoke-test checkouts succeed |
| DB migration: `add_loyalty_points_column` (v2.14.0) | Partial — the `loyalty_points` column is reversible (`DROP COLUMN`) without data loss because no other process has written to it yet, but **requires explicit approval from the on-call DBA before executing** | 1. Confirm `SELECT count(*) FROM orders WHERE loyalty_points IS NOT NULL;` = 0 (nothing written yet) 2. Run `down` migration `2026071201_add_loyalty_points_column` 3. Verify `\d orders` no longer shows the column | None if step 1's count is 0; if greater than 0, STOP and escalate — those records would be lost on `DROP COLUMN` | `SELECT * FROM orders LIMIT 5;` returns without error; `orders` integration suite green |
