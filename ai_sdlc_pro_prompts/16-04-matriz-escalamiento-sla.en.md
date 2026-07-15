# 16.4 — Severity-Based Escalation and SLA Matrix

## Description

Prompt to define the support policy matrix for a product/team: severity levels (P0-P3 or the team's equivalent scheme), the first-response and resolution SLA per level, and an explicit escalation chain — who to escalate to and after how long without meeting the SLA. It does not triage individual tickets or draft a response to a live incident: it produces the policy document that other day-to-day operation prompts use as their reference.

**When to use it:** when first establishing a product/team's support policy, or when reviewing it periodically (change in team capacity, new contractual SLAs, recent incidents that exposed gaps in the escalation chain). Distinction from related prompts: `16-01-triage-tickets-soporte` classifies real incoming tickets against the severity levels already defined here — this prompt designs those levels, it does not apply them. `16-02-diagnostico-respuesta-incidente-soporte` diagnoses and responds to a specific incident already in progress, using this matrix's SLA as the clock it must operate against — this prompt does not diagnose or respond to incidents, it only sets the rules of the game before they occur.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | policy/process design |
| Expected risk | medium — a miscalibrated SLA matrix creates unmeetable expectations for clients/users and commits the support team to deadlines it cannot sustain with its real capacity, but the prompt itself only drafts a policy proposal, it never publishes it or applies it to a real ticket |
| Required inputs | catalog of known incident/ticket types (if available), the support team's real capacity (headcount, coverage hours, existence of on-call), existing contractual SLAs with clients (if any), severity definitions currently in use (even if informal), available escalation channels |
| Allowed tools | reading existing support documentation, client contracts/SLAs, the team's org chart and on-call schemes; the output is a text policy document — it does not configure alerting/paging tools or modify the ticketing system |
| Permitted autonomy | A0 — Analyze (survey existing SLAs and capacity); A1 — Propose (the severity matrix, SLAs, and escalation chain); never A2/A3 — the matrix requires explicit human approval before being adopted as official support policy |
| Stop criteria | stop and escalate to a human if no real support team capacity data is available (headcount, coverage hours) — never fabricate an SLA matrix without verifying the team can sustain it; flag the proposal as low-confidence if contractual SLAs with clients exist but could not be confirmed |
| Expected output | see `## Expected output` |
| Minimum evidence | each severity level includes a concrete example of the incident type that triggers it, its corresponding first-response and resolution SLA, and the exact point in the escalation chain (who, and after how long without meeting the SLA) is explicit per level |
| Recommended next prompt | `16-01-triage-tickets-soporte` to apply this matrix by classifying incoming tickets in day-to-day operation |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a Support/Reliability Lead specialized in service policy design. Define a severity-based escalation and SLA matrix for the given product/team: clear severity levels, the first-response and resolution SLA per level, and the escalation chain with timing and owners for when the SLA is not met.

Inputs:
- support product/team: [PRODUCT OR TEAM NAME]
- catalog of known incident/ticket types: [LIST, or "none — infer from ticket/incident history"]
- support team's real capacity: [HEADCOUNT, COVERAGE HOURS, IS THERE ON-CALL OUTSIDE BUSINESS HOURS?]
- existing contractual SLAs with clients: [DESCRIPTION, or "none"]
- severity definitions currently in use: [DESCRIPTION, or "none — this is the first formal definition"]
- available escalation channels: [SLACK / PAGERDUTY / PHONE / EMAIL / OTHER]
- desired number of severity levels: [ex: 4 LEVELS (P0-P3) / OTHER SCHEME]

Steps:

1. CURRENT CONTEXT SURVEY
   Gather the team's real capacity (headcount, coverage hours, existence of on-call rotation), any existing contractual SLAs with clients, and any severity definitions currently used, even if informal.
   - if the team's real capacity is not available, state this explicitly and stop at this point: a sustainable SLA cannot be calibrated without that data.

2. SEVERITY LEVEL DEFINITION
   Define the requested number of levels (default to P0-P3 if no other scheme is specified), with an objective, verifiable criterion for each one (ex: scope of affected users, existence of a workaround, data loss, revenue/reputation impact). Avoid subjective criteria like "very serious" without an observable anchor.

3. FIRST-RESPONSE AND RESOLUTION SLA PER LEVEL
   For each severity level, define the first-response SLA (time until a human confirms the ticket/incident was received and is being worked) and the resolution SLA (time until the incident is considered closed or mitigated). Both must be concrete times (ex: "15 minutes", "4 business hours"), never vague ranges like "as soon as possible".

4. ESCALATION CHAIN PER LEVEL
   For each level, define who the ticket/incident escalates to if the first-response or resolution SLA is about to expire or already expired, on which channel, and who is next in the chain (ex: on-call engineer → tech lead → engineering manager → VP). Specify the exact time trigger for each escalation hop (ex: "if there is no first response within 10 minutes of a P0, auto-escalate to the on-call tech lead").

5. COVERAGE HOURS AND EXCEPTIONS
   Clarify whether the defined SLAs apply 24/7 or only during business hours, and what happens with high-severity incidents outside that window (on-call activation, a different off-hours SLA, etc.). Do not assume 24/7 coverage if the capacity surveyed in step 1 does not support it.

6. RECLASSIFICATION CRITERIA
   Define when and how the severity of an already-open ticket/incident can be reclassified (upward or downward), and who has the authority to do so, to avoid severity staying frozen at an incorrect initial classification.

7. FEASIBILITY VALIDATION AGAINST REAL CAPACITY
   Cross-check each proposed SLA against the real capacity surveyed in step 1 (headcount, coverage hours). If an SLA is not sustainable with current capacity, flag it explicitly as a risk instead of proposing it as if it were viable.

8. EXECUTIVE SUMMARY AND NEXT STEPS
   Summarize the full matrix, the feasibility risks identified in step 7, and what a human must approve before adopting this matrix as official support policy.

Constraints:
- never define a resolution or first-response SLA without cross-checking it against the team's real capacity (headcount, coverage hours); if that capacity was not provided, stop and request the data instead of assuming 24/7 coverage or an unconfirmed team size.
- every severity level must have an objective criterion and a concrete example of the incident type that triggers it; avoid subjective definitions without an observable anchor.
- every hop in the escalation chain must have an exact time trigger (how long without meeting the SLA) and a named owner by role, never "escalate to whoever is appropriate".
- this prompt designs and proposes a policy; it never publishes it as official, never notifies clients of the new SLA, and never configures alerting/paging/on-call tools — all of that requires explicit human approval and execution outside this prompt.
- if contractual SLAs already exist with clients, the proposed matrix cannot propose less favorable terms than those contracts without explicitly flagging it as a conflict for a human to resolve.
```

---

## Use with standard formula

```text
Use the severity-based escalation and SLA matrix prompt and adapt it to:
- support product/team: [PRODUCT OR TEAM NAME]
- catalog of known incident/ticket types: [LIST OR "infer from history"]
- support team's real capacity: [HEADCOUNT, HOURS, ON-CALL YES/NO]
- existing contractual SLAs with clients: [DESCRIPTION OR "none"]
- severity definitions currently in use: [DESCRIPTION OR "none"]
- available escalation channels: [SLACK / PAGERDUTY / PHONE / EMAIL]
- desired number of severity levels: [ex: 4 LEVELS (P0-P3)]
- documents to review: client contracts, support org chart, ticket/incident history
- specific output objective: severity matrix, response/resolution SLA, and escalation chain ready for human review
- depth level: high
```

---

## Expected output

| Level | Definition / example | First-response SLA | Resolution SLA | Escalation chain |
|---|---|---|---|---|
| P0 — Critical | Service down for all users or data loss in progress; no workaround (ex: full production outage) | 10 minutes, 24/7 | 4 hours | On-call engineer auto-notified on open → if no first response within 10 min, escalates to on-call tech lead → if not resolved within 2 hours, escalates to engineering manager → at 4 hours, escalates to VP of Product |
| P1 — High | Key functionality degraded for a large subset of users; partial workaround exists | 30 minutes, extended hours (7am-11pm) | 8 business hours | On-call support engineer → if no first response within 30 min, escalates to tech lead → if not resolved within 6 hours, escalates to engineering manager |
| P2 — Medium | Secondary functionality affected or bug with a clear workaround for a limited number of users | 4 business hours | 3 business days | On-call support engineer → if no first response within 4 hours, escalates to tech lead |
| P3 — Low | Cosmetic defect, enhancement request, or question with no functional impact | 1 business day | 10 business days | On-call support engineer; no automatic escalation — reviewed in the weekly support backlog meeting |

> Note: the full table should include one row per defined severity level, explicitly flagging any SLA that step 7 of the prompt marked as unsustainable with current team capacity, and distinguishing 24/7 coverage from business/extended hours at each level.

### Executive summary

- **Adopted severity scheme:** [ex: P0-P3, 4 levels] — main classification criterion: [SCOPE OF AFFECTED USERS / EXISTENCE OF A WORKAROUND / DATA LOSS / OTHER].
- **Level with the highest risk of non-compliance:** [LEVEL] — reason: [ex: a 10-minute 24/7 SLA requires on-call coverage the team does not yet have].
- **Conflicts with existing contractual SLAs:** [NONE / DESCRIPTION OF THE CONFLICT TO RESOLVE].
- **Approval required before adopting as official policy:** [ROLE/PERSON] must validate capacity feasibility and authorize publishing this matrix.
