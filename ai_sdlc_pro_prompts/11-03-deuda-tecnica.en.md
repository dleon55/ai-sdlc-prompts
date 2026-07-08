# 11.3 — Technical debt and continuous improvement

## Description

Prompt to identify the technical debt of the repository and generate a prioritized improvement backlog classified by architecture, code, tests, documentation, security, CI/CD, observability, data and performance.

**When to use it:** at the close of a sprint, in periodic technical reviews, or when planning structural project improvements.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | low — generates an inventory and prioritized backlog; does not modify code or systems |
| Required inputs | main branch, components or modules to analyze, access to source code, tests, CI/CD configuration, architecture and documentation |
| Allowed tools | read-only access to the repository (code, tests, CI/CD configuration, documentation) |
| Permitted autonomy | A0 — Analyze: inventory and recommendations, without applying changes |
| Stop criteria | if it cannot access an area declared as "to analyze" (nonexistent module or outside the repo), it must flag the omission instead of completing the matrix with assumptions |
| Expected output | see `## Expected output` |
| Minimum evidence | each matrix item references a real file, module, or configuration in the repository, with priority, impact, and effort justified |
| Recommended next prompt | `05-01-plan-implementacion` to plan the resolution of prioritized items; `11-06-gestion-parches-actualizaciones` if the identified debt is outdated dependencies |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Identify technical debt in the repository and propose a prioritized backlog of improvements.

Steps:
1. Go through architecture: identify tight coupling, modules that should be split apart, and design decisions that no longer reflect how the system actually grew.
2. Go through code: identify duplication, high-complexity functions or classes, dead code, and violations of the conventions the repository itself already establishes.
3. Go through tests: identify insufficient coverage in critical modules, flaky tests, and missing integration or E2E tests where the component's risk warrants them.
4. Go through documentation: identify docs that are out of sync with the current code, missing architecture decision records (ADRs), and READMEs that no longer match real behavior.
5. Go through security: identify narrow-scope insecure practices worth tracking in the backlog (missing validation, outdated dependencies) without substituting for a full audit (`11-02-hardening-seguridad`).
6. Go through CI/CD: identify slow pipelines, manual steps that could be automated, and missing quality gates (lint, tests, minimum coverage) before merge.
7. Go through observability: identify missing metrics, logs, or traces on critical paths, or alerts that are poorly calibrated (too noisy or silent during real failures).
8. Go through data: identify schemas without versioned migrations, missing indexes on frequent queries, or inconsistencies between the data model and how it's actually used in code.
9. Go through performance: identify known bottlenecks, N+1 queries, synchronous operations that should be async, or missing caching on high-traffic paths.
10. For each item found, estimate impact (the cost of leaving it unresolved) and effort (the work needed to fix it), and prioritize first what combines high impact with low or medium effort.

Constraints:
- every backlog item must reference a real file, module, or configuration in the repository — don't generalize with phrases like "improve the architecture" without concrete evidence,
- don't propose or apply code changes: this is an inventory and prioritization phase, not implementation,
- if an area declared for analysis isn't accessible (nonexistent module or outside the repo), flag the omission explicitly instead of completing the matrix with assumptions,
- don't duplicate as a backlog item a finding that belongs to a full security audit — reference `11-02-hardening-seguridad` if the finding is of that nature.

Deliver:
- technical debt matrix,
- priority,
- impact,
- estimated effort,
- attention recommendation.
```

---

## Use with standard formula

```text
Use the technical debt prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [MAIN BRANCH]
- components: [MODULES OR AREAS TO ANALYZE]
- documents to review: source code, tests, CI/CD, architecture, docs
- specific output objective: prioritized technical debt backlog with estimated effort
- depth level: high
```

---

## Expected output

| Item | Category | Description | Priority | Impact | Effort | Recommendation |
|---|---|---|---|---|---|---|
| Email validation duplicated across 4 modules | code | email format validation is reimplemented in `auth/register.js`, `auth/reset.js`, `admin/invite.js`, and `api/webhook.js`, with slightly different rules | high | high — the inconsistency already caused a valid email to be rejected at registration (issue #310) | low (2-3h) | extract into a single `isValidEmail()` utility function and replace all four usages |
| No integration tests for the payment flow | tests | the `billing/` module only has unit tests mocking the gateway; there's no test that verifies the full flow against the provider's sandbox | high | high — a change in the integration could break payments in production without any test catching it | medium (1-2 days) | add an integration suite against the payment sandbox, run in CI before every release |
