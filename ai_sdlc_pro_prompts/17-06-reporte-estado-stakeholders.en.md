# 17.6 — Stakeholder status report

## Description

Prompt to generate a periodic progress report for a project or initiative aimed at non-technical stakeholders (sponsors, leadership, internal clients), built from real sources (issues/PRs for the period, CI/CD status, project charter milestones, active risks), translated into business language, without inventing unverified progress or hiding blockers or risks.

**When to use it:** at the close of a sprint or milestone, or on the periodic communication cadence agreed with stakeholders (weekly/biweekly).

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | report |
| Expected risk | medium — a report that overstates real progress or downplays a risk can lead stakeholders to make business decisions (customer commitments, additional investment) on a false basis; this prompt only reports and translates into business language, it does not decide or execute anything |
| Required inputs | committed milestones (from `00-D-01` or the current roadmap), issues/PRs closed and opened in the period, CI/CD status for the period, active risks (from `05-02` or the current register), period to report, audience (expected technical detail level) |
| Allowed tools | reading the task/issue tracker, PR history, CI results, and existing risk/milestone documents; the output is a report document — it does not reassign tasks, close issues, or modify the roadmap |
| Permitted autonomy | A0 — Analyze (gather real progress from the sources); A1 — Propose (draft the report in business language); never A2/A3 — this prompt does not communicate directly with stakeholders, it produces the document for a human to review and send |
| Stop criteria | stop and explicitly flag if a milestone reported as "in progress" has no verifiable associated issue/PR — do not report progress that cannot be traced to a real source; stop if the period to report is not defined |
| Expected output | see `## Expected output` |
| Minimum evidence | every milestone reported as completed or in progress cites the issue, PR, or CI result that supports it; every mentioned risk is traced to its source risk register |
| Recommended next prompt | `05-02-riesgos-implementacion` if a new, unregistered risk appears that should be formalized; `17-04-reporte-capacidad-equipo` if the report reveals the delay is due to team overload |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Generate the period's status report for non-technical stakeholders, translating real progress (verifiable in the provided sources) into business language, without inventing progress or hiding blockers or risks.

Inputs:
- committed milestones: [PASTE OR REFERENCE TO 00-D-01/ROADMAP]
- period's issues/PRs: [PASTE OR LINK TO TASK TRACKER]
- period's CI/CD status: [SUMMARY OR LINK]
- active risks: [PASTE OR REFERENCE TO 05-02/RISK REGISTER]
- period to report: [e.g. CURRENT SPRINT / LAST 2 WEEKS]
- audience: [EXECUTIVE SPONSOR / INTERNAL CLIENT / LEADERSHIP — expected technical detail level]

Steps:
1. VERIFIABLE PROGRESS COLLECTION
   For each committed milestone, determine its real status (completed/in progress/blocked/not started) citing the concrete issue, PR, or CI result that supports it. If a milestone has no verifiable evidence of progress, do not report it as "in progress" — report it as "no evidence of progress this period" instead of assuming optimism.

2. TRANSLATION INTO BUSINESS LANGUAGE
   Rewrite every technical milestone and blocker in terms a non-technical stakeholder can understand without knowing the architecture or stack (avoid technical jargon unless the declared audience requires it); connect each item to the relevant business impact (committed date, delivered value, risk to the customer).

3. RISKS AND BLOCKERS
   Incorporate the active risks from the provided register, translating their technical impact into business impact (what happens if the risk materializes, in terms of date, scope, or cost). Do not omit a high risk just because it lacks a confirmed mitigation yet — report it anyway, flagging that mitigation is pending.

4. PENDING DECISIONS
   Explicitly flag which business (not technical) decisions are blocking progress and require a response from stakeholders (e.g. scope approval, additional budget, prioritization between conflicting items).

5. UPCOMING MILESTONES
   List the upcoming committed milestones for the next period, with their target date and confidence level (high/medium/low) based on real observed progress, not the original plan if it has already diverged from reality.

6. EXECUTIVE SUMMARY
   Close with a one-screen summary: overall project status (on track / at risk / blocked), 2-3 achievements of the period, 2-3 main risks or blockers, and the decision(s) needed from stakeholders.

Constraints:
- never report a milestone as "completed" or "in progress" without being able to cite the issue, PR, or CI result that supports it — if there is no evidence, report it explicitly as no evidence of progress,
- do not downplay or omit an active risk or blocker to make the report look better — the goal is to inform accurately, not to manage the stakeholder's perception,
- do not make or hint at business decisions in this prompt (prioritization, budget approval) — flag that they are needed, but the human stakeholder makes the decision,
- adapt the technical detail level to the declared audience, but never sacrifice accuracy for simplicity — if simplifying a technical term loses a nuance important to the decision, keep it with a brief clarification instead of omitting it.

Output:
- executive summary: overall status, achievements, main risks, decisions required
- milestone table: milestone, status, cited evidence, target date
- active risks and blockers, in business language
- pending decisions from stakeholders
- upcoming milestones with confidence level
```

---

## Use with standard formula

```text
Use the stakeholder status report prompt and adapt it to:
- repository/project: [NAME OR URL]
- committed milestones: [REFERENCE TO 00-D-01/ROADMAP]
- period's issues/PRs: [LINK TO TASK TRACKER]
- CI/CD status: [SUMMARY OR LINK]
- active risks: [REFERENCE TO 05-02/RISK REGISTER]
- period to report: [CURRENT SPRINT / LAST 2 WEEKS]
- audience: [EXECUTIVE SPONSOR / INTERNAL CLIENT]
- documents to review: roadmap, task tracker, risk register
- specific output objective: status report ready to send to stakeholders
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Executive summary | Overall status, achievements, main risks, decisions required — one screen |
| Milestone table | Milestone, status, cited evidence, target date |
| Risks and blockers | Technical impact translated into business impact |
| Pending decisions | What business decision is needed and from whom |
| Upcoming milestones | Target date and confidence level based on real progress |

### Example (excerpt)

**Executive summary:** Overall status: **at risk**. Achievements this period: authentication migration completed and in production (PR #214); payments module test coverage rose from 40% to 78%. Main risk: the external billing provider integration has been blocked for 2 weeks due to missing sandbox credentials from the provider — no confirmed mitigation. Decision required: approve extending the "automated billing" milestone by 1 week, or drop that feature from the current release.

| Milestone | Status | Evidence | Target date |
|---|---|---|---|
| Authentication migration | Completed | PR #214, merged and deployed (deploy-gcp run #189, smoke test OK) | Met |
| External billing integration | Blocked | No new PRs in 9 days; issue #231 flags blockage due to provider credentials | At risk — depends on business decision |
