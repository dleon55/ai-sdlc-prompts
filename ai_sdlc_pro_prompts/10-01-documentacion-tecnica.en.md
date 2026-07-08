# 10.1 — Update technical documentation

## Description

Prompt to review and propose updates to the technical documentation affected by a change: README, docs, architecture, diagrams, contracts, use cases, deployment notes and troubleshooting.

**When to use it:** at the close of each change, before merging to the main branch.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | low — proposes documentation content, does not modify code or running systems; the real risk is stale or misleading documentation if left unreviewed |
| Required inputs | reference issue or requirement, integrated branch, modified components, existing documents to review (README, docs/, architecture, API contracts) |
| Allowed tools | read-only access to the repository (code and existing documentation); does not apply changes directly to documents, only delivers proposed content |
| Permitted autonomy | A1 — Propose: delivers the list of documents to update with proposed content, without applying the change |
| Stop criteria | if the actual change or modified components are unclear, it must request that information instead of proposing invented content |
| Expected output | see `## Expected output` |
| Minimum evidence | each proposed document references a real path existing in the repository and a reason for change tied to the declared issue or branch |
| Recommended next prompt | `10-02-memoria-tecnica` to consolidate the change's audit record; `10-03-release-changelog` if the change is grouped into a release |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Update or propose update of the technical documentation affected by the change.

Steps:
1. Identify the existing repository documents related to the modified components: README, docs/, architecture diagrams, API contracts, use cases, deployment notes, and troubleshooting.
2. For each document, determine whether the change makes it stale (content that is no longer true), incomplete (missing coverage of the new behavior), or whether it calls for a new document that doesn't exist yet.
3. Prioritize: update the README and API contracts first (they affect anyone integrating with or using the system) before internal troubleshooting notes or secondary diagrams.
4. Draft the proposed content in the same format and level of detail as the original document, citing the exact section to modify (heading or reference line) instead of rewriting the whole file.
5. If the change introduces a new deployment step (environment variable, migration, feature flag), add an explicit deployment note even if no prior section existed for it.
6. Flag any document that becomes inconsistent with the code but that you cannot update due to missing information, instead of inventing content.

Constraints:
- don't apply the changes directly to the files, only deliver the proposed content,
- don't invent document paths that don't exist in the repository; if the document doesn't exist but should, mark it explicitly as "new document to create",
- if the actual change or modified components are unclear, stop and request that information instead of proposing invented content,
- each proposed document must reference a real existing path in the repository (or be marked as new) and a reason for change tied to the declared issue or branch.

Deliver:
- documents to update,
- proposed content,
- reason for the change.
```

---

## Use with standard formula

```text
Use the technical documentation update prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [INTEGRATED BRANCH]
- components: [MODIFIED COMPONENTS]
- documents to review: README, docs/, architecture, API contracts
- specific output objective: list of documents to update with proposed content
- depth level: medium
```

---

## Expected output

| Document | Path | Reason for change | Proposed content |
|---|---|---|---|
| README — "Configuration" section | `README.md` | Added the `RATE_LIMIT_WINDOW_MS` environment variable required by the new rate limiter (issue #482) | Add a row to the environment variables table: `RATE_LIMIT_WINDOW_MS` — window in ms for rate limiting, default `60000` |
| API contract — POST /orders endpoint | `docs/api/orders.md` | The endpoint now returns 429 when the rate limit is exceeded (issue #482) | Add `429 Too Many Requests` response code with an example error payload and `Retry-After` header |
| Deployment notes | `docs/deployment.md` | New mandatory environment variable in production before deployment (issue #482) | Add step "3. Set `RATE_LIMIT_WINDOW_MS` in the environment; without it the service uses the 60s default" |
