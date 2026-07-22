# 16.2 — Support Incident Diagnosis and First Response

## Description

Prompt to guide the systematic diagnosis of a support ticket that has already been triaged: reproduce the problem, isolate the probable cause, review known incidents and knowledge base (KB) articles, and classify the finding. From that diagnosis, it drafts the first response to the user or client with next steps and a realistic time expectation. It does not apply any fix in production or modify code or configuration: it is diagnosis and communication.

**When to use it:** immediately after a ticket has been classified and prioritized by `16-01-triage-tickets-soporte`. Distinction from related prompts: `16-01-triage-tickets-soporte` decides **which** ticket to work on first and at what severity, without investigating the cause; this prompt investigates **why** the problem occurs and communicates status to the user, without touching production. If the diagnosis confirms a real bug that requires a code change, this prompt stops and escalates to `03-01-incidentes-github` or `11-01-troubleshooting` for the technical execution investigation; if the ticket turns out to be a production incident with significant impact, it escalates to `11-04-incident-response` instead.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis/communication |
| Expected risk | medium — a rushed diagnosis or a poorly calibrated client response (an unrealistic time promise, an inappropriate tone, a miscommunicated cause) can damage the client relationship or compromise an SLA expectation, even though the prompt itself does not apply any change to the system |
| Required inputs | ticket already triaged with priority and severity assigned (output of `16-01`), reproduction steps reported by the user, affected environment, available evidence (logs, screenshots, error messages), read access to known incidents and the knowledge base, SLA or response-time commitment agreed with the client |
| Allowed tools | reading logs, monitoring dashboards, incident history and knowledge base; drafting the user response — applying code changes, configuration changes, deployments, rollbacks, or any modification to the system or to production is explicitly forbidden |
| Permitted autonomy | A0 — Analyze (diagnosis: reproduce, isolate probable cause, review KB); A1 — Propose (draft the first user response); never A2/A3 — this prompt does not execute or publish changes to the system |
| Stop criteria | stop and escalate to an execution/engineering prompt (`03-01-incidentes-github` or `11-01-troubleshooting`) if the diagnosis confirms a code bug that requires a change; stop and escalate to `11-04-incident-response` if it is a production incident with significant impact; if the problem is not reproducible with the available evidence, do not promise a cause or a resolution date — flag the diagnosis as low-confidence and ask the user for more evidence |
| Expected output | see `## Expected output` |
| Minimum evidence | every cause hypothesis cites the real evidence backing it (a log, a reproduction step, a referenced KB article or prior incident); the first response to the user never promises a resolution date that is not backed by the agreed SLA or by an estimate explicitly labeled as such |
| Recommended next prompt | `16-01-triage-tickets-soporte` (previous step, if the ticket has not been triaged yet); `03-01-incidentes-github` or `11-01-troubleshooting` if the diagnosis confirms a real bug requiring a code change; `11-04-incident-response` if it escalates to a production incident with significant impact |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as an L2 Technical Support Specialist responsible for diagnosing already-triaged incidents. Reproduce the reported problem, isolate the most probable cause with real evidence, review known incidents and the knowledge base, and draft the first response to the user with next steps and a realistic time expectation. Do not apply any change to the system.

Inputs:
- triaged ticket: [TICKET ID, PRIORITY AND SEVERITY ASSIGNED IN 16-01]
- symptom reported by the user: [DESCRIPTION AS WRITTEN BY THE USER/CLIENT]
- reported reproduction steps: [STEPS, OR "not provided" IF APPLICABLE]
- affected environment: [PRODUCTION / STAGING / APP VERSION / BROWSER / DEVICE]
- available evidence: [LOGS, SCREENSHOTS, ERROR MESSAGES, TRANSACTION ID — or "none" if applicable]
- knowledge sources to review: [KB, HISTORY OF SIMILAR INCIDENTS, RECENT CHANGELOG]
- SLA or response time agreed with the client: [ex: FIRST RESPONSE WITHIN 4H / RESOLUTION WITHIN 2 BUSINESS DAYS]

Steps:

1. CONFIRM TRIAGED TICKET CONTEXT
   Verify the ticket already has priority and severity assigned. If it does not, state this explicitly and recommend running triage first (`16-01-triage-tickets-soporte`) before continuing.

2. REPRODUCTION ATTEMPT
   Using the reported reproduction steps and the stated environment, attempt to reproduce the problem (or precisely describe what would be needed to reproduce it if you cannot execute it directly). Document the outcome: reproduced / not reproduced / partially reproduced, with the evidence obtained on each attempt.

3. REVIEW KNOWN ISSUES AND THE KNOWLEDGE BASE (KB)
   Search the incident history and the KB for an identical or similar case already documented. If one exists, cite the exact reference (incident ID or KB article) and its known solution or workaround.

4. ISOLATE THE PROBABLE CAUSE
   From the reproduction, the available logs, and the known issues reviewed, formulate one or more probable-cause hypotheses, each backed by concrete evidence (do not speculate without evidence). Order the hypotheses from most to least likely.

5. CLASSIFY THE DIAGNOSIS
   Classify the finding into one of these categories: (a) confirmed code bug — requires a code change, (b) configuration or data issue — can be resolved without a code change, (c) user error — only needs an explanation, (d) duplicate of an already-known incident with an existing workaround, (e) not reproducible — more evidence is needed.

6. ESCALATION DECISION
   If the classification is (a) confirmed code bug, explicitly state that this prompt stops here and that the diagnosis must be handed off to an execution/engineering prompt (`03-01-incidentes-github` or `11-01-troubleshooting`) to implement the fix. If the environment is PRODUCTION and the impact is significant (affects multiple users or a critical function), state that it should escalate to `11-04-incident-response` instead of continuing as a standard support ticket.

7. FIRST RESPONSE TO THE USER/CLIENT
   Draft the first response addressed to the user or client, in a professional and empathetic tone, including: (1) confirmation that the problem was understood and is being investigated, (2) a summary of the finding in non-technical language appropriate for the recipient, (3) the concrete next step (a workaround if one exists, or the planned escalation), (4) a time expectation aligned with the agreed SLA or explicitly labeled as an estimate if there is no formal SLA.

8. INTERNAL EXECUTIVE SUMMARY
   Summarize for the internal team: diagnosis classification, key evidence, escalation decision (if applicable), and the time commitment communicated to the user.

Constraints:
- never apply, suggest automatically applying, or execute a code change, configuration change, deployment, or rollback in any environment — this prompt diagnoses and communicates, it does not repair.
- never promise the user a confirmed root cause or a resolution date that is not backed by real evidence or by the agreed SLA; if the diagnosis is low-confidence, say so explicitly in the response to the user instead of sounding more certain than the evidence allows.
- if the problem could not be reproduced with the available evidence, do not assume a cause: ask the user for the specific additional evidence that is missing (logs, exact steps, screenshots) in the first response.
- if the classification indicates a confirmed code bug, stop this prompt's flow at the escalation step — do not continue proposing or describing the code fix as if it were part of this prompt.
- always distinguish in the output what is real evidence (log, KB, reproduction) from what is an unconfirmed hypothesis.
- do not describe a fix as "in progress" or "being worked on" if the escalation step has not yet been confirmed with a real, assigned issue/PR — use "was escalated to engineering" instead of "is being fixed" unless there is evidence the work has already started.
```

---

## Use with standard formula

```text
Use the support incident diagnosis and first response prompt and adapt it to:
- repository/product: [NAME OR URL]
- triaged ticket: [ID, PRIORITY, SEVERITY — output of 16-01]
- reported symptom: [USER DESCRIPTION]
- affected environment: [PRODUCTION / STAGING / VERSION]
- available evidence: [LOGS / SCREENSHOTS / "none"]
- agreed SLA: [ex: first response within 4h]
- documents to review: knowledge base (KB), history of similar incidents, recent changelog
- specific output objective: classified diagnosis with evidence and a draft first response to the user
- depth level: medium
```

---

## Expected output

| Step | Result | Cited evidence | Classification |
|---|---|---|---|
| Reproduction | Reproduced in staging following the user's steps, 500 error when confirming checkout with an expired coupon | application log `req_id=8841af`, screenshot attached by the user | reproduced |
| Probable cause | Coupon validation does not check the expiration date before applying the discount at the confirmation step | application log + comparison with a recent commit in the coupon module (changelog) | confirmed code bug |
| Known issues/KB | No identical prior incident exists; a KB article on invalid coupons exists but does not cover this case | KB search (no exact match) | no known workaround applies |
| Escalation decision | Diagnosis stops here; requires a code change in the coupon validation module | classification (a) | escalate to `03-01-incidentes-github` / `11-01-troubleshooting` |

> Note: the full table should include one row per relevant diagnosis step (reproduction, KB, probable cause, classification, escalation decision), always citing the real evidence used. If any step lacks sufficient evidence, its row must explicitly say "no evidence — low-confidence diagnosis" instead of inventing a cause.

### Draft first response to the user

> Hi [USER NAME], thanks for reporting this. We confirmed the error when applying an expired coupon during checkout and have identified the cause in our coupon validation system, so we've escalated the case to our engineering team for a fix. As a next step, we recommend completing the purchase without the coupon while we resolve the issue, or contacting us to apply the discount manually. We expect to have an update before [DEADLINE PER AGREED SLA OR EXPLICIT ESTIMATE]. We'll let you know as soon as it's resolved.

### Executive summary

- **Diagnosis:** [CLASSIFICATION] — [ONE-LINE SUMMARY OF THE PROBABLE CAUSE].
- **Key evidence:** [LOGS / REPRODUCTION / KB CITED].
- **Escalation decision:** [NONE / ESCALATES TO 03-01 OR 11-01 / ESCALATES TO 11-04-INCIDENT-RESPONSE].
- **Commitment communicated to the user:** [NEXT STEP AND DEADLINE], aligned with the agreed SLA: [YES / NO — IF NO, LABELED AS AN ESTIMATE].
- **Residual risks:** [non-reproducible diagnosis, insufficient evidence, SLA at risk of being missed].
