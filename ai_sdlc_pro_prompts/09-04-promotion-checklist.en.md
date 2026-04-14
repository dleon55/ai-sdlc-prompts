# 9.4 — Promotion checklist: integration and deployment between environments

## Description

Prompt to plan and document the promotion of changes between environments (dev → qa → staging → prod): pre-checks, deployment steps, post-deployment validations, go/no-go criteria and rollback plan. Includes considerations for environments with AI agents operating.

**When to use it:** before any deployment to a higher environment, especially before going to production. Also useful to define the project's standard promotion process.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Generate the complete promotion checklist for deploying this change between environments.

Required inputs:
- repository: [NAME OR URL]
- change to deploy: [REFERENCE TO ISSUE OR PR]
- source branch: [BRANCH WITH CHANGES]
- source environment: [DEV / QA / STAGING]
- target environment: [QA / STAGING / PROD]
- deployment stack: [Docker / Kubernetes / VM / GCP / AWS / other]
- database migrations: [YES / NO]
- infrastructure changes: [YES / NO]
- environment variable changes: [YES / NO]

Deliver:

## 1. PRE-DEPLOYMENT CHECKS (pre-flight)
### Code and quality
- [ ] PR is approved by at least [N] reviewers
- [ ] CI/CD passes green: lint, build, tests, coverage
- [ ] No secrets or credentials exposed in the diff
- [ ] Basic security review completed (applicable OWASP Top 10)
- [ ] New technical debt documented in backlog
- [ ] CHANGELOG.md updated with the change

### Database (if applicable)
- [ ] Migrations reviewed and tested in source environment
- [ ] Backup of target environment performed BEFORE deployment
- [ ] Migrations are reversible or data rollback is available
- [ ] Migration scripts tested with representative dataset

### Environment variables (if applicable)
- [ ] New variables documented in .env.example
- [ ] Variables configured in target environment BEFORE deployment
- [ ] Secrets managed in secrets manager (Vault / GitHub Secrets)

### Infrastructure (if applicable)
- [ ] Infrastructure changes reviewed by responsible
- [ ] Necessary resources available (CPU, memory, storage)
- [ ] Network and firewall configuration validated

### For AI agents (if they participated in the change)
- [ ] Human validation of agent output completed
- [ ] PR only touches authorized scope files
- [ ] No agent instructions in code comments

## 2. GO / NO-GO CRITERIA
Explicitly define what conditions MUST be met to continue:

### ✅ GO — Continue if:
- all checks from point 1 are marked
- smoke tests from source environment pass
- maintenance window is active (if applicable)
- rollback responsible is available during deployment

### 🔴 NO-GO — Stop if:
- any critical check from point 1 fails
- target environment has active incidents
- no responsible available for rollback
- it is Friday afternoon or eve of important date (operational hygiene rule)

## 3. DEPLOYMENT STEPS
Exact and ordered sequence of commands or actions for this change.
For each step indicate:
- description of the action
- exact command or procedure
- expected result
- how to verify the step was successful
- rollback action for that step if it fails

## 4. POST-DEPLOYMENT VALIDATIONS (minimum smoke test)
- [ ] Application responds HTTP 200 at target environment URL
- [ ] Critical flows work: [SPECIFIC LIST FOR THIS CHANGE]
- [ ] Logs show no new errors in first 5 minutes
- [ ] Performance metrics within normal thresholds
- [ ] No active alerts in monitoring system

## 5. OBSERVATION WINDOW
- Recommended post-deployment observation time: [X hours]
- Criteria to close the change as successful:
  - zero incidents during observation window
  - stable metrics
  - validation by change requester

## 6. ROLLBACK PLAN
- When to execute rollback: [concrete conditions]
- Ordered rollback steps (inverse to deployment):
  1. [Step 1]
  2. [Step 2]
  ...
- Estimated rollback time: [X minutes]
- Rollback responsible: [ROLE]
- Post-rollback notification: [to whom and by which channel]

## 7. COMMUNICATION
- Notify BEFORE deployment to: [LIST]
- Notify UPON COMPLETION to: [LIST]
- Incident communication channel: [CHANNEL]
- Rollback decision made by: [ROLE / PERSON]
```

---

## Use with standard formula

```text
Use the promotion checklist prompt and adapt it to:
- repository: [NAME OR URL]
- change: [REFERENCE TO ISSUE OR PR]
- source branch: [BRANCH]
- source environment → target environment: [SOURCE → TARGET]
- deployment stack: [STACK]
- database migrations: [YES / NO]
- infrastructure changes: [YES / NO]
- documents to review: CHANGELOG, PR diff, runbooks/, architecture
- specific output objective: complete go/no-go checklist + deployment steps + rollback plan
- depth level: high
```

---

## Expected output

### Change deployment summary

| Field | Value |
|---|---|
| Issue / PR | #[N] |
| Branch | [BRANCH] |
| Target environment | [ENVIRONMENT] |
| Change type | feat / fix / refactor / ops |
| Database migrations | Yes / No |
| Infra changes | Yes / No |
| Estimated window | [X] minutes expected downtime |
| Responsible | [NAME] |
| Rollback available | Yes / No |

### Go/no-go semaphore

| Area | Status | Observation |
|---|---|---|
| CI/CD green | 🟢 / 🔴 | |
| Database backup | 🟢 / 🔴 | |
| Reviewers approved | 🟢 / 🔴 | |
| Target environment stable | 🟢 / 🔴 | |
| Rollback responsible present | 🟢 / 🔴 | |
| **Decision** | **GO / NO-GO** | |
