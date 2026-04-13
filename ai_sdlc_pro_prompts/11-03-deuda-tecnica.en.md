# 11.3 — Technical debt and continuous improvement

## Description

Prompt to identify the technical debt of the repository and generate a prioritized improvement backlog classified by architecture, code, tests, documentation, security, CI/CD, observability, data and performance.

**When to use it:** at the close of a sprint, in periodic technical reviews, or when planning structural project improvements.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Identify technical debt in the repository and propose a prioritized backlog of improvements.

Classify by:
- architecture,
- code,
- tests,
- documentation,
- security,
- CI/CD,
- observability,
- data,
- performance.

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
