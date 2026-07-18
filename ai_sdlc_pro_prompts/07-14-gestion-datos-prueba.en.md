# 7.14 — QA test data management strategy

## Description

Prompt to design the cross-cutting test data strategy for shared QA/staging environments: generating representative synthetic datasets or masking a production snapshot, the volume needed for representativeness, the isolation mechanism between parallel runs, and the environment's refresh/reset policy. Distinct from the per-scenario test data already covered by `07-01`/`07-02`/etc. — this prompt designs the environment's complete data strategy, not an individual flow's.

**When to use it:** when setting up a new shared QA/staging environment, or when test failures appear due to inconsistent/contaminated data between runs or collisions between parallel executions.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | medium — a poorly designed production-data masking scheme can leak real sensitive data into a lower-security environment; a poorly designed reset strategy can corrupt the state of other teams sharing the environment |
| Required inputs | test environment(s) to cover, dataset origin (synthetic / masked production snapshot / mixed), data volume needed for representativeness, number of pipelines/agents running in parallel, applicable compliance policy for the data (PII, PCI, or other, if any) |
| Allowed tools | reading schemas, existing seed/fixture scripts, and data policies; the prompt designs the strategy and generates generation/masking scripts — execution against a real shared environment requires explicit approval, and never against production |
| Permitted autonomy | A1 — Propose (strategy and scripts); A2 — Execute controlled only in the indicated isolated test environment, never against production or a shared environment without explicit approval |
| Stop criteria | stop if asked to start from a production snapshot without an already-defined PII/sensitive-data masking policy — do not design the masking on your own without that policy; stop if the data volume needed for representative tests cannot be confirmed |
| Expected output | see `## Expected output` |
| Minimum evidence | every sensitive field identified in the dataset has an explicit masking strategy (never "left as-is" without justification); the isolation mechanism between parallel runs is described in concrete terms (namespacing, transactions, ephemeral containers) |
| Recommended next prompt | `07-01`/`07-02`/`07-03` for designing specific tests that consume this data; `13-08-gestion-secretos-credenciales` if the strategy requires production-access credentials for the initial snapshot |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design the test data management strategy for the indicated QA environment(s): generation or masking of the base dataset, isolation mechanism between parallel runs, and the environment's refresh/reset policy.

Inputs:
- environment(s) to cover: [QA / STAGING / BOTH]
- base dataset origin: [100% SYNTHETIC / MASKED PRODUCTION SNAPSHOT / MIXED]
- data volume needed: [e.g. N RECORDS PER MAIN ENTITY FOR REPRESENTATIVENESS]
- pipelines/agents running in parallel: [NUMBER OR "unknown"]
- applicable compliance policy for the data: [PII / PCI / NONE KNOWN / OTHER]
- database stack: [STACK]

Steps:
1. SENSITIVE FIELD CLASSIFICATION
   If the dataset starts from a production snapshot, identify every field that contains or could contain PII or other sensitive data per the provided compliance policy (names, emails, phone numbers, addresses, payment data, government IDs). If no compliance policy was provided and starting from production is requested, stop and request it before designing the masking.

2. MASKING OR SYNTHETIC GENERATION STRATEGY
   For each sensitive field, define the masking technique (deterministic substitution, hashing, format-preserving synthetic generation) so the data stops being identifiable while retaining the shape or statistical distribution needed for tests to remain representative (e.g. same relative date range, same postal code distribution).

3. VOLUME AND REPRESENTATIVENESS
   Define how many records per main entity are needed for performance/load tests and edge cases (pagination, sorting, aggregations) to be representative, and how to generate the specific edge cases (null values, length limits, special characters) that a real dataset does not necessarily cover.

4. ISOLATION BETWEEN PARALLEL RUNS
   If multiple pipelines or agents run tests against the same shared environment, design the isolation mechanism: per-run data namespacing (unique prefixes/suffixes), transactions rolled back at the end of each run, or ephemeral containers/databases per run. Explicitly flag the collision risk if none of these mechanisms is implemented.

5. REFRESH AND RESET POLICY
   Define when and how the base dataset is refreshed (cadence, manual or automatic trigger) and the procedure to reset to a known clean state between runs or at the end of the day, including what to do if the reset affects other teams sharing the environment.

6. INTEGRITY VALIDATION
   Define how to verify, before each run, that the dataset is in the expected state (not corrupted by a previous failed run) and what to do if the validation fails.

Constraints:
- never propose using real unmasked production data in a lower-security environment (QA/staging) — if the origin is a production snapshot, every sensitive field must have an explicit masking strategy before proposing the dataset's use,
- if no compliance policy was provided and the dataset starts from production, stop and request the policy instead of deciding on your own which fields to mask,
- do not execute the masking or the dataset load against a real shared environment without explicit approval, and never against production,
- every isolation mechanism between parallel runs must be described in concrete, implementable terms, never as "ensure no collision" without specifying how,
- if the data volume needed for representativeness cannot be confirmed, state it as pending instead of assuming an arbitrary number.

Output:
- dataset origin strategy (synthetic/masked/mixed), with justification
- table of sensitive fields and their masking technique, if applicable
- recommended data volume per entity and edge cases to generate
- isolation mechanism between parallel runs
- environment refresh/reset policy
- pre-run integrity validation procedure
```

---

## Use with standard formula

```text
Use the QA test data management prompt and adapt it to:
- repository/project: [NAME OR URL]
- environment(s): [QA / STAGING / BOTH]
- dataset origin: [SYNTHETIC / MASKED SNAPSHOT / MIXED]
- volume needed: [N RECORDS PER ENTITY]
- parallel runs: [NUMBER OR "unknown"]
- compliance policy: [PII / PCI / NONE KNOWN]
- documents to review: DB schemas, existing seed scripts, data policy
- specific output objective: complete test data strategy for the environment
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Dataset origin | Synthetic, masked, or mixed, with justification |
| Sensitive fields | Table of field → masking technique applied |
| Volume and edge cases | Records per entity and edge cases to generate |
| Parallel isolation | Concrete mechanism (namespacing, transactions, ephemeral containers) |
| Refresh/reset | Cadence, trigger, and reset procedure |
| Integrity validation | Pre-run check and action if it fails |

### Example (excerpt)

| Sensitive field | Masking technique |
|---|---|
| `email` | Deterministic substitution: hash of the original email mapped to `user_{hash}@test.example` — the same original email always produces the same masked value, preserving uniqueness for duplicate tests |
| `date_of_birth` | Year is kept, month/day randomized — preserves age distribution for segmentation tests without exposing the real date |
| `card_number` | Replaced with valid test numbers from the payment gateway's schema (never a real PAN, not even masked) |

**Isolation between parallel runs:** each CI pipeline prefixes the records it creates with a unique tag (`run_{build_id}_`) and runs its suite inside a transaction that is rolled back at the end — prevents two concurrent runs from seeing or modifying each other's records.
