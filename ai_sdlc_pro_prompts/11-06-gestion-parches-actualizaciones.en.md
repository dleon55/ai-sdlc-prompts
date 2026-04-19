# 11.6 — Patch and Update Management

## Description

Prompt to plan and execute the complete patch management cycle: dependency and component inventory, update criticality assessment, environment-by-environment application plan, regression verification, and cycle documentation. Covers application dependencies, operating system, containers, and infrastructure.

**When to use:** as a periodic pending update review (monthly/quarterly), when receiving CVE alerts affecting project dependencies (`13-02` SCA), or before a major release to ensure components are up to date.

---

## Required prior context

> Include the block from `00-framework.md` before this prompt.
> If a result from `13-02` (SCA) or `13-07` (Vulnerability Management) exists, attach it to prioritize security patches.

---

## Full prompt

```text
Objective:
Plan and execute the complete patch management cycle for the project:
inventory outdated components, assess the criticality of each update,
define the environment-by-environment application plan with rollback criteria,
verify no regressions are introduced, and document patch status for auditing.

Steps:

1. INVENTORY OF COMPONENTS TO PATCH
   Generate the complete inventory of components with available updates:
   
   a) Application dependencies (by package manager):
      - Node.js: `npm outdated` or `yarn outdated`
      - Python: `pip list --outdated` or `pip-review`
      - PHP: `composer outdated`
      - Java/Maven: `mvn versions:display-dependency-updates`
      - Ruby: `bundle outdated`
      - Go: `go list -m -u all`
      - .NET: `dotnet list package --outdated`
   
   b) Container images (if Docker is used):
      - base images used in Dockerfiles: are newer versions available?
      - auxiliary service images (DB, cache, proxy): current vs. available versions?
      - are floating tags (`:latest`) being used that mask real versions?
   
   c) Operating system and runtime (if infrastructure is managed):
      - pending OS patches: Ubuntu/Debian (`apt list --upgradable`), RHEL (`yum check-update`)
      - runtime version: Node.js, Python, Java, PHP — on LTS version with active support?
      - web server / proxy version: Nginx, Apache, Caddy
   
   d) Infrastructure tools:
      - Kubernetes / Helm / kubectl version
      - Terraform / Ansible / CDK version
      - CI/CD agent versions (runners, agents)
      - TLS certificates: expiration date (alert if < 30 days)

2. UPDATE CLASSIFICATION
   For each outdated component, classify:
   
   Update type (semver):
   - PATCH (x.x.N → x.x.N+1): bug fix — low risk, always apply
   - MINOR (x.N.x → x.N+1.x): backward-compatible new feature — medium risk, review changelog
   - MAJOR (N.x.x → N+1.x.x): possible breaking change — high risk, requires full testing
   
   Update category:
   - SECURITY: fixes a CVE — top priority, SLA based on CVSS
   - FIX: resolves a bug that affects us — high priority
   - FIX: resolves a bug that does not directly affect us — medium priority
   - IMPROVEMENT: new feature — low priority, evaluate in planned cycle
   - DEPRECATION: warns of upcoming removal in next MAJOR — plan migration
   
   Priority matrix:
   | Category | PATCH | MINOR | MAJOR |
   |---|---|---|---|
   | Security CRITICAL | Apply < 24h | Apply < 7 days | Urgent evaluation |
   | Security HIGH | Apply < 7 days | Apply < 30 days | Evaluate in sprint |
   | Bug affecting us | Apply this sprint | Evaluate | Plan |
   | Improvement / Other | Monthly cycle | Quarterly cycle | Evaluate roadmap |

3. IMPACT AND RISK ANALYSIS
   For MINOR and MAJOR updates:
   
   a) Review the changelog / release notes between current and new version:
      - are there API changes used in the project? (breaking changes)
      - are there default behavior changes that may affect tests?
      - are there new transitive dependencies that introduce conflicts?
   
   b) Assess the change surface in the project:
      - how many files use the dependency directly?
      - does test coverage cover the code using this dependency?
      - are there workarounds or local patches that may break?
   
   c) Regression risk:
      - LOW: dependency with good test coverage, no breaking changes, PATCH or MINOR without API changes
      - MEDIUM: important dependency, MINOR with some API changes, partial coverage
      - HIGH: critical dependency, MAJOR, breaking changes, low coverage

4. ENVIRONMENT-BY-ENVIRONMENT APPLICATION PLAN
   Define the application sequence by environment with intermediate validations:
   
   Environment 1 — Development (local / feature branch):
   - apply the update in a dedicated branch: `chore/update-[package]-vX.Y.Z`
   - run the full test suite: unit + integration + E2E
   - manually review critical flows if tests do not have full coverage
   - advancement criterion: 0 failing tests, no startup errors
   
   Environment 2 — Staging:
   - deploy the update branch to staging
   - run smoke tests (`07-10`) to validate the system starts correctly
   - run performance benchmark (`07-11`) to detect performance regressions
   - keep active in staging for at least 24 hours before promoting to production
   
   Environment 3 — Production:
   - deploy during low-traffic maintenance window (if the change has MEDIUM or HIGH risk)
   - canary or blue-green deployment if available
   - active monitoring for 1 hour post-deployment: metrics, error rate, logs
   - rollback criterion: error rate > N% or P95 > threshold × 1.5 for 5 minutes
   
   Rollback plan:
   - define the exact previous commit or version to restore
   - estimated rollback time: [minutes]
   - authorized to approve rollback: [role]

5. GROUPING TO MINIMIZE DISRUPTIONS
   Organize updates into logical groups for efficient application:
   
   Group 1 — Urgent security updates (apply immediately):
   - list critical/high CVEs with SLA expired or about to expire
   
   Group 2 — PATCH fixes + medium/low security updates:
   - group in a single PR to minimize noise
   
   Group 3 — MINOR updates without breaking changes:
   - apply one by one with intermediate tests, or in small batches with good coverage
   
   Group 4 — MAJOR updates / breaking changes:
   - each in its own PR, with a prior analysis spike if critical
   - plan in a dedicated sprint

6. DOCUMENTATION AND AUDITING
   Upon completing the patch cycle:
   - generate the cycle record: date, updated components, versions, test results
   - update the project CHANGELOG with dependency updates
   - update the dependency inventory (if maintained separately)
   - record any postponed update (with justification and next review date)
   - report status to stakeholders: "N components updated, M postponed, K pending MAJOR version"

7. PREVENTIVE AUTOMATION
   If no automation exists, propose:
   - Dependabot (GitHub) or Renovate: automatic update PRs with grouping configured
   - automatic CVE alerts for dependencies (GitHub Security Advisories, Snyk, Socket)
   - CI pipeline running `npm audit` / `pip-audit` / `trivy` on every PR
   - TLS certificates monitored with expiration alerts at 30 and 7 days

Deliverables:
- inventory of outdated components with classification (type, category, priority),
- grouped patch plan table with environment sequence and rollback criteria,
- risk analysis for MINOR and MAJOR updates,
- audit record of the completed patch cycle,
- preventive automation recommendations for the project.
```

---

## Standard formula usage

```text
Use the patch management prompt and adapt it to:
- repository: [NAME OR URL]
- technology stack: [language, package manager, runtime, containers]
- available environments: [dev / staging / production]
- vulnerability context: [ATTACH 13-02 SCA RESULT if available]
- CI/CD tools: [GitHub Actions / GitLab CI / Jenkins / other]
- existing automation: [Dependabot / Renovate / none]
- last time patches were applied: [date]
- security SLAs committed: [standard SLA by CVE severity]
- documents to review: package.json, requirements.txt, Dockerfile, Terraform/Helm files
- specific output goal: inventory + grouped plan + risk analysis
- depth level: high
```

---

## Expected output

### Pending updates inventory

| Component | Current version | Available version | Type | Category | Priority | Risk |
|---|---|---|---|---|---|---|
| `express` | 4.17.1 | 4.21.2 | PATCH | Security — CVE-2024-43796 | CRITICAL | Low |
| `django` | 4.1.0 | 5.0.4 | MAJOR | Security + new features | HIGH | High |
| `lodash` | 4.17.20 | 4.17.21 | PATCH | Bug fix | Medium | Low |
| `react` | 17.0.2 | 18.3.1 | MAJOR | Improvement — Concurrent Mode | Low | High |
| Base image node | `node:18-alpine` | `node:22-alpine` | MAJOR | LTS upgrade | Medium | High |

### Grouped patch plan

| Group | Components | Starting environment | Estimated date | Owner |
|---|---|---|---|---|
| 1 — Urgent security | `express` + 2 more CVEs | Dev → Staging → Prod | This week | Backend lead |
| 2 — PATCH + medium security | `lodash` + 8 more | Dev → Staging | This sprint | Any dev |
| 3 — MINOR without breaking | 12 dependencies | Dev → Staging | Next sprint | Tech lead |
| 4 — MAJOR (`django`) | `django` 4→5 | Prior analysis spike first | Q3 | Full team |
