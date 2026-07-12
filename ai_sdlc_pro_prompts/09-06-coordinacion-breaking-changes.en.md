# 9.6 — Cross-Team Breaking Change Coordination

## Description

Prompt to coordinate the outbound communication of an already-decided breaking change with the teams, services, and external consumers that depend on the affected contract: identifies who is impacted, drafts the message (what's changing, why, timeline, migration path), picks the channel and escalation path per audience, and tracks each consumer's readiness confirmation before the change ships. It does not design the technical change or the versioning strategy — it coordinates the outward communication of it.

**When to use it:** when a change breaks (or may break) a contract that other teams, services, or external consumers depend on, and the outbound communication needs coordinating before deployment — not just the technical design of the change. This prompt is distinct from `06-03-coordinacion-programa-multiagente`: that one coordinates a fleet of AI agents working in parallel INSIDE the same development program; this one coordinates OUTWARD COMMUNICATION to teams and consumers who are not part of that program and may not use AI agents at all. It is also distinct from — and comes after — `04-05-versionado-deprecacion-api`: that one designs the contract's versioning strategy and deprecation calendar (what counts as breaking, compatibility windows, date milestones); this one executes the actual notification to each affected party and tracks their readiness once that plan already exists.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | operation/coordination — drafts the communication and tracks consumer readiness; it does not execute the breaking change itself nor the versioning strategy behind it |
| Expected risk | medium-high — if consumers aren't properly notified or given enough migration time, the breaking change causes real outages for them once it ships; preventing exactly that is this prompt's purpose |
| Required inputs | an existing versioning/deprecation plan (from `04-05-versionado-deprecacion-api` or an equivalent document), the known list of teams/services/consumers that depend on the contract, the target cutover or release date, the communication channels available per audience |
| Allowed tools | reading consumer documentation, API/schema/event contracts, prior changelogs, support tickets, and existing communication channels; drafting notices, a notice-period calendar, and a readiness-tracking checklist — it does not send real messages, does not modify any consumer-facing system, and does not execute the cutover |
| Permitted autonomy | A1 — Propose (drafts the communication, the notice calendar, and the readiness checklist; actually sending the communication, escalating directly to a consumer, and deciding to proceed with the cutover require human or team-owner approval) |
| Stop criteria | stop and escalate if the full list of affected consumers can't be confirmed — declare it incomplete rather than treating it as closed; stop if no minimum notice period per audience has been defined; never recommend proceeding with the cutover if a high-impact consumer hasn't explicitly confirmed readiness |
| Expected output | see `## Expected output` |
| Minimum evidence | every consumer/team listed with impact, channel used, deadline, and confirmation status citing the concrete source (message sent, response received, ticket, channel ack); explicit note when the consumer list is incomplete or unverifiable |
| Recommended next prompt | `09-04-promotion-checklist` once external readiness is confirmed, to run the actual deployment checklist |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Coordinate the communication of this breaking change with every affected team, service, and external consumer, and track their readiness until you can confirm they're prepared ahead of the cutover date.

Required inputs:
- change and reference versioning/deprecation plan: [REFERENCE TO 04-05 OR ANOTHER DOCUMENT]
- affected contract: [API / SCHEMA / EVENT / FILE FORMAT / OTHER]
- nature of the breaking change: [WHAT EXACTLY CHANGES]
- target cutover or release date: [DATE]
- known consumers so far: [LIST, OR "UNKNOWN / PARTIAL"]
- available communication channels: [INTERNAL SLACK / PUBLIC CHANGELOG / EMAIL / ACCOUNT MANAGER / STATUS PAGE / OTHER]

Steps:
1. Identify every team, service, or external consumer that depends on the contract being broken, using verifiable sources (API usage logs, subscriber records, integration documentation, prior support tickets, commercial contracts). Don't assume the initial list provided is complete: explicitly flag what part of the consumer base you can't verify with the sources available.
2. Classify each identified team/consumer by impact severity (critical / high / medium / low, based on how central the broken contract is to their operation) and by estimated migration difficulty (trivial / moderate / complex), distinguishing internal from external consumers and, among external ones, commercial-contract customers from informal integrations.
3. Draft the base communication: exactly what's changing, why the change is being made, the full timeline (notice date, coexistence window if any, cutover date), concrete migration steps with before/after examples where applicable, and who to contact with questions. Avoid vague date language ("soon," "in the coming weeks") — use exact dates.
4. Choose the right channel and escalation path per audience: an internal Slack channel or an issue comment may be enough for an internal team; a large external consumer or one with a commercial contract needs direct outreach (account manager, dedicated email) in addition to any general notice (public changelog, status page) — don't rely on a single channel for high-impact audiences.
5. Define the minimum notice period appropriate to each audience, not one generic deadline: internal teams with direct code access and visibility into the migration usually need less lead time than external consumers who depend on their own release cycles. If a specific consumer's stated migration capacity is known, that's the floor, not an optional reference.
6. Design a concrete mechanism to track readiness confirmation per consumer (checklist with individual status, ack form, required ticket reply, etc.) — "we sent the email" is not evidence a consumer is ready; you need an explicit confirmation from them or verifiable technical evidence that they already migrated.
7. Define what happens for each consumer who hasn't confirmed readiness by the deadline: hard cutover anyway, a targeted extension, or a per-consumer exception (e.g., keeping the old contract active for just that customer for a limited time) — make the decision and its cost explicit, not implicit.
8. Prepare a pause/rollback communication template to use if the cutover has to be postponed after being announced, so that communication doesn't have to be improvised under pressure if a last-minute blocker appears.

Constraints:
- never assume silence means acknowledgment — an unread or unanswered notification is not evidence the consumer is ready,
- never set a deadline shorter than the audience's own stated migration capacity, when that information is available — negotiating a shorter window requires that audience's explicit agreement, not a unilateral decision,
- this prompt drafts the communication and tracks readiness; it does not execute the breaking change, deploy the change, or modify any consumer-facing system,
- if you can't verify the full list of affected consumers, say so explicitly in the deliverable instead of presenting a partial list as complete,
- don't mark a consumer "ready" by inference (e.g., "they've probably seen it by now") — only by their explicit confirmation or verifiable technical evidence of migration.

Deliver:
- list of identified teams/services/consumers, with impact, migration difficulty, and the source backing each data point, including an explicit note on what part of the base couldn't be verified,
- drafted communication (what's changing, why, timeline, migration steps, contact for questions), adapted per audience where the content differs substantially,
- assigned channel and escalation path per audience,
- notice deadline per audience, justifying why that window is sufficient,
- readiness-tracking mechanism and per-consumer status table (see `## Expected output`),
- handling plan for consumers not ready by the deadline (cutover / extension / exception),
- a ready-to-use pause/rollback communication template in case the cutover is postponed.
```

---

## Use with standard formula

```text
Use the breaking change coordination prompt and adapt it to:
- repository: [NAME OR URL]
- reference change or versioning plan: [REFERENCE TO ISSUE/PR/04-05]
- affected contract: [API / SCHEMA / EVENT / OTHER]
- known consumers: [LIST, OR "PARTIAL/UNKNOWN"]
- target cutover date: [DATE]
- documents to review: versioning and deprecation plan, changelog, consumer integration documentation, prior support tickets
- specific output objective: per-audience drafted communication + readiness confirmation tracking table
- depth level: high
```

---

## Expected output

| Consumer/Team | Impact | Migration difficulty | Channel | Deadline | Confirmation status |
|---|---|---|---|---|---|
| Payments team (internal) | High — consumes the `/v1/orders` endpoint directly in the checkout flow | Moderate — needs to update the internal HTTP client | Slack #eng-payments + comment on issue #512 | 2026-07-25 | 🟢 Confirmed — ack in Slack on 2026-07-14, migration PR open |
| External customer ACME Corp (commercial contract) | Critical — nightly batch integration on the same endpoint | Complex — their release cycle is monthly | Account manager (direct outreach) + email to support@acme | 2026-08-15 | 🟡 Pending — email sent 2026-07-12, no response yet |
| Anonymous consumers via public API | Unknown — no per-consumer API key records exist for this legacy contract | Not estimable | Public changelog + status page banner | 2026-08-15 (same cutover as ACME, as a floor) | 🔴 Unverifiable — consumer base can't be identified with current sources; declared explicitly as an open risk |
| Reporting team (internal) | Low — uses a derived field that doesn't change directly | Trivial | Comment on issue #512 | 2026-07-20 | 🟢 Confirmed — no action needed on their end |
