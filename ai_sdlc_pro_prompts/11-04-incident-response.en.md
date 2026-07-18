# 11.4 — Production incident response runbook

## Description

Prompt to execute the complete incident response process in production: detection, severity classification, team activation, diagnosis, containment, resolution, communication, post-mortem and lessons learned. Compatible with multi-agent environments.

**When to use it:** when an active incident is detected in production, to document the response process afterwards, or to design the project's standard runbook before the first incident occurs.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | operation |
| Expected risk | high — coordinates actions on active production, including containment with possible rollback |
| Required inputs | symptom/alert, affected system, environment, detection time, detection source, stack |
| Allowed tools | phases 1-3 and 6-7: log/metrics reading only; phase 4 (containment) may require rollback or mitigation, always with approval |
| Permitted autonomy | A0 — Analyze in phases 1-3 and 6-7; A3 — Publish in phase 4 (rollback, mitigation, or mutation against live production is a deployment/remote mutation per `00-framework.md`, not execution in an isolated workspace), only if the runbook already authorized the specific action and with the explicit or pre-authorized-policy approval that A3 requires |
| Stop criteria | the prompt itself requires stopping all AI agent operations in the repository and not deploying code while the incident is active |
| Expected output | see `## Expected output` |
| Minimum evidence | timeline with exact time for each phase and responsible actor |
| Recommended next prompt | `03-02-causa-raiz` for formal analysis if the post-mortem requires additional depth; `11-07-sre-postmortem-runbook` to consolidate lessons learned |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Execute or design the complete incident response process for this system in production.

Required inputs:
- detected symptom or alert: [DESCRIPTION]
- affected system/service: [SERVICE]
- environment: PROD
- detection time: [HH:MM timezone]
- detected by: [automatic monitoring / user / team / AI agent]
- system stack: [STACK]

Constraints:
- during an active incident, prioritize containing the impact over pursuing the root cause: stabilizing the system for users comes before fully understanding what failed — deep root cause analysis belongs in the post-mortem (Phase 7), not in the middle of a SEV-1.
- no destructive remediation action (rollback, forced restart, failover, maintenance mode, production configuration change) is executed without explicit approval from the on-call lead, even in SEV-1 — the urgency to contain doesn't replace authorization, which can be granted in seconds over the coordination channel but must be logged.
- define and respect clear escalation and handoff triggers: if the incident exceeds its severity's resolution SLA, if the initial responder can't continue, or if diagnosis reveals the affected system isn't the one originally assumed, escalate explicitly to a higher-level responsible party or another team and document the handoff (time, from whom to whom, known state at that point).
- honor the AI-agent and deployment freeze from Phase 2 for the entire duration of the active incident, not just at the moment of detection.

## PHASE 1 — DETECTION AND CLASSIFICATION (0–5 min)

### Severity classification
Classify the incident by its impact:

| Severity | Criterion | Response SLA | Resolution SLA | Example |
|---|---|---|---|---|
| SEV-1 (Critical) | System unavailable or compromised data | 5 min | 1 hour | Site down, data breach |
| SEV-2 (High) | Critical functionality degraded | 15 min | 4 hours | Slow login, API with > 5% errors |
| SEV-3 (Medium) | Non-critical functionality affected | 1 hour | 24 hours | Secondary feature broken |
| SEV-4 (Low) | Minimal or cosmetic impact | 4 hours | 72 hours | Wrong text, warning in logs |

Respond:
- What is the severity of this incident and why?
- How many users or processes are affected?
- Is there risk of data loss or corruption?

## PHASE 2 — ACTIVATION (0–10 min)

### Notification protocol
Indicate who should be notified based on severity:
- SEV-1/2: technical lead + business stakeholder immediately
- SEV-3/4: technical lead during business hours

### Coordination channel
- Main incident channel: [CHANNEL]
- Update frequency: every [N] minutes
- Update format: [HH:MM] Status: [active/contained/resolved] | Impact: [...] | Next update: [HH:MM]

### For active AI agents in the repository during the incident
- STOP all AI agent operations in the repository
- Do not merge open PRs until incident is resolved
- Do not deploy code during the incident

## PHASE 3 — DIAGNOSIS (5–30 min)

Execute the following diagnostic steps ordered by probability and impact:

### 3.1 Immediate health verification
Commands or actions to confirm the problem scope:
- service status
- recent error logs
- key metrics (CPU, memory, latency, error rate)
- recent changes (last deploys, config changes)

### 3.2 Ordered hypotheses
Generate hypotheses by probability order:
1. [Hypothesis 1] → How to validate it → Command or evidence
2. [Hypothesis 2] → How to validate it → Command or evidence
3. ...

### 3.3 Temporal correlation
- Does the incident start coincide with a recent deploy?
- Does it coincide with a load spike or external event?
- Are other services also affected?

## PHASE 4 — CONTAINMENT (immediate if SEV-1/2)

Actions to limit impact WHILE the root cause is sought:
- rollback of last deploy (if incident started after a deploy)
- increased logging / debug mode
- rate limiting or circuit breaker if overloaded
- traffic diversion to healthy instance
- maintenance mode if necessary

Indicate the exact command and time estimate for each containment action.

## PHASE 5 — RESOLUTION

Once root cause is identified:
- description of confirmed root cause
- applied fix: description + commit + PR
- proof that the fix resolves the problem
- post-fix validation: minimum smoke test

## PHASE 6 — COMMUNICATION

### Communication during the incident
Generate communication templates for each moment:
- Initial notification (when detected)
- Progress update (every N min for SEV-1/2)
- Resolution notification

### Initial notification template
```
🔴 [ACTIVE INCIDENT] [SYSTEM] — SEV-[N]
Detection time: [HH:MM]
Symptom: [DESCRIPTION]
Impact: [AFFECTED USERS/PROCESSES]
Responding team: [RESPONSIBLE PERSON]
Next update: [HH:MM]
```

### Resolution template
```
✅ [INCIDENT RESOLVED] [SYSTEM]
Resolution time: [HH:MM]
Total duration: [X hours Y minutes]
Root cause: [BRIEF DESCRIPTION]
Applied fix: [DESCRIPTION]
Post-mortem: [SCHEDULED DATE]
```

## PHASE 7 — POST-MORTEM (within 48–72h)

This phase produces an immediate post-mortem summary. For the formal document with detailed blameless guidance and a reusable on-call runbook, continue with `11-07-sre-postmortem-runbook`.

Document the complete incident in a blameless post-mortem:

### Timeline
| Time | Event |
|---|---|
| HH:MM | First symptom detected |
| HH:MM | Alert activated |
| HH:MM | Team notified |
| HH:MM | Root cause identified |
| HH:MM | Fix deployed |
| HH:MM | Incident resolved |

### Root cause analysis (5 Whys)
Why did the incident occur → why that cause → until reaching the systemic root cause.

### Lessons learned and corrective actions
| Lesson | Corrective action | Responsible | Deadline | Issue created |
|---|---|---|---|---|
```

---

## Use with standard formula

```text
Use the incident response prompt and adapt it to:
- repository: [NAME OR URL]
- symptom: [INCIDENT DESCRIPTION]
- affected system: [SERVICE]
- environment: PROD
- detection time: [HH:MM]
- detected by: [SOURCE]
- stack: [STACK]
- documents to review: production logs, recent deploys, runbooks/, metrics
- specific output objective: severity classification + diagnostic steps + communication template
- depth level: high
```

---

## Expected output

### Incident record

| Field | Value |
|---|---|
| Incident ID | INC-[YYYYMMDD]-[NNN] |
| Severity | SEV-[N] |
| Affected system | [SYSTEM] |
| Detection time | [HH:MM TZ] |
| Resolution time | [HH:MM TZ] |
| Duration | [X hours Y min] |
| Affected | [N users / processes] |
| Root cause | [DESCRIPTION] |
| Fix | [COMMIT / PR] |
| Post-mortem | [DATE] |
| Status | active / contained / resolved |

### Incident timeline

| Time | Phase | Event | Actor |
|---|---|---|---|
| HH:MM | Detection | | |
| HH:MM | Activation | | |
| HH:MM | Diagnosis | | |
| HH:MM | Containment | | |
| HH:MM | Resolution | | |

### Example applied

| Field | Value |
|---|---|
| Incident ID | INC-20260312-014 |
| Severity | SEV-2 |
| Affected system | Checkout API |
| Detection time | 14:32 UTC |
| Resolution time | 15:10 UTC |
| Duration | 38 min |
| Affected | ~2,400 users (6.8% error rate) |
| Root cause | DB connection pool exhausted after a deploy that removed the concurrent connection limit |
| Fix | rollback of deploy `a1b2c3d` (PR #482) |
| Post-mortem | 2026-03-14 |
| Status | resolved |

| Time | Phase | Event | Actor |
|---|---|---|---|
| 14:32 | Detection | Error rate alert > 5% on checkout API | Datadog (automatic) |
| 14:36 | Activation | On-call team notified via PagerDuty, channel #inc-014 opened | on-call SRE |
| 14:50 | Containment | Rollback of deploy `a1b2c3d` executed | on-call SRE (with tech lead approval) |
| 15:10 | Resolution | Error rate back to < 0.1%, incident closed | on-call SRE |
