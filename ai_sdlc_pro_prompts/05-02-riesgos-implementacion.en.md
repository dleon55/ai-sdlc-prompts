# 5.2 — Implementation risk and impact analysis

## Description

Prompt to identify and classify implementation risks: functional, technical, data, security, operations, agent concurrency, integration and deployment. Generates a risk matrix with probability, impact and mitigation plan.

**When to use it:** in parallel with the implementation plan (`05-01`), before executing any change.

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
