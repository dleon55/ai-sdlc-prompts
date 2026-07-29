# 0-D.3 — Project work plan: schedule, WBS, and resource allocation

## Description

Prompt to build the **whole-project work plan**: work breakdown structure (WBS), estimation per phase or deliverable, dependencies, schedule with critical path, and resource allocation. This is the whole-project-level plan — distinct from `05-01-plan-implementacion`, which plans the execution of an already-designed change or feature within an existing component.

**When to use it:** after approving the Project Charter (`00-D-01`) and, if it already exists, the initial stack/architecture (`00-D-02`) — before starting project execution, to have a schedule and resource allocation that the team or sponsor can approve.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | high — the resulting schedule and resource allocation condition date commitments to the sponsor and the team's workload; an optimistic estimate or an undetected resource overallocation is typically discovered late, when it's already expensive to fix |
| Required inputs | approved Project Charter (`00-D-01`), scope and main deliverables, available team (roles, capacity, calendar), deadline or target window if it exists, known external dependencies (other teams, vendors, approvals) |
| Allowed tools | none for execution — the prompt produces a planning document (WBS, schedule, allocation table); it does not create real issues, milestones, or calendar events |
| Permitted autonomy | A1 — Propose (schedule and resource allocation remain marked as a proposal until approved by the sponsor or team) |
| Stop criteria | if the declared deadline is not achievable with the given team and scope, do not adjust the estimates to "make it fit" — report it explicitly as a conflict with the trade-off options; if team capacity information is missing, stop and request it before allocating resources |
| Expected output | see `## Expected output` |
| Minimum evidence | every WBS deliverable has an estimate with a declared method, every dependency between deliverables is listed, the critical path is explicitly identified, and any resource overallocation is flagged with the row and the affected resource |
| Recommended next prompt | `05-02-riesgos-implementacion` to go deeper into schedule-execution risks; `05-01-plan-implementacion` once each WBS deliverable enters its individual design/implementation phase |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Build the complete project work plan: work breakdown structure (WBS), estimation, dependencies, schedule with critical path, and resource allocation.

Inputs:
- approved Project Charter: [PASTE OR REFERENCE TO 00-D-01]
- scope and main deliverables: [LIST OR DESCRIPTION]
- available team: [ROLES, CAPACITY PER PERSON (hours/week), KNOWN CALENDAR/ABSENCES]
- deadline or target window: [DATE OR "not yet declared"]
- known external dependencies: [OTHER TEAMS, VENDORS, REQUIRED APPROVALS, OR "none declared"]

Activities:
1. WORK BREAKDOWN STRUCTURE (WBS)
   Decompose the scope into deliverables and, within each deliverable, into work packages small enough to estimate with confidence (rule of thumb: no package should exceed ~2 weeks of effort; if it does, decompose it further). Each work package must have a single identifiable owner (role, not necessarily a named person).

2. ESTIMATION
   For each work package, estimate the effort with an explicitly declared method (analogy with similar prior work, expert judgment, three-point PERT decomposition, or other) — never present a figure without indicating where it comes from. Declare the confidence level of each estimate (high/medium/low) based on the information available at estimation time.

3. DEPENDENCIES
   Identify dependencies between work packages (sequential, shared-resource, external) and classify them by type. Explicitly flag external dependencies (outside the team's direct control) because they carry the highest schedule risk.

4. SCHEDULE AND CRITICAL PATH
   From the estimates and dependencies, build the schedule and calculate the critical path (the sequence of work packages that determines the project's minimum duration). Explicitly flag how much slack each package outside the critical path has.

5. RESOURCE ALLOCATION
   Assign each work package to a role or person according to declared capacity. Detect and explicitly flag any overallocation (a resource committed beyond its declared capacity within the same time window) — do not resolve it on your own by reassigning or cutting scope without flagging it as a pending decision.

6. VALIDATION AGAINST THE DEADLINE
   If a deadline or target exists, compare it against the date resulting from the schedule. If the schedule doesn't meet the date, do not compress the estimates to force a fit — present the real trade-off options (reduce scope, add resources, extend the date, accept the risk of compressing with no margin) for the sponsor to decide.

Constraints:
- never lower an estimate solely to make the schedule meet a declared deadline — if there's a gap, report it explicitly with the trade-off options, don't hide it by compressing numbers,
- every work package must declare the estimation method used and its confidence level — an estimate with no declared method is reported as "unverifiable estimate", not as a definitive figure,
- do not assign a resource above its declared capacity without explicitly flagging it as overallocation — never leave it implicit in the allocation table,
- if team capacity or scope information is missing to plan with confidence, stop and request the missing information instead of assuming undeclared capacity or scope.

Output:
0. JSON metadata block (keys: status, work_package_count, critical_path_duration_days, overallocated_resources_count, confidence_score [0.0 to 1.0]).
1. WBS: Deliverable | Work package | Owner (role) | Estimate | Estimation method | Confidence
2. Dependencies: Work package | Depends on | Dependency type | Risk if delayed
3. Schedule with critical path: Work package | Start | End | On critical path? | Slack
4. Resource allocation: Resource (role/person) | Assigned packages | Total load vs. capacity | Overallocated?
5. Validation against the deadline: date resulting from the schedule, gap against the target date (if any), trade-off options if there's a gap.
6. Assumptions and information gaps pending confirmation before approving the plan.
```

---

## Usage with standard formula

```text
Use the project work plan prompt and adapt it to:
- repository/project: [NAME OR URL]
- Project Charter: [REFERENCE TO 00-D-01]
- scope and main deliverables: [LIST]
- available team: [ROLES AND CAPACITY]
- documents to review: Project Charter, initial architecture (00-D-02) if it exists
- specific output objective: WBS, schedule with critical path, and resource allocation
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the plan summary |
| WBS (1) | Complete table of deliverables and work packages with estimate and method |
| Dependencies (2) | All relevant dependencies, with external ones explicitly flagged |
| Schedule and critical path (3) | Dates per package, critical path identified, slack for each package outside it |
| Resource allocation (4) | Load per resource vs. capacity, with overallocations flagged |
| Validation against the deadline (5) | Explicit comparison against the target date, with trade-off options if there's a gap |
| Assumptions and gaps (6) | Information pending confirmation before approving the plan |

### Example (excerpt)

```json
{
  "status": "planned_with_gap",
  "work_package_count": 14,
  "critical_path_duration_days": 42,
  "overallocated_resources_count": 1,
  "confidence_score": 0.68
}
```

| Section | Example content |
|---|---|
| Resource allocation (4) | Backend dev (1 person, 30h/week) \| 5 packages assigned in weeks 3-6 \| 38h/week average vs. 30h/week capacity \| Yes — overallocated in week 4 |
| Validation against the deadline (5) | Declared target date: September 15. Date resulting from the schedule: September 29 (2-week gap). Options: (a) add a second backend dev starting week 3, (b) move the advanced reports deliverable to a phase 2, (c) accept the September 29 date |
