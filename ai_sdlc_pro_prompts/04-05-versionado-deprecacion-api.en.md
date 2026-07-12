# 4.5 — API Versioning and Deprecation

## Description

Prompt to design the versioning and deprecation strategy for an API when its contract must change: version numbering scheme, backward-compatibility window, deprecation timeline with concrete milestones, and migration guidance for consumers. Produces the contract evolution plan, not the code that implements it.

**When to use it:** when a change to an API breaks (or may break) the existing contract with its consumers — renaming/removing fields, changing types, modifying authentication, changing status codes or the semantics of an endpoint — and you need to decide how to introduce it without leaving clients unaware. It is more specific and tactical than `04-04-adr-decisiones-arquitectura`: an ADR documents and justifies an architectural decision in general, while this prompt exclusively resolves the evolution of an API's contract (numbering, windows, communication). Also use it as a specialized follow-on to `04-01-diseno-solucion` when the resulting design exposes or modifies a public API surface, or one consumed by other systems.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | low-medium — the prompt only produces a strategy document, but a poorly calibrated deprecation plan (insufficient window, weak communication) can break real consumer integrations if followed as-is without review |
| Required inputs | affected endpoint(s) or operation, nature of the proposed change, known consumers of the API (internal/external, if known), the project's existing versioning policy (if any), current SLA or support agreements with consumers |
| Allowed tools | reading the existing API specification (OpenAPI/Swagger, GraphQL SDL, contracts), previous changelogs and consumer documentation; only drafts the strategy document — does not modify API code or configuration |
| Permitted autonomy | A1 — Propose |
| Stop criteria | stop and escalate if it cannot be determined whether the change is breaking or not; stop if the consumer base is entirely unknown and the prompt cannot explicitly flag that gap; never propose removing a version without a defined notice period |
| Expected output | see `## Expected output` |
| Minimum evidence | every change explicitly classified as breaking or non-breaking with justification; date milestones (announcement, dual-support window, end of support) defined even if estimated; explicit note when consumers or their usage volume are unknown |
| Recommended next prompt | `09-06-coordinacion-breaking-changes` to notify and coordinate with the affected teams and consumers once the versioning strategy is defined |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design the versioning and deprecation strategy for the described API contract change(s), so that existing consumers have a clear migration path and a reasonable amount of time to adopt it.

Required inputs:
- affected endpoint(s) or operation: [PATH / OPERATION]
- proposed change: [DESCRIPTION OF THE CHANGE]
- known consumers: [INTERNAL / EXTERNAL / UNKNOWN]
- current versioning scheme of the project (if any): [URI PATH / HEADER / QUERY PARAM / NONE]
- current SLA or support agreements: [IF ANY]

Steps:

1. CLASSIFY THE CHANGE
   Determine whether the change is breaking or non-breaking relative to the current contract.
   Breaking examples: removing/renaming a field, changing a data type, tightening
   validation, changing the authentication mechanism, changing an expected status code,
   changing the order or semantics of an operation.
   Non-breaking examples: adding an optional field, adding a new endpoint, relaxing
   a validation, adding a new value to an enum already treated as open.
   When in reasonable doubt, treat the change as breaking.

2. CHOOSE AND JUSTIFY THE VERSIONING SCHEME
   Evaluate the options in the context of this specific API and justify the one chosen:
   - URI path versioning (/v1/, /v2/)
   - header versioning (Accept-Version, X-API-Version)
   - query param versioning
   - content negotiation (versioned media type)
   If the project already has an established scheme, use it unless there is explicit
   justification to change it.

3. DEFINE THE DEPRECATION TIMELINE
   With concrete milestones (date or "days since announcement"):
   - announcement date of the new version / deprecation of the old one
   - start of the dual-support window (both versions active)
   - sunset date (end of support for the old version)
   - minimum duration of the dual-support window, justified by the type of consumer
     (a public third-party API needs more time than an internal service owned by the same team)

4. DEFINE BACKWARD COMPATIBILITY AND ADAPTER FEASIBILITY
   - what "backward compatible" means for this specific change
   - whether it is feasible to avoid the breaking change entirely with an adapter/shim
     (field mapping, default value, translation layer) instead of a new major version
   - if the adapter introduces technical debt, state it and with what retirement date

5. DRAFT THE DEPRECATION NOTICE AND CHANGELOG ENTRY
   - deprecation notice text (for changelog, API README, or HTTP headers
     `Deprecation` / `Sunset` per RFC 8594 where applicable)
   - migration guidance: what the consumer must change, with a before/after
     request/response example

6. IDENTIFY CONSUMERS AND COMMUNICATION CHANNELS
   - list of known consumers and their criticality
   - if there is no way to identify them (public API with no client registry), state
     that explicitly and do not assume low impact
   - notice channels: email, public changelog, documentation banner, HTTP header,
     in-app notification, issue/PR to known consumer repos

7. DEFINE MONITORING OF OLD-VERSION USAGE
   - metric or log to instrument to measure traffic to the deprecated version
   - residual traffic threshold considered "safe to remove"
   - what to do if there is still significant traffic when the sunset date arrives
     (extend the window vs. remove anyway, and who decides)

8. SUMMARIZE RISKS AND FINAL DECISION
   - residual risk of following the proposed timeline
   - conditions under which this plan should be re-evaluated

Constraints:
- never remove or mark a version as retired without a minimum notice period
  appropriate to this API's consumer base (longer for external or unknown
  consumers than for internal services owned by the same team)
- never propose silently breaking a contract: every breaking change requires
  a major version bump or an explicit breaking-change signal
- if consumers or their usage volume are unknown, say so explicitly in the
  output instead of assuming low impact or low criticality
- this prompt designs the strategy; it does not modify API code, gateway/infrastructure
  configuration, or execute deployments

Deliver:
- classification of the change (breaking / non-breaking) with justification
- chosen versioning scheme and justification
- deprecation timeline with milestones (see `## Expected output`)
- backward-compatibility definition and adapter/shim feasibility assessment
- deprecation notice text and migration guidance with before/after examples
- list of identified consumers (or explicit statement that they are unknown) and communication channels
- monitoring plan for old-version usage during the sunset window
```

---

## Use with standard formula

```text
Use the API versioning and deprecation prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [CURRENT BRANCH]
- environment: [DEV / QA / PROD]
- components: [API / AFFECTED ENDPOINT(S)]
- documents to review: OpenAPI/GraphQL specification, previous changelog, consumer documentation, related ADRs
- specific output objective: versioning strategy and deprecation timeline with migration guidance
- depth level: high
```

---

## Expected output

| Change | Type (breaking/non-breaking) | New version | Announcement date | End of dual support (sunset) | Consumer action |
|---|---|---|---|---|---|
| Rename `user_id` to `userId` in `GET /v1/orders` and switch authentication from API key to OAuth2 | breaking | v2 (`/v2/orders`, header `Accept-Version: 2`) | 2026-07-15 | 2026-10-15 (90-day dual support) | Migrate clients to `/v2/orders`, update parsing of the `userId` field, and replace the API key with an OAuth2 client_credentials flow before 2026-10-15; see migration guide in the changelog |

### Example deprecation notice (changelog / HTTP header)

```http
Deprecation: version="1", date="2026-07-15"
Sunset: date="2026-10-15"
Link: <https://docs.example.com/migration-v2>; rel="deprecation"
```

### Before / after (migration example)

```json
// v1 (deprecated, removal 2026-10-15)
{
  "user_id": "abc123",
  "order_total": 49.90
}
```

```json
// v2 (current)
{
  "userId": "abc123",
  "orderTotal": 49.90
}
```
