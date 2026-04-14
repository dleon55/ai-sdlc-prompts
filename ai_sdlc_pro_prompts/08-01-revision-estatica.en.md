# 8.1 — Static code review

## Description

Prompt to perform a static review of the code related to the change: quality, maintainability, security, complexity, error handling and consistency with project standards.

**When to use it:** after implementing changes, before opening a PR or merging.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Perform a static review of the code related to the change and evaluate quality, maintainability, security and consistency with project standards.

Review:
- structure,
- clarity,
- duplication,
- complexity,
- error handling,
- validations,
- logging,
- security,
- naming consistency,
- alignment with architecture.

Deliver:
1. critical findings
2. medium findings
3. minor observations
4. detected technical debt
5. punctual recommendations
```

---

## Use with standard formula

```text
Use the static review prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [BRANCH WITH CHANGES]
- files to review: [PATHS OF MODIFIED FILES]
- documents to review: project code standards, architecture
- specific output objective: findings report classified by criticality
- depth level: high
```

---

## Expected output

### Critical findings

| File | Line | Description | Risk | Recommended action |
|---|---|---|---|---|

### Medium findings

| File | Line | Description | Risk | Recommended action |
|---|---|---|---|---|

### Minor observations

| File | Description | Suggestion |
|---|---|---|

### Detected technical debt

| Item | Impact | Priority |
|---|---|---|
