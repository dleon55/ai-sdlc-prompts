# 13.2 — SCA: Software Composition Analysis and Dependencies

## Description

Prompt to analyze third-party dependencies of the project and identify known vulnerabilities (CVEs), problematic licenses, abandoned dependencies, and supply chain risks. Applies to direct and indirect (transitive) dependencies.

**When to use:** in every PR that modifies dependencies, as a periodic review (at least monthly), before a production release, and in response to published security alerts (GitHub Dependabot, OSS-Index, etc.).

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | security |
| Expected risk | medium — read-only analysis, but an undetected or poorly prioritized supply chain vulnerability can escalate to high if not remediated in time |
| Required inputs | the project's dependency management files and lock files (package.json, requirements.txt, go.mod, etc.), product type (commercial/open source/internal) for license analysis; previous `13-07` findings if they exist |
| Allowed tools | reading of dependency files and lock files; recommends pip-audit/npm audit/Snyk/Trivy/etc. commands, but does not execute them or modify installed versions |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if lock files are not accessible, state the analysis as incomplete and indicate what is missing instead of simulating nonexistent CVEs; escalate to legal/compliance for problematic or unlicensed dependencies |
| Expected output | see `## Expected output` |
| Minimum evidence | each reported CVE includes package, installed version, CVSS score, and version with an available fix (or alternative mitigation if no fix exists) |
| Recommended next prompt | `13-07-gestion-vulnerabilidades-cves` to triage and prioritize the CVEs and licenses found |

---

## Required prior context

> Include the block from `00-framework.md` before this prompt.
> If there are findings from `13-07` (CVE Management), attach it to correlate with the current triage state.

---

## Full prompt

```text
Objective:
Analyze the project's third-party dependencies to identify known vulnerabilities
(CVEs), problematic licenses, abandoned dependencies, and supply chain attack risks.

Steps:

1. DEPENDENCY INVENTORY
   Identify the dependency management files present:
   - Python: requirements.txt, requirements-dev.txt, Pipfile, pyproject.toml
   - JavaScript/Node: package.json, package-lock.json, yarn.lock, pnpm-lock.yaml
   - Java: pom.xml, build.gradle
   - Ruby: Gemfile, Gemfile.lock
   - Go: go.mod, go.sum
   - PHP: composer.json, composer.lock
   - .NET: *.csproj, packages.config

   For each detected file:
   - list the total direct dependencies
   - list the total transitive dependencies (if lock file is available)
   - identify whether exact version pinning or permissive ranges are used

2. RECOMMENDED ANALYSIS TOOLS
   Based on the detected language, provide exact commands for the analysis:
   - Python: pip-audit, safety check, dependabot
   - JavaScript: npm audit, yarn audit, npm audit --json
   - Java: OWASP Dependency-Check, mvn dependency-check:check
   - Ruby: bundle audit
   - Go: govulncheck ./...
   - PHP: composer audit
   - Multi-language: Snyk (snyk test), Trivy (trivy fs .), Grype (grype dir:.)
   - GitHub: Dependabot alerts + Security Advisories

3. KNOWN VULNERABILITY ANALYSIS
   For each detected vulnerability (or simulated if no execution access):
   - affected package and installed version
   - CVE ID and CVSS v3.1 score
   - impact description
   - version with available fix
   - if no fix: alternative mitigation
   - whether the project actually uses the vulnerable functionality (scope analysis)

4. LICENSE ANALYSIS
   Classify the licenses found:
   - PERMISSIVE (MIT, BSD, Apache 2.0): no commercial restrictions
   - WEAK COPYLEFT (LGPL, MPL): specific distribution conditions
   - STRONG COPYLEFT (GPL, AGPL): requires code openness if distributed
   - PROBLEMATIC or NO LICENSE: legal risk — escalate to legal/compliance

5. DEPENDENCY HEALTH
   For the 20 most critical dependencies (by usage and data access):
   - latest available version vs installed version
   - date of last commit in the dependency's repository
   - number of active maintainers
   - whether the dependency has been officially abandoned or deprecated
   - if the dependency has not been updated for more than 2 years: flag as risk

6. SUPPLY CHAIN RISKS
   Evaluate the following vectors:
   - Is a lock file with integrity hashes used? (npm --integrity, pip hash)
   - Are dependencies published from official registries? (npmjs.com, pypi.org)
   - Are there dependencies with names similar to popular packages? (typosquatting)
   - Does the CI pipeline validate dependency integrity before installing?
   - Are dependencies used directly from git repositories (without fixed version)?

7. PRIORITIZATION AND REMEDIATION PLAN
   Classify findings:
   - CRITICAL: CVE with CVSS ≥ 9.0 or GPL license in commercial product
   - HIGH: CVE with CVSS 7.0-8.9 or abandoned dependency in critical path
   - MEDIUM: CVE with CVSS 4.0-6.9 or dependency outdated > 2 years
   - LOW: CVE with CVSS < 4.0 or ambiguous license
   - INFORMATIONAL: dependency with minor updates available

Constraints:
- never invent a CVE, a CVSS score, or a fix status — report only vulnerabilities verifiable in public databases (NVD, GitHub Advisory Database, OSV) and mark as "requires confirmation with audit tool" any finding you can't verify directly,
- this is read-only analysis: don't run `npm audit fix`, `pip install --upgrade`, or any command that modifies installed versions or lock files — deliver the commands for a human to run,
- if you find a token or credential embedded in a dependency file, lock file, or private registry configuration, treat it as a secret: never reveal its value, only its location and type,
- for a problematic or unlicensed dependency, escalate to legal/compliance instead of assuming it's acceptable for the product type,
- if you don't have access to the lock files, state the analysis as incomplete and indicate exactly what is missing instead of simulating nonexistent CVEs.

Deliverables:
- dependency inventory with versions and security status,
- CVE findings table with severity and available fix,
- license classification risk table,
- critical dependency health report,
- prioritized update plan,
- remediation commands ready to execute.
```

---

## Standard formula usage

```text
Use the SCA prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [MAIN OR WORKING BRANCH]
- language(s): [AUTO-DETECT]
- product type: [COMMERCIAL / OPEN SOURCE / INTERNAL] — affects license analysis
- preferred tool: [AUTO-DETECT / npm audit / pip-audit / Snyk / Trivy]
- documents to review: dependency files, lock files, active Dependabot alerts
- specific output goal: CVE + license report + update plan
- depth level: high
```

---

## Expected output

### Vulnerability summary

| Severity | Count | With fix available | Without fix |
|---|---|---|---|
| Critical | N | N | N |
| High | N | N | N |
| Medium | N | N | N |
| Low | N | N | N |

### CVE table

| Package | Installed version | CVE | CVSS | Description | Fixed in version | Action |
|---|---|---|---|---|---|---|
| `lodash` | 4.17.15 | CVE-2020-8203 | 7.4 | Prototype pollution: allows adding or modifying arbitrary global object properties via `_.merge`/`_.zipObjectDeep` with untrusted input | 4.17.19 | Update immediately |
| `axios` | 0.21.1 | CVE-2021-3749 | 7.5 | ReDoS via a vulnerable regular expression in URL trailing-slash handling | 0.21.2 | High — update before the next release (a CVSS of 7.5 falls in this prompt's own HIGH range) |

### Update plan

| Package | From version | To version | Change type | Breaking change risk | Priority |
|---|---|---|---|---|---|
| `lodash` | 4.17.15 | 4.17.21 | Minor | Low — no public API changes | 1 |
| `axios` | 0.21.1 | 0.21.4 | Patch | Low — compatible, only fixes URL parsing | 2 |
