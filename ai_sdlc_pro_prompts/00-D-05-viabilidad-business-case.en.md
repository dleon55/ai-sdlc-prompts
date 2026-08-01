# 0-D.5 — Feasibility study and business case: should we even do this project?

## Description

Prompt to evaluate whether an idea or initiative **is worth formalizing as a project**, before investing time drafting the Project Charter: technical, economic, operational, and legal/regulatory feasibility, alternatives considered (including doing nothing), and an explicit go/no-go recommendation.

**When to use it:** upon receiving a project idea or business initiative, **before** `00-D-01-project-charter` — this prompt determines whether the project should be formalized at all; the Charter assumes that decision has already been made.

**Fast path — low risk:** for small, reversible initiatives (e.g. an internal improvement with no customer impact or significant budget), answer the 4 dimensions (technical, economic, operational, legal) in one paragraph each instead of the extensive document — reserve the exhaustive analysis for significant or hard-to-reverse investment decisions.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | high — this analysis's go/no-go recommendation conditions whether budget and team time get invested in formalizing the project; an optimistic or biased analysis can justify projects that shouldn't have been approved, although the prompt does not execute or commit anything by itself |
| Required inputs | raw idea or initiative, business context, known constraints (maximum budget, deadline, available resources), alternatives already considered if any |
| Allowed tools | none for execution — reading existing context and documentation; produces an analysis document, does not execute or approve anything |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if neither cost nor benefit can be estimated with minimal confidence, do not force a go/no-go recommendation — declare "feasibility not determinable with available information" instead of inventing a figure |
| Expected output | see `## Expected output` |
| Minimum evidence | each feasibility dimension (technical, economic, operational, legal/regulatory) has an explicit, cited verdict; discarded alternatives, including "doing nothing", are documented |
| Recommended next prompt | `00-D-01-project-charter` if the verdict is GO or conditional GO |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Evaluate whether the described idea or initiative justifies being formalized as a project: technical, economic, operational, and legal/regulatory feasibility, alternatives considered, and an explicit go/no-go recommendation.

Inputs:
- idea or initiative: [RAW DESCRIPTION]
- business context: [WHY THIS IDEA CAME UP, WHAT PROBLEM IT SOLVES]
- known constraints: [MAXIMUM BUDGET, DEADLINE, AVAILABLE RESOURCES, OR "not yet declared"]
- alternatives already considered: [PASTE OR "none considered yet"]

Activities:
1. TECHNICAL FEASIBILITY
   Assess whether the technology and team capability (current or acquirable) exist to execute this idea. Identify the major technical risks that could make it infeasible.

2. ECONOMIC FEASIBILITY
   Estimate the approximate cost (order of magnitude, with the estimation method declared) and the expected benefit (quantified if possible, qualitative if not). Calculate approximate ROI or payback period if there's enough information; if not, declare that explicitly instead of inventing a figure.

3. OPERATIONAL FEASIBILITY
   Assess whether the organization can operate and maintain the result once built: impact on existing processes, the team's capacity to sustain it over time, new operational dependencies it introduces.

4. LEGAL/REGULATORY FEASIBILITY
   Identify compliance constraints (industry regulation, data protection, licensing) that could block or significantly increase the cost of the project.

5. ALTERNATIVES CONSIDERED
   Compare at least: build, buy/adopt an existing solution, and doing nothing — with pros and cons of each. "Doing nothing" must always be evaluated explicitly, never skipped as obvious.

6. RECOMMENDATION
   Issue a verdict: GO / NO-GO / CONDITIONAL GO (with the specific conditions that must be met). Never issue a recommendation without justifying it against the 4 feasibility dimensions evaluated.

Constraints:
- never declare economic feasibility without declaring the cost/benefit estimation method used — a figure with no method is reported as unverifiable, not as a valid estimate,
- always include "doing nothing" as an explicit alternative to compare, never skip it as obvious,
- do not recommend GO if any feasibility dimension has a critical unmitigated risk — in that case, the recommendation must be NO-GO or CONDITIONAL GO on resolving that risk first,
- always distinguish an estimate based on real data from one based on assumptions — never present them with the same level of certainty.

Output:
0. JSON metadata block (keys: status, feasibility_verdict ["go", "no_go", "go_conditional", "not_determinable"], dimensions_evaluated, confidence_score [0.0 to 1.0]).
1. Technical feasibility: capability, technology, major risks.
2. Economic feasibility: estimated cost, expected benefit, ROI/payback if applicable, estimation method.
3. Operational feasibility: process impact, capacity to sustain the result.
4. Legal/regulatory feasibility: constraints identified.
5. Alternatives considered: build / buy / do nothing, with pros and cons.
6. Final recommendation: GO / NO-GO / CONDITIONAL GO, with conditions if applicable.
```

---

## Usage with standard formula

```text
Use the feasibility study and business case prompt and adapt it to:
- repository/project: [NAME OR URL, IF IT ALREADY EXISTS]
- idea or initiative: [RAW DESCRIPTION]
- business context: [WHY THIS IDEA CAME UP]
- documents to review: business context, known budget constraints
- specific output objective: go/no-go recommendation with the 4 feasibility dimensions
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the feasibility verdict |
| Technical feasibility (1) | Capability and major technical risks |
| Economic feasibility (2) | Cost, benefit, ROI/payback with declared estimation method |
| Operational feasibility (3) | Process impact and sustainment capacity |
| Legal/regulatory feasibility (4) | Compliance constraints identified |
| Alternatives (5) | Build / buy / do nothing, compared |
| Recommendation (6) | Go/no-go/conditional verdict, justified |

### Example (excerpt)

```json
{
  "status": "evaluated",
  "feasibility_verdict": "go_conditional",
  "dimensions_evaluated": 4,
  "confidence_score": 0.68
}
```

| Section | Example content |
|---|---|
| Economic feasibility (2) | Estimated cost: $80,000-120,000 USD (analogy with a similar prior payment-integration project, see previous `00-D-01`) \| Expected benefit: 15% reduction in checkout abandonment (qualitative estimate, no historical data of our own) \| ROI not reliably calculable — missing real current conversion data |
| Recommendation (6) | CONDITIONAL GO: proceed only if current checkout abandonment rate is instrumented for 4 weeks before approving the full budget, to validate the benefit assumption with real data instead of a qualitative estimate |
