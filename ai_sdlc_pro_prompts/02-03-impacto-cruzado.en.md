# 2.3 — Cross-impact analysis

## Description

Prompt to evaluate the impact of the change on all modules, processes, data, integrations, environments and pipelines of the system. Detects direct and indirect impacts and generates a severity matrix.

**When to use it:** after deep technical analysis (`02-02`) and before solution design (`04-01`).

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze the impact of the requested change on other modules, processes, data, integrations, environments and pipelines.

Activities:
1. Evaluate impact on:
   - frontend,
   - backend,
   - database,
   - integrations,
   - infrastructure,
   - CI/CD,
   - security,
   - monitoring,
   - documentation.
2. Detect direct and indirect impacts.
3. Evaluate affectation to other use cases.

Output:
- impact matrix,
- severity,
- affected component,
- impact type,
- risk,
- recommendation.
```

---

## Use with standard formula

```text
Use the cross-impact analysis prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [CURRENT BRANCH]
- environment: [DEV / QA / PROD]
- components: [INVOLVED COMPONENTS]
- documents to review: architecture, API contracts, DB schema
- specific output objective: cross-impact matrix with severity by component
- depth level: high
```

---

## Expected output

| Component | Impact type | Severity | Risk | Recommendation |
|---|---|---|---|---|
| frontend | | | | |
| backend | | | | |
| database | | | | |
| integrations | | | | |
| infrastructure | | | | |
| CI/CD | | | | |
| security | | | | |
| monitoring | | | | |
| documentation | | | | |
