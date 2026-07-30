# 11.14 — Platform or legacy system migration and cutover plan

## Description

Prompt to design the migration plan for moving a platform, system, or stack from an old one to a new one: data migration strategy (big-bang vs. incremental, dual-write, backfill), traffic cutover sequencing (all-at-once vs. progressive), consistency verification between the source and target systems, and a rollback plan specific to the migration. This is the step that happens **before** the source system can be decommissioned with `11-11-plan-decomiso-sistema-legacy`, and is distinct from `08-05-revision-migracion-esquema-bd`, which only reviews the safety of an already-written database schema change — this prompt designs the complete movement of an application, its data, and its traffic between two systems.

**When to use it:** when deciding to move an application, its data, or its traffic from an old system/stack/cloud to a new one (major stack upgrade, cloud migration, system consolidation, monolith→microservices) — before executing any real cutover, and as a mandatory prior step to `11-11` if the end goal is to shut down the source system.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | high — a poorly sequenced migration can cause data loss, unplanned downtime, or inconsistency between systems if traffic is cut over before backfill or verification are complete; the prompt does not execute any data migration or move real traffic by itself |
| Required inputs | source and target systems (description, stack, data volume), target architecture if it exists (`00-D-02`/`04-01`), tolerable downtime constraints, known dependents of the source system (`11-11` inventory if it exists) |
| Allowed tools | none for execution — reading existing documentation and architecture; produces a plan document, does not execute any data migration or traffic cutover |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if a data-consistency verification strategy between source and target cannot be confirmed, do not declare the cutover plan ready to execute — mark it blocking instead of assuming consistency |
| Expected output | see `## Expected output` |
| Minimum evidence | each cutover stage declares a verifiable advancement criterion and a specific rollback plan; the data migration strategy declares the consistency-verification method used |
| Recommended next prompt | `11-11-plan-decomiso-sistema-legacy` once cutover is complete and the source system no longer receives traffic; `11-09-runbook-rollback` for a single deployment's rollback within the cutover plan, if applicable |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design the migration and cutover plan for moving an old system, platform, or stack to a new one, with a data migration strategy, traffic cutover sequencing, consistency verification, and a rollback plan specific to the migration.

Inputs:
- source system: [DESCRIPTION, STACK, APPROXIMATE DATA VOLUME]
- target system: [DESCRIPTION, STACK, OR REFERENCE TO 00-D-02/04-01]
- reason for migration: [STACK UPGRADE / CLOUD MIGRATION / CONSOLIDATION / MONOLITH→MICROSERVICES / OTHER]
- tolerable downtime: [MAXIMUM ACCEPTABLE WINDOW, OR "zero downtime required"]
- known dependents of the source system: [PASTE OR REFERENCE TO THE 11-11 INVENTORY, OR "not yet inventoried"]

Activities:
1. SCOPE INVENTORY
   Define what migrates (data, functionality, integrations, users/tenants) and what is explicitly left out of this migration phase, with the reason — don't leave any source-system component without an explicit decision on whether it migrates or not.

2. DATA MIGRATION STRATEGY
   Define big-bang (single cutover of all data) vs. incremental (by batch, tenant, or region); if incremental, define the order. If the system must keep operating during the migration, define the dual-write strategy (writing to both systems simultaneously) or continuous sync, and the backfill mechanism for historical data predating the start of migration.

3. CONSISTENCY VERIFICATION
   Define how it will be confirmed, with concrete evidence (record counts, checksums, sampling, reconciliation), that data in the target system is consistent with the source before cutting over traffic. Never declare consistency achieved without a cited verification method; also define the acceptable discrepancy threshold, if any.

4. CUTOVER STRATEGY
   Define all-at-once vs. progressive (canary by user segment, tenant, or region). If progressive, define the objective advancement criterion between stages and who has authority to decide advancing to the next stage.

5. ROLLBACK PLAN SPECIFIC TO THE MIGRATION
   Distinct from a single deployment's rollback: define how to revert traffic back to the source system if the target fails after cutover, including what happens to data written to the target during the window it was active (it's lost, reconciled back to the source, or other). If no viable rollback strategy exists for a given stage, declare it as an open risk instead of omitting it.

6. SUCCESS AND CLOSURE CRITERIA
   Define what confirms the migration is complete (target system stably serving 100% of traffic, with no pending reconciliation errors). This is the point at which the source system becomes a candidate for `11-11-plan-decomiso-sistema-legacy`.

7. COMMUNICATION
   Define which stakeholders or teams must be notified before, during, and after cutover, and through which channel.

Constraints:
- never declare "migration complete" without a cited and confirmed data-consistency verification criterion — a migration with no verification is reported as unverifiable, not as successful,
- every stage of a progressive cutover must declare its own advancement criterion and its own rollback plan — don't assume the last stage's rollback covers earlier stages,
- do not propose cutting over 100% of traffic in a single step if the declared tolerable downtime is "zero" and there is no dual-write or continuous-sync strategy — flag that contradiction explicitly instead of ignoring it,
- this prompt designs the plan; it does not execute any data migration, cut over real traffic, or modify infrastructure configuration,
- if data about the source system's dependents (users, integrations, other services) is missing, stop and request the inventory — or run the inventory phase of `11-11` first — before proposing the plan.

Output:
0. JSON metadata block (keys: status, migration_strategy, cutover_stages_count, unmitigated_rollback_risks_count, confidence_score [0.0 to 1.0]).
1. Scope inventory: what migrates, what doesn't, and why.
2. Data migration strategy: method, backfill, dual-write if applicable.
3. Consistency verification plan: method, acceptable discrepancy threshold.
4. Cutover plan: stages, advancement criterion per stage, decision owner.
5. Rollback plan per stage.
6. Success and closure criteria (ready for `11-11`).
7. Communication plan.
```

---

## Usage with standard formula

```text
Use the platform migration and cutover prompt and adapt it to:
- repository/project: [NAME OR URL]
- source system: [DESCRIPTION AND STACK]
- target system: [DESCRIPTION AND STACK, OR REFERENCE TO 00-D-02/04-01]
- tolerable downtime: [MAXIMUM ACCEPTABLE WINDOW]
- documents to review: target architecture, dependents inventory (11-11) if it exists
- specific output objective: migration and cutover plan with consistency verification and per-stage rollback
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the plan summary |
| Scope inventory (1) | What migrates and what doesn't, with justification |
| Data migration strategy (2) | Method (big-bang/incremental), backfill, dual-write if applicable |
| Consistency verification (3) | Concrete method and acceptable discrepancy threshold |
| Cutover plan (4) | Stages with advancement criterion and decision owner |
| Rollback plan (5) | Reversal strategy specific to each cutover stage |
| Success and closure criteria (6) | Objective condition to consider the migration complete |
| Communication (7) | Stakeholders to notify, timing, and channel |

### Example (excerpt)

```json
{
  "status": "plan_defined_with_open_risk",
  "migration_strategy": "incremental_per_tenant_with_dual_write",
  "cutover_stages_count": 4,
  "unmitigated_rollback_risks_count": 1,
  "confidence_score": 0.71
}
```

| Stage | Scope | Advancement criterion | Owner | Rollback |
|---|---|---|---|---|
| 1 — Canary | 2% of tenants (internal test accounts) | 0 reconciliation errors in 48h, P95 latency within ±10% of the source system | Migration tech lead | Revert DNS/routing to the source system; data written to target during the window is discarded (no real-user writes occurred) |
| 2 — 10% of tenants | Low-volume tenants, no strict contractual SLA | 0 reconciliation errors in 72h | Tech lead + Product approval | Revert routing; reconcile data written to target during the window back to the source (short window, low volume) |
| 4 — 100% | All tenants | Target system stable for 7 days with no high-severity incidents | Project sponsor | **[OPEN RISK]** no viable reconciliation strategy exists to revert 100% of traffic after 7 days of writes to the target — requires a sponsor decision on data-loss tolerance in case of a late rollback |
