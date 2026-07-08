# 7.5 — Browser automation with Google Antigravity

## Description

Prompt to design and document a browser test automation strategy using Google Antigravity: scenarios, navigation, selectors, test data, visual validations and fragile points in the flow.

**When to use it:** to automate E2E or regression tests of critical flows impacted by the change. Use this prompt instead of `07-03`+`07-09` when the automation will run through Google Antigravity's browser agent (autonomous verification with captures/video) rather than a traditional E2E scripting framework.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design/documentation — produces a browser automation strategy, does not execute it directly |
| Expected risk | medium — although the prompt only documents the strategy, it is handed as-is to Google Antigravity's browser agent for autonomous execution against QA/staging, without an intermediate code review as in `07-03`+`07-09` |
| Required inputs | use cases or critical flows to automate, prior E2E plan if it exists, UI design, base URL of the QA/STAGING environment |
| Allowed tools | reading documentation and UI design; no browser access or execution — the actual run happens outside this prompt, performed by Google Antigravity's agent |
| Permitted autonomy | A1 — Propose (delivers the strategy as an artifact; autonomous execution by Google Antigravity is a later external step that requires the environment and test credentials to already be authorized) |
| Stop criteria | stop if the target environment is not QA/STAGING (never automate directly against production); stop if stable selectors or test data are missing, since that would produce fragile automation |
| Expected output | see `## Expected output` |
| Minimum evidence | each scenario must list navigation, key selector, test data, expected validation, evidence (capture/video), and identified fragile point |
| Recommended next prompt | none in the library — the strategy is handed directly to Google Antigravity's browser agent for autonomous execution (alternative to `07-03`+`07-09`) |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design and document a browser test automation strategy using Google Antigravity to validate the impacted flows.

Steps:
1. Identify the scenario and the critical flow to automate, and confirm the target environment is QA or STAGING (never production).
2. Define step-by-step navigation: entry URL, clicks, forms, and expected screen transitions.
3. Identify stable selectors for each key element (prefer `data-testid` or semantic attributes over CSS classes or DOM position, which are fragile to style changes).
4. Define the test data to use — only datasets marked as "test data," never real data.
5. Specify the expected visual and functional validations at each step, and what evidence (screenshot, video) must be generated as proof of execution.
6. Identify fragile points in the flow: dynamic elements, animations, asynchronously loaded content, or selectors likely to change frequently.

Constraints:
- never run automation against production,
- use environment variables exclusively for test credentials, never hardcode them,
- if stable selectors or defined test data are missing, stop and flag it — automating over fragile selectors produces recurring false negatives.

Deliver:
- automation strategy with scenarios, selectors, and validations,
- list of identified fragile points and suggested mitigation.
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
| Copy prompt to clipboard | Home → search prompt → click copy button | `[data-testid="copy-btn"]` | section 07 prompt (test data) | copied text matches the displayed prompt and a visual confirmation appears | before/after click screenshot + flow video | visual confirmation is a temporary toast — verify before it disappears |
