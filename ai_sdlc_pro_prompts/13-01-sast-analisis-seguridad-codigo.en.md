# 13.1 — SAST: Static Application Security Testing

## Description

Prompt to perform a static security analysis of source code (SAST — Static Application Security Testing): detects OWASP Top 10 vulnerabilities, insecure patterns, improper handling of sensitive data, authentication/authorization issues, and security debt before they reach production.

**When to use:** before opening a PR, after implementing a change with security implications, or as a periodic codebase review. Complements (does not replace) automated SAST tools.

---

## Required prior context

> Include the block from `00-framework.md` before this prompt.
> If a `13-04` (Threat Modeling) result exists, attach it as context for known attack surfaces.

---

## Full prompt

```text
Objective:
Perform a static security analysis (SAST) of the indicated code, identifying
vulnerabilities, insecure patterns, and security debt according to OWASP Top 10
and secure development best practices.

Steps:

1. CODE RECONNAISSANCE
   - Identify the language, framework, and version.
   - Map data entry points: HTTP endpoints, forms, CLI arguments,
     message queues, file imports, environment variables.
   - Identify outputs: HTTP responses, logs, generated files, DB, external APIs.
   - Detect the authentication and authorization model in use.

2. OWASP TOP 10 (2021) ANALYSIS BY CATEGORY
   For each category, report: does it apply to the code?, findings, severity.

   A01 — Broken Access Control
   - Permission verification at each sensitive endpoint/function
   - Direct ID exposure (IDOR)
   - Authorization bypass via parameter manipulation

   A02 — Cryptographic Failures
   - Sensitive data in plaintext (passwords, tokens, PII)
   - Weak or deprecated algorithms (MD5, SHA1, DES, ECB)
   - Hardcoded certificates, keys, or secrets in source code

   A03 — Injection
   - SQL Injection (concatenated queries, not parameterized)
   - Command Injection (OS calls with user input)
   - LDAP, XPath, NoSQL Injection
   - Template Injection (SSTI)

   A04 — Insecure Design
   - Exploitable business logic
   - Absence of rate limiting on critical operations
   - Flows without state validation

   A05 — Security Misconfiguration
   - Missing HTTP security headers (CSP, HSTS, X-Frame-Options, etc.)
   - Debug mode enabled or stack traces exposed
   - Permissive CORS (*) on private APIs
   - Verbose error configuration

   A06 — Vulnerable and Outdated Components
   - Dependencies with known CVEs (refer to 13-02 for full analysis)
   - Outdated runtime or framework versions

   A07 — Identification and Authentication Failures
   - No login attempt limit / brute force protection
   - Predictable session tokens or without expiration
   - Insecure password recovery

   A08 — Software and Data Integrity Failures
   - Insecure deserialization of external data
   - No integrity verification in updates or pipelines
   - Dependencies without lock files or version pinning

   A09 — Security Logging and Monitoring Failures
   - Absence of security event logging (failed logins, permission changes)
   - Sensitive data in logs
   - No alerts on anomalous patterns

   A10 — Server-Side Request Forgery (SSRF)
   - Calls to URLs built with user input
   - No schema and host validation on external URLs

3. ADDITIONAL ANALYSIS
   - Hardcoded secrets: API keys, passwords, tokens in code or comments
   - Error handling: are internal details exposed to the client?
   - Input validation: is type, length, and format validated at the correct layer?
   - Race conditions on critical operations (payments, inventory, permissions)
   - Third-party dependencies loaded from CDN without integrity (SRI)

4. RECOMMENDED TOOLS
   Based on the detected language, provide exact commands for automated SAST
   as a complement to this analysis:
   - Python: bandit, semgrep, pylint-django (if applicable)
   - JavaScript/TypeScript: eslint-plugin-security, semgrep, njsscan
   - Java: SpotBugs + FindSecBugs, SonarQube
   - PHP: PHPCS Security Audit, Psalm
   - Go: gosec, staticcheck
   - Ruby: brakeman
   - Generic: semgrep with ruleset p/owasp-top-ten

5. FINDINGS CLASSIFICATION
   Use CVSS v3.1 scale for severity:
   - CRITICAL (CVSS 9.0-10.0): remotely exploitable, no auth, total impact
   - HIGH (CVSS 7.0-8.9): exploitable with minimal conditions
   - MEDIUM (CVSS 4.0-6.9): exploitable under specific conditions
   - LOW (CVSS 0.1-3.9): limited impact or difficult exploitation
   - INFORMATIONAL: best practice, not a vulnerability

Deliverables:
- findings table with severity, OWASP category, component, description, and remediation,
- recommended SAST tools list with execution commands,
- executive summary: overall risk level of the analyzed code,
- prioritized remediation plan by severity.
```

---

## Standard formula usage

```text
Use the SAST prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [BRANCH TO ANALYZE]
- files or modules to review: [PATHS — or "entire repository"]
- language and framework: [AUTO-DETECT]
- authentication model: [JWT / session / OAuth2 / API key / other]
- sensitive data handled: [PII / financial / credentials / none]
- documents to review: threat model if available (13-04), architecture, API contracts
- specific output goal: complete SAST report with remediation plan by severity
- depth level: high
```

---

## Expected output

### Executive summary

| Dimension | Result |
|---|---|
| Overall risk level | [CRITICAL / HIGH / MEDIUM / LOW] |
| Critical findings | N |
| High findings | N |
| Medium findings | N |
| Low findings | N |
| Informational | N |

### Findings table

| ID | OWASP Category | Severity | Component / Line | Description | Remediation | Est. CVSS |
|---|---|---|---|---|---|---|
| SAST-001 | A03 — Injection | CRITICAL | `api/views.py:42` | SQL query concatenated with user input | Use ORM or parameterized queries | 9.8 |
| SAST-002 | A02 — Crypto Failures | HIGH | `utils/auth.py:18` | Password hashed with MD5 | Migrate to bcrypt / Argon2 | 7.5 |

### Remediation plan

| Priority | Finding | Effort | Owner | Suggested deadline |
|---|---|---|---|---|
| 1 | SAST-001 — SQL Injection | Low | Backend dev | Immediate |
| 2 | SAST-002 — MD5 passwords | Medium | Dev + DBA | Current sprint |
