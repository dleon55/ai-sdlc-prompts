# 4.7 — Detailed data model design: entities, relationships, and schema

## Description

Prompt to design the detailed data schema of a feature or project: entities with their fields and types, relationships with cardinality and delete policy, normalization level, indexes justified by query pattern, and evolution strategy. Produces the schema design, not the executable migration script.

**When to use it:** during the design phase (after `04-01`, in parallel with or after `04-03`), when the change or project requires a new data model or a significant extension of the existing one — before writing the actual migration. Distinct from `00-D-02-stack-arquitectura-inicial`, which only sketches the data model at a high level (up to 10 entities, no field- or index-level detail), and from `08-05-revision-migracion-esquema-bd`, which audits the **safety** of an already-written migration (locking, compatibility, reversibility): this prompt designs the detailed schema itself.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | high — the data schema is one of the most expensive decisions to reverse once real data exists in production (destructive migrations, downtime, loss of integrity); the prompt does not execute any migration or modify any database |
| Required inputs | domain entities and relationships (or the solution design `04-01` / use cases `04-03` to infer them from), database engine (relational/document/other), expected volume and access pattern (reads vs. writes, frequent queries), existing data model if extending one |
| Allowed tools | reading the current schema and related documentation — no migrations executed and no database modified; produces the design, not the migration script |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if the database engine or the expected access pattern is unknown, stop and request it before proposing a schema — normalization and indexing strategy depend directly on that information |
| Expected output | see `## Expected output` |
| Minimum evidence | each entity declares its fields with type and nullability; each relationship declares cardinality and delete policy; each proposed index is justified by a cited query pattern, not by intuition |
| Recommended next prompt | `08-05-revision-migracion-esquema-bd` once the migration script is written from this design |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design the detailed data schema for the described domain or change: entities, fields, relationships, normalization, indexes, and integrity, with justification for each decision.

Inputs:
- domain entities and relationships: [DESCRIPTION, OR REFERENCE TO 04-01/04-03]
- database engine: [RELATIONAL (Postgres/MySQL/...) / DOCUMENT (MongoDB/...) / OTHER]
- expected volume and access pattern: [READS VS. WRITES, FREQUENT QUERIES, APPROXIMATE VOLUME]
- existing data model (if extending one): [PASTE OR "new model, no prior schema"]

Activities:
1. ENTITIES
   For each domain entity, define its fields: name, type, nullability, default value, and constraints (unique, check). Don't omit basic audit fields (creation/update) unless the domain explicitly justifies their absence.

2. RELATIONSHIPS
   For each relationship between entities, define cardinality (1:1, 1:N, N:M), foreign key, and delete policy (cascade/restrict/set null) — justify the delete-policy choice by citing business impact, never leave it at the engine's default with no conscious decision.

3. NORMALIZATION
   Assess the appropriate normalization level (up to 3NF by default) and justify any deliberate denormalization by citing the access pattern that motivates it (e.g. a computed column to avoid an expensive JOIN in a high-frequency query).

4. INDEXES
   Propose indexes based on the declared query patterns (filters, joins, frequent sorts). Never propose an index without being able to cite the specific query that justifies it.

5. INTEGRITY AND CONSTRAINTS
   Define database-level constraints (not null, unique, check, foreign key) that must exist independently of any validation in the application layer.

6. EVOLUTION STRATEGY
   Flag how this schema is expected to grow (fields likely to be added, risk of breaking compatibility), and define the soft-delete vs. hard-delete strategy and auditing (created_at/updated_at, version, actor) if applicable to the domain.

Constraints:
- do not propose an index without being able to cite the specific query pattern that justifies it — an index with no justification is technical debt, not optimization,
- every relationship must explicitly declare its delete policy (cascade/restrict/set null) — never leave it implicit or "the engine's default" without a conscious, justified decision,
- if the database engine or the expected access pattern is unknown, stop and request it — do not assume a default engine or read/write pattern,
- this prompt delivers the schema design; it does not generate the executable migration script or run it against any environment — that belongs to implementation and the subsequent review with `08-05`.

Output:
0. JSON metadata block (keys: status, entity_count, relationship_count, index_count, confidence_score [0.0 to 1.0]).
1. Entity catalog: Entity | Field | Type | Nullable | Default | Constraints
2. Relationships: Source entity | Target entity | Cardinality | Foreign key | Delete policy
3. Proposed indexes: Index | Fields | Justification (query pattern)
4. Deliberate denormalizations (if any) and their justification.
5. Evolution strategy, soft/hard delete, and auditing.
```

---

## Usage with standard formula

```text
Use the data model design prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [TARGET BRANCH]
- components: [SERVICE(S) / MODULE(S) THAT WILL USE THIS SCHEMA]
- documents to review: solution design (04-01), use cases (04-03), current schema if extending one
- specific output objective: detailed schema with entities, relationships, indexes, and delete policy
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the schema summary |
| Entity catalog (1) | All fields of each entity, with type and nullability |
| Relationships (2) | Cardinality and delete policy of each relationship |
| Proposed indexes (3) | Each index with the query that justifies it |
| Denormalizations (4) | Exceptions to normalization, with their access-pattern justification |
| Evolution strategy (5) | Expected growth, soft/hard delete, and auditing |

### Example (excerpt)

```json
{
  "status": "designed",
  "entity_count": 4,
  "relationship_count": 3,
  "index_count": 5,
  "confidence_score": 0.8
}
```

| Entity | Field | Type | Nullable | Default | Constraints |
|---|---|---|---|---|---|
| `orders` | `status` | `varchar(20)` | no | `'pending'` | `check (status in ('pending','paid','shipped','cancelled'))` |
| `orders` | `customer_id` | `uuid` | no | — | `foreign key -> customers(id)` |

| Index | Fields | Justification |
|---|---|---|
| `idx_orders_customer_status` | `(customer_id, status)` | Frequent customer-panel query: "list this customer's active orders", run on every dashboard load |
