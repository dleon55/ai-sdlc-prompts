# 7.4 — Smoke tests

## Description

Prompt to define a smoke test plan that quickly validates the system remains operational after a change or deployment: authentication, critical flows, modules, minimal integrations and visible errors.

**When to use it:** immediately after a deployment or merge, for a quick health validation before complete tests.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Define a smoke test plan to quickly validate that the system remains operational after the change.

Include:
- login/authentication if applicable,
- main critical flow,
- module access,
- basic operations,
- minimal integrations,
- visible errors.
```

---

## Use with standard formula

```text
Use the smoke tests prompt and adapt it to:
- repository: [NAME OR URL]
- branch or deployed version: [REFERENCE]
- environment: [QA / STAGING / PROD]
- critical modules: [MODULES THAT MUST WORK]
- documents to review: documented critical flows, last stable version
- specific output objective: smoke checklist executable in less than 15 minutes
- depth level: low
```

---

## Expected output

| Step | Action | Expected result | Status |
|---|---|---|---|
