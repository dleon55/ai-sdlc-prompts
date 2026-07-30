# 0-D.4 — Project risk register (RAID): risks, assumptions, issues and dependencies

## Description

Prompt to build and maintain the **whole-project risk register** following the RAID format (Risks, Assumptions, Issues, Dependencies): potential risks with probability/impact, assumptions the plan rests on, issues already materialized that require resolution, and external dependencies that can block the schedule. This is the whole-project-level register — distinct from `05-02-riesgos-implementacion`, which analyzes the risks of a single already-designed change or feature.

**When to use it:** together with the Project Charter (`00-D-01`) and the work plan (`00-D-03`), at the start of the project, and reviewed periodically (each milestone or sprint) throughout execution — a risk register filled in only once at the start loses its value.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | high — this register is the input the sponsor uses for go/no-go and mitigation-investment decisions; a high risk omitted or misclassified at the whole-project level can materialize with no one having seen it coming, impacting date, budget, or scope, although the prompt does not execute or commit anything by itself |
| Required inputs | Project Charter (`00-D-01`), initial stack/architecture (`00-D-02`) if it exists, work plan (`00-D-03`) if it exists, known business constraints, history of materialized risks from similar projects if available |
| Allowed tools | none for execution — reads existing documentation; produces a register document (RAID log), does not apply any mitigation by itself |
| Permitted autonomy | A0 — Analyze (risks, assumptions, issues, and dependencies already declared or evident in context); A1 — Propose (mitigations, inferred risks not explicitly declared by the business, always marked as a proposal) |
| Stop criteria | if a risk is classified as high (high probability or high impact) with no viable mitigation, do not minimize it or leave it implicit — declare it explicitly as blocking approval of the Charter or the work plan |
| Expected output | see `## Expected output` |
| Minimum evidence | each risk (R-XXX) declares category, probability, impact, mitigation, and contingency; each assumption (A-XXX) declares what happens if it turns out false and how it will be validated; each issue (I-XXX) and dependency (D-XXX) declares an owner and a status |
| Recommended next prompt | `05-02-riesgos-implementacion` once each individual feature or change in the project enters its design/implementation phase — that prompt covers the specific risk of THAT change, it does not replace this project register |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Build the whole-project risk register in RAID format: risks, assumptions, issues already materialized, and external dependencies, with classification, owner, and action plan for each.

Inputs:
- Project Charter: [PASTE OR REFERENCE TO 00-D-01]
- initial stack/architecture: [PASTE OR REFERENCE TO 00-D-02, OR "not yet defined"]
- work plan: [PASTE OR REFERENCE TO 00-D-03, OR "not yet defined"]
- known business constraints: [BUDGET, DEADLINE, COMPLIANCE, OR "none declared"]
- history of materialized risks from similar projects: [DESCRIPTION OR "not available"]

Activities:
1. RISKS (R)
   Identify potential project risks by category: technical, business, resources/staffing, schedule, third parties/vendors, regulatory/compliance, financial. For each: identifier (R-XXX), category, description, probability (low/medium/high), impact (low/medium/high), owner, mitigation, contingency, and status (open/mitigated/closed/materialized). Base probability and impact on cited evidence (history, Charter, constraints) — if there isn't enough evidence, declare it as "risk not evaluable with available information" instead of assuming it's low.

2. ASSUMPTIONS (A)
   Identify the assumptions the Charter and work plan rest on (technical, business, resource, market). For each: identifier (A-XXX), description, what happens if it turns out false (impact of invalidation), how and when it will be validated, and status (validated/pending validation/invalidated).

3. ISSUES (I)
   Record problems already materialized (not hypothetical) that require active resolution right now — unlike risks, which are potential. For each: identifier (I-XXX), description, current impact, owner, resolution deadline, and status.

4. DEPENDENCIES (D)
   Identify dependencies external to the project team's direct control: other teams, vendors, regulatory or business approvals, shared infrastructure. For each: identifier (D-XXX), description, type (internal/external), which activity or milestone it blocks, date by which it's needed, and status.

5. PRIORITIZATION AND ESCALATION
   Prioritize risks by severity (probability × impact) and explicitly flag which ones require a sponsor decision or escalation before continuing. Never resolve a high risk with no viable mitigation on your own — report it as a pending decision.

6. REVIEW CADENCE
   Propose a review cadence for this register (weekly/biweekly/per milestone) proportional to the risk level declared in the Charter.

Constraints:
- never classify a risk as low just because evidence against it is missing — if there isn't enough information to evaluate it, declare it as "risk not evaluable with available information",
- no high risk may be left without explicit mitigation or contingency in the output — if no viable mitigation exists, declare it blocking instead of omitting or minimizing it,
- always distinguish a risk, assumption, issue, or dependency explicitly declared by the business/Charter from one you infer — never present them with the same level of certainty,
- do not confuse this project register with the risk analysis of a single implementation (`05-02`) — if you detect a risk that applies only to a specific change already in design, flag that it belongs in `05-02` instead of mixing it in here,
- if there is no reference Project Charter, stop and request it before building the register on your own assumptions.

Output:
0. JSON metadata block (keys: status, risk_count, high_risk_unmitigated_count, open_issues_count, confidence_score [0.0 to 1.0]).
1. Risks (R): ID | Category | Description | Probability | Impact | Owner | Mitigation | Contingency | Status
2. Assumptions (A): ID | Description | Impact if false | How/when validated | Status
3. Issues (I): ID | Description | Current impact | Owner | Deadline | Status
4. Dependencies (D): ID | Description | Type | Blocks | Date needed | Status
5. High risks with no viable mitigation — blockers for the sponsor.
6. Recommended review cadence.
```

---

## Usage with standard formula

```text
Use the project risk register (RAID) prompt and adapt it to:
- repository/project: [NAME OR URL]
- Project Charter: [REFERENCE TO 00-D-01]
- work plan: [REFERENCE TO 00-D-03, OR "not yet defined"]
- documents to review: Project Charter, initial architecture (00-D-02), work plan (00-D-03)
- specific output objective: complete RAID register with prioritized high risks
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the register summary |
| Risks (1) | Complete risk table with probability, impact, mitigation, and contingency |
| Assumptions (2) | Assumptions table with invalidation impact and validation plan |
| Issues (3) | Problems already materialized, with owner and deadline |
| Dependencies (4) | External dependencies with the date they're needed by |
| Unmitigated high risks (5) | List of blockers requiring a sponsor decision |
| Review cadence (6) | Recommended frequency to review the register |

### Example (excerpt)

```json
{
  "status": "registered_with_blockers",
  "risk_count": 11,
  "high_risk_unmitigated_count": 1,
  "open_issues_count": 2,
  "confidence_score": 0.7
}
```

| Section | Example content |
|---|---|
| Risks (1) | R-004 \| Third parties/vendors \| The payment gateway vendor hasn't confirmed sandbox availability for the integration start date \| Medium \| High \| Tech lead \| Escalate vendor contact this week; explore an alternate vendor as plan B \| If there's no sandbox in 2 weeks, move the payment integration to phase 2 of the schedule \| Open |
| Unmitigated high risks (5) | R-004 has no confirmed mitigation — it depends on an external response outside the team's control; requires a sponsor decision on whether to move the payment integration date before approving the final schedule |
