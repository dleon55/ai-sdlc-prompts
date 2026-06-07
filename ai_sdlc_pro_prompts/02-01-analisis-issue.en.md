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
- repository or module: [INDICATE]
- workspace/subproject: [INDICATE IF APPLICABLE]
- standard/compliance: [PSP / TSP / ISO / MOPROSOFT / MAAGTICSI / NONE]

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
1. Functional summary
2. Impacted use cases
3. Detected business rules
4. Involved technical components
5. Functional and technical risks
6. Attention recommendation
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
| Functional summary | Problem or need in business language |
| Impacted use cases | List of affected or derived UCs |
| Business rules | Restrictions, validations, detected logic |
| Technical components | Modules, services, involved tables |
| Risks | Identified functional and technical |
| Recommendation | Priority and suggested attention order |
