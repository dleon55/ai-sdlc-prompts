# 10.3 — Release or changelog documentation

## Description

Prompt to draft release notes or changelog of a change with technical and functional focus: summary, impacted modules, fixes, improvements, risks and deployment considerations.

**When to use it:** when preparing a release or closing a sprint to document delivered changes.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | low — a release communication document; the risk is reputational/operational if it omits breaking changes or deployment notes, it does not act on the system |
| Required inputs | version or tag, release branch, included issues or PRs, commits of the period |
| Allowed tools | read-only access (commit history, merged PRs, closed issues); does not publish the release or create the tag |
| Permitted autonomy | A1 — Propose: delivers the changelog ready to publish; the actual publication in GitHub Releases or CHANGELOG.md is a separate, explicit A3 action |
| Stop criteria | if it detects breaking changes without a clear migration note, it must stop and request that information before treating the changelog as complete |
| Expected output | see `## Expected output` |
| Minimum evidence | each changelog entry is traceable to a real commit or PR within the declared period |
| Recommended next prompt | `10-02-memoria-tecnica` if the change's audit record does not exist yet; `09-04-promotion-checklist` to validate the release is ready for promotion |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Draft the release notes or changelog of the change with technical and functional focus.

Steps:
1. Gather the commits and merged PRs within the declared period or version, filtering by the release branch.
2. Classify each entry as a fix, an improvement, an internal change (no user impact), or a breaking change; drop purely maintenance commits (formatting, minor dependency bumps) from the visible changelog unless they carry security impact.
3. Draft the executive summary first (2-4 sentences), aimed at someone reading the release with no prior technical context.
4. For each fix or improvement, describe the observable impact for the user or integrator (not just the commit's technical title) and link the PR or commit number.
5. Identify impacted modules, grouping by functional area, prioritizing ones that touch public contracts (API, CLI, data schema) over purely internal changes.
6. If you detect a change that breaks compatibility, document the explicit migration note (what the upgrader must do) before treating the changelog as complete; if that note doesn't exist, stop and request it.
7. Add deployment considerations: new variables, migrations to run, and deployment order if there are dependencies between services.

Constraints:
- every changelog entry must be traceable to a real commit or PR within the declared period; don't include changes outside that range,
- don't publish the changelog or create the tag — actual publication is a separate, explicit A3 action,
- if you detect breaking changes without a clear migration note, stop and request that information before delivering the changelog as complete,
- don't mix marketing language with the technical report: describe the real impact, without overselling benefits or hiding known risks.
```

---

## Use with standard formula

```text
Use the release/changelog prompt and adapt it to:
- repository: [NAME OR URL]
- version: [TAG OR VERSION]
- branch: [RELEASE BRANCH]
- included issues: [LIST OF ISSUES OR PRs]
- documents to review: commits of the period, merged PRs, closed issues
- specific output objective: changelog ready to publish in GitHub Releases or CHANGELOG.md
- depth level: medium
```

---

## Expected output

### Header

```
## [vX.X.X] - YYYY-MM-DD
```

### Changelog sections

| Section | Content |
|---|---|
| Summary | v2.3.0 introduces per-user rate limiting on the orders API to prevent abuse, fixes the intermittent timeout on `POST /payments`, and upgrades the authentication library for a medium-severity vulnerability |
| Fixes | `POST /payments` no longer times out under high concurrent load (PR #498); fixed tax calculation with combined discounts (PR #495) |
| Improvements (features) | New configurable per-user rate limiting on `POST /orders`, 100 req/min by default (PR #501) |
| Impacted modules | `orders-api`, `payments-service`, `auth-lib` (bump v3.4.1 → v3.4.2) |
| Risks | Users with integrations that legitimately burst > 100 req/min may receive 429s (mitigated by documenting the `Retry-After` header) |
| Deployment notes | Set `RATE_LIMIT_WINDOW_MS` in production before deployment; run migration `2026_07_08_add_rate_limit_table` before deploying `orders-api` |
| Compatibility | No breaking changes in this version; `auth-lib` v3.4.2 is backward compatible with v3.4.x |
