# 7.4 — Smoke tests

## Description

Prompt to define a smoke test plan that quickly validates the system remains operational after a change or deployment: authentication, critical flows, modules, minimal integrations and visible errors.

**When to use it:** immediately after a deployment or merge, for a quick health validation before complete tests.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design — defines a smoke test checklist, does not execute it |
| Expected risk | low — the prompt only produces the checklist; executing the steps (potentially in PROD) is left to a human or to `07-10` |
| Required inputs | documented critical flows, reference to the deployed branch or version, target environment (QA/STAGING/PROD) |
| Allowed tools | read-only access to documentation of critical flows and the last stable version; does not run commands or access live systems |
| Permitted autonomy | A1 — Propose (delivers a prioritized checklist as an artifact, without executing it against the system) |
| Stop criteria | stop if no critical flows are identified or the target environment is undefined, since the checklist would lose its usefulness as a quick validation |
| Expected output | see `## Expected output` |
| Minimum evidence | the checklist must cover authentication, main critical flow, module access, minimal integrations, and absence of visible errors, each step marked critical or not and executable in under 15 minutes |
| Recommended next prompt | `07-10-implementacion-pruebas-humo` to automate execution of the checklist |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Define a smoke test plan to quickly validate that the system remains operational after the change.

Steps:
1. Identify the login/authentication flow if applicable: it is usually the first point of failure and, if broken, blocks verification of everything else.
2. Verify the system's main critical flow (the highest-use or highest-impact business path) end to end, without going deep into alternative paths.
3. Confirm access to each main module: that it loads without error, without validating its internal logic in detail — that belongs to full functional tests.
4. Run one representative basic operation per module, prioritizing those that read or write critical business data over purely informational ones.
5. Verify the minimal indispensable integrations (payment gateway, external authentication, queues, third-party services) only for response availability, not their edge cases.
6. Check that there are no visible errors in the UI, in startup logs, or in the browser console that would indicate a regression.
7. Mark each step as critical (blocks the release if it fails) or informational, and order them so the full checklist is executable in under 15 minutes.

Constraints:
- this does not replace complete functional, integration, or E2E tests — its only purpose is to detect whether the system is badly broken,
- each step must be verifiable in seconds or a few minutes; if a step requires more time or depth, it belongs to `07-02` or `07-03`, not to smoke testing,
- if the target environment is production, explicitly flag which steps are read-only and which could produce side effects (e.g., creating test records),
- don't invent critical flows or modules: if they aren't documented, request them before generating the checklist.

Deliver:
- prioritized smoke test checklist, executable in under 15 minutes.
```

---

## Use with standard formula

```text
Use the smoke tests prompt and adapt it to:
- repository: [NAME OR URL]
- branch or deployed version: [REFERENCE]
- environment: [QA / STAGING / PROD]
- critical modules: [MODULES THAT MUST WORK]
- documents to review: documented critical flows, last stable version
- specific output objective: smoke checklist executable in less than 15 minutes
- depth level: low
```

---

## Expected output

| Step | Action | Expected result | Critical | Status |
|---|---|---|---|---|
| 1 | Login / authentication | Access granted | Yes | |
| 2 | Access to main module | Loads without error | Yes | |
| 3 | Critical basic operation | Correct result | Yes | |
| 4 | Minimal integration | Responds without error | Yes | |
| 5 | No visible errors in UI | No critical alerts | Yes | |
