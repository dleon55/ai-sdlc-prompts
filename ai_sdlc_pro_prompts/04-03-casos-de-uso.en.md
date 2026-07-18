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
Formally document the use cases related to the analyzed requirement or module, based on the prior functional analysis (`02-01`).

Inputs:
- prior functional analysis: [PASTE OR REFERENCE TO 02-01]
- existing use-case documentation: [REFERENCE OR "none"]
- target module or functionality: [MODULE]

Steps:
1. Review the cited functional analysis and any existing use-case documentation to identify what behavior is already defined and what is missing.
2. For each use case, document: name, objective, actors, trigger, preconditions, main flow, alternate flows, postconditions, business rules, acceptance criteria, and related technical components.
3. The main flow must reflect the complete happy path; alternate flows must cover at least the exceptions and variations already mentioned in the functional analysis.
4. Verify that every acceptance criterion is objectively verifiable (observable in the system), not a vague aspiration.
5. If business rules, postconditions, or verifiable acceptance criteria are missing from the cited functional analysis for any use case, do not invent them.

Constraints:
- do not fill a field (postconditions, business rules, acceptance criteria) by inventing plausible content when the cited functional analysis does not specify it — mark that use case explicitly as "pending functional validation" instead,
- every use case must include at least one alternate flow; if the functional analysis mentions no exceptions, flag it as an empty gap to validate instead of omitting the section,
- do not propose architecture or implementation changes in this prompt — the goal is to formalize already-analyzed behavior, not to design or resolve it,
- cite the functional analysis or existing documentation as the source for every non-obvious business rule or precondition; do not present them as if self-evident.

Output:
- see `## Structure of each use case`
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
