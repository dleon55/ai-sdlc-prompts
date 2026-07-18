# 11.11 — Legacy system/service decommission plan

## Description

Prompt to plan the complete, safe shutdown of a system, service, or database that is being retired — distinct from partial API versioning/deprecation (covered by `04-05-versionado-deprecacion-api`). Includes an inventory of active dependents, data retention/export obligations before shutdown, a communication plan with a grace window, and a phased shutdown sequence with rollback checkpoints in case an undetected dependent surfaces.

**When to use it:** when a decision is made to fully retire a system, service, or database, before executing any shutdown action.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | operation |
| Expected risk | high — decommissioning a system with undetected dependents can break production services or reports without warning; losing data subject to a retention obligation (legal, tax, contractual) can have legal consequences |
| Required inputs | system/service to decommission, known inventory of consumers/integrations, applicable data retention obligations, target shutdown date, availability of recent access/traffic logs for the system |
| Allowed tools | reading access/traffic logs, code of known integrations, data retention contracts, and architecture documentation; the plan design is analysis and proposal only — actual shutdown execution requires explicit approval and happens outside this prompt |
| Permitted autonomy | A0 — Analyze (dependent inventory, retention obligations); A1 — Propose (communication plan and shutdown sequence); A3 — Publish only to execute each shutdown phase (disable writes, switch to read-only, final shutdown) against the real system, and only with explicit approval before each phase — it does not execute any shutdown phase on its own |
| Stop criteria | stop if recent access/traffic logs are unavailable or do not cover a representative period — do not assume "no visible traffic" means "no dependents"; stop if a data retention obligation exists without a compliance plan before the shutdown date |
| Expected output | see `## Expected output` |
| Minimum evidence | every identified dependent cites the source that confirms it (access log, integration code, documentation); every shutdown phase has a verification checkpoint and an explicit rollback criterion |
| Recommended next prompt | `04-05-versionado-deprecacion-api` if the decommission is partial (one API version, not the full system) and this prompt does not apply; `11-09-runbook-rollback` if an undetected dependent surfaces during execution and an already-executed phase must be reverted |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design the complete safe decommission plan for a system, service, or database being retired: dependent inventory, data retention obligations, communication plan, and a phased shutdown sequence with rollback checkpoints.

Inputs:
- system/service to decommission: [NAME OR DESCRIPTION]
- known inventory of consumers/integrations: [LIST OR "to be determined"]
- available recent access/traffic logs: [PERIOD COVERED OR "not available"]
- data retention obligations: [LEGAL / TAX / CONTRACTUAL / NONE KNOWN]
- target shutdown date: [DATE]
- system stack/infrastructure: [STACK]

Steps:
1. ACTIVE DEPENDENT INVENTORY
   From recent access/traffic logs and known integration code, identify every active consumer of the system (services, reports, batch jobs, external integrations, direct users). If the logs do not cover a representative period (e.g. processes that run only monthly/quarterly), explicitly flag it as a visibility gap before concluding there are no dependents.

2. DEPENDENT CRITICALITY CLASSIFICATION
   For each identified dependent, classify the impact of it ceasing to work (business-critical, acceptable degradation, already obsolete) and whether an alternative is already available or migration is needed before shutdown.

3. DATA RETENTION AND EXPORT OBLIGATIONS
   Verify whether a data retention obligation (legal, tax, contractual) applies to the system's information. If it does, define what data must be exported, in what format, to where, and for how long it must be kept after shutdown. If you cannot confirm whether an applicable obligation exists, state it as an unresolved risk instead of assuming it does not apply.

4. COMMUNICATION PLAN AND GRACE WINDOW
   Define who must be notified (owners of identified dependents, direct users if applicable), how much advance notice, and what grace window is offered for dependents to migrate or stop using the system before final shutdown.

5. SAFE SHUTDOWN SEQUENCE (phased)
   Design the shutdown in phases of decreasing reversibility, never all at once:
   a) Disable new writes (the system remains available read-only) — reversible phase.
   b) Read-only during the agreed grace window, monitoring for unexpected traffic.
   c) Final shutdown (the system stops responding) — lowest-reversibility phase, only after confirming no traffic in the previous phase.
   For each phase, define the verification checkpoint (what to check before advancing to the next) and the rollback criterion if an undetected dependent surfaces.

6. PER-PHASE ROLLBACK PLAN
   For each phase of the sequence, explicitly define how to revert if an undetected dependent surfaces (e.g. re-enable writes, restore the system from the last backup) and the estimated time for that reversal.

Constraints:
- do not conclude a system has no dependents just because recent traffic logs show no activity — if the covered period is not representative (infrequent processes, seasonal integrations), flag it as a visibility gap and treat the risk as unresolved,
- do not propose or execute the final shutdown in a single phase — shutdown must be progressive (disable writes → read-only → final shutdown), with a verification checkpoint between each phase,
- if a data retention obligation exists and there is no confirmed export/preservation plan, stop and do not continue with the shutdown sequence until it is resolved,
- every shutdown phase actually executed against the real system requires prior explicit approval — this prompt designs the plan, it does not execute it on its own,
- if an undetected dependent surfaces during any phase, the plan must explicitly call for reverting that phase before continuing, never "wait and see if it resolves itself".

Output:
- dependent inventory, with criticality and confirming source
- data retention obligations and export/preservation plan
- communication plan and grace window
- phased shutdown sequence, with checkpoint and rollback criterion per phase
- residual risks (visibility gaps, unconfirmable dependents)
```

---

## Use with standard formula

```text
Use the legacy system decommission plan prompt and adapt it to:
- repository/project: [NAME OR URL]
- system/service to decommission: [NAME OR DESCRIPTION]
- known inventory of consumers: [LIST OR "to be determined"]
- available access logs: [PERIOD COVERED OR "not available"]
- retention obligations: [LEGAL / TAX / CONTRACTUAL / NONE KNOWN]
- target shutdown date: [DATE]
- documents to review: traffic logs, integration code, retention contracts
- specific output objective: complete decommission plan with a safe shutdown sequence
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Dependent inventory | Consumer, criticality, confirming source |
| Data retention | Applicable obligation, what to export, format, and preservation time |
| Communication plan | Who to notify, how much advance notice, grace window |
| Shutdown sequence | Phases with verification checkpoint and rollback criterion |
| Residual risks | Visibility gaps or unconfirmable dependents |

### Example (excerpt)

| Dependent | Criticality | Source |
|---|---|---|
| Monthly financial reporting service | Critical — generates the accounting close | Scheduled job detected in the task orchestrator, runs on day 1 of each month (outside the initially reviewed log window — the review window was extended to 60 days to capture it) |
| Logistics provider integration (deprecated 8 months ago) | Already obsolete | No traffic in the last 90 days of logs; confirmed with the logistics team that they migrated to the new provider |

**Shutdown sequence, phase 1:** Disable new writes. Checkpoint: monitor for 5 business days looking for rejected write attempts in the logs. Rollback: re-enable writes immediately if an unanticipated attempt appears; estimated reversal time: under 10 minutes (configuration flag).
