# 4.6 — API contract design: endpoints, schemas, and interface semantics

## Description

Prompt to design a new API contract (or a new set of endpoints/operations) from scratch: conventions, catalog of operations with their request/response schemas, error matrix, per-operation authentication/authorization, and cross-cutting rules (pagination, idempotency, rate limiting). Produces the contract specification, not the code that implements it.

**When to use it:** after the solution design (`04-01`) when it exposes a new API, or as a standalone step when the requirement is explicitly to design an interface. Distinct from `04-05-versionado-deprecacion-api`, which evolves the contract of an **already existing** API: this prompt designs the contract from scratch, before any consumer exists.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | medium — a poorly designed contract (inconsistent, without a complete error-handling story, without a pagination or versioning strategy from the start) is expensive to fix once real consumers are integrated; the prompt does not implement or deploy anything by itself |
| Required inputs | related solution design (`04-01`) if it exists, related use cases (`04-03`) if they exist, intended consumers (internal/external), API style (REST/GraphQL/gRPC/other), existing project conventions if any |
| Allowed tools | reading design, use cases, and existing contracts — no execution or changes; produces a text contract specification, not code or gateway configuration |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if the API style (REST/GraphQL/gRPC) is not defined and cannot be inferred from existing project conventions, ask before assuming one; no operation may be left without its error matrix defined |
| Expected output | see `## Expected output` |
| Minimum evidence | every operation in the catalog declares method/path (or its equivalent in the chosen style), required authentication, request schema, success response schema, and error matrix; every deviation from an existing project convention is explicitly declared |
| Recommended next prompt | `04-05-versionado-deprecacion-api` when this contract needs to evolve later; `05-01-plan-implementacion` to plan the build; `07-02-pruebas-integracion` to design the contract's tests |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design the complete contract of the API or set of endpoints/operations described: conventions, catalog of operations with request/response schemas, error matrix, authentication/authorization, and cross-cutting rules.

Inputs:
- related solution design: [PASTE OR REFERENCE TO 04-01, OR "doesn't exist yet"]
- related use cases: [PASTE OR REFERENCE TO 04-03, OR "don't exist yet"]
- intended consumers: [INTERNAL / EXTERNAL / BOTH]
- API style: [REST / GraphQL / gRPC / OTHER]
- existing project conventions: [PASTE OR "none, this is the project's first API"]

Activities:
1. GENERAL CONVENTIONS
   Define or reuse the contract's conventions: naming (camelCase/snake_case), plural/singular in paths or types, date/time format and timezone, versioning strategy from day one (even if implicitly v1). If the project already has a prior API, reuse its conventions; any departure must be explicitly declared as a deviation, not introduced silently.

2. OPERATIONS CATALOG
   For each operation (REST endpoint, GraphQL query/mutation, gRPC RPC, depending on the chosen style): purpose, method+path or equivalent operation, request schema (parameters, query, body) with type and whether required or optional, success response schema, and error matrix (code + condition that triggers it + error payload). No operation may be left without its error matrix.

3. AUTHENTICATION AND AUTHORIZATION
   For each operation, define whether it is public, requires authentication, or requires a specific role/scope. If the required policy for a sensitive operation is unclear, mark it explicitly as "[PENDING DECISION: verify with security]" instead of assuming an access level.

4. CROSS-CUTTING RULES
   Define pagination (cursor vs. offset and why), supported filtering and sorting, rate limiting, idempotency on write operations (is an idempotency key required?), and a uniform date/time format.

5. CONSISTENCY WITH EXISTING CONVENTIONS
   If the project already exposes another API, compare the new contract against its conventions and flag any inconsistency detected — do not resolve it silently by adopting a different style without declaring it.

6. PENDING DECISIONS
   Explicitly flag with "[PENDING DECISION: reason]" any aspect the business or security team hasn't defined yet (e.g. exact rate-limiting thresholds, retention policy for exposed data).

Constraints:
- no operation may be left without its error behavior defined (code + payload) — an operation with no declared error path is reported as incomplete, never silently omitted,
- do not invent new conventions if the project already has an established style — reuse it; if you depart from it, explicitly declare it as a deviation to validate,
- do not assume by default the authentication/authorization level of a sensitive operation — if unclear, mark it as "[PENDING DECISION: verify with security]",
- this prompt produces a text contract specification (OpenAPI-style/descriptive schema); it does not generate code, configure gateway infrastructure, or deploy anything.

Output:
0. JSON metadata block (keys: status, endpoint_count, pending_decisions_count, confidence_score [0.0 to 1.0]).
1. General contract conventions.
2. Operations catalog: Operation | Method/path or equivalent | Auth required | Request schema | Response (success) | Error matrix
3. Cross-cutting rules: pagination, filtering/sorting, rate limiting, idempotency, date/time format.
4. Deviations from existing project conventions (if any).
5. Decisions pending validation with business or security.
```

---

## Usage with standard formula

```text
Use the API contract design prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [TARGET BRANCH]
- components: [SERVICE(S) THAT WILL EXPOSE THE API]
- documents to review: solution design (04-01), use cases (04-03), existing API conventions
- specific output objective: endpoint catalog with request/response schemas and error matrix
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the contract summary |
| Conventions (1) | Naming, date format, versioning strategy from the start |
| Operations catalog (2) | Each operation with its complete request/response and error schema |
| Cross-cutting rules (3) | Pagination, rate limiting, idempotency, sorting/filtering |
| Deviations (4) | Inconsistencies flagged against existing conventions, if any |
| Pending decisions (5) | Aspects not yet defined by business or security |

### Example (excerpt)

```json
{
  "status": "designed_with_pending_items",
  "endpoint_count": 6,
  "pending_decisions_count": 1,
  "confidence_score": 0.75
}
```

| Operation | Method/path | Auth required | Request | Response (success) | Errors |
|---|---|---|---|---|---|
| Create order | `POST /v1/orders` | Authenticated (end user) | `{ "items": [{ "sku": string, "qty": int }], "shippingAddressId": string }` | `201` `{ "orderId": string, "status": "pending", "total": number }` | `400` invalid data · `401` not authenticated · `409` repeated `idempotency-key` with a different payload · `422` nonexistent `sku` |
| Cancel order | `POST /v1/orders/{orderId}/cancel` | Authenticated + order owner or `support` role | (no body) | `200` `{ "orderId": string, "status": "cancelled" }` | `401` not authenticated · `403` not the owner and no `support` role · `404` order not found · `409` order already shipped, not cancellable |
