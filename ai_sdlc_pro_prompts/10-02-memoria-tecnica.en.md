# 10.2 — Technical memory of the change

## Description

Prompt to generate a clear and executive technical memory of the change made: context, problem, analysis, implemented solution, tests, risks, results and pending points.

**When to use it:** at the close of each issue or sprint, as a formal record of the work performed for audit and future reference.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | low — generates an audit/record document; does not act on the system, but as an input to formal audit, inaccuracies undermine traceability of the change |
| Required inputs | issue or requirement, integrated branch, environment, modified components, commits/PRs, approved design, executed test results |
| Allowed tools | read-only access (commits, PRs, approved design, test results); does not execute commands or modify the repository |
| Permitted autonomy | A1 — Propose: drafts the technical memory document; does not publish or archive it itself |
| Stop criteria | if test results are missing or the approved design is unavailable, it must flag that explicitly in the relevant section instead of inventing results |
| Expected output | see `## Expected output` |
| Minimum evidence | each section (root cause, executed tests, risks) is backed by a verifiable reference (commit, PR, or test result), not generic |
| Recommended next prompt | `10-03-release-changelog` if the change is grouped into a release; `11-03-deuda-tecnica` to record pending points as formal technical debt |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Generate a clear and executive technical memory of the change made.

Steps:
1. Context: summarize in 2-3 sentences the system's prior state and why the change was needed, citing the originating issue or requirement.
2. Problem or requirement: describe the concrete problem or business need without mixing it with the solution adopted.
3. Analysis: document the alternatives considered and why they were discarded, referencing the approved design if it exists.
4. Root cause (if applicable): if the change is a fix, identify the confirmed root cause and distinguish it from symptoms or hypothetical causes ruled out during analysis.
5. Implemented solution: describe exactly what was implemented in verifiable terms — not "the system was improved," but which logic, endpoint, or configuration changed.
6. Modified components: list the affected files, modules, or services, with references to the corresponding commits or PRs.
7. Executed tests: for each relevant test type (unit, integration, E2E, performance) state whether it ran, the result, and the reference to the artifact (pipeline run, report). If a relevant type was not executed, state that explicitly instead of omitting it.
8. Risks: residual risks that persist after the change, prioritized by severity, stating whether they have a mitigation plan or remain accepted without mitigation.
9. Results: the final observable state of the system after deployment (metrics, behavior validated in production or staging), not just the intent of the change.
10. Pending points: derived tasks, new technical debt, or necessary follow-ups, each with a suggested owner when possible.

Constraints:
- each section must be backed by a verifiable reference (commit, PR, test result, or pipeline run), not written generically,
- if test results are missing or the approved design is unavailable, flag that explicitly in the relevant section instead of inventing results,
- don't mix the problem with the solution in the context and problem sections — each answers a different question,
- explicitly distinguish between mitigated risks and accepted risks that remain unresolved.
```

---

## Use with standard formula

```text
Use the technical memory prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [INTEGRATED BRANCH]
- environment: [PROD / STAGING]
- components: [MODIFIED COMPONENTS]
- documents to review: commits, PRs, approved design, test results
- specific output objective: complete technical memory for audit
- depth level: high
```

---

## Expected output

| Section | Content |
|---|---|
| Context | The orders service (`orders-api`) had been receiving spikes of automated traffic since mid-June that degraded P95 latency across all endpoints (issue #482) |
| Problem / Requirement | Prevent a single client from saturating `POST /orders` without blocking legitimate traffic, while meeting a P95 < 300ms SLA |
| Analysis | Evaluated gateway-level rate limiting (Kong) vs. application-level; chose application-level because it allows per-authenticated-user limits, not just per-IP |
| Root cause | No per-user rate control on `POST /orders`; the gateway only limited by IP, which was insufficient against bots rotating IPs |
| Implemented solution | `rateLimiter` middleware in `src/middleware/rateLimiter.ts`, limit of 100 req/min per `userId`, window configurable via `RATE_LIMIT_WINDOW_MS` |
| Modified components | `src/middleware/rateLimiter.ts`, `src/routes/orders.ts`, `docs/api/orders.md` (PR #501) |
| Executed tests | Unit: 12/12 passing (PR #501, CI run #3892). Load: k6 confirmed P95 280ms at 300 sustained req/s. Checkout E2E: not re-run, pending |
| Risks | Accepted: users with multiple active tabs may hit the limit; mitigated with a clear error message and `Retry-After` header |
| Results | `POST /orders` P95 latency stable in production after 48h of monitoring; 0 saturation incidents reported |
| Pending points | Re-run the checkout E2E suite with the middleware active (ticket #503, no owner assigned yet) |
