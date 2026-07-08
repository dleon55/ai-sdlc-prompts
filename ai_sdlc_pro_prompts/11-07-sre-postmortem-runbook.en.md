# 11.7 — Blameless Post-Mortem and Runbook Generation (SRE)

## Description

Prompt designed to adopt the SRE (Site Reliability Engineering) culture. It takes raw data from a resolved incident (logs, Slack chats, metrics) and generates a "Blameless" Post-Mortem document, identifying the true root cause and extracting an automatable Runbook to mitigate similar future incidents.

**When to use it:** Immediately after resolving a critical incident or production outage (Phase 03 completed), to document institutional learning.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | medium — the resulting runbook can be executed directly by the on-call team in future incidents, so an incorrect or unreviewed step can worsen a real incident |
| Required inputs | raw incident data (timeline, logs, chat), applied resolution; optionally the root cause analysis result from `03-02` |
| Allowed tools | read-only access to the provided incident data; does not execute commands against live systems, the incident is already resolved |
| Permitted autonomy | A1 — Propose: delivers the post-mortem document and the proposed runbook; adopting it as the official runbook operable by on-call requires human review (A3) |
| Stop criteria | if the 5 Whys analysis converges on attributing the failure to a person instead of a system or process, it must reframe the finding in blameless terms before continuing; if there is insufficient incident data, it must flag that instead of inventing the timeline |
| Expected output | see `## Expected output` |
| Minimum evidence | timeline with verifiable times and phases, action items formulated as actionable tickets, and a runbook with executable, checkable commands/queries |
| Recommended next prompt | `10-04-observabilidad-instrumentacion` if the post-mortem reveals monitoring blind spots; `11-06-gestion-parches-actualizaciones` if the root cause is an outdated dependency |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.
> Attach the root cause analysis result (`03-02`) if available.

---

## Complete prompt

```text
Objective:
Act as a Site Reliability Engineer (SRE). Draft a Blameless Post-Mortem document based on the provided incident data, and generate an actionable Runbook for the on-call team.

Inputs:
- incident_data: [PASTE TIMELINES, LOGS, OR INCIDENT SUMMARY HERE]
- applied_resolution: [HOW THE PROBLEM WAS SOLVED]

Analysis Activities:
1. INCIDENT TIMELINE: Chronologically reconstruct the event (Detection, Triage, Mitigation, Resolution).
2. BLAMELESS ANALYSIS: Identify failures in the system, observability, or processes, NEVER in people ("The system allowed a direct push to break production" instead of "John broke production").
3. ROOT CAUSE (5 Whys): Execute the 5 Whys to reach the underlying structural defect.
4. RUNBOOK DESIGN: Create deterministic steps for a mitigating on-call engineer (or a bot) to resolve this in the future.

Mandatory Output:
1. POST-MORTEM DOCUMENT: Structured with: User Impact, Timeline, Root Cause, and Action Items (preventive tickets).
2. ON-CALL RUNBOOK: Step-by-step instructions (terminal commands, queries, dashboards to check) to mitigate if it happens again.

Constraints:
- keep the blameless principle throughout the whole document, not only in the 5 Whys analysis: if a recommendation or action item implies "the person should be more careful," reframe it as a system or process change (better validation, automated gate, additional alert).
- do not publish the post-mortem with timeline claims that aren't backed by evidence (log timestamps, chat messages, metrics) — if a milestone is uncertain, explicitly flag it as estimated instead of presenting it as a verified fact.
- explicitly distinguish contributing factors (conditions that worsened the incident or delayed its detection or mitigation) from the root cause (the structural defect that, had it not existed, would have prevented the incident) — don't mix them into a single unlabeled list.
- if the provided incident data isn't enough to reconstruct a timeline step or confirm the root cause, flag the gap explicitly in the document instead of filling it in with a reasonable assumption.
```

---

## Use with standard formula

```text
Use the SRE post-mortem prompt and adapt it to:
- incident_data: [INCIDENT TEXT]
- applied_resolution: [TEXT]
- specific output objective: generate institutional post-mortem document and on-call playbook.
- depth level: exhaustive
```

---

## Expected output

| Section | Expected content |
|---|---|
| Post-Mortem | Standard SRE document (Impact, Timeline, 5 Whys, Action Items) |
| Blameless Approach | Language that audits processes and systems, not individuals |
| Runbook | Executable commands and checks for On-Call |

### Example applied

| Section | Example content |
|---|---|
| Post-Mortem | "On March 12, a deploy without a connection-limit review removed the configured maximum on the checkout API's connection pool, exhausting database connections. Duration: 38 minutes. Impact: ~2,400 users with failed checkout (6.8% error rate)." |
| Runbook | "1. Check `SELECT count(*) FROM pg_stat_activity;` — if it exceeds 90% of the configured pool, 2. Run `kubectl rollout restart deploy/checkout-api` to free orphaned connections, 3. If the count doesn't drop within 2 minutes, escalate to the on-call DBA." |
