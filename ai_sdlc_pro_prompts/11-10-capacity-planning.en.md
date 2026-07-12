# 11.10 — Capacity Planning and Scaling Forecast

## Description

Prompt to project future capacity needs (compute, database, cache, storage, third-party API rate limits) against a growth hypothesis, identify the first component that will hit its ceiling, and define scaling thresholds and the lead time needed to act before the bottleneck occurs. It does not measure current performance under load or provision infrastructure: it projects forward from explicit data and assumptions.

**When to use it:** when planning for expected growth (traffic, data volume, user base) before it happens, or after `07-06-pruebas-performance-carga` reveals a capacity ceiling under current load that needs a forward-looking capacity plan. Distinction from related prompts: `07-06-pruebas-performance-carga` measures current capacity under load through executed tests; this prompt projects **future** capacity needs against a growth curve, using load-test results as one input among several. `11-08-finops-cloud-cost-audit` audits **current** cloud spend; this prompt projects how much and when future scaling will cost, which naturally feeds a future cost audit.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis/planning |
| Expected risk | medium — a wrong capacity projection can lead to over-provisioning (wasted budget) or under-provisioning (service outage when the ceiling is hit), but the prompt itself only analyzes and recommends, it never provisions infrastructure |
| Required inputs | current utilization metrics per layer (compute, DB connections/storage, cache, third-party API rate limits, queue depth), expected growth hypothesis and its source (real business projection or assumption), load-test results if available (`07-06`) |
| Allowed tools | reading metrics, dashboards, load-test results and business projections; the output is a text analysis and recommendation document — it does not execute infrastructure changes or configure autoscaling |
| Permitted autonomy | A0 — Analyze (metrics reading and projection); A1 — Propose (scaling plan and thresholds); never A2/A3 — this prompt does not provision, resize, or modify infrastructure |
| Stop criteria | stop and escalate if no real utilization metric is available for the critical component — never fabricate plausible-looking figures; flag the projection as low-confidence if the growth hypothesis is an unsupported assumption |
| Expected output | see `## Expected output` |
| Minimum evidence | each projection cites the real baseline metric (or explicitly states it is estimated), the growth assumption used and its source, and the projection model applied (linear or otherwise, with justification) |
| Recommended next prompt | `07-06-pruebas-performance-carga` to validate the projected ceiling with an actual load test before committing to the plan; `11-08-finops-cloud-cost-audit` to validate the cost impact of the proposed scaling plan |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as an Infrastructure Architect specialized in capacity planning. Project the capacity needs of each system layer against the given growth hypothesis, identify the first component that will hit its current ceiling, and define a scaling plan with concrete thresholds and execution lead time.

Inputs:
- components/layers to evaluate: [COMPUTE / DATABASE (connections, storage, IOPS) / CACHE / QUEUES / THIRD-PARTY API RATE LIMITS / CDN / OTHER]
- available current utilization metrics: [DASHBOARD, METRICS EXPORT, RESULTS FROM 07-06 OR OTHER SOURCE — or "not available" if applicable]
- growth hypothesis to plan for: [ex: 3x active users in 6 months / +40% transaction volume in Q1]
- source of the growth hypothesis: [FORMAL BUSINESS PROJECTION / TEAM ASSUMPTION / EXTRAPOLATION OF HISTORICAL TREND]
- planning horizon: [ex: 6 MONTHS / 12 MONTHS]

Steps:

1. CURRENT UTILIZATION BASELINE
   For each layer (compute, DB connections and storage, cache, queue depth, third-party API rate limits), gather the actual current utilization (P50/P95, peak, average) from existing metrics.
   - if a layer has no available metrics, state this explicitly and mark it as "no data — low-confidence projection" instead of assuming a value.

2. GROWTH HYPOTHESIS AND ITS SOURCE
   Document the growth hypothesis to use (ex: 3x users in 6 months) and classify its origin: formal business projection, team assumption, or extrapolation of a historical trend. State the confidence level for each classification.

3. PER-LAYER PROJECTION
   For each component, project when it will hit its current ceiling under the growth hypothesis, using the simplest defensible model (linear extrapolation by default). If there is reason to expect non-linear growth (viral, seasonal, network effect), use that model and justify why.

4. IDENTIFY THE MAIN BOTTLENECK
   Among all projected layers, identify which one will be the FIRST to hit its ceiling (the binding constraint). Do not treat every layer as equally urgent: prioritize by estimated saturation date, not by perceived severity.

5. SCALING OPTIONS FOR THE BOTTLENECK
   For the component identified as the binding constraint, evaluate options (vertical scaling, horizontal scaling, additional caching, read replicas, partitioning, architectural change) with rough cost, complexity, and implementation-time tradeoffs.

6. SCALING THRESHOLDS AND TRIGGERS
   Define concrete, actionable thresholds (ex: "scale out horizontally when CPU P95 > 70% sustained for 10 minutes", "add a read replica when active connections > 80% of pool for 15 minutes"). Avoid vague recommendations like "monitor and react".

7. EXECUTION LEAD TIME
   Estimate how long it takes to execute the recommended scaling action (provisioning, budget approval, migration, API vendor contract change) and verify that lead time fits before the projected saturation date. If it doesn't, flag it as an urgent risk.

8. EXECUTIVE SUMMARY AND NEXT STEPS
   Summarize the main bottleneck, the estimated saturation date, the recommended action, and when it must start to avoid compromising the service.

Constraints:
- never present a capacity projection without stating the underlying growth hypothesis and its confidence level — every projection depends on an assumption that must be made explicit.
- always distinguish real utilization data (with cited source) from estimated or assumed figures; label every number in the output as "real" or "estimated".
- this prompt analyzes and recommends; it never provisions, resizes, or modifies infrastructure, nor executes deployment or scaling commands (`terraform apply`, `kubectl scale`, cloud provider tier changes, etc.).
- if baseline utilization metrics are unavailable for a layer, say so explicitly and mark that layer's entire projection as low-confidence instead of fabricating plausible-looking numbers.
- if the execution lead time for the recommended action exceeds the time remaining until the projected saturation date, flag it as a critical risk requiring immediate human decision and prioritization.
```

---

## Use with standard formula

```text
Use the capacity planning prompt and adapt it to:
- repository: [NAME OR URL]
- components/layers to evaluate: [COMPUTE / DB / CACHE / QUEUES / RATE LIMITS]
- available current utilization metrics: [SOURCE OR "not available"]
- growth hypothesis: [ex: 3x users in 6 months]
- source of the hypothesis: [BUSINESS PROJECTION / ASSUMPTION / HISTORICAL TREND]
- planning horizon: [6 MONTHS / 12 MONTHS]
- documents to review: metrics dashboards, load-test results (07-06), business projections
- specific output objective: identify the main bottleneck and a scaling plan with thresholds and lead time
- depth level: high
```

---

## Expected output

| Component | Current utilization | Projection at [N months] | Current ceiling | Estimated saturation date | Recommended action |
|---|---|---|---|---|---|
| DB connection pool (primary Postgres) | 65% average, 82% P95 (real, last 30 days) | +3x traffic in 6 months (business projection, high confidence) → P95 exceeds 100% by month 3 | 100 max configured connections | month 3 of the horizon (linear extrapolation over P95) | add pgBouncer in transaction mode + read replica for reads; estimated lead time 3-4 weeks — start in month 1 to avoid compromising the service |

> Note: the full table should include one row per evaluated layer (compute, DB, cache, queues, third-party rate limits, etc.), identifying which is the main bottleneck (earliest saturation date) and explicitly separating "real" from "estimated" utilization in each cell.

### Executive summary

- **Main bottleneck:** [COMPONENT] — first to hit its ceiling, on [ESTIMATED DATE].
- **Growth hypothesis used:** [DESCRIPTION] — source: [BUSINESS PROJECTION / ASSUMPTION] — confidence: [HIGH / MEDIUM / LOW].
- **Recommended action and lead time:** [ACTION] — must start before [DEADLINE] to avoid compromising the service.
- **Residual risks:** [layers without utilization data, growth assumptions not validated by business, tight or insufficient lead time].
