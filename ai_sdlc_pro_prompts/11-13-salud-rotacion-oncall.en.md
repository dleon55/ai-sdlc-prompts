# 11.13 — On-call rotation health audit

## Description

Prompt to audit the health of an already-operating on-call schedule: real distribution of pages/alerts per person (business hours, night, weekend), fairness against the configured rotation schedule, correlation with fatigue or staff turnover signals, and rebalancing recommendations — without executing any changes to the schedule. Distinct from `17-04-reporte-capacidad-equipo` (committed backlog capacity vs. availability) and `11-04-incident-response` (execution of a single incident).

**When to use it:** periodically as a health check of the on-call schedule, or when the team reports fatigue, complaints of rotation inequity, or signals of high staff turnover in on-call roles.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | low — the prompt only analyzes and recommends; it does not modify the on-call schedule or reassign shifts. The risk is that an inequitable on-call schedule left undetected contributes to burnout or staff turnover, which does carry real cost |
| Required inputs | period's page/alert history (who received it, timestamp, time band), configured rotation schedule (who is on call when), period to evaluate, qualitative burnout or complaint signals if any (optional) |
| Allowed tools | reading the page history, the configured rotation schedule, and, if available, surveys or team climate signals; does not modify the on-call schedule or reassign shifts — produces the analysis and recommendation |
| Permitted autonomy | A0 — Analyze (real page distribution, rotation fairness); A1 — Propose (rebalancing recommendation); never A2/A3 — actually changing the on-call schedule requires human decision and execution by the responsible lead or manager |
| Stop criteria | stop if the page history does not distinguish business hours from night/weekend — do not assume all pages carry the same fatigue cost; stop if the configured rotation schedule is not available, do not infer shifts from the page history alone |
| Expected output | see `## Expected output` |
| Minimum evidence | every person in the distribution table cites the real page count per time band; every claim of inequity is compared against the expected distribution per the configured rotation schedule, not against an arbitrary average |
| Recommended next prompt | `17-04-reporte-capacidad-equipo` if on-call overload coincides with general backlog overload; `11-12-auditoria-ruido-alertas` if a large share of page volume turns out to be noise rather than real incidents |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Audit the health of the on-call schedule in the indicated period: real distribution of pages per person and time band, fairness against the configured rotation schedule, and correlation with fatigue or staff turnover signals, with rebalancing recommendations.

Inputs:
- period's page history: [PASTE OR LINK — who received it, timestamp, associated alert]
- configured rotation schedule: [PASTE OR LINK — who is on call when]
- period to evaluate: [e.g. LAST QUARTER]
- qualitative burnout/complaint signals: [PASTE IF ANY OR "none reported"]
- team's standard business hours: [e.g. Mon-Fri 9-6, TIME ZONE]

Steps:
1. REAL PAGE DISTRIBUTION PER PERSON
   For each person in the rotation schedule, count total pages received in the period, broken down by time band: business hours, night (outside standard business hours), and weekend. A page outside business hours does not carry the same fatigue cost as one during business hours — never aggregate them without distinguishing.

2. COMPARISON AGAINST EXPECTED ROTATION
   Compare the real page distribution against what the configured rotation schedule would predict (if everyone is on call a similar fraction of the time, do they receive a similar fraction of pages, or do some people disproportionately concentrate more due to their specialty's nature or errors in the schedule's configuration?).

3. INEQUITY IDENTIFICATION
   Explicitly flag if any person receives a notably higher proportion of night/weekend pages than their proportion of on-call time — and if so, whether it is due to the schedule's configuration (poorly distributed shifts) or because their specialty concentrates more real incidents (which points to a different problem: bus factor or the need to train backup, not just rotation).

4. CORRELATION WITH FATIGUE SIGNALS
   If qualitative signals are available (surveys, complaints, retrospective comments), relate the volume or time band of pages received per person to those signals. If no qualitative signals are available, state so explicitly and limit the analysis to quantitative data — do not infer burnout without evidence.

5. TREND OVER TIME
   If data from more than one period exists, flag whether on-call load is increasing, stable, or decreasing, and whether it coincides with any known event (user growth, prolonged incident, architecture change).

6. REBALANCING RECOMMENDATIONS
   Propose at least one concrete option for each identified inequity: redistribute night/weekend shifts more evenly, add one more person to the rotation if total load is high for the team's size, or train backup if the concentration is due to specialization rather than poor schedule configuration. State the approximate tradeoff of each option.

Constraints:
- never combine business-hours pages with night/weekend pages into a single figure without breaking them down — they carry different fatigue costs and hiding the distinction hides the real inequity,
- do not infer burnout or dissatisfaction without a qualitative signal to support it — if only quantitative page data exists, limit conclusions to load distribution, not the team's emotional state,
- this prompt analyzes and recommends; it never reassigns shifts, never modifies the rotation schedule, nor executes any change — that requires human decision and execution by the responsible lead or manager,
- if the configured rotation schedule is not available, stop and request it — do not infer expected shifts solely from the page history, which may not reflect the planned rotation if there were unrecorded manual changes.

Output:
- distribution table: person, business-hours pages, night pages, weekend pages, % of total
- comparison against expected rotation, with inequities explicitly flagged
- correlation with fatigue signals, if data exists (or its stated absence)
- trend over time, if data from more than one period exists
- prioritized rebalancing recommendations, with the tradeoff of each
```

---

## Use with standard formula

```text
Use the on-call rotation health audit prompt and adapt it to:
- repository/project: [NAME OR URL]
- page history: [LINK TO THE PERIOD'S HISTORY]
- rotation schedule: [LINK TO ON-CALL CONFIGURATION]
- period to evaluate: [LAST QUARTER]
- qualitative signals: [PASTE IF ANY OR "none reported"]
- standard business hours: [Mon-Fri 9-6, TIME ZONE]
- documents to review: page history, rotation schedule
- specific output objective: on-call load distribution with rebalancing recommendations
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Page distribution | Person, pages per time band, % of total |
| Comparison vs. expected rotation | Inequities explicitly flagged |
| Correlation with fatigue | Relationship with qualitative signals, or its stated absence |
| Trend | Load evolution if more than one period of data exists |
| Recommendations | Prioritized rebalancing, with tradeoff of each option |

### Example (excerpt)

| Person | Business-hours pages | Night pages | Weekend pages | % of total |
|---|---|---|---|---|
| Ana Torres | 8 | 14 | 6 | 38% (on-call = 25% of the team's time) |
| Luis Ramírez | 6 | 3 | 2 | 17% (on-call = 25% of the team's time) |

**Identified inequity:** Ana Torres receives 38% of total pages despite being on call 25% of the time — she concentrates twice as many night pages as the rest of the team. The cause is not a schedule configuration error (shifts are evenly distributed); Ana is the only one with deep knowledge of the payments module, which generates most of the night incidents. **Recommendation:** this is a bus-factor problem, not just a rotation one — train a second backup on the payments module before rebalancing shifts, since redistributing the shift without resolving the concentrated knowledge would only move the problem to someone without the context to resolve it.
