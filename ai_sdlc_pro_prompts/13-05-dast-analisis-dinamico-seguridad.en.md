# 13.5 — DAST: Dynamic Application Security Analysis

## Description

Prompt to design and execute dynamic application security testing (DAST) against a running application: identifies exploitable vulnerabilities in real time, validates the exposed attack surface, and tests security controls at the transport layer, authentication, session management, and APIs.

**When to use:** when the application can be started in an isolated environment (local, staging, Docker), before promoting to production, or as part of the CI/CD pipeline in the security validation phase. Complements static analysis (`13-01` SAST) and threat modeling (`13-04`).

---

## Required prior context

> Include the block from `00-framework.md` before this prompt.
> Attach results from `13-04` (Threat Modeling) to use the identified attack surface as a testing guide.
> Attach results from `13-01` (SAST) if available, to complement with dynamic findings.

---

## Full prompt

```text
Objective:
Perform dynamic application security testing (DAST) against the running application,
identifying exploitable vulnerabilities in real time, validating the exposed attack surface,
and testing transport, authentication, session management, and API security controls.

Steps:

1. DYNAMIC ATTACK SURFACE RECONNAISSANCE
   With the application running, map:
   - All accessible HTTP/HTTPS endpoints (routes, methods, parameters)
   - Exposed REST or GraphQL APIs: endpoints, accepted methods, response types
   - Web forms and input fields (GET and POST)
   - Publicly accessible static files and directories
   - HTTP response headers and cookies
   - Exposed authentication mechanisms (login, OAuth, tokens, API keys)
   - Redirect flows and session management

2. TRANSPORT LAYER ANALYSIS
   Verify communication security:
   
   a) TLS/SSL:
      - Protocol version: TLS 1.2+ only? TLS 1.0/1.1 disabled?
      - Cipher suites: weak suites enabled? (RC4, DES, 3DES, NULL)
      - Certificate: validity, trust chain, wildcard, SANs
      - HSTS: Strict-Transport-Security header present with max-age ≥ 31536000?
      - HSTS includeSubDomains and preload enabled
   
   b) HTTP security headers:
      - Content-Security-Policy (CSP): present? restricts inline scripts and sources?
      - X-Frame-Options or frame-ancestors in CSP: clickjacking protection
      - X-Content-Type-Options: nosniff
      - Referrer-Policy: does not expose internal URLs
      - Permissions-Policy: limits access to browser APIs
      - Cache-Control on responses containing sensitive data

3. AUTHENTICATION AND SESSION TESTING
   
   a) Authentication mechanism:
      - User enumeration possible? (different responses for wrong username vs. wrong password)
      - Rate limiting or CAPTCHA implemented?
      - Credentials transmitted in plaintext or GET parameters?
      - API keys or tokens appearing in URLs, logs, or unprotected headers?
   
   b) Session management:
      - Session cookies with HttpOnly, Secure, SameSite=Strict/Lax attributes?
      - Session ID sufficiently random? (minimum 128 bits of entropy)
      - Session ID regenerated after successful login?
      - Session properly invalidated on logout?
      - Origin verified on state-changing requests? (CSRF protection)

4. INJECTION TESTING (DYNAMIC)
   Submit payloads at all entry points to detect:
   
   a) SQL Injection (if DB technology applies):
      - Basic payloads: `'`, `''`, `1' OR '1'='1`, `1; DROP TABLE`, `UNION SELECT NULL`
      - Error behavior: database messages exposed in response?
      - Blind SQL: compare response times with `1 AND SLEEP(3)`
   
   b) Cross-Site Scripting (XSS):
      - Reflected XSS: `<script>alert(1)</script>` in GET/POST parameters
      - Stored XSS: submit payload in fields that persist and are later displayed
      - DOM-based XSS: check handling of `document.location`, `innerHTML`, `eval()`
      - CSP bypass: is the payload blocked or executed despite the CSP?
   
   c) OS Command Injection:
      - `; ls`, `| id`, `&& whoami`, `$(id)` in input fields processed by the system
   
   d) SSRF (Server-Side Request Forgery):
      - Internal URLs in URL fields: `http://localhost:8080/admin`, `http://169.254.169.254/`
      - Alternative protocols: `file:///etc/passwd`, `dict://`, `gopher://`
   
   e) XXE (XML External Entity) if the app processes XML:
      - External entity payloads in XML documents sent to the server

5. ACCESS CONTROL TESTING
   
   a) Horizontal access control (IDOR):
      - Access another user's resources by changing IDs in URL or body? (e.g., `/api/users/123` → `/api/users/124`)
      - Modify or delete another user's resources with own session?
   
   b) Vertical access control (privilege escalation):
      - Can an unprivileged user access admin routes?
      - Does changing roles or permissions in the JWT token modify access?
      - Admin API endpoints accessible without authentication?
   
   c) Unauthorized HTTP methods:
      - PUT, DELETE, PATCH allowed on resources that should not accept them?
      - OPTIONS revealing unexpected methods?

6. INFORMATION EXPOSURE TESTING
   Verify the application does not expose:
   - Stack traces or detailed error messages in responses (framework names, versions, internal paths)
   - Sensitive data in JSON responses not needed by the client
   - Accessible configuration files: `.env`, `config.json`, `database.yml`, `.git/config`
   - Listable directories or residual files (`.bak`, `.old`, `~`, `.swp`)
   - Tokens, keys, or credentials in HTML comments or JavaScript

7. FINDING DOCUMENTATION AND CLASSIFICATION
   For each vulnerability found:
   - Unique ID: DAST-XXX
   - OWASP category (A01-A10)
   - Exact reproduction method: URL, HTTP method, payload, headers
   - Server response confirming the vulnerability
   - Potential impact if exploited
   - CVSS v3.1 severity (full vector)
   - Recommended remediation
   - Status: confirmed / requires manual verification / false positive

Recommended tools (use in isolated environment, never in production without authorization):
- OWASP ZAP (Zed Attack Proxy): automated scanning + manual testing
- Burp Suite Community/Pro: traffic interception and modification
- Nikto: web server and insecure configuration scanning
- Nuclei: known vulnerability templates (CVEs)
- testssl.sh or ssllabs: TLS configuration analysis
- sqlmap: automated SQLi detection (ONLY on owned environments with authorization)

Deliverables:
- dynamic attack surface map (endpoints, forms, APIs),
- DAST findings table (ID, OWASP, severity, reproducible payload, remediation),
- security controls summary: which pass and which fail,
- comparison with SAST findings to identify vulnerabilities not caught statically,
- prioritized remediation plan by CVSS.
```

---

## Standard formula usage

```text
Use the DAST prompt and adapt it to:
- repository: [NAME OR URL]
- test environment: [BASE URL where the application is running — staging / local Docker]
- technology stack: [frontend / backend / DB / authentication]
- application type: [traditional web / SPA / REST API / GraphQL API]
- authentication mechanism: [sessions / JWT / OAuth2 / API key]
- highest-risk areas from threat model: [ATTACH 13-04 RESULT if available]
- available tools: [ZAP / Burp Suite / Nikto / none — manual only]
- documents to review: source code, threat model 13-04, SAST results 13-01
- specific output goal: DAST findings table + attack surface map
- depth level: high
```

---

## Expected output

### Dynamic attack surface map

| Endpoint | Method | Auth required | Input parameters | Notes |
|---|---|---|---|---|
| `/api/users` | GET | Yes — JWT | `page`, `limit` | Verify IDOR |
| `/api/search` | GET | No | `q` | Candidate for reflected XSS |
| `/login` | POST | No | `username`, `password` | Verify user enumeration |

### DAST findings table

| ID | OWASP | Severity | Endpoint | Payload / Method | Impact | Remediation | CVSS |
|---|---|---|---|---|---|---|---|
| DAST-001 | A03 — Injection | CRITICAL | `/api/search?q=` | `<script>alert(1)</script>` | Reflected XSS — session hijacking | Escape output, strengthen CSP | 8.1 |
| DAST-002 | A05 — Misc. Config | MEDIUM | Response header | (absent) | Missing X-Frame-Options — clickjacking possible | Add `X-Frame-Options: DENY` | 5.3 |

### Security controls summary

| Control | Status | Observation |
|---|---|---|
| TLS 1.3 active | ✅ Pass | Correct protocol |
| HSTS enabled | ⚠️ Partial | Missing `includeSubDomains` |
| Content-Security-Policy | ❌ Fail | Policy absent — XSS unmitigated |
| Secure cookies (HttpOnly + Secure) | ✅ Pass | Correct attributes |
| Login rate limiting | ❌ Fail | No rate limiting — brute force possible |
