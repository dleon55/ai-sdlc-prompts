# 9.2 — Local and remote CI monitoring

## Description

Prompt to review the CI pipeline status locally and on GitHub and determine if changes are ready to be integrated: lint, build, tests, quality gates, artifacts and PR checks.

**When to use it:** before opening or approving a PR, before merging to any protected branch.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | low — read-only diagnosis of pipeline status, does not modify workflows, code, or re-run jobs |
| Required inputs | local CI logs and GitHub Actions logs, PR check status, files under `.github/workflows/` |
| Allowed tools | reading CI logs and PR checks — no re-running jobs, no modifying workflows |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if any PR check is pending or has no accessible logs, mark it as "pending" in the approval criterion instead of assuming it passed or failed |
| Expected output | see `## Expected output` |
| Minimum evidence | each reported failure must cite the job, the step, and the specific error message from the log |
| Recommended next prompt | `09-01-integracion-ramas` if the pipeline is green and integration with the target branch proceeds |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Review the CI pipeline status both locally and on GitHub and determine if the changes are ready to be integrated.

Validate:
- lint,
- build,
- tests,
- quality gates,
- workflows,
- artifacts,
- PR checks.

Constraints:
- this is read-only monitoring: don't re-run, cancel, or approve CI jobs, and don't modify workflow files as part of this analysis — any action on the pipeline requires explicit human approval outside this prompt,
- every reported failure must cite the exact job and step, along with the specific error message from the log — don't generalize "tests failed" without naming which ones,
- explicitly distinguish an intermittent failure (flaky test, infrastructure timeout, a downed external dependency) from a genuine regression caused by the change under review; if there isn't enough evidence to decide, mark it as "needs retry or further investigation" instead of classifying it as either,
- if a check remains pending or has no accessible logs, don't count it as passed or failed — report it as pending in the final approval criterion.

Deliver:
1. general status,
2. detected failures,
3. probable cause,
4. recommended action,
5. approval or rejection criterion.
```

---

## Use with standard formula

```text
Use the CI monitoring prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [PR OR INTEGRATION BRANCH]
- environment: [QA / STAGING / PROD]
- components: [MODIFIED COMPONENTS]
- documents to review: .github/workflows/, CI logs, PR checks
- specific output objective: pipeline status + approval criterion
- depth level: medium
```

---

## Expected output

| Validation | Status | Result | Probable cause | Action |
|---|---|---|---|---|
| lint | | | | |
| build | | | | |
| tests | ⚠️ Failed | 2 of 148 tests failed in `test_build_unit.py::test_missing_field` | Intermittent timeout reading `00-framework.md` on the CI runner (isolated failure, not reproducible locally) | Retry the job before blocking the PR; if it persists on a second attempt, investigate as a regression |
| quality gates | | | | |
| workflows | | | | |
| artifacts | | | | |
| PR checks | ✅ Approved | All required checks (`lint`, `build`, `tests`) are green | — | None — ready to merge once the item above is resolved |

**Approval criterion:** [APPROVED / REJECTED / PENDING]
