# 4.1 — Functional and technical solution design

## Description

Prompt to design the complete solution before implementing: objective, scope, assumptions, restrictions, changes by component, risks, dependencies, validation strategy and rollback.

**When to use it:** once functional, technical and impact analysis is complete, before planning or executing any change.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | medium — the resulting design directly guides implementation; an incomplete design regarding risks or rollback strategy can lead to an unsafe implementation or one without a reversal plan, although this prompt does not execute changes |
| Required inputs | completed functional, technical, and cross-impact analysis (`02-01`, `02-02`, `02-03`), existing architecture and contracts |
| Allowed tools | reading of code, architecture, and documentation — no execution or changes; the output is a design document, not code |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if there is no viable rollback strategy for a critical component, state it as an open risk in the design instead of omitting it |
| Expected output | see `## Expected output` |
| Minimum evidence | every proposed change by component must be linked to a risk and its mitigation, and to cited findings from the prior analysis |
| Recommended next prompt | `05-01-plan-implementacion`; in parallel, `04-02-diagramas-mermaid` if the design requires architecture or flow diagrams before continuing |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design a complete, functional and technical solution for the analyzed requirement or incident.

Steps:
1. Define the solution objective: what problem it solves, for whom, and what observable result confirms it is resolved — without a verifiable objective there is no way to validate the design afterward.
2. Define the scope: what is explicitly in and what is explicitly out, to keep implementation from expanding without control or leaving gaps uncovered.
3. Document the assumptions the design relies on (available data, third-party behavior, existing infrastructure); if an assumption turns out to be false, the design must be declared invalid rather than silently adjusted during implementation.
4. Document the technical, business, time, or compatibility restrictions that limit the design options.
5. List the impacted use cases and how their behavior changes, citing the findings from the functional analysis (`02-01`) that support them.
6. List the new or modified business rules, citing the corresponding technical and cross-impact analysis (`02-02`/`02-03`).
7. Detail the changes required by component: what changes, why that component is the right point of intervention, and which existing contracts (APIs, schemas, file formats) are affected.
8. Identify the design's risks and, for each one, a concrete mitigation — prioritize risks on critical components or without a clear rollback strategy over minor or cosmetic risks.
9. List dependencies between components and with external systems, flagging which ones block the implementation order.
10. Define the validation strategy: how it will be confirmed, with concrete evidence, that the solution meets the objective before considering it done.
11. Define the rollback strategy for each critical component; if no viable strategy exists, state it as an open risk in the design instead of omitting it.

Constraints:
- this prompt produces only a design document: do not propose commands to run or modify code, configuration, or infrastructure,
- every proposed change by component must be explicitly linked to a risk, its mitigation, and the finding from the prior analysis (02-01/02-02/02-03) that justifies it — do not include changes without that traceability,
- if no viable rollback strategy exists for a critical component, state it as an open risk instead of inventing one or omitting it,
- if the prior functional, technical, or cross-impact analysis is unavailable or incomplete, stop and request it before designing — do not fill those gaps with assumptions,
- if a design decision contradicts existing architecture or contracts, flag it explicitly as a deviation to validate, not present it as a settled fact.

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

### Applied example: automated ES/EN parity check in the build

**Affected components**

| Component | Change type | Description |
|---|---|---|
| `build.py` | Modification | Add a `check_i18n_parity()` step that compares the header structure (`##`) of each `.md` file against its `.en.md` counterpart before generating `index.html` |
| `tests/test_i18n.py` | Modification | Add test cases for the new section-parity validator |

**Risks and mitigations**

| Risk | Mitigation |
|---|---|
| False positives from minor formatting differences (whitespace, line breaks) between the `.md` and its `.en.md` | Normalize whitespace before comparing header structure |
| The validator blocks the build on legitimate PRs that translate a file incrementally | Allow an explicit, documented exception while the PR is tagged as translation-in-progress |
