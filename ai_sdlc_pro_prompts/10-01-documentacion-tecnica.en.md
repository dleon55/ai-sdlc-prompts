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

Review and update:
- README,
- docs,
- architecture,
- diagrams,
- contracts,
- use cases,
- deployment notes,
- troubleshooting.

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
