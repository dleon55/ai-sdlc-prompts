# 8.4 — SQL Execution Plan Audit and Profiling (DBA)

## Description

Specialized prompt to act as a Database Administrator (DBA). It analyzes the output of tools like `EXPLAIN ANALYZE` or ORM logs to detect bottlenecks, N+1 issues, massive sequential scans, and propose index optimizations or query rewrites.

**When to use it:** When an endpoint or service exhibits slowness (high latency) in production, or during the review of PRs that introduce complex database queries.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — does not execute or apply database changes; the real risk is that the proposed DDL or query gets applied to production without further validation |
| Required inputs | `EXPLAIN ANALYZE` output or ORM log, DDL or models of the relevant schema, database engine used |
| Allowed tools | reading the provided execution plan/log and schema — no access to the real database or query execution |
| Permitted autonomy | A1 — Propose (delivers diagnosis, optimized query and index DDL as a proposal; does not execute them) |
| Stop criteria | if the schema or execution plan lacks real table volumetry or up-to-date statistics, present the diagnosis as preliminary and do not guarantee the estimated impact |
| Expected output | see `## Expected output` |
| Minimum evidence | the diagnosis must cite the specific execution plan node (or the exact N+1 query) responsible for the bottleneck |
| Recommended next prompt | `08-01-revision-estatica` to validate the optimized query and index DDL before applying them |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a Senior Database Administrator (DBA). Analyze the provided SQL execution plan or ORM logs to identify performance issues and propose optimization solutions.

Inputs:
- db_engine: [PostgreSQL / MySQL / SQL Server / MongoDB / etc.]
- log_or_explain: [PASTE THE EXPLAIN ANALYZE OR ORM LOG HERE]
- relevant_schema: [PASTE THE DDL OF THE INVOLVED TABLES OR ORM MODELS]

Analysis Activities:
1. BOTTLENECK DETECTION: Identify the most expensive nodes in the execution plan (e.g., Seq Scan, expensive Hash Join, in-memory Sort).
2. INDEX ANALYSIS: Evaluate if the correct indexes are being used or if a composite/covering index is missing.
3. ORM ANTI-PATTERNS: If it is an ORM log (Hibernate, Prisma, Eloquent, etc.), look for the N+1 queries problem or unnecessary fetching of heavy columns.
4. RESOURCE OPTIMIZATION: Check if filtering or aggregation operations could be performed more efficiently.

Constraints:
- never run profiling or `EXPLAIN ANALYZE` directly against production; if the provided `log_or_explain` doesn't clearly state its source environment, ask for explicit confirmation before assuming it's safe to reproduce or treating its results as valid,
- every index or query-rewrite recommendation must be grounded in concrete evidence from the provided execution plan or log (specific node, cost, rows scanned) — don't propose optimizations based on generic "best practice" assumptions without that evidence,
- if a recommendation implies a schema change (new column, data type, normalization), explicitly flag the migration risk: table locking, estimated application time, compatibility with existing data,
- the proposed index DDL is a deliverable for human review: never execute it or imply it has already been applied.

Mandatory Output:
1. DIAGNOSIS: Clear summary of why the query is slow (e.g., "Missing index on column X, causing a sequential scan of 1M rows").
2. OPTIMIZED QUERY: The rewritten SQL query (or adjusted ORM code) applying best practices.
3. INDEX DDL: Exact SQL code to create the recommended indexes (e.g., `CREATE INDEX CONCURRENTLY...`).
4. ESTIMATED IMPACT: Expected reduction in computational cost or execution time.
```

---

## Use with standard formula

```text
Use the SQL profiling audit prompt and adapt it to:
- db_engine: [ENGINE]
- log_or_explain: [TEXT]
- relevant_schema: [DDL]
- specific output objective: identify bottlenecks and generate indexes.
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Diagnosis | Technical explanation of the bottleneck (Seq Scan, N+1, etc.) |
| Optimized Query | Refactored SQL query or ORM code |
| Index DDL | Exact scripts to apply the missing indexes |
| Impact | Expected benefit in latency or CPU/I/O consumption |

### Concrete example

| Section | Content |
|---|---|
| Diagnosis | The `Seq Scan on orders (cost=0.00..48291.00 rows=1200000 width=64)` node shows the query uses no index on `orders.customer_id`, scanning 1.2M rows on every execution |
| Optimized query | `SELECT id, total FROM orders WHERE customer_id = $1 AND status = 'paid' ORDER BY created_at DESC LIMIT 20;` |
| Index DDL | `CREATE INDEX CONCURRENTLY idx_orders_customer_status ON orders (customer_id, status, created_at DESC);` |
| Estimated impact | Reduces the plan cost from ~48000 to ~120 (planner estimate), moving from a sequential scan to a composite index — needs validation with `EXPLAIN ANALYZE` against real data before confirming the improvement |
