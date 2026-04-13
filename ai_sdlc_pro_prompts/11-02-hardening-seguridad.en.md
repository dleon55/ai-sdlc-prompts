# 11.2 — Security hardening and operations

## Description

Prompt to analyze the repository and operational configuration for security strengthening opportunities: hardening, secrets management, permissions, service exposure and deployment risks.

**When to use it:** periodically as security review, before a production deployment, or when security findings are detected in code review.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze the repository and operational configuration to detect security strengthening opportunities, hardening, secrets management, permissions, service exposure and deployment risks.

Deliver:
- findings,
- criticality,
- mitigation,
- priority.
```

---

## Use with standard formula

```text
Use the hardening and security prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [MAIN BRANCH]
- environment: [PROD / STAGING]
- components: [INFRASTRUCTURE, SERVICES, CONFIGURATIONS]
- documents to review: docker-compose, nginx, .env, workflows, GitHub permissions
- specific output objective: security findings report with prioritized mitigation plan
- depth level: high
```

---

## Expected output

| Finding | Category | Criticality | Component | Mitigation | Priority |
|---|---|---|---|---|---|
