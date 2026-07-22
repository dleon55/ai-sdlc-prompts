# 16.5 — Aggregate Trend and Root Cause Analysis of Tickets

## Description

Prompt to analyze a batch or period of already-resolved support tickets and detect aggregate patterns: recurring categories, root causes common to multiple tickets, and the volume/cost associated with each pattern. It does not resolve tickets or go into the technical detail of an individual case: it groups signals across the whole batch to decide whether a pattern warrants an engineering initiative (recurring bug, missing documentation, product gap) instead of continuing to be absorbed case by case in support.

**When to use it:** periodically (monthly or quarterly) over a batch of tickets that were already individually handled and closed via `16-02`, as a retrospective exercise that feeds product and engineering decisions. Distinction from related prompts: `16-01` triages a single incoming ticket to classify and route it in the moment; `16-02` resolves one specific already-triaged ticket; this prompt does not touch individual tickets — it analyzes the already-resolved set to find signals that no isolated ticket reveals on its own. `02-04-triage-backlog-github` manages the backlog of engineering issues already created; this prompt is the upstream step that decides whether a ticket pattern warrants becoming one of those issues.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | low — the prompt only analyzes historical data from already-closed tickets and produces recommendations; it does not modify tickets, contact customers, or execute product or code changes |
| Required inputs | export or read access to the batch of resolved tickets for the period to analyze (ideally with category, summary, resolution, and resolution time for each), the date range or period to cover, existing category taxonomy if the team already uses one |
| Allowed tools | reading the ticketing/helpdesk system, support exports or dashboards; the output is a text analysis and recommendation document — it does not create, edit, or close tickets, and does not directly create engineering issues |
| Permitted autonomy | A0 — Analyze (reading and aggregate categorization of the batch); A1 — Propose (recommend engineering or documentation initiatives); never A2/A3 — this prompt does not create issues, deploy documentation, or execute product changes |
| Stop criteria | stop and escalate if the available ticket batch is too small or lacks the minimum fields (category, summary, resolution) to support an aggregate pattern — never invent categories or root causes without evidence from at least several repeated tickets; flag as low-confidence any pattern based on fewer than [MINIMUM THRESHOLD] tickets |
| Expected output | see `## Expected output` |
| Minimum evidence | each recurring category cites the real count of tickets that compose it and the date range of the batch analyzed; each aggregate root cause references at least the identifiers or summaries of the tickets that support it (not a single anecdote); each initiative recommendation explicitly distinguishes between recurring bug, documentation gap, and product gap |
| Recommended next prompt | `02-04-triage-backlog-github` if the recommendation is to create one or more engineering issues for a pattern identified as a recurring bug or product gap; `10-01-documentacion-tecnica` if the recommendation is to close a documentation gap identified as an aggregate root cause; `16-06-auditoria-base-conocimiento` to cross-check the detected recurring categories against the KB corpus and find coverage gaps |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a Support Analyst specialized in aggregate trend and root cause analysis. From a batch of support tickets already resolved in a given period, identify recurring categories, group root causes common to multiple tickets (not ticket by ticket), and recommend whether any pattern warrants an engineering or documentation initiative instead of continuing to be resolved case by case.

Inputs:
- source of the ticket batch: [CSV/JSON EXPORT, HELPDESK ACCESS (ZENDESK/JIRA SERVICE MANAGEMENT/FRESHDESK/OTHER), SUPPORT DASHBOARD]
- period to analyze: [ex: JUNE 2026 / Q2 2026]
- total ticket volume in the period: [NUMBER OR "unknown until analysis"]
- fields available per ticket: [CATEGORY/TAG, SUMMARY, RESOLUTION APPLIED, RESOLUTION TIME, AFFECTED PRODUCT/MODULE — state which are missing if applicable]
- existing category taxonomy: [THE ONE THE TEAM ALREADY USES, or "none exists — propose one during the analysis"]
- minimum ticket threshold to consider a pattern significant: [ex: 5 OR MORE TICKETS IN THE PERIOD]

Steps:

1. BATCH INVENTORY
   Confirm the real volume of tickets available for the period and the fields each one has. If key fields (category, summary, resolution) are missing for a relevant portion of the batch, state this explicitly and scope the analysis to the portion with sufficient data.

2. AGGREGATE CATEGORIZATION
   Group the batch's tickets into recurring categories (using the existing taxonomy if there is one, or proposing one based on the data if not). Do not analyze ticket by ticket in the output: report the count and percentage of the batch that each category represents.

3. IDENTIFICATION OF AGGREGATE ROOT CAUSES
   For each category with relevant volume (above the stated minimum threshold), identify the root cause common to the tickets that compose it — not the cause of an isolated ticket. Explicitly distinguish between:
   - recurring bug (the same software defect generates multiple tickets),
   - missing documentation (users cannot find or understand information that should already exist),
   - product gap (the product lacks a feature users need, so they turn to support as a substitute),
   - usage error or misaligned expectation (does not require an engineering change, but may require communication or onboarding).

4. VOLUME AND ASSOCIATED COST PER PATTERN
   For each identified aggregate root cause, quantify its impact: number of tickets, percentage of the period's total volume, and aggregate resolution time invested by the support team in that category (if the data is available).

5. "DOES IT WARRANT AN INITIATIVE?" EVALUATION
   For each pattern with relevant volume, evaluate whether it warrants a formal initiative (engineering issue for a recurring bug or product gap, documentation update for a documentation gap) instead of continuing to be resolved case by case in support. Justify the recommendation with the volume/cost quantified in step 4, not with subjective perception of urgency.

6. LOW-CONFIDENCE PATTERNS
   Explicitly flag any category or root cause that falls below the stated minimum ticket threshold, or that rests on very few cases — do not present these with the same level of certainty as well-supported patterns.

7. TIME TREND (IF DATA FROM PRIOR PERIODS IS AVAILABLE)
   If data from prior periods is available, indicate whether each recurring category is growing, stable, or declining relative to the previous period. If no historical data exists, state this explicitly instead of assuming a trend.

8. EXECUTIVE SUMMARY AND NEXT STEPS
   Summarize the highest-volume categories, the most significant aggregate root causes, and the recommended initiatives prioritized by volume/cost — not by order of appearance.

Constraints:
- never report a pattern or aggregate root cause based on a single ticket or a handful of cases below the stated minimum threshold; if the volume is insufficient to support a pattern, state this explicitly and mark it as a low-confidence finding.
- do not go into the resolution detail of an individual ticket — the goal is the batch's aggregate signal, not a ticket-by-ticket summary.
- always distinguish recurring bug, missing documentation, and product gap as separate root-cause categories — do not blend them under a generic label like "user issue".
- this prompt analyzes and recommends; it never creates, edits, or closes tickets, does not contact customers, does not directly create engineering issues, and does not publish documentation changes.
- if the ticket batch lacks minimum fields (category, summary, resolution) for a relevant portion, state this explicitly and scope the analysis to the portion with sufficient data instead of extrapolating over missing data.
```

---

## Use with standard formula

```text
Use the aggregate ticket trend and root cause analysis prompt and adapt it to:
- repository/product: [NAME OR URL]
- source of the ticket batch: [EXPORT OR HELPDESK SYSTEM]
- period to analyze: [ex: Q2 2026]
- total ticket volume: [NUMBER OR "unknown"]
- fields available per ticket: [CATEGORY, SUMMARY, RESOLUTION, RESOLUTION TIME]
- existing category taxonomy: [THE TEAM'S OR "propose one"]
- minimum ticket threshold per pattern: [ex: 5]
- documents to review: ticket export for the period, prior category taxonomy if it exists
- specific output objective: identify recurring categories, aggregate root causes, and whether they warrant an engineering or documentation initiative
- depth level: high
```

---

## Expected output

| Recurring category | Volume (tickets / % of period) | Aggregate root cause | Root cause type | Warrants initiative? |
|---|---|---|---|---|
| PDF report export errors | 23 tickets / 18% of June 2026 volume | The PDF generator truncates tables with more than 50 rows — same defect reported in tickets #4021, #4088, #4150 and 20 other cases | Recurring bug | Yes — create engineering issue (high priority, sustained volume for two consecutive months) |
| Confusion about configuring team permissions | 14 tickets / 11% of June 2026 volume | Existing documentation does not cover the nested-permissions flow introduced in the latest version | Missing documentation | Yes — update the permissions guide with the new flow |
| Recurring request to export to Excel in addition to PDF | 9 tickets / 7% of June 2026 volume | The product does not offer Excel export; users request the data in another format as a substitute | Product gap | Evaluate with product — volume still below the high-priority threshold, monitor next quarter |
| Questions about how to change the interface language | 3 tickets / 2% of June 2026 volume | Isolated cases with no identifiable common cause | Low confidence — insufficient volume | No — below the minimum threshold, keep resolving case by case |

> Note: the full table should include one row per recurring category identified in the batch, stating the real volume, the aggregate root cause with reference tickets, the root cause type (recurring bug / missing documentation / product gap / usage error), and the initiative recommendation prioritized by volume or cost, not by order of appearance.

### Executive summary

- **Period analyzed:** [PERIOD] — [N] resolved tickets analyzed out of a total of [N TOTAL] in the system.
- **Highest-volume categories:** [LIST OF 2-3 MAIN CATEGORIES] with their percentage of the total.
- **Recommended initiatives, prioritized:** [LIST OF INITIATIVES] — each with the root cause type and the volume/cost that supports it.
- **Low-confidence patterns:** [CATEGORIES BELOW THE THRESHOLD] — not yet actionable, keep under observation next period.
- **Residual risks:** [missing data in the batch, lack of historical comparison, taxonomy not validated with the support team].
