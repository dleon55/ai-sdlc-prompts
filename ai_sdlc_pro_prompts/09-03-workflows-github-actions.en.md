# 9.3 — GitHub Actions workflows review

## Description

Prompt to audit the repository workflows and verify if they adequately cover validation, tests, security, deployment and quality. Detects gaps, risks and proposes improvements.

**When to use it:** periodically as pipeline health review, or when incorporating new modules or environments.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — does not modify workflows directly, only audits and recommends |
| Required inputs | contents of `.github/workflows/`, CI/CD README |
| Allowed tools | reading workflow files — no job execution or pipeline changes |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if a workflow references secrets or permissions that cannot be inspected without access to the repository configuration, document it as a visibility gap instead of assuming its state |
| Expected output | see `## Expected output` |
| Minimum evidence | each reported gap must cite the workflow file and the specific job |
| Recommended next prompt | `11-02-hardening-seguridad` if security gaps are detected in the pipeline |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze the repository workflows and determine if they adequately cover validation, tests, security, deployment and quality.

Steps:
1. Inventory every workflow in `.github/workflows/`: name, file, triggers (push, pull_request, schedule, workflow_dispatch, release) and the jobs each one contains.
2. For each job, identify what it actually validates (lint, build, tests, security scanning, deployment) and with which tool — don't assume from the job name, inspect the steps.
3. Compare the inventory against the expected coverage areas (validation/lint, build, unit tests, integration tests, security analysis, per-environment deployment, notifications) and mark each one as covered, partial, or missing.
4. For covered areas, assess whether the coverage is actually sufficient: does the job really block the merge or is it only informational? Does it run on every push or only in some cases? Does it have defined failure thresholds (minimum coverage, vulnerability severity)?
5. For missing or partial areas, prioritize by risk: first, security and uncontrolled-deployment gaps (can cause production incidents); then testing gaps (can let bugs through); and last, notification or efficiency gaps.
6. Check the permissions and secrets each workflow uses (`permissions:`, `secrets.*`) and whether they follow least privilege; if you can't inspect the actual repository configuration (secrets, protected environments), document this as a visibility gap instead of assuming its state.
7. Write recommended improvements, prioritized and actionable, pointing to the specific file and job to modify.

Constraints:
- don't execute or trigger any workflow, and don't modify files under `.github/workflows/` — this is a read-only audit,
- don't assume the state of secrets, permissions, or protected environments you can't inspect directly; declare it as a visibility gap instead of inventing its configuration,
- every reported gap must cite the workflow file and the specific job affected — don't generalize without concrete evidence,
- if a workflow depends on an external service (registry, deployment environment) whose state you can't verify, flag it explicitly instead of assuming it works.

Deliver:
- complete workflow inventory,
- coverage analysis per area with gaps and risks,
- recommended improvements prioritized by risk.
```

---

## Use with standard formula

```text
Use the workflows review prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [MAIN BRANCH]
- documents to review: .github/workflows/, CI/CD README
- specific output objective: workflows inventory with gaps and recommended improvements
- depth level: medium
```

---

## Expected output

### Workflow inventory

| Workflow | File | Trigger | Jobs | Purpose |
|---|---|---|---|---|
| CI Build & Test | `.github/workflows/ci.yml` | `push` to any branch, `pull_request` into `main`/`develop` | `lint`, `build`, `unit-tests`, `integration-tests` | Validate the code builds, passes lint, and passes tests before merging |
| Security Scan | `.github/workflows/security.yml` | `pull_request` into `main`, weekly `schedule` | `dependency-scan`, `sast`, `secret-scan` | Detect vulnerable dependencies, insecure code, and leaked secrets |
| Deploy Staging | `.github/workflows/deploy-staging.yml` | `push` to `develop` | `build-image`, `deploy-staging`, `smoke-test` | Automatically deploy to Staging after every merge to `develop` |
| Deploy Production | `.github/workflows/deploy-prod.yml` | `release: published`, `workflow_dispatch` | `build-image`, `approve-gate`, `deploy-prod`, `notify` | Deploy to production with manual approval after cutting a release |

### Coverage analysis

| Area | Covered | Workflow | Missing | Risk | Recommendation |
|---|---|---|---|---|---|
| validation / lint | Yes | CI Build & Test (`lint`) | — | low | keep as-is |
| build | Yes | CI Build & Test (`build`) | — | low | cache dependencies to reduce pipeline time |
| unit tests | Yes | CI Build & Test (`unit-tests`) | no minimum coverage gate | medium | add a coverage threshold that blocks the merge if it drops below target |
| integration tests | Yes | CI Build & Test (`integration-tests`) | runs against mocks, not a real ephemeral DB | medium | migrate the job to an ephemeral DB container for more realistic tests |
| security analysis | Partial | Security Scan (`dependency-scan`, `sast`) | no scan of the final Docker image | high | add `trivy` (or similar) to the image build job |
| DEV deploy | No | — | no DEV deployment workflow exists, done manually | medium | automate DEV deployment on every push to `develop` or feature branches |
| QA deploy | No | — | no QA environment separate from Staging | low | assess whether a dedicated QA environment is needed or Staging covers it |
| PROD deploy | Yes | Deploy Production | no automatic rollback if the post-deploy smoke test fails | high | add an automatic rollback job on smoke test failure |
| notifications | Partial | Deploy Production (`notify`) | only notifies prod deployments, not CI failures on `main`/`develop` | low | add Slack/Teams notification when CI fails on protected branches |
