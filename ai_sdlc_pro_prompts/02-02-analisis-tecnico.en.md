# 2.2 — Deep technical analysis of existing code

## Description

Prompt to analyze how the existing code really works today: end-to-end flow, couplings, technical debt, missing validations and regression risks.

**When to use it:** after functional analysis (`02-01`) and before cross-impact analysis (`02-03`) and solution design (`04-01`).

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze the existing code related to the requirement or incident and explain how it really works today.

Activities:
1. Locate files, classes, functions, endpoints, services, queries, tables and UI components involved.
2. Describe the current end-to-end flow.
3. Identify:
   - couplings,
   - dependencies,
   - technical debt,
   - missing validations,
   - regression risks,
   - design problems.
4. Indicate exactly which files and modules are involved.

Output format:
1. Current flow
2. Affected components
3. Relevant files
4. Technical findings
5. Modification risks
```

---

## Use with standard formula

```text
Use the deep technical analysis prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [CURRENT BRANCH]
- environment: [DEV / QA / PROD]
- components: [INVOLVED COMPONENTS]
- documents to review: source code, DB schema, API contracts
- specific output objective: documented current flow with technical findings
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Current flow | Step-by-step description of real behavior |
| Affected components | List of services, modules and tables |
| Relevant files | Exact paths in the repository |
| Technical findings | Debt, couplings, detected risks |
| Modification risks | What can break when changing |
