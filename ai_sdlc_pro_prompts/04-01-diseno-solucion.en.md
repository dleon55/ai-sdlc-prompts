# 4.1 — Functional and technical solution design

## Description

Prompt to design the complete solution before implementing: objective, scope, assumptions, restrictions, changes by component, risks, dependencies, validation strategy and rollback.

**When to use it:** once functional, technical and impact analysis is complete, before planning or executing any change.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design a complete, functional and technical solution for the analyzed requirement or incident.

Include:
1. Solution objective
2. Scope
3. Assumptions
4. Restrictions
5. Impacted use cases
6. Business rules
7. Changes required by component
8. Risks
9. Dependencies
10. Validation strategy
11. Rollback strategy

Output format:
1. Design summary
2. Functional design
3. Technical design
4. Affected components
5. Risks and mitigations
6. Implementation recommendation
```

---

## Use with standard formula

```text
Use the solution design prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [TARGET BRANCH]
- environment: [DEV / QA / PROD]
- components: [INVOLVED COMPONENTS]
- documents to review: previous analysis, architecture, contracts
- specific output objective: complete design with risks and rollback strategy
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Design summary | Executive description of the solution |
| Functional design | Changes in flows, rules and use cases |
| Technical design | Components, contracts, changes by module |
| Affected components | Precise list with change type |
| Risks and mitigations | Identified risks with mitigation plan |
| Recommendation | Order and priority of implementation |
