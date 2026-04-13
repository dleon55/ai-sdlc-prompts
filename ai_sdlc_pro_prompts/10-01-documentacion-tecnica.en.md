# 10.1 — Update technical documentation

## Description

Prompt to review and propose updates to the technical documentation affected by a change: README, docs, architecture, diagrams, contracts, use cases, deployment notes and troubleshooting.

**When to use it:** at the close of each change, before merging to the main branch.

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
