# 2.7 — Whole-project requirements traceability matrix

## Description

Prompt to maintain a **living, aggregated traceability matrix** for all of a project's requirements: which business need originated each requirement, and whether it already has linked design, implementation, and test evidence. Complements `08-02-cumplimiento-requerimiento`, which validates compliance for **one** specific issue, not an aggregated view of the whole project.

**When to use it:** periodically during the execution of a project with multiple requirements already analyzed (`02-05`), to detect orphaned requirements (missing design, code, or test) or code with no formal requirement backing it, before the project is considered closed.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — an outdated or incomplete matrix gives a false sense of complete coverage when in reality there are requirements missing design/implementation/test, or functionality built with no formal backing; the prompt does not execute or modify anything by itself |
| Required inputs | list of the project's business requirements (or issues already analyzed with `02-05`), associated designs, related implementations/PRs, available test results |
| Allowed tools | reading existing issues, designs, code, and test results — no new tests executed and nothing modified |
| Permitted autonomy | A0 — Analyze (aggregate already-evidenceable traceability); A1 — Propose (flag and prioritize gaps) |
| Stop criteria | if a requirement cannot be linked to any design, code, or test evidence, do not mark it as "covered" — explicitly report it as orphaned |
| Expected output | see `## Expected output` |
| Minimum evidence | every requirement in the project appears exactly once in the matrix with its cited coverage status at each stage (requirement → design → implementation → test) |
| Recommended next prompt | `08-02-cumplimiento-requerimiento` to dig deeper into a specific requirement flagged as incomplete or orphaned |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Build and maintain the aggregated traceability matrix for all of the project's requirements: the link between each requirement and its design, implementation, and test, identifying orphans at any stage.

Inputs:
- project business requirements: [PASTE LIST OR REFERENCE TO 02-05]
- associated designs: [PASTE OR REFERENCE]
- related implementations/PRs: [PASTE OR REFERENCE]
- available test results: [PASTE OR REFERENCE, OR "not yet available"]

Activities:
1. REQUIREMENTS INVENTORY
   List all known business requirements of the project, with their identifier and a brief description.

2. DESIGN LINKAGE
   For each requirement, verify whether a design (`04-01` or another design artifact) explicitly covers it. Cite the concrete reference, don't assume coverage by similarity.

3. IMPLEMENTATION LINKAGE
   For each requirement, verify whether code or a PR implements it. Cite the concrete reference (commit, PR, file).

4. TEST LINKAGE
   For each requirement, verify whether real test evidence exists — absence of a test is a gap even if the code "looks correct".

5. ORPHAN IDENTIFICATION
   Explicitly flag each requirement missing a link at any stage (design, implementation, or test) — distinguish "not yet implemented" (expected in an ongoing project) from "orphaned with no traceability" (a real gap requiring attention).

6. ORPHAN CODE IDENTIFICATION
   Flag implemented functionality with no formal requirement linked to it — this is a signal of scope creep or a requirement that was never formally documented, and must be reported, not omitted.

Constraints:
- never mark a requirement as "covered" at a stage without a concrete cited reference (design, PR, or specific test result) — coverage with no evidence is reported as unverifiable,
- always distinguish "not yet implemented" (normal in an ongoing project, with an expected date if known) from "orphaned with no traceability" (a real gap requiring action),
- do not ignore or omit code or functionality with no formal requirement linked — report it explicitly instead of assuming it's documented elsewhere,
- if the project's business requirements list is incomplete or doesn't exist, stop and request it before building the matrix on assumptions.

Output:
0. JSON metadata block (keys: status, requirement_count, orphan_requirements_count, orphan_code_count, confidence_score [0.0 to 1.0]).
1. Complete traceability matrix: Requirement | Design | Implementation | Test | Status
2. Orphaned requirements, with the stage where traceability breaks.
3. Code or functionality with no formal requirement linked.
4. Prioritized recommendations to close the detected gaps.
```

---

## Usage with standard formula

```text
Use the requirements traceability matrix prompt and adapt it to:
- repository/project: [NAME OR URL]
- business requirements: [PASTE LIST OR REFERENCE TO 02-05]
- documents to review: designs, PRs/implementations, test results
- specific output objective: complete traceability matrix with orphans identified
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the coverage summary |
| Traceability matrix (1) | All requirements with their status at each stage, with cited references |
| Orphaned requirements (2) | List with the exact stage where traceability breaks |
| Orphan code (3) | Implemented functionality with no formal requirement linked |
| Recommendations (4) | Prioritized actions to close detected gaps |

### Example (excerpt)

```json
{
  "status": "matrix_with_orphans",
  "requirement_count": 24,
  "orphan_requirements_count": 3,
  "orphan_code_count": 1,
  "confidence_score": 0.74
}
```

| Requirement | Design | Implementation | Test | Status |
|---|---|---|---|---|
| BR-014 Export filtered report to CSV | `04-01` section 3.2 | PR #482 | No evidence of a test with the filter applied | Orphaned at test |
| BR-015 Email notification on ticket close | No formal design found | PR #501 (implemented) | Unit test `test_email_on_close` | Orphaned at design — implemented with no prior formal design |

| Section | Example content |
|---|---|
| Orphan code (3) | Endpoint `POST /reports/schedule` (scheduled report delivery) implemented in PR #495, with no business requirement linked in the backlog — possible scope creep or a verbal requirement that was never documented; needs the requirement backfilled or its removal justified |
