# 17.3 — Tool/License Adoption Evaluation and Decision

## Description

Prompt to produce an evaluation and decision sheet for a candidate tool, paid library, or SaaS service under consideration for adoption (ex: a new APM, a new commercially licensed library, a new cloud service). It covers total cost of ownership (licensing + integration time + maintenance), alternatives considered — including the option of not adopting — risks of vendor lock-in, data security/compliance, and single-vendor dependency, closing with an explicit recommendation to adopt, reject, or evaluate further. It does not buy, contract, or sign anything: it is a decision input for whoever approves budget to decide with informed judgment.

**When to use it:** before formally adopting a new tool, SaaS, or paid library that implies recurring cost or dependency on an external vendor. Distinction from related prompts: `11-08-finops-cloud-cost-audit` audits cloud spend for services the organization **already contracted**; this prompt evaluates the decision to adopt a service **not yet contracted**, and its output — if the tool involves recurring cloud cost — naturally feeds a future audit with `11-08-finops-cloud-cost-audit` once adopted.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis/decision — execution of the purchase, contracting, or signing of the vendor agreement is delegated to whoever approves budget; this prompt never executes an acquisition |
| Expected risk | medium — a poorly done evaluation sheet can lead to unnecessary spend, unanticipated vendor lock-in, or exposing sensitive data to a vendor without due compliance analysis, but the prompt itself only produces an analysis and recommendation document, never executes the purchase |
| Required inputs | name of the candidate tool/service, problem or need it solves, known alternatives (or a statement that none have been identified yet), available budget if applicable, proposed licensing model, type of data the tool will touch |
| Allowed tools | reading the vendor's public documentation, comparing alternatives, and calculating estimated total cost of ownership from provided or verifiable data; it does not execute purchases, sign contracts, or enter real company data into the vendor's platform for testing |
| Permitted autonomy | A1 — Propose (evaluation sheet with an adopt/reject/evaluate-further recommendation); never A2/A3 — this prompt does not approve budget or contract the vendor |
| Stop criteria | stop and escalate if no verifiable license price is available — never fabricate plausible-looking figures; stop if no alternative (including the option of not adopting) has been identified for comparison |
| Expected output | see `## Expected output` |
| Minimum evidence | every cost cited states its source (vendor documentation, quote, or "estimated" if no verified figure exists), at least one alternative besides "do not adopt" was listed, and the risks of vendor lock-in, security/compliance, and single-vendor dependency are made explicit with their severity |
| Recommended next prompt | `11-08-finops-cloud-cost-audit` if the adopted tool implies recurring cloud cost that should be periodically audited once in production |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a Procurement/FinOps Analyst specialized in tool and SaaS license evaluation. Produce an evaluation and decision sheet for the candidate tool indicated, covering total cost of ownership, alternatives considered, risks, and an explicit recommendation. Do not execute any purchase, contracting, or vendor sign-up: your output is a decision input for a human with budget authority to decide.

Inputs:
- candidate tool/service: [NAME OF THE TOOL OR SERVICE]
- problem or need it solves: [DESCRIPTION OF THE PROBLEM]
- known alternatives: [LIST OF ALTERNATIVES, INCLUDING "KEEP WITHOUT A TOOL" — or "none identified yet" if applicable]
- available budget (if applicable): [AMOUNT AND PERIODICITY, OR "not defined"]
- proposed licensing model: [PER USER / USAGE-BASED / FIXED SUBSCRIPTION / PERPETUAL WITH SUPPORT / OTHER]
- data the tool will touch or process: [TYPE OF DATA — ex. customer data, PII, source code, credentials, "nothing sensitive"]
- team or role requesting the adoption: [TEAM/ROLE]

Steps:

1. TOTAL COST OF OWNERSHIP (TCO)
   Break down the cost into:
   - license cost (monthly and annual, per the indicated model)
   - estimated integration time (person-hours required multiplied by a reference hourly cost)
   - expected ongoing maintenance cost (support, updates, operating time)
   - exit/migration cost if the tool is discontinued in the future
   Mark each figure as "verified" (with a source: quote, vendor documentation, public pricing) or "estimated" if there is no confirmed figure — never present an estimated figure as if it were verified.

2. ALTERNATIVES CONSIDERED
   List the alternatives evaluated, always including the "do not adopt / keep the status quo" option as the baseline for comparison. For each alternative, summarize approximate cost, product/vendor maturity, and expected adoption curve.

3. RISKS
   Explicitly assess:
   - vendor lock-in: how reversible the decision is, how tightly the system becomes tied to the vendor's proprietary format/API, and what it would cost to migrate away in the future.
   - data security and compliance: what data the vendor will see or process, whether an applicable regulatory requirement exists (ex. data protection, data residency, vendor certifications), and whether the tool would pass the organization's standard security review.
   - single-vendor dependency: what happens if the vendor unilaterally raises prices, changes service terms, is acquired by another company, or discontinues the product.
   - operational risk: the team's learning curve, quality of vendor support, and whether an SLA exists with real guarantees.
   For each risk, state severity (low/medium/high) and whether a known mitigation exists.

4. EXPECTED BENEFIT AND SUCCESS CRITERION
   Describe the problem the tool would solve in concrete terms and how adoption success would be measured if approved (a verifiable metric or observation), not in vague terms like "improves productivity".

5. RECOMMENDATION
   Conclude with one of three explicit recommendations: ADOPT, REJECT, or EVALUATE FURTHER (ex. via a time- and scope-bounded pilot or POC). Justify the recommendation by citing the findings from steps 1 through 4 — never present it without a traceable justification.

6. EXECUTIVE SUMMARY
   Summarize in a few lines the tool evaluated, the estimated total cost, the main risk identified, and the final recommendation, in a format that whoever approves budget can read without opening the rest of the document.

Constraints:
- never fabricate license prices or cost figures; if unavailable or unverified, state this explicitly as "unverified / estimated" and reflect that uncertainty in the final TCO.
- this prompt does not execute the purchase, sign contracts, create trial accounts with real company data, or enter sensitive data into the vendor's platform to evaluate it.
- every recommendation must compare against at least one real alternative, explicitly including the option of not adopting the tool.
- always explicitly flag if the tool would require sharing sensitive or regulated data with the vendor, even if the final recommendation is to adopt.
- the final decision to approve budget and contract the vendor belongs to a human with purchasing authority; this prompt only produces the sheet that supports that decision.
```

---

## Use with standard formula

```text
Use the tool/license evaluation prompt and adapt it to:
- repository/context: [PROJECT NAME OR URL]
- candidate tool/service: [TOOL NAME]
- problem it solves: [DESCRIPTION]
- known alternatives: [LIST OR "none identified yet"]
- available budget: [AMOUNT OR "not defined"]
- licensing model: [PER USER / USAGE-BASED / SUBSCRIPTION / OTHER]
- data the tool will touch: [TYPE OF DATA]
- documents to review: vendor's public quote or pricing, vendor security/compliance policy if available
- specific output objective: evaluation sheet with TCO, alternatives, risks, and an adopt/reject/evaluate-further recommendation
- depth level: high
```

---

## Expected output

| Criterion | Detail |
|---|---|
| Candidate tool | Datadog APM (Pro plan) |
| Problem it solves | lack of distributed tracing across microservices; mean incident diagnosis time > 2h |
| Estimated total cost (year 1) | license: USD 31/host/month × 12 hosts × 12 months = ~USD 4,464/year (verified, public pricing); integration: ~80 person-hours × USD 45/h = USD 3,600 (estimated); ongoing maintenance: ~4h/month × USD 45/h × 12 = USD 2,160/year (estimated) → year 1 TCO ≈ USD 10,224 |
| Alternatives considered | (1) do not adopt / keep current centralized logs — cost USD 0, but does not solve distributed tracing; (2) OpenTelemetry + self-hosted backend (Jaeger) — license cost USD 0 but higher integration time and self-managed operational maintenance (estimated 160h upfront + 8h/month); (3) New Relic APM — similar pricing, comparable maturity, not evaluated in depth due to lack of a quote |
| Vendor lock-in risk | medium — instrumentation via a proprietary SDK in the services' code; migrating to another APM would require re-instrumentation, mitigable by adopting OpenTelemetry as the instrumentation layer |
| Security/compliance risk | low-medium — the tool will process request traces that may include user metadata (no direct PII if redaction is configured correctly); vendor holds SOC 2 Type II certification (verified in its public documentation) |
| Single-vendor dependency risk | medium — no failover alternative; if the vendor raises prices or changes terms, migration takes weeks, not days |
| Recommendation | EVALUATE FURTHER — start a 30-day pilot on 2 non-critical services, with success criterion: reduce mean incident diagnosis time below 30 minutes, before committing to the full annual spend |

> Note: the full table should include every row of the analysis (broken-down TCO, each alternative considered, each risk assessed separately with severity), explicitly marking each cost figure as "verified" or "estimated".

### Executive summary

- **Tool evaluated:** [TOOL NAME] — solves [PROBLEM] for the [REQUESTING TEAM].
- **Estimated total cost (year 1):** [AMOUNT] — [VERIFIED / ESTIMATED, with license + integration + maintenance breakdown].
- **Main risk:** [HIGHEST-SEVERITY RISK] — proposed mitigation: [MITIGATION OR "none identified"].
- **Recommendation:** [ADOPT / REJECT / EVALUATE FURTHER] — [ONE-LINE JUSTIFICATION].
- **Decision pending on:** budget approval by [ROLE/PERSON WITH PURCHASING AUTHORITY] — this document does not authorize or execute the contracting.
