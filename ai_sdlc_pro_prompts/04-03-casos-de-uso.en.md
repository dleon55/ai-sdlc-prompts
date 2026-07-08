# 4.3 — Use case design

## Description

Prompt to formally document the use cases of the analyzed requirement or module: actors, triggers, main and alternate flows, business rules and acceptance criteria.

**When to use it:** during the design phase, to formalize the expected system behavior before implementing.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | low — it formalizes already-analyzed behavior into documentation without executing changes; the risk is that incomplete use cases (alternate flows, acceptance criteria) create ambiguity for subsequent implementation and testing |
| Required inputs | prior functional analysis (`02-01`), existing use-case documentation, target module or functionality |
| Allowed tools | reading of documentation and related code — no execution or changes |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if business rules, postconditions, or verifiable acceptance criteria are missing for a flow, mark it as pending functional validation instead of inventing them |
| Expected output | see `## Structure of each use case` |
| Minimum evidence | every use case must include a main flow, at least one alternate flow, and acceptance criteria verifiable against the cited functional analysis |
| Recommended next prompt | `04-04-adr-decisiones-arquitectura` if architecture decisions derived from the use cases are pending; `05-01-plan-implementacion` if the design is already complete |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Formally document the use cases related to the analyzed requirement or module.

For each use case include:
- name,
- objective,
- actors,
- trigger,
- preconditions,
- main flow,
- alternate flows,
- postconditions,
- business rules,
- acceptance criteria,
- related technical components.
```

---

## Use with standard formula

```text
Use the use case design prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- module: [MODULE OR FUNCTIONALITY]
- components: [INVOLVED COMPONENTS]
- documents to review: functional analysis, existing UC documentation
- specific output objective: formal use cases ready for review and validation
- depth level: high
```

---

## Structure of each use case

| Field | Content |
|---|---|
| Name | Use case name |
| Objective | What this use case achieves |
| Actors | Who executes or participates |
| Trigger | What event or action initiates it |
| Preconditions | What must be true before executing |
| Main flow | Sequence of steps for happy path |
| Alternate flows | Variations and exceptions |
| Postconditions | System state at the end |
| Business rules | Applicable restrictions and validations |
| Acceptance criteria | How to verify it is correctly implemented |
| Technical components | Involved modules, services and tables |
