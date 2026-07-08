# 7.5 — Browser automation with Google Antigravity

## Description

Prompt to design and document a browser test automation strategy using Google Antigravity: scenarios, navigation, selectors, test data, visual validations and fragile points in the flow.

**When to use it:** to automate E2E or regression tests of critical flows impacted by the change. Use this prompt instead of `07-03`+`07-09` when the automation will run through Google Antigravity's browser agent (autonomous verification with captures/video) rather than a traditional E2E scripting framework.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design and document a browser test automation strategy using Google Antigravity to validate the impacted flows.

Include:
- scenario,
- navigation,
- expected selectors,
- test data,
- visual and functional validations,
- captures or expected evidence,
- possible fragile points in the flow.
```

---

## Use with standard formula

```text
Use the Antigravity automation prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- flows to automate: [CRITICAL FLOWS TO COVER]
- environment: [QA / STAGING]
- base URL: [ENVIRONMENT URL]
- documents to review: use cases, E2E plan, UI design
- specific output objective: automation strategy with steps, selectors and validations
- depth level: high
```

---

## Expected output

| Scenario | Navigation | Selectors | Test data | Validations | Evidence | Fragile points |
|---|---|---|---|---|---|---|
