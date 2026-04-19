# 13.7 — Vulnerability Analysis and CVE Management

## Description

Prompt to perform triage, classification, prioritization, and full lifecycle management of vulnerabilities detected by any security tool (SAST, SCA, DAST, pentesting, scanners). Converts raw findings into an actionable security backlog with remediation SLAs.

**When to use:** after running any security analysis tool (`13-01` SAST, `13-02` SCA, `13-05` DAST, `13-06` pentesting), upon receiving alerts about new CVEs affecting project dependencies, or as a periodic security status review.

---

## Required prior context

> Include the block from `00-framework.md` before this prompt.
> Attach security tool results: reports from `13-01`, `13-02`, `13-05`, `13-06`, or automated scanner outputs.

---

## Full prompt

```text
Objective:
Perform triage, classification, prioritization, and management of detected vulnerabilities,
converting security findings into an actionable backlog with remediation SLAs,
assigned owners, and verifiable closure criteria.

Steps:

1. FINDINGS CONSOLIDATION
   Consolidate all reported vulnerabilities from different sources:
   - originating tool or source (SAST, SCA, DAST, pentesting, scanner, manual)
   - original finding ID in the source tool
   - affected component, file, line, or dependency
   - technical description of the issue
   - eliminate duplicates: if the same vulnerability appears in multiple sources,
     consolidate into a single item referencing all sources

2. TRIAGE AND VALIDATION
   For each finding, determine if it is a true positive:
   - Is the vulnerable code actually executable in the project's context?
   - Is there any compensating control that mitigates the risk?
   - Is it a tool false positive? (document the reasoning)
   - Is it a previously known and accepted vulnerability?
   
   Classify the triage result:
   - TRUE POSITIVE: remediation required
   - FALSE POSITIVE: document and suppress in the tool
   - ACCEPTED WITH RISK: record decision with approval and review date
   - OUT OF SCOPE: document why it does not apply

3. SCORING AND SEVERITY
   For each true positive, calculate or validate severity using CVSS v3.1:

   Base vector:
   - Attack Vector (AV): Network / Adjacent / Local / Physical
   - Attack Complexity (AC): Low / High
   - Privileges Required (PR): None / Low / High
   - User Interaction (UI): None / Required
   - Scope (S): Unchanged / Changed
   - Confidentiality Impact (C): High / Low / None
   - Integrity Impact (I): High / Low / None
   - Availability Impact (A): High / Low / None

   Contextual adjustment (Environmental Score):
   - What is the actual business impact if this vulnerability is exploited?
   - Are the exposed data public, internal, or highly confidential?
   - Is the affected system critical to business operations?

   Adjusted severity scale:
   - CRITICAL (CVSS ≥ 9.0): immediate threat — SLA 24 hours
   - HIGH (CVSS 7.0-8.9): significant risk — SLA 7 days
   - MEDIUM (CVSS 4.0-6.9): moderate risk — SLA 30 days
   - LOW (CVSS 0.1-3.9): limited risk — SLA 90 days
   - INFORMATIONAL: no SLA — evaluate in next technical debt review

4. EXPLOITABILITY ANALYSIS
   For critical and high findings, evaluate:
   - Does a known public exploit exist? (Exploit-DB, Metasploit, PoC on GitHub)
   - Is it being actively exploited (KEV — CISA Known Exploited Vulnerabilities)?
   - Does exploitation require authentication?
   - Is internal network access needed, or can it be exploited from the internet?
   - EPSS score if available (Exploit Prediction Scoring System)

   If a public active exploit exists → escalate SLA to immediate, regardless of CVSS.

5. REMEDIATION PLAN
   For each vulnerability, define:
   
   a) Preferred remediation (permanent fix):
      - what exact change must be made (update dependency, change code, configure)
      - affected files or components
      - estimated effort: [< 1h / half day / 1 day / > 1 day]
      - regression risk of the fix: [low / medium / high]

   b) Temporary mitigation (if fix takes time):
      - compensating control that reduces risk while the fix is implemented
      - examples: WAF rule, feature flag, additional validation in upper layer, temporary patch

   c) Fix verification:
      - how to verify the vulnerability was correctly remediated
      - specific test or command to confirm closure

6. SECURITY BACKLOG
   Generate the security issues backlog ready to create in GitHub Issues / Jira:
   - title: [SEVERITY] [CVE-ID or SAST-ID] — Brief problem description
   - labels: security, [severity], [OWASP category if applicable]
   - description: vector, impact, affected component, remediation steps
   - acceptance criteria: what must be met to close the issue
   - deadline according to SLA

7. METRICS AND REPORTING
   Generate security status metrics for the project:
   - Mean Time to Detect (MTTD): average time between introduction and detection
   - Mean Time to Remediate (MTTR): average remediation time by severity
   - Total security debt: sum of open vulnerabilities weighted by severity
   - Trend: is the number of vulnerabilities rising, falling, or stable?
   - SLA compliance: % of vulnerabilities closed within defined SLA

Deliverables:
- consolidated vulnerability table with triage and CVSS severity,
- security backlog in issues format ready to create,
- prioritized remediation plan with SLAs and owners,
- project security status metrics,
- summary dashboard for executive reporting.
```

---

## Standard formula usage

```text
Use the vulnerability and CVE management prompt and adapt it to:
- repository: [NAME OR URL]
- finding sources: [SAST 13-01 / SCA 13-02 / DAST / pentesting / Dependabot alert]
- attached results: [ATTACH TOOL REPORTS]
- target environment: [DEV / QA / STAGING / PROD]
- system criticality: [CRITICAL / HIGH / MEDIUM — based on business impact]
- defined SLAs: [USE STANDARD / CUSTOMIZE: critical=Xh, high=Xd, medium=Xd]
- documents to review: previous vulnerability records, security CHANGELOG
- specific output goal: prioritized security backlog + status metrics
- depth level: high
```

---

## Expected output

### Consolidated vulnerability table

| ID | Source | Component | Description | CVSS | Severity | Triage | Fix available | SLA | Owner |
|---|---|---|---|---|---|---|---|---|---|
| VUL-001 | SAST-001 | `api/views.py:42` | SQL Injection in search | 9.8 | CRITICAL | True positive | Yes — parameterize query | 24h | Backend dev |
| VUL-002 | SCA | `requests==2.25.0` | CVE-2023-32681 SSRF | 6.1 | MEDIUM | True positive | Yes — update to 2.32.3 | 30 days | DevOps |

### Security dashboard

| Metric | Value |
|---|---|
| Total vulnerabilities | N |
| Open critical | N |
| Open high | N |
| % within SLA | N% |
| MTTR critical | Xh |
| Security debt | Score |
