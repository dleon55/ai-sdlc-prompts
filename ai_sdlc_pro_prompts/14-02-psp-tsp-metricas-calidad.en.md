# 14.2 — Quality metrics logging and PSP/TSP estimations

## Description

Structured prompt to guide the developer in recording size, effort, times per phase, and defect log metrics, following the formal PSP (Personal Software Process) and TSP (Team Software Process) methodologies.

**When to use it:** at the beginning of development to record the base estimation (plan) and at the end of each software engineering phase to record actual effort and defects.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | low — records metrics and a defect log, does not modify code, configuration, or the build process |
| Required inputs | current issue or requirement, cycle phase (Planning, Design, Coding, Code Review, Testing, Post-mortem), previous metrics or log if they exist |
| Allowed tools | reading of previous time/defect history and the current issue — no execution or access to external tracking systems required |
| Permitted autonomy | A0 — Analyze the current status; A1 — Propose the updated log of estimates and actual metrics |
| Stop criteria | do not invent actual times or defects not reported by the developer; if the base estimate (plan) for a phase is missing, request it before calculating yield or defect density |
| Expected output | see `Output:` inside `## Complete prompt` |
| Minimum evidence | each time or defect entry is tied to a specific phase and, for defects, to its injection and removal phase |
| Recommended next prompt | repeat this same prompt at the close of the next cycle phase; `14-03-iso-moprosoft-compliance` if the metrics feed into a formal compliance audit |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Generate or update the planning and actual metrics log (times, defects, and size) of the development cycle for the current requirement.

Inputs:
- issue or requirement: [PASTE]
- current phase (Planning, Design, Coding, Code Review, Testing, Post-mortem): [CURRENT PHASE]
- previous metrics (if any): [PASTE HISTORY]

Activities:
1. Calculate and record the estimates (Plan) of:
   - size in lines of code (LOC) or function points,
   - estimated time per phase (in minutes).
2. During/at the end of the current phase, record actual metrics:
   - actual time consumed in the phase,
   - log of defects found (injection phase, removal phase, defect type, description, and fix time).
3. Calculate process yield and defect density (defects/KLOC).

Constraints:
- don't invent actual times or defects not reported by the developer — if a data point wasn't provided, mark it as pending instead of estimating it,
- don't calculate yield or defect density if the phase's base estimate (Plan) is missing — request it before continuing,
- record the injection phase and removal phase of each defect separately; don't collapse them into a single field,
- don't overwrite the metrics history of previous cycles or phases — the log is cumulative, it doesn't replace prior data.

Output:
1. Planning vs. Actual Summary (Time per Phase)
2. Defect Log (Injected/Removed)
3. Process Quality Indicators (Yield, Defect Density)
4. Corrective actions for the next cycle
```

---

## Use with standard formula

```text
Use the PSP/TSP metrics prompt and adapt it to:
- repository: [NAME OR URL]
- workspace/subproject: [IF APPLICABLE]
- standard/compliance: PSP
- issue or requirement: [REFERENCE]
- branch: [BRANCH]
- environment: DEV
- components: payments module
- documents to review: previous time logs, design plan
- specific output objective: estimation vs. actual report and defect log
- depth level: high
```

---

## Expected output

| Phase | Estimated time (min) | Actual time (min) | Deviation | Defects injected | Defects removed | Density (defects/KLOC) |
|---|---|---|---|---|---|---|
| Planning | 60 | 75 | +25% | 0 | 0 | — |
| Design | 90 | 80 | -11% | 1 | 0 | — |
| Coding | 240 | 310 | +29% | 5 | 2 | 3.2 |
| Code Review | 45 | 60 | +33% | 0 | 3 | — |
| Testing | 120 | 150 | +25% | 0 | 1 | — |
