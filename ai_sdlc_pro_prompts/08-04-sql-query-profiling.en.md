# 8.4 — SQL Execution Plan Audit and Profiling (DBA)

## Description

Specialized prompt to act as a Database Administrator (DBA). It analyzes the output of tools like `EXPLAIN ANALYZE` or ORM logs to detect bottlenecks, N+1 issues, massive sequential scans, and propose index optimizations or query rewrites.

**When to use it:** When an endpoint or service exhibits slowness (high latency) in production, or during the review of PRs that introduce complex database queries.

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
