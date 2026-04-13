# 10.3 — Release or changelog documentation

## Description

Prompt to draft release notes or changelog of a change with technical and functional focus: summary, impacted modules, fixes, improvements, risks and deployment considerations.

**When to use it:** when preparing a release or closing a sprint to document delivered changes.

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
