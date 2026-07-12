# 8.5 — Database Schema Migration Review

## Description

Prompt to review a database schema migration BEFORE it runs: what the DDL actually does, what locks it acquires and for how long, whether it stays compatible with the currently deployed application code during a rolling deploy, whether it requires an expand-contract pattern, whether a tested rollback path exists, and whether there is any data-loss risk.

**When to use it:** before running a schema migration against staging or production — as part of the PR that introduces the migration file, or as a final gate before `migrate up` in the deployment pipeline. Don't confuse it with `08-04-sql-query-profiling`: that prompt analyzes the execution plan of a QUERY against a schema that already exists (`EXPLAIN ANALYZE`, N+1, missing indexes); this prompt evaluates the SAFETY of the schema CHANGE itself — table locking, compatibility with deployed code, the expand-contract pattern, and reversibility — before that change is executed.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis / validation |
| Expected risk | high — a poorly assessed schema migration that gets applied blindly can lock high-traffic tables, break the currently deployed code during a rolling deploy, or cause irreversible data loss; the prompt itself is read-only, but the cost of an incomplete diagnosis is paid in production |
| Required inputs | migration script or file (exact DDL, up and down if they exist), database engine and version, approximate size and traffic of the affected table(s), relevant fragment of the currently deployed code that reads or writes those columns/tables, deployment strategy (rolling / blue-green / maintenance window allowed) |
| Allowed tools | reading the provided migration script, current schema, and code — no access to a real database, no executing the migration or any DDL/DML against any environment |
| Permitted autonomy | A0 — Analyze (risk diagnosis); A1 — Propose (corrected migration version, expand-contract plan, rollback script, as a proposal); never A2/A3 — this prompt never executes or applies the migration under any circumstance |
| Stop criteria | stop and escalate to explicit human approval if the migration acquires a full table lock on a high-traffic table without a maintenance-window plan; stop if compatibility with the currently deployed code cannot be confirmed; never treat an irreversible data-loss operation as acceptable just because the requester says it's fine — flag it explicitly regardless |
| Expected output | see `## Expected output` |
| Minimum evidence | every flagged risk must cite the exact DDL statement responsible (ADD COLUMN, DROP COLUMN, ALTER TYPE, CREATE INDEX, etc.) and, when applicable, the fragment of currently deployed code that would become incompatible |
| Recommended next prompt | `11-09-runbook-rollback` to document and prepare the rollback procedure in case the migration needs to be reverted after being applied |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a Database Reliability Engineer / Senior DBA. Review the proposed schema migration and determine whether it is safe to apply, identifying locking behavior, incompatibilities with deployed code, data-loss risk, and the need for an expand-contract pattern, BEFORE it runs against any shared environment.

Inputs:
- db_engine_and_version: [PostgreSQL 15 / MySQL 8 / SQL Server / etc.]
- migration: [PASTE THE FULL MIGRATION DDL — UP AND DOWN IF THEY EXIST]
- affected_table_volume: [APPROXIMATE ROW COUNT, READ/WRITE TRAFFIC PER SECOND IN PRODUCTION]
- relevant_deployed_code: [CODE/ORM FRAGMENTS THAT READ OR WRITE THE AFFECTED COLUMNS/TABLES]
- deployment_strategy: [ROLLING / BLUE-GREEN / MAINTENANCE WINDOW ALLOWED]

Steps:

1. IDENTIFY WHAT THE MIGRATION ACTUALLY DOES
   Break the DDL down into atomic operations: ADD COLUMN, DROP COLUMN, RENAME COLUMN, ALTER COLUMN TYPE,
   ADD/DROP CONSTRAINT (NOT NULL, FK, UNIQUE, CHECK), CREATE/DROP INDEX, RENAME TABLE, etc.
   For each operation, state whether it is additive (safe by nature) or destructive/blocking (needs
   further analysis).

2. ASSESS LOCKING BEHAVIOR FOR THE STATED ENGINE
   For each operation: does it acquire a table-level or row-level lock? Is it an exclusive lock that
   blocks reads and writes, or does it allow concurrency (e.g. `CREATE INDEX CONCURRENTLY` in PostgreSQL,
   `ALGORITHM=INPLACE, LOCK=NONE` in MySQL)? Estimate how long that lock would be held given the declared
   row volume — do not assume a development-sized table.

3. VERIFY BACKWARD COMPATIBILITY WITH THE CURRENTLY DEPLOYED CODE
   Based on `relevant_deployed_code`, determine whether the code still running DURING the rolling deploy
   (before the new version is 100% rolled out) would keep working against the resulting schema. Typical
   breakage patterns: DROP of a column the old code still reads or writes, RENAME without a compatibility
   view/alias, a type change the old code cannot deserialize, a new NOT NULL column without a default
   that the old code doesn't populate on insert.

4. DETERMINE WHETHER AN EXPAND-CONTRACT PATTERN IS REQUIRED
   If step 3 finds an incompatibility, propose the expand-contract sequence as separate migrations:
   (a) expand — add the new column/table without touching the old one; (b) deploy code that writes to
   both; (c) backfill historical data; (d) deploy code that reads only from the new one; (e) contract —
   drop the old column/table in a LATER migration, only once no deployed code references it anymore.
   State which step of that sequence the migration under review corresponds to.

5. ASSESS DATA-LOSS RISK
   Explicitly flag any irreversible operation: DROP COLUMN, DROP TABLE, TRUNCATE, a type change that
   truncates or loses precision, a constraint downgrade that discards existing rows. State whether a
   verified backup or snapshot exists before execution. Do not accept "the data doesn't matter" at face
   value without it being documented as an explicit decision by the requester.

6. VERIFY THE ROLLBACK PATH
   Check whether a `down`/reverse script exists for this specific migration and whether it is symmetric
   and safe to run (e.g. a rollback that recreates a dropped column cannot recover the data that was
   already lost). If no rollback is defined or the rollback is incomplete, flag it as blocking.

7. VERIFY IDEMPOTENCY AND RE-RUN SAFETY
   Determine what happens if the migration runs twice (e.g. due to a pipeline retry) or fails halfway
   through: does it leave the schema in an inconsistent intermediate state? Does the DDL use
   `IF NOT EXISTS`/`IF EXISTS` or fail loudly on a safe re-run?

8. ESTIMATE EXECUTION TIME AND CLASSIFY AS ONLINE OR MAINTENANCE-WINDOW
   Project the application time against the real production volume declared (not against a development
   database). Classify the migration as safe to run online or as requiring a maintenance window, and
   justify it with the evidence from steps 2 and 8.

Constraints:
- never approve a migration that acquires a long, exclusive table-level lock on a high-traffic table
  without an explicit maintenance-window plan or an equivalent online alternative,
- never assume backward compatibility with deployed code without having reviewed the actual code
  fragment provided; if no relevant code was supplied, say so explicitly and mark compatibility as
  unverified instead of assuming it,
- flag every irreversible data-loss operation explicitly and prominently, even if the requester states
  it is acceptable — that acceptance must be recorded as a human decision, not silently absorbed into
  the approval,
- this prompt reviews and recommends; it never executes the migration, the proposed corrective DDL, or
  any command against a real database,
- if the production volume or traffic pattern of the affected table is unknown, say so explicitly and do
  not assume a small or low-traffic table scenario to qualify the migration as safe.

Deliver:
1. MIGRATION SUMMARY — what it does, statement by statement.
2. LOCKING RISK — lock type, estimated duration, affected tables/rows.
3. COMPATIBILITY WITH DEPLOYED CODE — compatible / incompatible and why, citing the code.
4. RECOMMENDED STRATEGY — direct application or a detailed expand-contract sequence.
5. DATA-LOSS RISK — irreversible operations flagged explicitly.
6. ROLLBACK PATH — existing/verified, incomplete, or absent.
7. VERDICT — safe for online execution / requires a maintenance window / blocked pending fixes, with the list of changes required before approval.
```

---

## Use with standard formula

```text
Use the database schema migration review prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- db_engine_and_version: [ENGINE AND VERSION]
- migration: [FILE OR DDL]
- environment: [STAGING / PROD]
- affected_table_volume: [ROWS AND TRAFFIC]
- documents to review: relevant deployed code, prior migrations, deployment runbook
- specific output objective: migration safety verdict + recommended strategy
- depth level: high
```

---

## Expected output

| Migration | Change type | Lock risk | Compatible with current code | Strategy (direct/expand-contract) | Rollback verified |
|---|---|---|---|---|---|
| `0042_add_status_not_null_orders.sql` | `ADD COLUMN status VARCHAR(20) NOT NULL` with no default on `orders` (18M rows, ~400 writes/s) | High — on most engines, `ADD COLUMN NOT NULL` without a default rewrites the entire table and holds an exclusive lock for the whole operation; at this volume it can take several minutes | No — the currently deployed code inserts rows into `orders` without sending `status`, so it would immediately fail against the new NOT NULL constraint | Expand-contract: (1) add a nullable column with a DEFAULT, (2) deploy code that writes `status` explicitly, (3) backfill historical rows, (4) later migration adds NOT NULL only once 100% of writes already send the value | No — the migration ships no `down` script; required before approval |
