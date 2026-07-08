# 11.1 — Environment troubleshooting

## Description

Prompt to analyze an environment, deployment, service, container, pipeline or configuration problem: symptom, involved services, hypotheses, commands to review and resolution path.

**When to use it:** when a service fails, a deployment doesn't work as expected, or there's a configuration problem in any environment. If the environment is PROD and there is significant user impact, use `11-04-incident-response` instead.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — analyzes an environment with possible service impact; if the environment is PROD with significant impact, the prompt itself requires escalating to `11-04-incident-response` |
| Required inputs | symptom, environment (DEV/QA/STAGING/PROD), involved services, available evidence (logs, errors, captures) |
| Allowed tools | read-only access for diagnosis (logs, service status, metrics); explicitly forbidden to run restarts, rollbacks, configuration changes, or destructive commands |
| Permitted autonomy | A0 — Analyze: diagnosis and hypotheses; the resolution path is left proposed and pending approval before moving to A2 |
| Stop criteria | if the environment is PROD and there is significant user impact, it must stop and escalate to `11-04-incident-response` instead of continuing standard troubleshooting |
| Expected output | see `## Expected output` |
| Minimum evidence | hypotheses ordered by probability with associated evidence, and diagnostic commands limited to read-only |
| Recommended next prompt | `11-04-incident-response` if it escalates to a PROD incident with significant impact; `03-02-causa-raiz` if a formal root cause analysis is needed after resolution |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze an environment, deployment, service, container, pipeline or configuration problem and determine possible causes, necessary validations and resolution path.

Include:
- symptom,
- involved services,
- suggested review,
- commands or evidence to review,
- hypotheses,
- resolution path.

⚠️ Prioritize read-only diagnostic commands (logs, service status, metrics). Do not run restarts, rollbacks, configuration changes, or destructive commands — include them as part of the proposed "resolution path" instead, pending approval.
```

---

## Use with standard formula

```text
Use the environment troubleshooting prompt and adapt it to:
- repository: [NAME OR URL]
- symptom: [PROBLEM DESCRIPTION]
- environment: [DEV / QA / STAGING / PROD]
- involved services: [CONTAINERS, SERVICES, PIPELINES]
- available evidence: [LOGS, ERRORS, CAPTURES]
- documents to review: configurations, docker-compose, nginx, environment variables
- specific output objective: ordered hypotheses + diagnostic commands + resolution path
- depth level: high
```

---

## Expected output

| Section | Content |
|---|---|
| Symptom | Observed behavior with evidence |
| Involved services | Containers, services and affected components |
| Suggested review | What to review first and why |
| Commands to execute | Ordered diagnostic commands |
| Hypotheses | Possible causes by probability order |
| Resolution path | Concrete steps to resolve |
