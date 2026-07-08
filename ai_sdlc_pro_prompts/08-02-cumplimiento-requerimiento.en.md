# 8.2 — Requirement compliance review

## Description

Prompt to validate if the implementation really complies with the issue, requirement, use case and acceptance criteria. Compares what was requested, what was designed, what was implemented and what was tested.

**When to use it:** before closing an issue or opening a PR for merge, as a quality closure step.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | validation |
| Expected risk | medium — the verdict determines whether an issue can be closed; a false "compliant" can close incomplete work and a false "non-compliant" blocks unnecessarily |
| Required inputs | original issue or requirement, approved design, implemented code, test results |
| Allowed tools | reading the issue, design, code and existing test results — no new test execution or code modification |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if any of the four inputs to compare is missing (requested, designed, implemented or tested), stop and report it as an evidence gap before issuing a compliance verdict |
| Expected output | see `## Expected output` |
| Minimum evidence | each acceptance criterion must be marked as fully met, partial or not met, with the specific gap cited in the matrix |
| Recommended next prompt | `09-01-integracion-ramas` if compliance is total and the change is ready to integrate |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Validate if the implementation really complies with the issue, requirement, use case and acceptance criteria.

Steps:
1. Gather the four inputs to compare: original issue or requirement, approved design, implemented code, and test results; if any is missing, stop and report it as an evidence gap before continuing.
2. Compare what was requested against what was designed: verify the approved design literally covers each acceptance criterion in the issue, and flag any case the design left out.
3. Compare what was designed against what was implemented: verify each design decision was translated into real code, not into a simplified subset or an undocumented shortcut.
4. Compare what was implemented against what was tested: verify there is test evidence for each acceptance criterion, not just the happy path — a missing test is a gap even if the code "looks correct."
5. For each acceptance criterion, assign a status (fully met / partial / not met) citing the specific gap that supports it; never mark "fully met" without evidence traceable across the four inputs.
6. Prioritize the gaps by risk: a gap in a critical business or security criterion outweighs a cosmetic or naming gap.

Constraints:
- don't mark a criterion as "fully met" if there's no test evidence backing it, even if the code looks correct at a glance,
- don't run new tests or modify code — this review is read-only over existing evidence,
- if any of the four inputs (requested, designed, implemented, tested) is missing, stop the analysis and report it as an evidence gap instead of assuming compliance,
- explicitly distinguish "not implemented" from "not tested" — they are different gaps requiring different actions.

Deliver:
- total/partial/non compliance,
- detected differences,
- risks for non-compliance,
- required actions.
```

---

## Use with standard formula

```text
Use the requirement compliance prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [BRANCH WITH CHANGES]
- documents to review: original issue, approved design, implemented code, test results
- specific output objective: compliance matrix with gaps and required actions
- depth level: high
```

---

## Expected output

| Acceptance criteria | Requested | Designed | Implemented | Tested | Status | Gap |
|---|---|---|---|---|---|---|
| User can export the filtered list by date range to CSV | yes — issue #482 explicitly requests it | yes — section 3.2 of the approved design | yes — `GET /reports/export` endpoint accepts `from`/`to` | no — only an export-without-filter test exists | partial | missing test case covering the date filter |
| Export of 10k records must complete in under 5s (NFR) | yes — NFR listed in the issue | no — the design defines no pagination or streaming strategy | not verifiable without a reference design | no | not met | the performance requirement was never translated into design or a test |

### Compliance result

| Item | Status | Differences | Risk | Required action |
|---|---|---|---|---|
| Date filter without automated test | partial | the unit test covers export but not the date parameter | silent bug if the filter breaks in a future refactor | add a test case with a date range before closing the issue |
| Performance NFR not designed or tested | not met | the issue requires <5s for 10k records; there's no design or load-test evidence | large exports could time out in production | define a pagination/streaming strategy and run `07-06-pruebas-performance-carga` before merge |
