# 7.13 — Flaky test diagnosis and stabilization

## Description

Prompt to diagnose an automated test that fails intermittently (non-deterministically): reproduces the failure pattern across multiple runs, evaluates the most common causes (race condition, order dependency, non-deterministic timing, shared state, network dependency), identifies the most likely cause with evidence, and recommends stabilizing with a real fix, quarantining temporarily with follow-up, or removing the test.

**When to use it:** when an existing test fails intermittently in CI or locally with no apparent code changes, before deciding whether to ignore it, auto-retry it, or fix it at the root.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | diagnosis |
| Expected risk | medium — a poorly diagnosed flaky test placed in permanent quarantine can hide a real future regression; a "fix" that only masks the symptom without resolving the root cause (e.g. sleeps or blind retries) creates false confidence |
| Required inputs | test name/path, recent CI run history (pass/fail, timestamps), logs or stack traces from at least 2-3 failures, the test's code and the related code under test, whether it also fails locally or only in CI |
| Allowed tools | reading code, logs, and CI history; repeated execution of the test in an isolated environment (local or CI) to reproduce the failure pattern — no modification of the test until the root cause is identified |
| Permitted autonomy | A0 — Analyze (root-cause diagnosis); A1 — Propose (fix, quarantine, or removal); A2 — Execute controlled only to run the test repeatedly in an isolated environment for the purpose of reproducing the pattern, never to apply the fix without human review |
| Stop criteria | if the failure cannot be reproduced after the number of runs defined in the protocol, state "not reproduced" instead of guessing the cause; never recommend permanent quarantine without a follow-up ticket and review date |
| Expected output | see `## Expected output` |
| Minimum evidence | every candidate cause is backed by at least one reproduced run or an identifiable pattern in CI history (e.g. "fails more on the Linux runner than on macOS", "fails only when running after test X") |
| Recommended next prompt | `07-01`/`07-02`/`07-03` (depending on test type) if the test needs to be redesigned from scratch; `11-03-deuda-tecnica` if the flakiness pattern repeats across multiple tests and warrants a broader initiative |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Diagnose the root cause of an unstable (flaky) automated test and recommend an action: stabilize with a concrete fix, quarantine temporarily with follow-up, or remove the test if it no longer provides real detection value.

Inputs:
- test to diagnose: [TEST NAME/PATH]
- recent run history: [PASTE OR LINK TO CI HISTORY — pass/fail per run, with timestamps]
- failure logs/stack traces: [PASTE AT LEAST 2-3 FAILURE CAPTURES]
- test code: [PASTE OR PATH]
- related code under test: [PASTE OR PATH]
- environment context: [FAILS ONLY IN CI / ALSO FAILS LOCALLY / UNKNOWN]

Steps:
1. FAILURE PATTERN CLASSIFICATION
   From the CI history, characterize the pattern: does it fail at a stable percentage of runs (e.g. 1 in 10)? Only on a certain runner/OS? Only when run in parallel with other tests or in a certain order? Does it worsen under load (busy CI)? If the history lacks enough data to characterize the pattern, state so and request more runs before continuing.

2. CONTROLLED REPRODUCTION
   Design a reproduction protocol: how many repeated runs are needed for reasonable statistical confidence given the observed failure rate (e.g. if it fails 1 in 10, run it 20-30 times to confirm), in which environment (local/isolated CI), and whether it should run alone or alongside the full suite (to detect order dependency or shared state).

3. COMMON CAUSES CHECKLIST
   Evaluate each category with evidence from the code and logs, without ruling any out unreviewed:
   a) Timing/async: insufficient fixed waits, race conditions between async operations, tight timeouts.
   b) Order/isolation: the test depends on state left by another test (global variables, uncleaned database, un-reset singleton).
   c) Network/external dependencies: unmocked calls to external or third-party services, variable DNS or latency.
   d) Non-deterministic data: use of real dates/times, randomly generated IDs without a fixed seed, unguaranteed iteration order of data structures.
   e) Shared resources: ports, temp files, or locks shared between tests running in parallel.
   f) Runner environment: resource differences (CPU/memory) between CI runners that expose race conditions invisible locally.

4. MOST LIKELY CAUSE IDENTIFICATION
   Based on the failure pattern (step 1) and the checklist (step 3), identify the most likely cause with its supporting evidence. If more than one category is plausible, state so and prioritize by which has the most direct evidence, not by which is easiest to fix.

5. ACTION RECOMMENDATION
   - If the root cause is clear and fixable: propose the concrete fix (avoid "add a sleep" or "increase the timeout" as a final solution unless it is the actual fix for a documented race condition, not a cosmetic patch).
   - If the cause cannot be confirmed with available evidence but the test blocks CI: recommend temporary quarantine (mark as skip/quarantine) with a follow-up ticket and review date — never quarantine without a date or ticket.
   - If the test no longer provides real detection value (tests an obsolete path, duplicates coverage of another stable test): recommend removing it, justifying why this is not a coverage loss.

Constraints:
- do not apply or recommend a fix that only masks the symptom (arbitrarily increasing timeouts, adding unlimited retries, adding sleeps unrelated to an identified race condition) as a final solution — if there is no confirmed root cause, state so and recommend quarantine instead of a cosmetic patch,
- never recommend permanent quarantine without an explicit follow-up ticket and review date — a quarantined test with no return plan will silently stop catching real regressions,
- do not propose changes to production code to "fix" the flakiness if the cause is in the test itself (isolation, order) and not in the system's actual behavior,
- every candidate cause must be backed by at least one reproduced run or an identifiable pattern in the history — not by intuition about what "usually" causes flakiness,
- if you cannot reproduce the failure after the number of runs defined in the protocol, state it as "not reproduced" and do not invent a cause to close the diagnosis.

Output:
0. JSON metadata block (keys: status, failure_pattern, root_cause_category, confidence_score [0.0 to 1.0]).
1. Characterized failure pattern (frequency, associated conditions).
2. Reproduction protocol applied and result.
3. Common-causes checklist evaluation, by category, with evidence.
4. Most likely root cause, with supporting evidence.
5. Action recommendation (fix / quarantine with ticket and date / removal), with justification.
```

---

## Use with standard formula

```text
Use the flaky test diagnosis prompt and adapt it to:
- repository: [NAME OR URL]
- test to diagnose: [TEST NAME/PATH]
- run history: [LINK TO CI HISTORY]
- failure logs: [PASTE AT LEAST 2-3 CAPTURES]
- environment: [FAILS ONLY IN CI / ALSO LOCALLY]
- documents to review: test code, code under test, CI history
- specific output objective: confirmed root cause and action recommendation
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with diagnosis metadata |
| Failure pattern (1) | Observed frequency and conditions associated with the failure |
| Reproduction protocol (2) | Runs executed, environment used, result obtained |
| Causes checklist (3) | Evaluation of each common category with cited evidence |
| Root cause (4) | Most likely cause with its supporting evidence |
| Recommendation (5) | Concrete fix, quarantine with ticket/date, or justified removal |

### Example (excerpt)

```json
{
  "status": "cause_confirmed",
  "failure_pattern": "fails ~1 in 8 runs, only when run after test_create_user",
  "root_cause_category": "order/isolation",
  "confidence_score": 0.85
}
```

| Section | Example content |
|---|---|
| Root cause (4) | `test_login_flow` depends on a user created by `test_create_user` in the same test database without an isolated transaction; when the execution order changes (CI parallelization), the user does not yet exist — confirmed by reproducing the failure 6/30 runs when forcing reverse order |
| Recommendation (5) | Fix: create the test user within `test_login_flow` itself (fixture with isolated setup/teardown) instead of depending on another test; quarantine is not recommended because the cause is already confirmed and the fix is low-risk |
