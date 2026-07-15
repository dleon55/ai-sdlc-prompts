# 16.3 — Knowledge base article from a resolved ticket

## Description

Prompt to turn an already-resolved support ticket (symptom, root cause, applied fix) into a reusable knowledge base article: searchable title, symptoms, cause, solution steps, and the cases where that solution does NOT apply. It does not publish or modify the production KB system: it drafts text content for human review and later publication.

**When to use it:** after a ticket is resolved and the pattern (symptom + cause + fix) is likely to recur, so the next support agent doesn't have to re-diagnose the same case from scratch. Distinction from related prompts: `16-02-diagnostico-respuesta-incidente-soporte` diagnoses an **ongoing** incident and proposes a response to the user; this prompt acts **afterward**, on a ticket already closed with a confirmed root cause, and its output is not a reply to the user but a reusable article for future similar tickets. If the source ticket has no confirmed root cause (just a symptom that went away), this prompt must stop instead of fabricating a cause.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | low — the prompt only drafts text for human review; it does not publish or modify the production KB system. The real risk (an incorrect fix published and applied by another support agent) stays contained by the mandatory human review step before publishing |
| Required inputs | resolved ticket with reported symptom, confirmed root cause (own or coming from the `16-02` diagnosis), applied and validated solution steps, affected system/product/version, target audience for the article |
| Allowed tools | reading the resolved ticket and related existing KB articles (to avoid duplicates and keep style conventions); no access to production systems, no publishing or modifying the KB system — the output is a draft text document |
| Permitted autonomy | A1 — Propose (draft the KB article); never A2/A3 — publishing the article in the production KB system requires explicit human review and approval outside this prompt |
| Stop criteria | stop and escalate if the ticket has no confirmed root cause (only a resolved symptom without diagnosis) — never invent a plausible-looking cause; if the applied solution was not validated as effective (ticket closed without user or QA confirmation), mark the whole article as a low-confidence draft instead of presenting it as ready to publish |
| Expected output | see `## Expected output` |
| Minimum evidence | the article cites the source ticket (id/link), explicitly distinguishes confirmed root cause from hypothetical cause, and always includes the "when this solution does NOT apply" section |
| Recommended next prompt | `16-02-diagnostico-respuesta-incidente-soporte` as the typical source for this article when the resolved ticket comes from a prior diagnosis; the article produced here requires human review and publication in the KB system before it can be considered active |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a Technical Writer specialized in technical support knowledge bases. From an already-resolved ticket, draft a reusable knowledge base article with a searchable title, symptoms, root cause, validated solution steps, and the cases where that solution does NOT apply.

Inputs:
- resolved ticket (id or link): [TICKET ID OR LINK]
- symptom originally reported by the user: [SYMPTOM DESCRIPTION, EXACT ERROR MESSAGES]
- confirmed root cause: [CONFIRMED ROOT CAUSE — or "comes from the 16-02 diagnosis" if applicable]
- applied and validated solution steps: [EXACT STEPS THAT RESOLVED THE TICKET, IN ORDER]
- affected system/product/version: [SYSTEM, VERSION, ENVIRONMENT]
- article audience: [TIER 1 SUPPORT AGENTS / END USERS / BOTH]
- target KB system and style conventions if any: [KB SYSTEM NAME, STYLE GUIDE — or "not available"]
- related existing KB articles (to avoid duplicates): [LINKS OR "none identified"]

Steps:

1. VALIDATE THAT A CONFIRMED ROOT CAUSE EXISTS
   Review the ticket before drafting anything. If the ticket only records that the symptom went away (ex: "the user restarted and it worked") without a cause diagnosis, state this explicitly and stop: request the confirmed root cause or the `16-02` diagnosis before continuing. Do not fabricate a plausible-looking cause to fill in the article.

2. CHECK WHETHER A SIMILAR ARTICLE ALREADY EXISTS
   Review the related existing KB articles provided as input. If the pattern is already documented, state this and propose updating the existing article instead of creating a duplicate.

3. SEARCHABLE TITLE
   Write a title in the language the target audience would use when searching for the problem (symptom or error message as a user would describe it), not internal engineering jargon.

4. SYMPTOMS
   List the observable symptoms concretely: exact error messages, visible behavior, conditions under which it occurs (version, environment, configuration). Avoid vague descriptions like "doesn't work".

5. ROOT CAUSE
   Explain the root cause at the level of detail appropriate for the target audience. Explicitly distinguish whether it is a confirmed cause (validated in the ticket or in the source diagnosis) or whether some element remains unconfirmed, and mark it as such.

6. SOLUTION STEPS
   Write the solution steps numbered and reproducible, in the order they were applied and worked. Include prerequisites or required permissions if applicable.

7. WHEN THIS SOLUTION DOES NOT APPLY
   Identify similar symptoms that could have a different cause (known false positives, conditions that rule out this diagnosis) and what to do instead (ex: escalate, re-diagnose with `16-02`). This section is mandatory: an article without applicability limits leads to applying the wrong fix.

8. METADATA AND CLASSIFICATION
   Propose product, version, category, and tags to aid future searchability, and reference the source ticket (id/link) as traceable evidence.

9. REVIEW NOTE AND DRAFT STATUS
   Close the article with an explicit note that it is a draft requiring human review before publishing in the KB system, and state the article's confidence level (high if the cause and solution are fully validated; low if some element remains unconfirmed).

Constraints:
- never invent a root cause if the ticket does not explicitly record one and it does not come from a prior diagnosis (`16-02`); if missing, stop and flag it as blocking instead of filling in a hypothesis presented as fact.
- never publish or modify the production KB system, or any other system; the only output of this prompt is a draft text document for human review.
- generalize the case only as far as the ticket's evidence supports; do not extrapolate to scenarios, versions, or configurations that were not verified without explicitly marking them as unverified.
- always include the "when this solution does NOT apply" section — never deliver an article without defining its applicability limits.
- if the applied solution was not validated as effective (ticket closed without user or QA confirmation), mark the entire article as a low-confidence draft instead of presenting it as ready to publish.
```

---

## Use with standard formula

```text
Use the knowledge base article from resolved ticket prompt and adapt it to:
- repository/support system: [NAME OR URL]
- resolved ticket: [ID OR LINK]
- reported symptom: [DESCRIPTION]
- confirmed root cause: [ROOT CAUSE OR "16-02 diagnosis"]
- applied solution steps: [STEPS]
- system/product/version: [SYSTEM, VERSION]
- audience: [TIER 1 SUPPORT / END USERS / BOTH]
- target KB system: [NAME OR "not available"]
- documents to review: source ticket, related existing KB articles
- specific output objective: draft KB article ready for human review
- depth level: medium
```

---

## Expected output

```markdown
# Title: "'Could not sync calendar' error when connecting a Google Workspace account"

**Product/version:** Mobile app, v4.2+ · **Environment:** iOS and Android · **Category:** Integrations > Google Workspace
**Source ticket:** SUP-4821 (link) · **Article confidence:** high (cause and solution validated by QA)

## Symptoms
- The user sees "Could not sync calendar" when linking a Google Workspace account (does not occur with personal Gmail accounts).
- The calendar event does not appear in the app even though it exists in Google Calendar.
- Only occurs in organizations where the Workspace admin has restricted the `calendar.readonly` scope for third-party apps.

## Root cause (confirmed)
The app requests the `calendar.events` scope by default, but the organization's Google Workspace policy only authorizes `calendar.readonly` for third-party apps not verified by the admin. Google silently rejects the sync request and the app shows a generic error instead of indicating the missing scope. Confirmed in ticket SUP-4821 by reviewing the Google API logs (`insufficientPermissions` error) together with the customer's Workspace administrator.

## Solution steps
1. Confirm with the user that the affected account is a Google Workspace account (not a personal Gmail account) — see Symptoms.
2. Ask the user to request their Workspace administrator enable the `calendar.events` scope for the app in the Google admin console (Security > App access control).
3. Once the scope is enabled, ask the user to unlink and re-link the account from Settings > Integrations > Google Calendar.
4. Verify that a test event syncs correctly within 2 minutes.

## When this solution does NOT apply
- If the affected account is a personal Gmail account (not Workspace): this error should not occur for this reason; escalate to general diagnosis with `16-02`.
- If the user already has the `calendar.events` scope enabled and the error persists: the cause is different (possible OAuth token expiration); do not apply these steps, escalate as a new incident.
- If the error occurs intermittently (sometimes syncs, sometimes doesn't): this suggests a Google API rate-limiting issue, not a permissions issue; this solution does not apply.

## Metadata
- **Tags:** google-workspace, calendar, oauth-scope, sync
- **Audience:** tier 1 support agents
- **Status:** draft — pending human review before publishing in the KB system
```

### Executive summary

- **Article generated:** searchable title, symptoms, root cause (confirmed or flagged as hypothesis), numbered solution steps, and the mandatory "when it does not apply" section.
- **Source ticket:** [ID/LINK] — traceability kept for future audit.
- **Draft confidence level:** [HIGH / LOW] depending on whether the cause and solution were fully validated in the ticket.
- **Status:** draft — requires explicit human review and publication in the KB system; this prompt does not publish or modify the production KB system.
