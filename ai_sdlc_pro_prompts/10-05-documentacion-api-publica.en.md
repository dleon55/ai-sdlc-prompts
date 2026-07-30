# 10.5 — Public API documentation for external developers

## Description

Prompt to produce the public reference documentation for an already designed and implemented API: getting-started guide, endpoint reference with real examples, use-case guides, visible versioning, and usage limits — aimed at external developers integrating against the API, not the engineers building it. Distinct from `04-06-diseno-contrato-api` (contract design, for engineers, explicitly states it does not produce documentation) and from `10-01-documentacion-tecnica` (internal technical documentation of the repository).

**When to use it:** after the API contract is already designed (`04-06`) and implemented, before exposing it to external consumers (partners, customers, third parties).

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | low-medium — incorrect or outdated public documentation generates support tickets and adoption friction for external integrators, but the prompt does not execute or modify the API itself |
| Required inputs | already implemented API contract (reference to `04-06` or real specification), target audience (external developers/partners/customers), real usage examples if available |
| Allowed tools | reading the contract and the existing API code — no execution |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if the behavior to be documented cannot be verified against the real implementation (the design contract has drifted from the code), stop and flag the discrepancy instead of documenting the theoretical design as if it were real behavior |
| Expected output | see `## Expected output` |
| Minimum evidence | every documented endpoint includes a verified request/response example, the authentication mechanism, and at least one error example with cause and recommended action |
| Recommended next prompt | `10-03-release-changelog` when the API has a new version to announce to consumers |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Produce the public reference documentation for the described API, aimed at external developers integrating against it, verified against the implementation's real behavior.

Inputs:
- already implemented API contract: [PASTE OR REFERENCE TO 04-06 OR ANOTHER SPECIFICATION]
- target audience: [EXTERNAL DEVELOPERS / PARTNERS / CUSTOMERS]
- real usage examples: [PASTE OR "generate representative examples"]

Activities:
1. GETTING STARTED
   Document how to authenticate and a complete first example request, end to end, that an external developer can execute with no additional context.

2. ENDPOINT REFERENCE
   For each endpoint: description in plain language (no internal team jargon), parameters with type and whether required, a real request/response example, and error codes with what they specifically mean for the consumer.

3. USE-CASE GUIDES
   Beyond the flat reference, document 2-3 complete typical flows step by step (e.g. "how to process a refund end to end using this API").

4. VISIBLE VERSIONING AND DEPRECATION
   Document the current versioning scheme and, if a contract change is underway, reference the `04-05-versionado-deprecacion-api` strategy in terms the external consumer understands (what needs to change and by when).

5. LIMITS AND QUOTAS
   Document rate limiting and any usage quota in terms the external consumer can plan around (e.g. "300 requests/minute per API key", not just the 429 error code).

6. RECENT CHANGELOG
   Summarize recent API changes relevant to external consumers.

Constraints:
- never document a behavior without verifying it against the real contract or code — if there's a discrepancy between what was designed and what was implemented, flag it explicitly instead of documenting the "ideal" version as if it were real behavior,
- always use language aimed at the external consumer (what they need to do, what they get back) — never internal team jargon or internal component names the consumer can't see,
- every documented error code must explain the probable cause and the recommended action for the consumer, not just the bare HTTP code,
- never publish real credentials, functional example tokens, or real production data in examples — always use clearly marked placeholders.

Output:
0. JSON metadata block (keys: status, endpoints_documented, examples_count, confidence_score [0.0 to 1.0]).
1. Getting started: authentication and first example request.
2. Endpoint reference with request/response and error examples.
3. Complete use-case guides.
4. Versioning and deprecation visible to the consumer.
5. Usage limits and quotas.
6. Recent changelog relevant to consumers.
```

---

## Usage with standard formula

```text
Use the public API documentation prompt and adapt it to:
- repository: [NAME OR URL]
- components: [SERVICE(S) EXPOSING THE API]
- documents to review: API contract (04-06), implemented API code, prior changelog
- specific output objective: public reference documentation ready to publish
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the documentation summary |
| Getting started (1) | Authentication and a first request executable end to end |
| Endpoint reference (2) | Each endpoint with verified request/response and error examples |
| Use-case guides (3) | Complete flows documented step by step |
| Versioning (4) | Current scheme and changes underway, in consumer-facing terms |
| Limits and quotas (5) | Rate limiting explained in plannable terms |
| Changelog (6) | Recent changes relevant to external consumers |

### Example (excerpt)

```json
{
  "status": "documented_with_discrepancy",
  "endpoints_documented": 9,
  "examples_count": 14,
  "confidence_score": 0.79
}
```

| Endpoint | Description | Error example |
|---|---|---|
| `POST /v1/orders` | Creates a new order for the authenticated user | `422 { "error": "sku_not_found", "message": "SKU 'ABC-123' does not exist in the catalog. Verify the identifier before retrying." }` |

| Section | Example content |
|---|---|
| Discrepancy detected | The design contract (`04-06`) states that `GET /v1/orders/{id}` only requires user authentication, but the real implementation also requires the `orders:read` scope — documented per the real verified behavior in code, and flagged as a deviation to fix in the design contract |
