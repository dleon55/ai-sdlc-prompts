# 2.1 — Functional analysis of a requirement, issue or change

## Description

Prompt to analyze a requirement, issue or change and determine its functional scope: affected business flow, actors, current vs expected behavior, acceptance criteria and risks.

**When to use it:** as the first step when receiving a task, before any technical analysis or design.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze the requested requirement, issue or change and determine its functional and technical scope within the project, considering the monorepo structure and applicable standards.

Inputs:
- issue or requirement: [PASTE]
- repository: [NAME OR URL]
- module or functionality: [MODULE]
- workspace/subproject: [WORKSPACE/SUBPROJECT]
- standard/compliance: [STANDARD/COMPLIANCE]

Activities:
1. Understand the problem or need.
2. Identify:
   - affected business flow,
   - actor(s),
   - use case(s),
   - current behavior,
   - expected behavior,
   - functional and quality acceptance criteria.
3. Determine the affected monorepo subproject/workspace and if there are dependencies with other local packages.
4. Review if it is already documented in the project.
5. Relate the requirement to impacted modules, components and data.
6. Detect dependencies, risks, and security controls (DevSecOps/ISO 27001).

Output:
0. Start with a Task Metadata JSON Block (keys: status, impacted_components, risks_detected, confidence_score [0.0 to 1.0]).
1. Functional summary
2. Impacted use cases
3. Detected business rules
4. Involved technical components
5. Functional and technical risks
6. Attention recommendation
7. PSP/TSP Metrics Log (Estimated task duration in minutes, actual execution time, and initial estimated defects count).
```

---

## Use with standard formula

```text
Use the functional analysis prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [PASTE TEXT OR REFERENCE]
- branch: [CURRENT BRANCH]
- environment: [DEV / QA / PROD]
- components: [IF YOU ALREADY KNOW ANY]
- documents to review: README, docs/, existing use cases
- specific output objective: complete functional scope with acceptance criteria
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON Metadata (0) | Structured and parser-friendly JSON block containing primary diagnostic metadata |
| Functional summary (1) | Problem or need in business language |
| Impacted use cases (2) | List of affected or derived UCs |
| Business rules (3) | Restrictions, validations, detected logic |
| Technical components (4) | Modules, services, involved tables |
| Risks (5) | Identified functional and technical |
| Recommendation (6) | Priority and suggested attention order |
| PSP/TSP Metrics (7) | Logging block for time estimations (minutes) and projected defect rate |
