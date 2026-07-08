# 2.5 — Comprehensive Requirement Analysis and Issue Generation (PRO)

## Description

Senior software engineering prompt designed to perform a comprehensive analysis of new requirements. It integrates Architecture, Technical-Functional Analysis, DBA, DevOps, and QA visions into a single flow. Its objective is to transform an ambiguous idea or requirement into a traceability report and a GitHub Issue that strictly complies with the project's **Definition of Ready (DoR)**.

**When to use it:** when receiving a complex user requirement, a change request (CR), or a product idea that has not yet been technically formalized.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a multi-disciplinary engineering unit to analyze a requirement and generate the necessary technical and functional documentation (Issues) for its implementation.

Inputs:
- repository: [NAME OR URL]
- user_requirement: [PRIMARY INPUT]
- base_branch: [TARGET BRANCH]

Analysis Activities:
1. DISCOVERY: Identify the core intent and business value.
2. TECHNICAL MAPPING: Locate affected current components, processes, and files.
3. ISO/IEEE IMPACT ANALYSIS: Evaluate changes in Architecture, Database, Infrastructure/Docker, and Security (DevSecOps).
4. TRACEABILITY: Relate the requirement to use cases and business rules.
5. DoR VALIDATION: Ensure the final result is "Ready" for a developer or AI agent.

Mandatory Output:

1. ANALYSIS REPORT (Traceability):
   - FACTS: Confirmed current state in the repository.
   - FINDINGS: Detected inconsistencies, technical debt, or dependencies.
   - ASSUMPTIONS: Necessary clarifications or design assumptions.
   - RISKS: Potential impacts on performance, security, or multi-agent collisions.
   - RECOMMENDATIONS: Implementation suggestions or architecture decisions (ADR).

2. GITHUB ISSUE MARKDOWN:
   Generate a code block ready to copy into GitHub with:
   - Technical-functional title.
   - User Story (As a... I want... So that...).
   - Acceptance Criteria (Gherkin: Given/When/Then).
   - Technical Tasks Checklist.
   - QA & Testing Strategy.
   - Recommended Labels.

3. IMPACT MATRIX:
   Table with affected modules, tables, and services, and their impact severity.
```

---

## Use with standard formula

```text
Use the comprehensive analysis prompt and adapt it to:
- repository: [NAME OR URL]
- user_requirement: [PRIMARY INPUT]
- base_branch: [TARGET BRANCH]
- documents to review: README, docs/, current architecture, related code.
- specific output objective: [SPECIFIC OBJECTIVE]
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Report (F/F/A/R/R) | Formal engineering findings structure |
| Impact Matrix | Impacted modules, tables, and services |
| GitHub Issue | Complete Markdown with User Story and Acceptance Criteria |
| DoR Validation | Checklist confirming that the issue is ready for execution |
| QA Strategy | Suggested unit and integration testing plan |
