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

Steps:
1. Reproduce the problem: try to reproduce the symptom in a controlled way (same input, same environment if possible) before theorizing about the cause — without a reliable reproduction, any hypothesis is speculation.
2. Isolate variables: identify what changed relative to the last known-good state (code, configuration, data, infrastructure, external dependencies) to narrow the search space.
3. Check recent changes first: prioritize deploys, configuration changes, dependency updates, or migrations from the last few days — most environment incidents correlate with a recent change, not a spontaneous cause.
4. Gather read-only evidence: logs, service status, metrics (CPU, memory, latency, error rate), and traces related to the symptom, without modifying anything in the environment at this stage.
5. Formulate hypotheses ordered by probability: for each one, state how to validate it with concrete evidence (not just intuition) and what result would confirm or rule it out.
6. Validate or discard each hypothesis in order, documenting the result of every check — including dead ends, since they bound the problem for whoever continues the investigation.
7. Converge on the root cause: don't stop at the first coincidental symptom; confirm the cause fully explains the observed behavior, not just part of it.
8. Propose the resolution path: concrete steps to resolve, flagging which ones require human approval before execution (restarts, rollbacks, configuration changes).
9. Verify the proposed fix addresses the root cause rather than masking the symptom (e.g., restarting a service that temporarily relieves a memory leak without fixing it) — explicitly flag whether an action is palliative or definitive.

Constraints:
- prioritize read-only diagnostic commands (logs, service status, metrics); do not run restarts, rollbacks, configuration changes, or destructive commands — include them as part of the proposed "resolution path" instead, pending approval,
- do not apply or recommend applying a fix without having confirmed the root cause with evidence: a fix applied on an unverified hypothesis can hide the real problem or introduce a new one,
- do not execute or propose executing any action against production without explicit human approval, even if the diagnosis suggests an obvious fix,
- document the full investigation trail, including discarded hypotheses and dead ends — that record prevents someone else from repeating the same failed check in a future incident,
- if the environment is PROD and there is significant user impact, stop and escalate to `11-04-incident-response` instead of continuing this standard troubleshooting.

Deliver:
- symptom,
- involved services,
- suggested review,
- commands or evidence reviewed,
- hypotheses ordered with their validation,
- resolution path.
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

### Example applied

| Hypothesis | Probability | How to validate it | Result |
|---|---|---|---|
| The 14:32 deploy introduced a missing environment variable | High | Review the deploy diff and the container's startup logs | Confirmed — the container logs `KeyError: DATABASE_URL` after deploy `a1b2c3d` |
| The load balancer's TLS certificate expired | Medium | `openssl s_client -connect lb.internal:443` and check the expiration date | Ruled out — certificate valid until 2027-01 |
