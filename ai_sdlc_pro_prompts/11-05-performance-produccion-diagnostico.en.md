# 11.5 — Production Performance: Diagnosis and Optimization

## Description

Prompt to diagnose, analyze, and remediate performance problems in production: identifies bottlenecks in the application, database, and infrastructure using real observability signals, profiles the system under real load, and delivers an optimization plan with quantifiable changes.

**When to use:** when production performance degradation is detected (latency alerts, user complaints, accelerated SLO burn rate), after adding observability (`10-04`) and visualizing real-time metrics, or as a periodic performance health review.

---

## Required prior context

> Include the block from `00-framework.md` before this prompt.
> Attach metrics, traces, or logs from the degradation period (result from `10-04` or Grafana/Datadog/CloudWatch export).
> If a result from `07-06` (performance test design) or `07-11` (implementation) exists, attach it as context for expected thresholds.

---

## Full prompt

```text
Objective:
Diagnose, analyze, and remediate production performance problems using real observability
signals (metrics, traces, logs), identify the root causes of degradation, and deliver a
prioritized optimization plan with quantifiable impact.

Steps:

1. PROBLEM CHARACTERIZATION
   Describe the observed performance problem:
   - exact symptom: which metric or signal indicates degradation? (P99 latency, error rate, dropped throughput)
   - magnitude: how much worse compared to baseline? (e.g., P95 rose from 200ms to 1.2s)
   - problem onset: when did it start? does it coincide with a deployment, traffic increase, config change?
   - scope: does it affect all users or a subset? all endpoints or only some?
   - frequency: continuous, periodic, or random?
   - impacted SLO: which error budget is being consumed and at what rate?

2. TRACE AND LOG ANALYSIS
   With traces from the degradation period:
   
   a) Identify the slowest operation (heaviest span in the trace):
      - is it a DB query? external service call? CPU-bound process?
      - does it appear in all affected requests or only some?
      - does it correlate with any input parameter? (user type, payload size, region)
   
   b) Log analysis for the period:
      - are there errors, warnings, or timeouts during the degradation that did not exist before?
      - are there logs of "connection pool exhausted", "query timeout", "GC pause", "retry"?
      - does any external process start failing or slowing down in the same period?
   
   c) Temporal correlation:
      - does degradation coincide with a traffic spike, batch job, DB migration?
      - does it coincide with rate limiting from an external service?
      - is there a memory leak? (memory gradually rising without dropping)

3. LAYER-BY-LAYER DIAGNOSIS
   Analyze each stack layer to locate the bottleneck:
   
   a) Application layer:
      - are there N+1 queries? (N DB queries per item in a listing)
      - synchronous processing that should be asynchronous?
      - expensive loops or O(n²) or worse algorithmic complexity?
      - unnecessary or expensive serializations/deserializations?
      - frequent garbage collection or long pauses? (Java, .NET, Go)
      - DB connections not reused (no connection pool)?
   
   b) Database layer:
      - queries without index or with full table scan (EXPLAIN / EXPLAIN ANALYZE)
      - row locks or deadlocks (check pg_locks, SHOW PROCESSLIST, etc.)
      - queries returning more data than needed (SELECT *)
      - missing indexes on columns used in WHERE, JOIN, ORDER BY
      - stale DB statistics (ANALYZE / VACUUM not run)
      - result size: is it paginated correctly? are limits applied?
   
   c) Cache layer:
      - does a cache exist? what is the hit rate? is it dropping?
      - cache stampede? (multiple requests rebuilding the same cache simultaneously)
      - TTL too short?
      - cache invalidated too frequently?
   
   d) Network and infrastructure layer:
      - latency added by synchronous calls to high-latency external services?
      - calls without properly configured timeout?
      - circuit breaker absent or not activated?
      - CPU, memory, or network saturation on any node?
      - load balancer distributing unevenly?
      - auto-scaling configured but with too long a cooldown?

4. PROFILING (IF SAFELY EXECUTABLE)
   If a staging environment with real traffic or installed profiling tools is available:
   - CPU profiling: which function consumes the most CPU? (flame graph)
   - Memory profiling: which object accumulates in the heap?
   - DB profiling: identify the 10 slowest queries (pg_stat_statements, slow query log)
   - I/O profiling: are there blocking disk operations?
   
   ⚠️ Production profiling must be done carefully — it can add overhead.
   Prefer staging with mirrored traffic when possible.

5. OPTIMIZATION PLAN
   For each identified bottleneck, propose optimizations in order of impact/effort:
   
   Structure per finding:
   - ID: PERF-XXX
   - affected layer: [application / DB / cache / infrastructure / network]
   - problem description
   - estimated impact: expected latency reduction or throughput increase (%)
   - estimated effort: [< 1h / half day / 1 day / > 1 day]
   - change type: [code / configuration / infrastructure / DB index]
   - regression risk: [low / medium / high]
   - how to measure impact: which metric to check before and after
   - specific proposed change
   
   Prioritize by: high impact + low effort first (quick wins), then high impact + high effort.

6. IMPACT VALIDATION
   After implementing each optimization:
   - compare before/after metrics: P50, P95, P99, throughput, error rate
   - run reference benchmark (`07-11`) if available
   - verify no functional regressions were introduced
   - update the performance baseline in documentation

7. STRUCTURAL IMPROVEMENTS (LONG TERM)
   If problems reveal architectural limitations:
   - is a cache needed where none exists? (Redis, Memcached, in-memory cache)
   - are there synchronous operations that should be asynchronous? (message queues)
   - are read replicas available to offload read queries from the primary DB?
   - are there CDN or edge cache candidates?
   - does the database scale horizontally or need sharding?
   - is there a capacity plan based on projected growth?

Deliverables:
- diagnostic report: symptom, root cause identified by layer, trace/log evidence,
- prioritized optimization plan (PERF-XXX table with impact, effort, risk),
- quick wins executable in < 1 day,
- long-term structural improvements with estimated impact,
- before/after metrics to validate each implemented optimization.
```

---

## Standard formula usage

```text
Use the production performance prompt and adapt it to:
- repository: [NAME OR URL]
- observed symptom: [description of degradation — metric, magnitude, period]
- technology stack: [language, framework, DB, cache, messaging]
- infrastructure: [cloud / on-premise / containers]
- available observability tools: [Grafana / Datadog / CloudWatch / none]
- attached data: [trace export, logs from the affected period, EXPLAIN results]
- impacted SLO: [SLO description and error budget status]
- available profiling environment: [production only / staging / none]
- documents to review: 07-06 performance design, 07-11 thresholds, 10-04 dashboards
- specific output goal: root cause diagnosis + prioritized optimization plan
- depth level: high
```

---

## Expected output

### Performance findings table

| ID | Layer | Problem | Estimated impact | Effort | Risk | Validation metric |
|---|---|---|---|---|---|---|
| PERF-001 | DB | N+1 queries on order listing (48 queries/request) | −85% P95 latency | < 1h | low | P95 endpoint `/orders` |
| PERF-002 | Application | No cache on catalog endpoint (100% cache miss) | −60% latency, +3× throughput | Half day | low | Redis hit rate, P95 `/catalog` |
| PERF-003 | DB | Missing index on `orders.customer_id` | −70% query latency | < 1h | low | EXPLAIN ANALYZE, P95 `/orders` |
| PERF-004 | Infrastructure | Auto-scaling with 10 min cooldown on spikes | Eliminates saturation during spikes | < 1h | low | CPU peak, req/s during spike |
