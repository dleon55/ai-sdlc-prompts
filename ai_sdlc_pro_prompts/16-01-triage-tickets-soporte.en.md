# 16.1 — Support Ticket Triage and Classification

## Description

Prompt to triage and classify an incoming support ticket or batch of tickets: determines severity/priority with evidence, calculates the applicable SLA per the current policy, identifies whether the ticket is a duplicate or an already-known issue, and proposes the team/owner for first assignment. It does not diagnose the root cause or resolve the ticket, does not change its status, does not reassign it or notify the customer: it only classifies and routes with traceable evidence.

**When to use it:** when one or more new tickets arrive (support desk, help desk, customer incident channel) that need severity, SLA, and team assigned before anyone intervenes. Distinction from related prompts: this prompt (`16-01`) only classifies and routes, it never acts on the ticket; `16-02-diagnostico-respuesta-incidente-soporte` is the prompt that does intervene after triage — it diagnoses the cause and proposes or executes a response to the ticket already classified by this prompt. If the triage result indicates critical severity with signs of a broader production incident, also consider `11-04-incident-response` for incident coordination.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis/classification |
| Expected risk | medium — a miscalculated severity or SLA can delay attention to a critical ticket or overload the wrong team with false positives, but the triage does not apply any change to the system, it only classifies and routes; the risk only materializes if the proposed classification is used without human review to decide the actual response |
| Required inputs | text and metadata of the ticket or batch of tickets (title, description, reporter, timestamp, environment, attachments/logs if any), current SLA table or policy by severity, read access to ticket history or a knowledge base to detect duplicates/known issues, routing rules or support team structure |
| Allowed tools | reading and searching the ticket system, knowledge base, and prior incident history; the output is a classification and routing proposal in text/table form — it does not change the ticket's status, does not assign it, does not close it, and does not send communications to the customer or the team |
| Permitted autonomy | A0 — Analyze (reading the ticket, searching for duplicates/known issues); A1 — Propose (proposed severity, SLA, and team); never A2/A3 — this prompt does not assign the ticket, change its status, or execute any action on the ticket system |
| Stop criteria | stop and request more information if the ticket lacks enough data to determine severity (no description, no stated impact or environment) — never invent a plausible-looking severity; mark as "possible duplicate, unconfirmed" if the match with a prior ticket is unclear, instead of treating it as settled; if the ticket shows signs of a security incident or data leak, stop the routine triage and escalate immediately per the current security protocol instead of continuing to classify it as an ordinary ticket |
| Expected output | see `## Expected output` |
| Minimum evidence | every severity/priority cites the ticket field(s) or impact/urgency matrix criterion that supports it; every cited SLA references the SLA policy or table used; every duplicate/known match cites the matching ticket ID or knowledge base entry and the matching criterion (same error, same component, same user/environment, etc.) |
| Recommended next prompt | `16-02-diagnostico-respuesta-incidente-soporte` to diagnose the cause and respond to/resolve the already-classified ticket; `11-04-incident-response` if the triage reveals a production incident broader in scope than a single ticket |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a Support Analyst specialized in triage. Classify the given ticket or batch of tickets by severity/priority, determine the applicable SLA per the current policy, identify whether it is a duplicate or an already-known issue, and propose the team or owner for first assignment. Do not diagnose the root cause, do not resolve the ticket, do not change its status or actually assign it: your output is a proposed classification with evidence, for human review or the next prompt in the flow.

Inputs:
- ticket(s) to classify: [TEXT/EXPORT OF THE TICKET OR BATCH OF TICKETS — title, description, reporter, timestamp, environment, attachments/logs if any]
- current SLA policy: [SLA TABLE BY SEVERITY/PRIORITY — first-response and resolution times per level]
- source for detecting duplicates/known issues: [TICKET HISTORY, KNOWLEDGE BASE, KNOWN ISSUES LIST — or "not available" if applicable]
- routing rules/team structure: [MAP OF TEAMS BY COMPONENT/PRODUCT/AREA, OR CURRENT ASSIGNMENT CRITERIA]
- ticket origin channel: [EMAIL / SUPPORT PORTAL / CHAT / API / OTHER]

Steps:

1. INTAKE AND NORMALIZATION
   For each ticket, extract the relevant fields (title, description, affected component/product, environment, affected user/customer, report timestamp, referenced attachments or logs). If a critical field is missing, state this explicitly instead of assuming it.

2. SECURITY INDICATOR CHECK
   Before investing effort in standard classification, check whether the ticket shows signs of a security incident or data exposure (exposed credentials, reported unauthorized access, suspected data leak). If so, stop the routine triage of that ticket immediately and flag it for security escalation instead of continuing with the steps below.

3. SEVERITY/PRIORITY CLASSIFICATION
   Determine severity (e.g., critical/high/medium/low) and priority using an explicit impact x urgency matrix: impact (how many users/customers affected, whether there is data or revenue loss, total block vs. degradation) and urgency (whether a workaround exists, whether it worsens over time). Cite the specific ticket field or indicator supporting each assigned level — never assign severity without textual evidence from the ticket.

4. APPLICABLE SLA DETERMINATION
   Based on the assigned severity/priority, apply the current SLA policy to determine the target first-response and resolution time. If the SLA policy does not cover the case or was not provided, state this explicitly instead of inventing an SLA.

5. DUPLICATE OR KNOWN ISSUE DETECTION
   Search the provided ticket history or knowledge base for a prior ticket or known issue that matches (same error/message, same component, same environment or pattern). If you find a reasonable match, cite the matching ticket/entry ID and the matching criterion. If the match is partial or uncertain, mark it as "possible duplicate, unconfirmed" — never declare it a confirmed duplicate without clear evidence.

6. PROPOSED TEAM/OWNER FOR FIRST ASSIGNMENT
   Based on the affected component/product and the provided routing rules, propose the team or owner that should receive the ticket in the first instance. If the routing rules do not cover the identified component, flag it as "no routing rule defined" instead of assigning a default team without justification.

7. FLAGGING AMBIGUOUS OR INCOMPLETE CASES
   List separately the tickets lacking enough information to classify with confidence (severity, SLA, or team), and what specific information is missing to complete the triage.

8. EXECUTIVE SUMMARY AND CONSOLIDATED TABLE
   Summarize the classified batch: how many tickets per severity, how many duplicates/known issues detected, how many with insufficient information, and how many escalated due to security indicators.

Constraints:
- this prompt only classifies and routes; it never changes the ticket's status, does not actually assign it, does not close it, does not generate or send responses to the customer or the support team.
- never assign severity, SLA, or team without citing the concrete evidence (ticket field, SLA policy entry, or routing rule) that supports the decision.
- never declare a ticket a confirmed duplicate without a clear, cited match; when in doubt, use "possible duplicate, unconfirmed".
- if critical information is missing to classify a ticket (severity, environment, impact), state this explicitly and do not fabricate a plausible-looking classification to fill the table.
- if the ticket shows signs of a security incident or data leak, stop the routine triage and escalate immediately per the current security protocol; do not treat it as an ordinary support ticket.
```

---

## Use with standard formula

```text
Use the support ticket triage and classification prompt and adapt it to:
- repository/product: [NAME OR URL]
- ticket(s) to classify: [EXPORT OR PASTED TICKET/BATCH]
- current SLA policy: [SLA TABLE BY SEVERITY]
- duplicates/known issues source: [TICKET HISTORY / KNOWLEDGE BASE OR "not available"]
- routing rules: [MAP OF TEAMS BY COMPONENT]
- origin channel: [EMAIL / PORTAL / CHAT / API]
- specific output objective: severity, SLA, duplicate/known status, and proposed team per ticket
- depth level: medium
```

---

## Expected output

| Ticket ID | Severity/Priority | Applicable SLA | Duplicate/Known? | Proposed team | Evidence/Justification |
|---|---|---|---|---|---|
| TCK-4821 | High (impact: ~200 users unable to log in; urgency: no reported workaround) | First response 1h, resolution 8h ("High" SLA policy level) | Possible duplicate of TCK-4790 (same "auth-service" component, same "token expired prematurely" error message) — unconfirmed, requires human review | Platform/Auth team (rule: auth-service component → Platform) | Ticket description indicates total login block since 09:14; no workaround mentioned; partial error-message match with TCK-4790 |

> Note: the full table should include one row per ticket in the batch, plus a separate section for tickets with insufficient information (listing the missing data) and for tickets escalated due to security indicators (with the escalation reason, without detailing the vulnerability over an insecure channel).

### Executive summary

- **Tickets classified:** [N] — [X critical, Y high, Z medium, W low].
- **Duplicates/known issues detected:** [N] — [list of matching IDs, with confirmed/unconfirmed confidence level].
- **Tickets with insufficient information:** [N] — [missing data per ticket].
- **Tickets escalated for security indicators:** [N] — [escalation reason, without exposing sensitive details].
- **Recommended next action:** send the classified tickets to `16-02-diagnostico-respuesta-incidente-soporte` for diagnosis and response, prioritizing by severity and SLA.
</content>
