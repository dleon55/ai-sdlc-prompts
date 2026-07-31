# 9.4 — Promotion checklist: integration and deployment between environments

## Description

Prompt to plan and document the promotion of changes between environments (dev → qa → staging → prod): pre-checks, deployment steps, post-deployment validations, go/no-go criteria and rollback plan. Includes considerations for environments with AI agents operating.

**When to use it:** before any deployment to a higher environment, especially before going to production. Also useful to define the project's standard promotion process.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | operation |
| Expected risk | high — the checklist determines the go/no-go decision for a deployment that may include database migrations, infrastructure changes, and reach production |
| Required inputs | reference to the issue/PR, source branch, source and target environment, deployment stack, indication of whether there are DB migrations, infrastructure changes or environment variable changes |
| Allowed tools | reading CHANGELOG, PR diff, runbooks and architecture documentation — no executing the deployment, running commands against the target environment, or performing real rollback actions |
| Permitted autonomy | A1 — Propose (generates the checklist and the go/no-go semaphore; executing the deployment and rollback requires explicit A3 by the release owner) |
| Stop criteria | if no rollback owner is available, if there are DB migrations without a confirmed backup, or if any explicit NO-GO condition from section 2 is met, stop and do not recommend proceeding with the deployment |
| Expected output | see `## Expected output` |
| Minimum evidence | each item in the go/no-go semaphore must be marked with its status (🟢/🔴) and an observation justifying it |
| Recommended next prompt | `08-01-revision-completa-pr` before executing the promotion, to confirm the change's pipeline is green and the merge verdict is favorable |

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

Constraints:
- no checklist item can be marked as complete or skipped without explicit sign-off from the person responsible for that area (code, database, infrastructure) — "not applicable" also requires an explicit justification, it cannot be left blank.
- the promotion decision is all-or-nothing: do not propose or execute a partial promotion (e.g., deploying the code but postponing the database migration) without explicitly flagging the risk of leaving environments in inconsistent states.
- do not recommend GO if there is no verified rollback plan with an assigned owner — merely intending to roll back does not count as a plan.
- if the target environment is PROD, every deployment and rollback command is left proposed and pending explicit approval from the release owner; this prompt does not execute the deployment itself.

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
- the deployment time falls within a freeze window explicitly defined by the team (e.g. Friday afternoon, eve of a commercial event, fiscal period close) — if no freeze-window policy was provided as input, do not assume one on your own; flag it as data not provided instead of applying your own judgment of what counts as an "important date"

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

### Example applied

| Field | Value |
|---|---|
| Issue / PR | #482 |
| Branch | release/2026-03-12 |
| Target environment | PROD |
| Change type | fix |
| Database migrations | Yes — adds index to `orders.customer_id` |
| Infra changes | No |
| Estimated window | 5 minutes expected downtime (rolling deploy) |
| Responsible | María Ibáñez (release owner) |
| Rollback available | Yes — revert of previous deploy in < 3 min |

| Area | Status | Observation |
|---|---|---|
| CI/CD green | 🟢 | pipeline #1203 passed lint, tests, and 87% coverage |
| Database backup | 🟢 | snapshot `orders-prod-20260312-1400` confirmed |
| Reviewers approved | 🟢 | 2/2 approvals (required: 2) |
| Target environment stable | 🟢 | no active incidents, 0.05% error rate |
| Rollback responsible present | 🟢 | María Ibáñez available in #deploys channel until 17:00 |
| **Decision** | **GO** | all checks green, maintenance window active |
