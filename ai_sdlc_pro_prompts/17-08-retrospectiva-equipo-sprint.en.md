# 17.8 — Team retrospective per sprint/iteration

## Description

Prompt to structure a team's process retrospective at the close of a sprint or iteration: what worked well, what didn't, patterns recurring across previous retrospectives, and concrete improvement actions with an owner and follow-up. Distinct from `11-07-sre-postmortem-runbook` (postmortem of a single technical incident), from `17-07-revision-exito-post-lanzamiento` (business KPI review months after launch, not team process), and from `14-02-psp-tsp-metricas-calidad` (individual developer time/defect metrics, not a qualitative team discussion). `00-B-04-metodologia-framework` only defines when and with whom the retrospective ceremony happens; this prompt is the one that runs it and produces its output.

**When to use it:** at the close of each sprint or iteration, as a structured input to (or written record of) the team's retrospective meeting.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — a retrospective that omits or softens real process problems, or whose improvement actions are never followed up on in the next cycle, lets the same problems repeat sprint after sprint unnoticed; the prompt does not execute any process or tooling change by itself |
| Required inputs | what happened in the current sprint/iteration (as reported by the team, not inferred), previous retrospective(s) with their pending improvement actions, if any |
| Allowed tools | none for execution — reading previous retrospectives and what the team reported; produces a retrospective document, does not modify process, configuration, or tooling |
| Permitted autonomy | A0 — Analyze; A1 — Propose (prioritized improvement actions) |
| Stop criteria | do not invent problems, wins, or root causes the team did not explicitly report — if something wasn't mentioned by the team, it isn't included as if it had been; if a previous retrospective's improvement action was never completed, report it explicitly instead of omitting it |
| Expected output | see `## Expected output` |
| Minimum evidence | every improvement action from the previous retrospective appears with its real status (completed/partial/not started); every issue reported as recurring cites which previous retrospectives it already appeared in |
| Recommended next prompt | repeat this same prompt at the close of the next sprint/iteration, picking up pending improvement actions; `11-03-deuda-tecnica` if the retrospective reveals technical debt not formally logged |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Structure the team's process retrospective at the close of the current sprint/iteration: what worked well, what didn't, patterns recurring across previous retrospectives, and prioritized improvement actions with an owner and follow-up criterion.

Inputs:
- current sprint/iteration: [NUMBER OR NAME, DATES]
- what the team reported about this sprint: [PASTE NOTES, COMMENTS, OR CEREMONY TRANSCRIPT]
- previous retrospective(s) with their improvement actions: [PASTE OR REFERENCE, OR "team's first retrospective"]

Activities:
1. PREVIOUS ACTIONS FOLLOW-UP
   For each improvement action from the previous retrospective, report its real status: completed, partial, or not started — with cited evidence (don't assume it was completed just because no one mentioned otherwise). An action with no reported follow-up is marked "not started", never "completed" by default.

2. WHAT WORKED WELL
   List the sprint's wins explicitly reported by the team, with the reason it worked (so it can be repeated), not just the list.

3. WHAT DIDN'T WORK
   List the problems explicitly reported by the team — without softening or generalizing beyond what was said. If the team reported a symptom with no clear root cause, report it as "root cause not identified" — don't invent one.

4. RECURRING PATTERNS
   Compare this sprint's problems against available previous retrospectives — identify which ones already appeared before (citing which retrospective) and distinguish them from problems that are new to this cycle. A problem repeating 2+ times with no effective action is a signal that the previous improvement action didn't address the real cause.

5. IMPROVEMENT ACTIONS
   Propose concrete, actionable steps for the next cycle, each with a suggested owner and how success will be known — don't list generic good intentions ("communicate better") without a concrete, verifiable process change.

6. CLOSING
   Summarize the team's overall state this sprint (improving / stable / with growing problems) based only on what was reported, not on a general impression.

Constraints:
- never report a previous improvement action as "completed" without cited evidence that it happened — with no evidence, report it as unverifiable,
- never invent problems, wins, or root causes the team didn't explicitly mention — report only what was reported,
- a recurring problem is cited with the previous retrospectives where it already appeared, not presented as if it were new,
- this prompt does not execute any process, tooling, or configuration change by itself — it only produces the retrospective document,
- if no previous retrospective exists, state that explicitly and omit the previous-actions-follow-up and recurring-patterns sections instead of inventing them.

Output:
0. JSON metadata block (keys: status, previous_actions_completed_count, previous_actions_pending_count, recurring_issues_count, confidence_score [0.0 to 1.0]).
1. Previous retrospective's action follow-up, with real status.
2. What worked well, with the reason.
3. What didn't work, with root cause if identified.
4. Recurring patterns across retrospectives, citing where they already appeared.
5. Prioritized improvement actions, with suggested owner and verification criterion.
6. Closing: the team's overall state this sprint.
```

---

## Usage with standard formula

```text
Use the team retrospective per sprint prompt and adapt it to:
- repository/project: [NAME OR URL]
- methodology: [SCRUM / KANBAN / OTHER]
- current sprint/iteration: [NUMBER OR NAME, DATES]
- documents to review: retrospective ceremony notes, previous retrospective(s)
- specific output objective: structured retrospective with action follow-up and recurring patterns
- depth level: medium
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the follow-up summary |
| Previous actions follow-up (1) | Real status (completed/partial/not started) of each previous action, with evidence |
| What worked well (2) | Wins reported by the team, with the reason |
| What didn't work (3) | Problems reported, with root cause if identified |
| Recurring patterns (4) | Repeated problems, citing which previous retrospectives they appeared in |
| Improvement actions (5) | Concrete actions, suggested owner, verification criterion |
| Closing (6) | The team's overall state this sprint |

### Example (excerpt)

```json
{
  "status": "retrospective_with_recurring_pattern",
  "previous_actions_completed_count": 1,
  "previous_actions_pending_count": 2,
  "recurring_issues_count": 1,
  "confidence_score": 0.76
}
```

| Previous action | Status | Evidence |
|---|---|---|
| Add an additional reviewer to payments PRs | Not started | No change to the review process was reported during the sprint |
| Document the deployment runbook | Completed | Runbook added at `docs/deploy-runbook.md`, referenced by the team in the ceremony |

| Recurring pattern | Retrospectives where it appeared | Signal |
|---|---|---|
| Third-party integration story estimates consistently underestimated | Sprint 12, Sprint 13, Sprint 14 (current) | The Sprint 12 improvement action ("review estimates with the integrations team before committing") was never implemented — repeating the same action without a process change doesn't break the pattern |
