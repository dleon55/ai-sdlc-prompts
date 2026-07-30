# 17.7 — Post-launch success review: benefits realization against the Project Charter

## Description

Prompt to evaluate, weeks or months after a project or significant feature launches, whether the objectives and KPIs originally declared in the Project Charter (`00-D-01`) were met — closes the loop between what was promised and what was actually achieved. Distinct from `11-07-sre-postmortem-runbook` (postmortem of a single incident) and from `17-06-reporte-estado-stakeholders` (live status report during execution, not a benefits retrospective).

**When to use it:** weeks or months after launch, once real usage or business data is available — as a project's formal closure step or as a periodic review of already-launched initiatives.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — a biased or skipped success review leaves the organization with no real learning about whether its project investments generate the promised value, repeating the same benefit-estimation mistakes in future projects; the prompt does not execute or collect new data |
| Required inputs | original Project Charter with declared objectives/KPIs (`00-D-01`), real usage/adoption/business data since launch, elapsed time window |
| Allowed tools | reading existing documentation and already-collected data — no live data analysis or new instrumentation executed |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if a Charter KPI cannot be measured with available data, do not invent an approximate value — report it as "not measurable" and flag what instrumentation would be needed to measure it next time |
| Expected output | see `## Expected output` |
| Minimum evidence | every objective/KPI declared in the Charter appears in the review with its real measured value (or "not measurable" with the reason) and a met/partial/not-met verdict |
| Recommended next prompt | `11-03-deuda-tecnica` if the review reveals technical debt left pending from the original project |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Evaluate whether the launched project or feature met the objectives and KPIs declared in its original Project Charter, with real measured data, identifying unforeseen benefits and lessons for future estimates.

Inputs:
- original Project Charter: [PASTE OR REFERENCE TO 00-D-01]
- real usage/adoption/business data: [PASTE OR REFERENCE TO AVAILABLE DATA SOURCES]
- elapsed time since launch: [E.G. "6 weeks", "3 months"]

Activities:
1. RECOVER ORIGINAL OBJECTIVES
   Quote the objectives and KPIs declared in the original Project Charter verbatim — don't reinterpret them with the project's current hindsight.

2. REAL MEASUREMENT
   For each objective/KPI, measure the real value achieved with available data and compare it against the originally declared target.

3. VERDICT PER OBJECTIVE
   Classify each one: met / partially met / not met / not measurable (with the specific reason it isn't measurable).

4. UNFORESEEN BENEFITS
   Identify benefits (positive or negative) that materialized but weren't in the original Charter.

5. INVALIDATED ASSUMPTIONS
   Identify which assumptions from the original Charter turned out false in hindsight, and what's learned from that to improve future benefit estimates.

6. FOLLOW-UP RECOMMENDATION
   Recommend whether follow-up action is needed: additional investment to close a detected gap, new instrumentation to measure better next time, or closing the project as successful with no further action.

Constraints:
- never declare a KPI as "met" without a cited real measured value — if no data is available, it's "not measurable", never an optimistic assumption disguised as a measurement,
- quote the Charter's original objectives verbatim before evaluating them — don't reword them in a way that makes it easier to declare them met,
- explicitly distinguish a benefit truly caused by this project from a coincidental improvement from another cause — if causality can't be attributed with reasonable confidence, state that explicitly instead of attributing it,
- do not execute or collect new data — this review is read-only over already-available evidence; if instrumentation is missing to measure a KPI, report it as a finding, don't invent the missing data.

Output:
0. JSON metadata block (keys: status, kpis_evaluated, kpis_met_count, kpis_not_measurable_count, confidence_score [0.0 to 1.0]).
1. Original Charter objectives/KPIs (verbatim quote).
2. Real measured value per KPI, with the cited data source.
3. Verdict per KPI: met / partial / not met / not measurable.
4. Unforeseen benefits (positive and negative).
5. Charter assumptions that turned out false — lessons for the future.
6. Follow-up recommendation.
```

---

## Usage with standard formula

```text
Use the post-launch success review prompt and adapt it to:
- repository/project: [NAME OR URL]
- original Project Charter: [REFERENCE TO 00-D-01]
- elapsed time since launch: [E.G. "6 weeks"]
- documents to review: Project Charter, available usage/adoption/business data
- specific output objective: review of met/unmet KPIs with lessons learned
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the fulfillment summary |
| Original objectives (1) | Verbatim quote of the Charter's KPIs |
| Real measured value (2) | Real data per KPI, with cited source |
| Verdict (3) | Met/partial/not met/not measurable per KPI |
| Unforeseen benefits (4) | Unanticipated positive or negative effects |
| Invalidated assumptions (5) | What was assumed that turned out false, and the lesson |
| Recommendation (6) | Suggested follow-up action |

### Example (excerpt)

```json
{
  "status": "reviewed_with_findings",
  "kpis_evaluated": 4,
  "kpis_met_count": 2,
  "kpis_not_measurable_count": 1,
  "confidence_score": 0.71
}
```

| Original KPI (Charter) | Declared target | Real measured value | Source | Verdict |
|---|---|---|---|---|
| Checkout abandonment reduction | -15% in 8 weeks | -9% in 8 weeks | Conversion analytics dashboard | Partially met |
| Reduction in related support tickets | -20% | Not measurable | Ticket category wasn't tagged before launch to isolate this effect | Not measurable — missing instrumentation |

| Section | Example content |
|---|---|
| Invalidated assumptions (5) | The Charter assumed 80% of users would complete the new flow with no help; data shows 35% abandon at step 2 — the usability assumption was optimistic; for the next similar project, include a usability test with real users before committing to a conversion target |
