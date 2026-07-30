# 11.15 — Disaster recovery and business continuity plan (DR/BCP)

## Description

Prompt to design a system's disaster recovery and business continuity plan: RTO/RPO objective validation, dependency-recovery sequencing, failover procedure, backup-restore testing cadence, and plan-activation criteria for a catastrophic loss scenario (data-center/region loss, ransomware, massive data corruption). Distinct from `11-04-incident-response`, which handles an already-occurring incident of bounded scope, and from `11-09-runbook-rollback`, which reverts a single recent deployment — this prompt prepares and validates the system's full recovery capability ahead of a total-loss scenario, before it happens.

**When to use it:** when defining the initial architecture of a critical system (after `00-D-02`, where RPO/RTO objectives are declared), periodically to validate that the real recovery capability still meets those objectives, or when preparing the first formal recovery test (drill) of a system that has never been tested.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | high — an untested DR plan, or one whose RTO/RPO objectives were never validated against real recovery capability, gives a false sense of resilience until the real disaster occurs; the prompt does not execute any restore, failover, or recovery test by itself |
| Required inputs | declared RTO/RPO objectives (`00-D-02` or another source), system architecture and its critical dependencies, current backup mechanism (if any), last restore test performed (if any) |
| Allowed tools | none for execution — reading existing documentation and architecture; produces a plan document and a test procedure, does not execute any real restore or failover |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if it cannot be confirmed that the target RTO/RPO is achievable with the current backup/replication mechanism, do not declare the system "recoverable" — flag it as a capability gap and report the real estimated RTO/RPO instead |
| Expected output | see `## Expected output` |
| Minimum evidence | every critical dependency of the system appears in the recovery sequence with its own estimated RTO/RPO; any gap between the declared objective and the real recovery capability is reported explicitly, never assumed closed |
| Recommended next prompt | `11-07-sre-postmortem-runbook` if a drill or a real activation of the plan reveals failures requiring a postmortem; `00-D-04-registro-riesgos-proyecto` to log any unclosed recovery-capability gap as an open risk |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design the system's disaster recovery and business continuity plan: RTO/RPO validation, dependency-recovery sequencing, failover procedure, backup-restore testing cadence, and activation criteria.

Inputs:
- declared RTO/RPO objectives: [PASTE OR REFERENCE TO 00-D-02, OR "not declared yet"]
- system architecture and critical dependencies: [PASTE OR REFERENCE TO 04-01]
- current backup/replication mechanism: [DESCRIPTION, OR "no formal backup exists"]
- last restore test performed: [DATE AND RESULT, OR "never tested"]

Activities:
1. DISASTER SCENARIOS IN SCOPE
   Define the catastrophic scenarios covered by this plan (data-center/region loss, ransomware/massive data corruption, cloud-provider loss, irreversible accidental deletion) — don't assume every scenario recovers the same way; state whether any scenario is explicitly out of scope and why.

2. RTO/RPO VALIDATION
   For each scenario, estimate the *real* achievable RTO (recovery time) and RPO (maximum tolerable data loss) with the current backup/replication mechanism, comparing them against the declared objective — don't repeat the declared objective as if it were the verified real capability. If a gap exists between the objective and the real capability, report it explicitly with the size of the gap.

3. DEPENDENCY RECOVERY SEQUENCING
   List the system's critical dependencies (databases, queues, external services, secrets/credentials, DNS) and define the order in which they must be recovered — don't assume all of them recover in parallel with no conflict; flag which dependency blocks which.

4. FAILOVER PROCEDURE
   Define the concrete steps to activate the recovery site/region/environment, including who has authority to declare the disaster and activate the plan, and how real user traffic gets redirected.

5. TESTING CADENCE (DRILLS)
   Define how often real backup restoration must be tested and, if applicable, a full simulated failover (tabletop or technical) — a never-tested DR plan is reported as "not validated", not as "ready".

6. ACTIVATION AND DEACTIVATION CRITERIA
   Define the objective condition that formally activates the plan (vs. treating it as a normal `11-04` incident) and the condition confirming that normal operation can resume (failback).

7. CRISIS COMMUNICATION
   Define which stakeholders must be notified upon activation, through which channel, and at what update cadence while recovery is underway.

Constraints:
- never declare an RTO/RPO as "met" without verifying the real capability of the current backup/replication mechanism — an unverified objective is reported as not validated, not as achieved,
- every critical dependency must appear in the recovery sequence with its own estimated RTO/RPO — don't group distinct dependencies under one generic estimate,
- if the system has never had a real restore test, explicitly declare it as a high-severity open risk — don't omit it or assume the backup works just because it exists,
- this prompt designs the plan and the test procedure; it does not execute any real restore, failover, or recovery test,
- if the system's RTO/RPO objectives or dependency architecture are unknown, stop and request them before proposing the plan.

Output:
0. JSON metadata block (keys: status, scenarios_covered_count, rto_rpo_gaps_count, never_tested, confidence_score [0.0 to 1.0]).
1. Disaster scenarios in scope (and explicitly out of scope).
2. Target vs. real estimated RTO/RPO per scenario, with gaps flagged.
3. Critical-dependency recovery sequence, with order and blockers.
4. Failover procedure: steps, activation authority, traffic redirection.
5. Backup-restore and simulated-failover testing cadence.
6. Activation and failback criteria (return to normal operation).
7. Crisis communication plan.
```

---

## Usage with standard formula

```text
Use the disaster recovery and business continuity plan prompt and adapt it to:
- repository/project: [NAME OR URL]
- RTO/RPO objectives: [REFERENCE TO 00-D-02, OR "not declared yet"]
- architecture and critical dependencies: [REFERENCE TO 04-01]
- documents to review: current backup mechanism, result of the last restore test
- specific output objective: DR/BCP plan with validated RTO/RPO and testing cadence
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the plan summary |
| Scenarios in scope (1) | Catastrophic scenarios covered and explicitly excluded |
| Target vs. real RTO/RPO (2) | Comparison per scenario, with capability gaps flagged |
| Dependency sequence (3) | Recovery order of critical dependencies and their blockers |
| Failover procedure (4) | Steps, activation authority, traffic redirection |
| Testing cadence (5) | Frequency of restore tests and simulated failover |
| Activation/failback criteria (6) | Objective activation condition and return-to-normal condition |
| Crisis communication (7) | Stakeholders to notify, channel, and cadence |

### Example (excerpt)

```json
{
  "status": "plan_defined_with_open_gap",
  "scenarios_covered_count": 3,
  "rto_rpo_gaps_count": 1,
  "never_tested": true,
  "confidence_score": 0.68
}
```

| Scenario | Target RTO | Real estimated RTO | Target RPO | Real estimated RPO | Gap |
|---|---|---|---|---|---|
| Full region loss | 4 hours | ~9 hours (manual restore from daily backup in another region) | 1 hour | 24 hours (daily backup only, no continuous replication) | **[OPEN GAP]** neither the target RTO nor RPO is achievable with the current daily backup; requires continuous cross-region replication to close |
| Ransomware/massive data corruption | 8 hours | ~8 hours (restore from the most recent unaffected immutable backup) | 24 hours | 24 hours | Met — immutable backups verified in the last test |

| Section | Example content |
|---|---|
| Testing cadence (5) | A real restore from backup has never been executed — reported as a high-severity open risk; recommends a first restore test in an isolated environment within the next 2 weeks, followed by a quarterly cadence |
