# 0-D.1 — Project Charter: Formal Definition of New Project

## Description

Prompt for generating the **Project Charter** of a new project: the foundational document that establishes the why, what, who, and high-level how, authorized by the sponsor and accepted by the team before any technical work begins.

**When to use it:** at the start of a new project, when formalizing a project that began without documentation, or when updating scope after a significant strategic change.

---

## Required prior context

> Include the block from `00-framework.md` before this prompt.

---

## Full prompt

```text
Objective:
Generate the complete Project Charter to formalize the start of this project.

Required inputs:
- project name: [NAME]
- project type: [new product / improvement of existing system / migration / integration / internal platform / other]
- sponsor: [ROLE OR NAME]
- client or end user: [INTERNAL / EXTERNAL — brief description]
- business context or need: [PROBLEM OR OPPORTUNITY THAT ORIGINATES THE PROJECT]
- preliminary technology stack: [framework, language, database, infra — may be tentative]
- known constraints: [budget, regulatory deadlines, mandatory technology, fixed team, etc.]
- key assumptions: [what must be true for the project to succeed]

Deliver the following Project Charter sections:

1. PROJECT DESCRIPTION
   - formal name and internal code (if applicable)
   - one-page executive summary: what it is, why it exists, what problem it solves
   - project type and strategic category

2. OBJECTIVES AND EXPECTED BENEFITS
   - primary objective (SMART: Specific, Measurable, Achievable, Relevant, Time-bound)
   - secondary objectives (max. 4)
   - expected quantifiable benefits: time savings, cost reduction, revenue increase, etc.
   - project success KPIs (measuring progress and delivery, not the product itself)

3. SCOPE
   - IN SCOPE: list of features, integrations, or deliverables included
   - OUT OF SCOPE: explicit list of what is NOT included (prevents scope creep)
   - scope assumptions: conditions that must hold to maintain the defined scope

4. STAKEHOLDERS AND TEAM
   Table with columns: Name/Role | Type (Sponsor / Owner / Team / User / AI agent) | Primary Responsibility | Authorization Level

5. DELIVERABLES AND ACCEPTANCE CRITERIA
   Table with columns: Deliverable | Brief Description | Acceptance Criterion | Owner | Estimated Date

6. MAIN MILESTONES (MILESTONE PLAN)
   Table with columns: Milestone | Description | Closure Criterion | Target Date
   (include at minimum: Kickoff, Approved Design, MVP/first delivery, UAT, Go-live, Closure)

7. BUDGET AND RESOURCES
   - effort estimate by role (person-days or weeks)
   - infrastructure resources required (cloud, licenses, tooling)
   - approved or pending funds (indicate if preliminary estimate)
   - engagement model if applicable: fixed / time & material / hybrid

8. INITIAL RISKS
   Table with columns: Risk | Probability (H/M/L) | Impact (H/M/L) | Strategy (avoid / mitigate / accept / transfer) | Owner

9. CONSTRAINTS AND DEPENDENCIES
   - technical constraints (platform version, third-party APIs, compliance, etc.)
   - organizational constraints (team, budget, change windows)
   - external dependencies: parallel projects, vendors, pending decisions

10. INITIAL TECHNOLOGY STACK
    Table with columns: Layer | Selected or Candidate Technology | Status (confirmed / tentative) | Brief Justification
    (if detailed architecture analysis is needed, use prompt 00-D-02)

11. GOVERNANCE MODEL AND CHANGE CONTROL
    - progress report frequency
    - process for requesting scope changes (who approves, how it is documented)
    - issue and task tracking tool: [GitHub Issues / Jira / Linear / other]
    - official project repository(ies)

12. SIGNATURES AND APPROVAL
    Table with columns: Role | Name | Signature / Confirmation | Date
    (sponsor, project manager / tech lead, client if external)

Output format:
- Structured document with all sections above
- Markdown tables where indicated
- Formal but technically precise language
- Mark with [PENDING: reason] any data that must be confirmed before signing the charter
```

---

## Usage notes

- This prompt generates the **foundational document** of the project; it does not replace the detailed technical design (`04-01-diseno-solucion.md`) or implementation plan (`05-01-plan-implementacion.md`).
- For detailed analysis and selection of the technology stack, continue with prompt **`00-D-02-stack-arquitectura-inicial.md`**.
- To generate the repository structure from this charter, use **`00-B-01-scaffolding-repositorio.md`**.
- Keep the Project Charter in the repository under `docs/project-charter.md` or `docs/00-project-charter/` for traceability.
