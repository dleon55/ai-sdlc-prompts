# 12 — Master orchestrator prompt for complete cycle

## Description

Prompt that coordinates the entirety of the software engineering cycle for an assignment: from repository comprehension to final documentation, passing through analysis, design, implementation, tests and integration.

**When to use it:** for complete assignments that require going through all phases, or when working with an agent that must operate autonomously on an issue from start to finish.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Coordinate the complete software engineering cycle for this assignment within the repository.

Input:
- issue/requirement/incident: [PASTE]
- target branch: [INDICATE]
- environment: [INDICATE]
- components: [INDICATE]

I want you to work by phases:

Phase 1. Comprehension and inventory
- review documentation, processes, policies and repo structure.

Phase 2. Analysis
- functional,
- technical,
- impact,
- risks,
- concurrency with other agents.

Phase 3. Design
- functional solution,
- technical solution,
- use cases,
- mermaid diagrams,
- implementation plan.

Phase 4. Controlled execution
- change proposal per file,
- commit strategy,
- validations.

Phase 5. Quality
- unit tests,
- integration,
- E2E,
- smoke,
- browser automation,
- static review.

Phase 6. Integration
- branches,
- local CI,
- GitHub Actions,
- integration risks.

Phase 7. Documentation
- technical memory,
- documentation update,
- release notes.

Mandatory output format:
1. Executive summary
2. Findings
3. Risks
4. Proposed design
5. Implementation plan
6. Test strategy
7. Integration strategy
8. Required documentation
9. Final recommendation
```

---

## Use with standard formula

```text
Use the master orchestrator prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [PASTE COMPLETE TEXT]
- target branch: [TARGET BRANCH]
- environment: [DEV / QA / STAGING / PROD]
- components: [INVOLVED COMPONENTS]
- documents to review: README, docs/, architecture, workflows, related issues
- specific output objective: documented complete cycle ready for execution
- depth level: high
```

---

## Phases and expected deliverables

| Phase | Name | Deliverable |
|---|---|---|
| 1 | Comprehension and inventory | Technical inventory + governance map |
| 2 | Analysis | Functional + technical + cross-impact analysis |
| 3 | Design | Complete design + diagrams + use cases |
| 4 | Controlled execution | Changes proposal + atomic commits |
| 5 | Quality | Test suite + static review |
| 6 | Integration | Branch strategy + CI status |
| 7 | Documentation | Technical memory + release notes |
