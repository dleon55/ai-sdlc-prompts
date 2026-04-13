# 11.4 — Production incident response runbook

## Description

Prompt to execute the complete incident response process in production: detection, severity classification, team activation, diagnosis, containment, resolution, communication, post-mortem and lessons learned. Compatible with multi-agent environments.

**When to use it:** when an active incident is detected in production, to document the response process afterwards, or to design the project's standard runbook before the first incident occurs.

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
- affected system/service: [NAME]
- environment: PROD
- detection time: [HH:MM timezone]
- detected by: [automatic monitoring / user / team / AI agent]
- system stack: [STACK]

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
Responding team: [NAME]
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
