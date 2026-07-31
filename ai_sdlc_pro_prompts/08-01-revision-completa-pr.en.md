# 8.1 — Complete PR Review: Quality, Compliance, and Integration

## Description

A single review prompt for a PR before merging: evaluates static code quality, requirement/issue compliance, integration risk with other active branches, and CI pipeline status in one pass. Replaces what used to be 4 separate prompts (static review, requirement compliance, branch integration, CI monitoring) — all four dimensions are read-only, evaluated at the same real moment of work (reviewing a PR before approving it), and splitting them into separate documents only added friction without gaining any traceability.

**When to use it:** after implementing changes and before merging any PR — the complete review step before merge, in a single prompt instead of several separate invocations.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — doesn't modify code or execute the merge, but the combined verdict determines whether a PR is ready to integrate; a missed finding in any of the 4 dimensions can let through a defect, an incomplete requirement, an integration conflict, or a broken pipeline |
| Required inputs | the PR's real diff, associated issue/requirement, approved design if any, test results, commit history and related active branches, local and GitHub Actions CI logs, project code standards |
| Allowed tools | reading code, diff, documentation, git history and state (`git log`, `git diff`, `git branch`), CI logs and PR checks — no running new tests, no editing files, no merge/rebase/cherry-pick/push, no re-running CI jobs |
| Permitted autonomy | A1 — Propose (the verdict and integration strategy are proposed; executing the merge, applying remediation, or resolving conflicts requires a separate execution prompt and human approval) |
| Stop criteria | if the full diff, the original requirement, or any of the four compliance inputs (requested/designed/implemented/tested) is missing, declare the evidence gap in that specific dimension instead of omitting it or assuming it's fine; if local state isn't synced with remote, sync (`git fetch`) before evaluating integration; if a CI check is pending or has no accessible logs, mark it "pending," don't assume it passed |
| Expected output | see `## Expected output` |
| Minimum evidence | every quality finding cites file and line; every acceptance criterion is marked met/partial/not met with the gap cited; every integration conflict cites file and branch; every CI failure cites job, step, and message |
| Recommended next prompt | `08-03-remediacion-maestro` if there are critical or medium quality findings to fix before merge; `09-04-promotion-checklist` once the verdict across all 4 dimensions is favorable, to plan the deployment across environments |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Evaluate in one pass whether this PR is ready to merge: code quality, requirement compliance, integration risk, and CI pipeline status.

Steps:
1. Sync local state with remote (git fetch) before evaluating anything — analysis on stale information invalidates all 4 dimensions.
2. QUALITY — Review the real diff against project standards: prioritize defects, vulnerabilities, regressions, and broken contracts over style preferences. Every finding cites file and line, affected behavior, justified severity, and concrete remediation. Consider agentic security (malicious instructions in content, permission escalation, exfiltration, unsafe tool use).
3. COMPLIANCE — Gather the four inputs (requested, designed, implemented, tested) and, for each acceptance criterion in the issue, assign a status (met / partial / not met) citing the specific gap. Distinguish "not implemented" from "not tested" — they're different gaps. Never mark "met" without traceable test evidence.
4. INTEGRATION — Identify related active branches (same module, same issue/epic) and compare each one's diff against the source branch to detect potential conflicts (same files, same functions, concurrent migrations). Evaluate the recommended strategy (merge / rebase / cherry-pick / controlled wait / phased integration) and document what could break.
5. CI — Review the local and remote pipeline status (lint, build, tests, quality gates, PR checks). Every failure cites the specific job, step, and error message; a pending check is marked "pending," never assumed to have passed.
6. Consolidate a single "ready to merge: yes / no / conditional" verdict, citing which dimension (if any) blocks it, and what conditions must be met before approving the integration (green CI, code review approval, no active branches with unverified changes, rollback plan).

Constraints:
- read-only across all 4 dimensions: don't apply edits, don't run auto-formatters, don't run new tests, don't merge/rebase/cherry-pick/push, don't re-run CI jobs — this prompt evaluates and recommends, it doesn't execute,
- don't mark an acceptance criterion "met" without test evidence, even if the code looks correct,
- don't report a quality finding without a verifiable file and line — without an exact location, reclassify it as an open question,
- if any of the four compliance inputs is missing, stop that specific dimension and report it as an evidence gap, without blocking the rest of the analysis if the other dimensions do have complete evidence,
- every reported integration conflict must cite the specific file/area and the branch it collides with — don't generalize "there may be conflicts" without concrete evidence,
- if local state isn't synced with remote or there are active branches from other agents with unverified changes, stop and request synchronization before recommending a definitive integration strategy.

Deliver:
1. single verdict: ready to merge (yes / no / conditional) + which dimension blocks it, if any,
2. quality: findings by severity + open questions + missing tests,
3. compliance: acceptance criteria matrix (requested / designed / implemented / tested / status / gap),
4. integration: related branches, potential conflicts, recommended strategy, risks, merge conditions,
5. CI: pipeline status, failures cited with job/step/message, pending checks.
```

---

## Use with standard formula

```text
Use the complete PR review prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [BRANCH WITH THE CHANGES]
- issue or requirement: [REFERENCE]
- target branch: [DEVELOP / MAIN / RELEASE]
- documents to review: original issue, approved design, code standards, active branches, CI logs
- specific output objective: single ready/not-ready-to-merge verdict with all 4 dimensions evaluated
- depth level: high
```

---

## Expected output

### Verdict

| Ready to merge | Blocking dimension | Pending conditions |
|---|---|---|
| Conditional | Compliance (partial) | Add the date-filter test case before merging; every other dimension is green |

### 1. Quality

| File | Line | Description | Risk | Recommended action |
|---|---|---|---|---|
| `build.py` | 250-260 | `parse_editorial_contract` indexes the field without validating the row exists | An incomplete contract crashes the build with an uncontrolled `KeyError` | Explicit validation or `.get()` with a default value |

### 2. Compliance

| Acceptance criterion | Requested | Designed | Implemented | Tested | Status | Gap |
|---|---|---|---|---|---|---|
| Export the date-range-filtered list to CSV | yes — issue #482 | yes — design section 3.2 | yes — endpoint accepts `from`/`to` | no — only an unfiltered test exists | partial | missing test case covering the date filter |

### 3. Integration

| Element | Detail |
|---|---|
| Related branches | `feature/payment-retry` (PR #482 in review, green CI) touches `PaymentService`, same module as this PR |
| Potential conflicts | `src/services/PaymentService.ts` — both branches modify `processPayment()` |
| Recommended strategy | controlled wait: let `feature/payment-retry` merge first, then rebase |
| Merge conditions | green CI, approved code review, `feature/payment-retry` merged before the rebase |

### 4. CI

| Job | Step | Status | Message |
|---|---|---|---|
| `build` | `pytest` | ✅ green | 142 passed |
| `e2e` | `test_browser_e2e.py` | 🟡 pending | check still queued, no log available |
