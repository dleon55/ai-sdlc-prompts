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

Include:
- change summary,
- impacted modules,
- fixes,
- improvements,
- risks,
- deployment considerations,
- compatibility notes.
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
| Summary | Executive description of the release |
| Fixes | Bugs and defects corrected |
| Improvements (features) | New or improved functionalities |
| Impacted modules | List of modules with changes |
| Risks | Known risks in this version |
| Deployment notes | Special steps, migrations, new variables |
| Compatibility | Breaking changes |
