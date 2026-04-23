# 2.4 — GitHub Issues backlog triage and planning

## Description

Composite prompt to analyze a set of GitHub issues from the current repository or a target repository, filtered by component, assignee, labels, or pending status. It helps classify the backlog, detect logical groupings, prioritize attention, and propose an implementation or remediation plan aligned with the project's methodology, architecture, and standards.

**When to use it:** when you need to review open or pending issues as a work portfolio, order their attention by priority or component, or prepare a master execution plan for a sprint, remediation, or stabilization effort.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze the GitHub Issues backlog associated with the indicated repository and generate a structured diagnosis, a management-oriented categorization, and a prioritized, controlled, traceable attention plan.

Context:
- Work occurs in a multi-agent environment.
- Do not assume the state of the repository, branches, or issues is static.
- Before issuing recommendations, consider documentation, processes, active branches, CI/CD, concurrency risks, and dependencies between issues.

Inputs:
- repository: [ORG/REPO or URL]
- issues source: [gh issue list output / JSON export / CSV export / table / pasted text]
- applied filter: [assignee / label / component / milestone / status / no filter]
- pending backlog criteria: [open / open without PR / blocked / ready / triage pending / other]
- target component or area: [INDICATE or "all"]
- target assignee or owner: [INDICATE or "all"]
- target branch: [main / develop / release / INDICATE]
- target environment: [DEV / QA / STAGING / PROD]
- documents to review: [README, docs/, architecture, workflows, related issues]

Activities:
1. Validate the context:
   - review project documentation, processes, policies, standards, and guidelines;
   - review recent changes, active branches, and possible conflicts with other agents;
   - detect whether there are PRs or branches related to any analyzed issue.

2. Normalize the input:
   - convert each issue into a homogeneous record with:
     - number,
     - title,
     - status,
     - labels,
     - milestone,
     - assignee,
     - inferred component or module,
     - work type,
     - inferred severity or criticality,
     - dependency with other issues,
     - evidence of blocking or waiting,
     - relation with PR or branch if it exists.

3. Classify each issue by category:
   - bug,
   - incident,
   - requirement,
   - improvement,
   - technical debt,
   - testing / QA,
   - documentation,
   - security / DevSecOps,
   - infrastructure / CI/CD / operations,
   - pending analysis,
   - missing functional definition.

4. Classify each issue by attention state:
   - ready for analysis,
   - requires functional clarification,
   - requires technical analysis,
   - blocked by dependency,
   - blocked by environment,
   - blocked by another branch / PR,
   - ready to implement,
   - ready to validate,
   - candidate for closure,
   - duplicate / consolidable.

5. Evaluate actual priority considering:
   - business or user impact,
   - technical criticality,
   - regression risk,
   - operational risk,
   - security risk,
   - dependency with other issues,
   - estimated effort,
   - urgency of the target environment,
   - existence of workaround.

6. Identify groupings and consolidation opportunities:
   - issues in the same component,
   - issues in the same functional flow,
   - issues with the same root cause,
   - issues that should be addressed together in a single plan,
   - issues that must stay separate to preserve atomic commits and low risk.

7. Propose attention order:
   - safe quick wins first,
   - then functional or technical blockers,
   - then structural dependencies,
   - finally lower urgency improvements.

8. For each prioritized issue or issue group, propose:
   - attention objective,
   - scope,
   - affected component,
   - preconditions,
   - tasks,
   - suggested owner by role,
   - deliverables,
   - validations,
   - risks,
   - recommended branch / integration strategy.

9. If information is missing, document exactly what is missing:
   - insufficient description,
   - missing acceptance criteria,
   - ambiguous component,
   - unsupported priority,
   - unexplained dependency,
   - issue that should be split or consolidated.

10. If the source is `gh issue list`, assume the output may come raw or summarized. If the information is not enough to classify precisely, state it as an assumption and lower the confidence level.

Mandatory output format:
1. Executive summary
2. Confirmed facts
3. Findings
4. Assumptions
5. Risks
6. Normalized issues matrix
7. Categorization by component / owner / priority / attention state
8. Dependencies and potential conflicts
9. Attention or remediation plan
10. Final recommendations

Expected structure inside the output:

### Normalized issues matrix
| Issue | Title | GH Status | Component | Assignee | Type | Priority | Attention state | Dependencies | Observations |
|---|---|---|---|---|---|---|---|---|---|

### Categorization by component
| Component | Issues | Dominant severity | Aggregated risk | Recommendation |
|---|---|---|---|---|

### Categorization by owner
| Current owner | Assigned issues | General state | Load risk | Suggested action |
|---|---|---|---|---|

### Attention or remediation plan
| Order | Issue or group | Priority | Objective | Key tasks | Suggested owner | Deliverables | Dependencies | Risks | Validation |
|---|---|---|---|---|---|---|---|---|---|

### Suggested executable backlog
| Phase | Scope | Included issues | Expected outcome |
|---|---|---|---|
| 1 | Quick wins / low risk | | |
| 2 | Functional or technical blockers | | |
| 3 | Structural remediation | | |
| 4 | Improvements and hardening | | |

Decision rules:
- Do not mix unrelated issues in the same execution block.
- Do not propose issue closure without evidence.
- Do not propose implementation when functional or technical analysis is still missing.
- When several issues are similar, indicate whether it is better to:
  - consolidate them under an epic or master issue,
  - keep them separated,
  - relate them by dependency.
- Always distinguish between confirmed facts and inferred classification.
```

---

## Use with standard formula

```text
Use the GitHub Issues backlog triage and planning prompt and adapt it to:
- repository: [ORG/REPO]
- issues source: [PASTE gh issue list OUTPUT OR EXPORT]
- applied filter: [assignee / component / label / status]
- pending criteria: [open / blocked / without associated PR / triage pending]
- target component: [COMPONENT NAME OR "all"]
- target owner: [USER OR "all"]
- target branch: [main / develop / release]
- environment: [DEV / QA / STAGING / PROD]
- documents to review: README, docs/, architecture, workflows, related PRs and issues
- specific output objective: categorized backlog and attention plan with priorities, tasks, owners and deliverables
- depth level: high
```

```text
Example with gh issue list:
gh issue list \
  --repo [ORG/REPO] \
  --state open \
  --limit 200 \
  --json number,title,body,labels,assignees,milestone,state,createdAt,updatedAt,url
```

```text
Example invocation to the agent:
Use the GitHub Issues backlog triage and planning prompt and adapt it to:
- repository: [ORG/REPO]
- issues source: [PASTE gh issue list JSON]
- applied filter: assignee + component
- pending criteria: open without associated PR
- target component: [COMPONENT]
- target owner: [USER]
- target branch: main
- environment: QA
- documents to review: README, docs/, workflows, architecture, related issues
- specific output objective: prioritized matrix and phased attention plan
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Executive summary | Backlog overview and attention recommendation |
| Confirmed facts | Explicit data obtained from issues, branches, PRs and documentation |
| Findings | Detected patterns, groupings, gaps, overload or disorder |
| Assumptions | Inferences made because of incomplete data |
| Risks | Functional, technical, operational, security and concurrency risks |
| Issues matrix | Normalized and classified inventory |
| Categorization | View by component, owner, priority and attention state |
| Dependencies | Blocking, sequencing and recommended consolidations |
| Attention plan | Order, priorities, tasks, owners and deliverables |
| Final recommendations | Suggested decisions for execution and backlog governance |
