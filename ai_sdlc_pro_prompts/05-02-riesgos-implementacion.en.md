# 5.2 — Implementation risk and impact analysis

## Description

Prompt to identify and classify implementation risks: functional, technical, data, security, operations, agent concurrency, integration and deployment. Generates a risk matrix with probability, impact and mitigation plan.

**When to use it:** in parallel with the implementation plan (`05-01`), before executing any change.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — does not execute changes, but an omitted or misclassified risk can reach the execution phase (`06-01`) without mitigation |
| Required inputs | approved design, architecture, incident history, implementation plan (`05-01`) in progress or approved |
| Allowed tools | read-only access to design, architecture, and incident history; does not execute commands or modify the repository |
| Permitted autonomy | A0 — Analyze risks and potential impact; A1 — Propose the risk matrix with mitigation and contingency |
| Stop criteria | stop if there is no reference design or plan; escalate to human review before moving on to `06-01` if any risk remains classified as high without a viable mitigation |
| Expected output | see `## Expected output` |
| Minimum evidence | each risk with explicit category, probability, impact, mitigation, and contingency; no high risk left without an associated mitigation plan |
| Recommended next prompt | `06-01-implementacion-multiagente`, once the plan (`05-01`) and this risk matrix are approved |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Identify and analyze implementation risks and the potential impact of the change on other modules, processes, services, pipelines, integrations and users.

Classify risks by:
- functional,
- technical,
- data,
- security,
- operations,
- agent concurrency,
- integration,
- deployment.

Deliver:
- risk matrix,
- probability,
- impact,
- mitigation,
- contingency.
```

---

## Use with standard formula

```text
Use the implementation risk analysis prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [TARGET BRANCH]
- environment: [DEV / QA / PROD]
- components: [COMPONENTS TO MODIFY]
- documents to review: approved design, architecture, incident history
- specific output objective: complete risk matrix with mitigation plan
- depth level: high
```

---

## Expected output

| Risk | Category | Probability | Impact | Mitigation | Contingency |
|---|---|---|---|---|---|
