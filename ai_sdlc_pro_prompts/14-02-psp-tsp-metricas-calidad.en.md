# 14.2 — Quality metrics logging and PSP/TSP estimations

## Description

Structured prompt to guide the developer in recording size, effort, times per phase, and defect log metrics, following the formal PSP (Personal Software Process) and TSP (Team Software Process) methodologies.

**When to use it:** at the beginning of development to record the base estimation (plan) and at the end of each software engineering phase to record actual effort and defects.

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
