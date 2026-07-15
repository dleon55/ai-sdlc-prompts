# 17.5 — Vendor and Technology Contract Renewal Audit

## Description

Prompt to audit a vendor contract, SaaS subscription, or technology license before its renewal date: it compares observed real usage against what is licensed/contracted (are we overpaying?), contrasts the current solution against currently available market alternatives, weighs the risks of continuing (vendor lock-in, support quality, provider security posture) against the risks and migration cost/effort, and delivers an explicit recommendation to renew, renegotiate, migrate, or cancel. It does not execute the renewal or negotiate with the vendor: it is the audit brief that supports the decision of whoever administers the contract.

**When to use it:** in the cycle leading up to the renewal date of any technology vendor, SaaS, or license contract (ideally with enough lead time to leave room for negotiation or migration before expiration). Distinction from related prompts: `17-03-evaluacion-herramienta-licencia` is used to **adopt** a new tool that is not yet under contract, evaluating whether it is worth bringing in; this prompt is used to decide on a tool that is **already in production**, at its renewal point, with accumulated real usage and cost data. `11-08-finops-cloud-cost-audit` audits **aggregate** ongoing cloud infrastructure spend (compute, storage, networking across multiple providers); this prompt audits a **specific contract or license** at its renewal cycle, focused on the binary decision of whether to continue with that particular vendor or not.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis/audit — execution of the renewal, renegotiation, migration, or cancellation is delegated to whoever administers the contract (procurement, finance, or the technical owner of the vendor relationship), never to this prompt |
| Expected risk | medium — a wrong renewal recommendation can mean sustained overpayment, unnecessary lock-in, or migrating without sufficient justification, with cost and operational-continuity impact; the prompt itself only analyzes and recommends, it never executes the renewal or negotiates with the vendor |
| Required inputs | current contract or license terms (cost, contracted volume/seats, renewal date, cancellation or penalty clauses), real usage data (active seats, consumed volume, usage frequency by team/feature), known or to-be-researched market alternatives, vendor support or security incident history if available |
| Allowed tools | reading contracts, invoices, the vendor's own usage/analytics dashboards, public documentation of market alternatives; market research (web search) to compare current alternatives; the output is a text audit and recommendation document — it does not execute renewals, cancellations, migrations, or negotiations with the vendor |
| Permitted autonomy | A0 — Analyze (real usage vs. contracted, comparison of alternatives); A1 — Propose (recommendation to renew/renegotiate/migrate/cancel); never A2/A3 — this prompt does not renew, cancel, sign, or negotiate contracts, nor execute migration to an alternative |
| Stop criteria | stop and escalate if no real usage data is available to calculate the usage-vs-contracted ratio — never fabricate plausible-looking utilization figures; flag as a low-confidence recommendation if the comparison with market alternatives relies on outdated or unverified information; escalate as urgent if the renewal date is within less than the minimum lead time needed to negotiate or migrate |
| Expected output | see `## Expected output` |
| Minimum evidence | the real usage figure cites its source (vendor dashboard, access report, internal metrics) and its as-of date; current cost and renewal terms cite the corresponding contract or invoice; each market alternative mentioned states its source and consultation date |
| Recommended next prompt | `17-03-evaluacion-herramienta-licencia` if the recommendation is to migrate to an alternative — that alternative is re-evaluated as if it were a new adoption, with its own fit analysis |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a Technology Procurement Analyst specialized in vendor and SaaS contract renewal audits. Before the indicated renewal date, evaluate whether real usage justifies the contracted cost, whether the current solution is still the best option against currently available market alternatives, and the risks of continuing versus the risks and effort of migrating. Deliver an explicit recommendation: renew, renegotiate, migrate, or cancel.

Inputs:
- vendor/contract to audit: [VENDOR / PRODUCT / SERVICE NAME]
- renewal date: [DATE]
- current cost: [AMOUNT AND FREQUENCY — ex. USD 2,400/month, annual billing]
- contracted volume/plan: [ex. 50 SEATS / ENTERPRISE TIER / X REQUESTS-PER-MONTH]
- observed real usage: [AVAILABLE USAGE DATA — vendor analytics dashboard, access report, internal metrics — or "not available" if applicable]
- known market alternatives: [NAMES OF KNOWN COMPETITORS, or "none identified — requires research"]
- relevant contract clauses: [CANCELLATION NOTICE PERIOD, PENALTIES, AUTO-RENEWAL, DATA PORTABILITY]
- available lead time before the renewal date: [ex. 60 DAYS]

Steps:

1. REAL USAGE VS. CONTRACTED
   Calculate the ratio between what is actually used (active seats, consumed volume, usage frequency by team or feature) and what is contracted/licensed. Identify over-provisioning (paying for unused capacity) or under-provisioning (usage near the limit, risk of operational friction).
   - if no real usage data is available, state this explicitly and mark this section as "no data — low-confidence audit" instead of assuming a usage level.

2. CURRENT COST AND ITS TREND
   Document the current cost, its frequency, and how it has evolved across previous renewals if history is available (price increases, tier changes). Calculate the cost per real unit of usage (ex. cost per active seat, not per contracted seat) to expose overpayment if it exists.

3. COMPARISON WITH MARKET ALTERNATIVES
   Identify and compare at least 2-3 currently available market alternatives (or use the ones given in the inputs), evaluating equivalent functionality, approximate cost, and provider maturity. Cite the source and consultation date of each alternative. If no viable alternatives are identified, state this explicitly instead of inventing competitors.

4. RISKS OF CONTINUING WITH THE CURRENT VENDOR
   Evaluate vendor lock-in (difficulty and cost of leaving later), support quality and response times, the provider's security posture (certifications, known incidents, data policies), and the business's critical dependency on that tool.

5. RISKS AND COST/EFFORT OF MIGRATING
   If a viable alternative exists, estimate the migration effort (time, people, expected downtime, risk of data loss or transformation), the transition cost (double payment during the transition period, team training), and the risk that the alternative fails to meet requirements not evident today.

6. RELEVANT CONTRACTUAL CLAUSES
   Review cancellation notice periods, early-exit penalties, auto-renewal conditions, and data portability. Flag if any clause imposes a decision deadline earlier than the renewal date itself.

7. EXPLICIT RECOMMENDATION
   Based on the previous steps, deliver a single, explicit recommendation among: RENEW (no changes), RENEGOTIATE (renew with changes to price/plan/terms), MIGRATE (to an identified alternative), or CANCEL (no replacement). Justify the recommendation by citing the usage, cost, risk, and alternatives evidence gathered in the previous steps.

8. EXECUTIVE SUMMARY AND NEXT STEPS
   Summarize the recommendation, the estimated savings or cost of following it, the deadline to act (considering lead time and contractual clauses), and who must make the final decision.

Constraints:
- never present a real usage figure without citing its source and as-of date; if no usage data is available, say so explicitly and mark the audit as low-confidence instead of fabricating plausible-looking figures.
- always distinguish verified data (contract, invoice, usage dashboard) from estimates or assumptions; label every figure in the output as "real" or "estimated".
- this prompt analyzes and recommends; it never executes the renewal, the cancellation, the signing of a new contract, the negotiation with the vendor, or the technical migration to an alternative.
- if the available lead time before the renewal date is insufficient to execute the recommendation (negotiate, evaluate migration, process cancellation), flag it as an urgent risk requiring immediate human decision.
- if no viable market alternatives are identified, state this explicitly instead of inventing competitors or unverified comparisons.
```

---

## Use with standard formula

```text
Use the vendor renewal audit prompt and adapt it to:
- repository/organization: [NAME OR URL]
- vendor/contract to audit: [VENDOR / PRODUCT NAME]
- renewal date: [DATE]
- current cost: [AMOUNT AND FREQUENCY]
- contracted volume/plan: [SEATS / TIER / QUOTA]
- observed real usage: [DATA SOURCE OR "not available"]
- known alternatives: [NAMES OR "none identified"]
- available lead time: [ex. 60 DAYS]
- documents to review: current contract, recent invoices, vendor usage dashboard
- specific output objective: explicit recommendation to renew/renegotiate/migrate/cancel with usage, cost, and alternatives evidence
- depth level: high
```

---

## Expected output

| Dimension | Finding | Source / evidence |
|---|---|---|
| Real usage vs. contracted | 32 of 50 active seats over the last 90 days (64% utilization) — over-provisioning of 18 seats | vendor analytics dashboard, as of 2026-07-10 (real) |
| Current cost | USD 2,400/month (annual billing), no increase since the previous renewal | July 2026 invoice and current contract (real) |
| Cost per real unit of usage | USD 75/active seat (vs. USD 48/seat if the plan were adjusted to 32 seats) | derived calculation (estimated) |
| Market alternatives | 2 alternatives with equivalent functionality and 15-20% lower cost; 1 with more limited integration to the current stack | market research, consulted 2026-07-14 (real, subject to pricing changes) |
| Risks of continuing | moderate lock-in (data export possible but manual); support meeting 24h SLA over the last year; no reported security incidents | internal support ticket history (real) |
| Risks/cost of migrating | estimated effort 3-4 weeks of engineering, double payment during 1 month of transition, medium risk of team friction from the learning curve | technical team estimate (estimated) |
| Relevant clauses | auto-renewal with 30 days' notice required to cancel without penalty | current contract, clause 8.2 (real) |
| Recommendation | RENEGOTIATE: adjust the plan to 35 seats (with growth headroom) before renewal; if the vendor does not adjust price, evaluate migration in the next cycle | synthesis of the above findings |

> Note: the full table should cover every evaluated dimension (usage, cost, alternatives, risks of continuing, risks of migrating, contractual clauses), explicitly separating "real" evidence from estimates, and must always conclude with a single, explicit recommendation among RENEW / RENEGOTIATE / MIGRATE / CANCEL.

### Executive summary

- **Recommendation:** [RENEW / RENEGOTIATE / MIGRATE / CANCEL] — one-line justification.
- **Estimated savings or cost of following the recommendation:** [AMOUNT OR RANGE] compared to the current cost of renewing without changes.
- **Deadline to act:** [DATE], considering the available lead time and the contract's cancellation/auto-renewal clauses.
- **Residual risks:** [unavailable usage data, outdated market comparison, tight or insufficient lead time to execute the recommendation].
- **Owner of the final decision:** [ROLE/PERSON] — this prompt delivers the audit brief, it does not execute the renewal, renegotiation, migration, or cancellation.
