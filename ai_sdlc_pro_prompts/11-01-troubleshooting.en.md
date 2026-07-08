# 11.1 — Environment troubleshooting

## Description

Prompt to analyze an environment, deployment, service, container, pipeline or configuration problem: symptom, involved services, hypotheses, commands to review and resolution path.

**When to use it:** when a service fails, a deployment doesn't work as expected, or there's a configuration problem in any environment. If the environment is PROD and there is significant user impact, use `11-04-incident-response` instead.

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
