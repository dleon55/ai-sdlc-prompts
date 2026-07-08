# 11.2 — Security hardening and operations

## Description

Prompt to analyze the repository and operational configuration for security strengthening opportunities: hardening, secrets management, permissions, service exposure and deployment risks.

**When to use it:** periodically as security review, before a production deployment, or when security findings are detected in code review.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | security |
| Expected risk | high — can expose infrastructure configuration and secrets if used carelessly |
| Required inputs | docker-compose, nginx configuration, `.env` (structure, not values), workflows, GitHub permissions |
| Allowed tools | reading configuration and infrastructure — never execute configuration changes in the same step |
| Permitted autonomy | A0 — Analyze (only delivers findings and mitigation plan, does not apply changes) |
| Stop criteria | never include real secret values in the output, even if found exposed; reference only location and type |
| Expected output | see `## Expected output` |
| Minimum evidence | each finding must indicate the exact file/component and justified criticality |
| Recommended next prompt | `13-08-gestion-secretos-credenciales` if exposed credentials are detected; `13-03-secure-sdlc-revision` for a broader review |

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
