# 17.4 — Engineering Team Capacity and Workload Report

## Description

Prompt to produce a **people** capacity report: given a committed backlog or roadmap and the current composition of the engineering team (roles, seniority, availability, planned absences), it calculates committed workload against available capacity per period, identifies overload risks and specialty bottlenecks (including bus factor — points where only one person can do something critical), and proposes mitigation recommendations (redistribute work, replan dates, hire, train a backup). The prompt does not execute any of those recommendations: it does not reassign tasks, does not modify the roadmap, and does not manage hiring — it only reports the state and suggests options for a human (lead, PM, manager) to decide.

**When to use it:** when planning a sprint, quarter, or release with date commitments, or when there are signals of team overload (recurring delays, burnout, critical dependency on a single person). **Distinction from related prompts:** `11-10-capacity-planning` projects **infrastructure** capacity (compute, database, cache, rate limits) against a traffic or data growth hypothesis — it is the systems counterpart. This prompt, instead, reports the capacity of the team's **people**: how much human workload is committed versus available, and where there is a risk of overload or of a single team member concentrating critical knowledge. Both prompts answer the same question ("are we going to hit the ceiling?") but applied to different domains, and they must not be confused or merged: one measures servers, the other measures people.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis/planning |
| Expected risk | medium — a wrong capacity report can lead to committing to unreachable dates (team overload, burnout) or underutilizing available people, but the prompt itself only analyzes and recommends; the decision to redistribute work, replan, or hire is made by a human with authority over the team |
| Required inputs | current team composition (roles, seniority, specialties, weekly availability %), planned absences per person and period (vacation, leave, training), committed backlog or roadmap with effort estimates per item, period to evaluate |
| Allowed tools | reading task manager/backlog, absence calendar, roadmap and existing estimates; the output is a text report and recommendation document — it does not reassign tasks, does not modify the roadmap, does not open or close positions, and does not execute any personnel change |
| Permitted autonomy | A0 — Analyze (reading team composition, absences, and committed backlog); A1 — Propose (redistribution, replanning, or hiring recommendations); never A2/A3 — this prompt does not reassign tasks or execute personnel decisions, that is delegated to the human lead or manager responsible |
| Stop criteria | stop and escalate if there is no committed backlog/roadmap with effort estimates — never invent plausible-looking estimates; stop if team composition or planned absences are not confirmed and flag it as a residual risk instead of assuming full availability |
| Expected output | see `## Expected output` |
| Minimum evidence | each workload row cites the real source of the estimate (backlog item, ticket, or "estimated" if there is no formal item), each bus-factor risk identifies the single person and the affected specialty or system, and each recommendation states whether it applies short-term (redistribute within the period) or medium-term (hire, train a backup) |
| Recommended next prompt | `11-10-capacity-planning` — its infrastructure/compute counterpart, useful as a complement when team overload coincides with a technical growth roadmap (it does not replace this report, it evaluates a different domain); `05-01-plan-implementacion` to replan the scope or dates of committed items if the report reveals overload |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as an Engineering Manager or Team Lead specialized in team capacity planning. Based on the current composition of the engineering team and the committed backlog or roadmap, calculate committed workload against available capacity per period, identify risks of overload and of critical knowledge concentrated in a single person (bus factor), and propose recommendations to mitigate each risk.

Inputs:
- team composition: [LIST OF MEMBERS WITH ROLE, SENIORITY, SPECIALTY/STACK, AND WEEKLY AVAILABILITY %]
- planned absences: [PERSON, TYPE OF ABSENCE (VACATION/LEAVE/TRAINING), DATES — or "none confirmed" if applicable]
- committed backlog/roadmap: [LIST OF ITEMS WITH EFFORT ESTIMATE AND COMMITTED DATE, OR LINK TO TASK MANAGER]
- period to evaluate: [ex: CURRENT SPRINT / NEXT QUARTER / NEXT 3 MONTHS]
- critical specialties to watch: [ex: SOLE EXPERT IN PAYMENTS, SOLE PERSON WITH ACCESS/KNOWLEDGE OF LEGACY INFRASTRUCTURE — or "none identified yet" if applicable]

Steps:

1. AVAILABLE CAPACITY BASELINE
   For each team member, calculate the real available capacity in the evaluated period: weekly availability % minus planned absences minus time already committed to support/on-call/recurring meetings if known.
   - if a person's availability is not confirmed, state this explicitly and mark it as "estimated" instead of assuming 100%.

2. COMMITTED WORKLOAD PER PERSON AND ROLE
   Gather the committed backlog/roadmap and distribute the estimated effort per person or role/specialty according to current or planned assignment. If an item has no assigned owner, mark it as "unassigned" instead of distributing it arbitrarily.

3. COMMITTED VS. AVAILABLE WORKLOAD PER PERIOD
   Compare, per person and per aggregated role/specialty, the committed workload against the available capacity calculated in step 1. Express the result as a % utilization (committed workload / available capacity).

4. OVERLOAD IDENTIFICATION
   Explicitly flag any person or specialty with a projected utilization % above a reasonable threshold (ex: sustained >100%, or >85% with no margin for the unexpected). Do not treat overload as acceptable just because the commitment was already made.

5. BUS FACTOR AND SPECIALTY BOTTLENECK IDENTIFICATION
   For each critical specialty or system, identify whether there is only one person capable of doing that work (bus factor = 1). Explicitly flag the risk: what happens to the committed roadmap if that person is unavailable (absence, departure, parallel overload).

6. REPLANNING RISKS
   For each identified case of overload or bus factor, assess the impact on the roadmap's committed dates: which items would slip, and by how much, if no action is taken.

7. MITIGATION RECOMMENDATIONS
   For each identified risk, propose at least one concrete option: redistribute workload to people with available capacity, replan the dates or scope of affected items, train a second person as backup (reduce bus factor), or flag the need to hire if no internal option closes the gap. State the rough tradeoff of each option (time, quality risk, impact on other commitments).

8. EXECUTIVE SUMMARY AND NEXT STEPS
   Summarize the overall capacity state of the period, the people or specialties at greatest risk, and the recommendations prioritized by urgency.

Constraints:
- never present a committed workload figure without stating its source (backlog item with a real estimate, or "estimated" if there is no formal item) — every effort figure must be traceable to its origin.
- always distinguish confirmed availability (with cited source: absence calendar, hours contract) from assumed availability; label every figure in the output as "confirmed" or "estimated".
- this prompt analyzes and recommends; it never reassigns tasks, never modifies the roadmap or backlog, never opens, approves, or closes positions, nor executes any personnel change — all of that requires human decision and execution by the responsible lead or manager.
- if team composition or planned absences are not confirmed for a given person, say so explicitly and mark any capacity calculation depending on that data as low-confidence instead of assuming full availability.
- every bus-factor finding (a single person capable of a certain critical task) must be flagged as a risk even if there is no associated time overload — knowledge concentration is a risk independent of hourly workload.
```

---

## Use with standard formula

```text
Use the team capacity report prompt and adapt it to:
- repository/project: [NAME OR URL]
- team composition: [LIST OF MEMBERS WITH ROLE, SENIORITY, SPECIALTY, AND AVAILABILITY]
- planned absences: [SOURCE OR "none confirmed"]
- committed backlog/roadmap: [LINK TO TASK MANAGER OR LIST OF ITEMS]
- period to evaluate: [CURRENT SPRINT / NEXT QUARTER]
- critical specialties to watch: [LIST OR "none identified yet"]
- documents to review: task manager/backlog, absence calendar, committed roadmap
- specific output objective: identify overload and bus factor for the period, with prioritized recommendations
- depth level: high
```

---

## Expected output

| Person / Role | Available capacity | Committed workload | % Utilization | Identified risk | Recommendation |
|---|---|---|---|---|---|
| Ana Torres — Senior Backend, payments specialist | 32h/week (confirmed: 40h contract − 8h vacation week 3) | 38h/week (real, 4 assigned backlog items) | 119% — sustained overload | sole person able to touch the payments module (bus factor = 1); if unavailable, 3 committed roadmap items slip | redistribute 1 non-critical item to another backend engineer with available capacity; start backup training with [PERSON] before end of quarter |

> Note: the full table should include one row per evaluated team member or critical specialty, explicitly flagging bus-factor cases (a single person capable of a certain task) even when they have no associated hourly overload, and always separating "confirmed" from "estimated" availability.

### Executive summary

- **Overall capacity state of the period:** [OVERLOADED / TIGHT / WITH MARGIN] — average team utilization %: [VALUE].
- **People or specialties at greatest risk:** [LIST] — reason: [OVERLOAD / BUS FACTOR / BOTH].
- **Prioritized recommendations:** [ACTION 1 — high urgency], [ACTION 2 — medium urgency], [ACTION 3 — medium term].
- **Residual risks:** [people without confirmed availability, backlog items with no assigned owner, bus factor without an ongoing mitigation plan].
