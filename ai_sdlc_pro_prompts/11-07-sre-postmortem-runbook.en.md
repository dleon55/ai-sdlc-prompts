# 11.7 — Blameless Post-Mortem and Runbook Generation (SRE)

## Description

Prompt designed to adopt the SRE (Site Reliability Engineering) culture. It takes raw data from a resolved incident (logs, Slack chats, metrics) and generates a "Blameless" Post-Mortem document, identifying the true root cause and extracting an automatable Runbook to mitigate similar future incidents.

**When to use it:** Immediately after resolving a critical incident or production outage (Phase 03 completed), to document institutional learning.

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
