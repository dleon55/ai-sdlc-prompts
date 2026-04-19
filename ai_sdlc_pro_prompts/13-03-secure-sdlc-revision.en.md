# 13.3 — Secure SDLC Review

## Description

Prompt to verify that required security controls have been applied in each phase of the development cycle: from design to deployment. Acts as a structured Secure SDLC checklist based on OWASP SAMM, NIST SSDF, and Microsoft SDL, adaptable to new projects and incremental changes.

**When to use:** at the close of each sprint, before a production release, as a project security maturity review, or when a new team or agent is onboarded to the project.

---

## Required prior context

> Include the block from `00-framework.md` before this prompt.
> Attach available relevant results: `13-01` (SAST), `13-02` (SCA), `13-04` (Threat Modeling).

---

## Full prompt

```text
Objective:
Verify the project's security maturity level by evaluating whether required controls
have been applied in each phase of the Secure SDLC, and generate an improvement plan
for identified gaps.

Phases and controls to evaluate:

1. REQUIREMENTS AND DESIGN PHASE
   □ Was threat modeling performed before implementation?
   □ Were explicit security requirements defined (not assumed)?
   □ Were sensitive data identified and classified (PII, financial, confidential)?
   □ Was the authentication and authorization model designed before coding?
   □ Were secure design principles considered?
     - Least privilege
     - Defense in depth
     - Fail securely
     - Separation of concerns
     - No security by obscurity
   □ Was the system attack surface documented?

2. IMPLEMENTATION PHASE
   □ Were secure coding guidelines followed for the project's language/framework?
   □ Is all input validated and sanitized at the correct layer (not just on the client)?
   □ Are parameterized queries / ORM used for database access?
   □ Is output encoding applied to prevent XSS?
   □ Are errors handled without exposing internal information to the client?
   □ Are HTTP security headers applied? (CSP, HSTS, X-Content-Type-Options, etc.)
   □ Are secrets managed via environment variables or vault, never in code?
   □ Are passwords stored with adaptive hashing (bcrypt, Argon2, scrypt)?
   □ Is HTTPS enforced on all endpoints, including internal ones?
   □ Is file size and type limited on upload endpoints?

3. SECURITY TESTING PHASE
   □ Was SAST executed as part of the CI pipeline? (see 13-01)
   □ Was SCA / dependency analysis performed? (see 13-02)
   □ Was dynamic security testing (DAST) performed on the QA environment?
   □ Were authentication and authorization tests performed (roles, permissions, JWT)?
   □ Were basic injection tests performed (SQL, Command, SSTI)?
   □ Were the most critical endpoints manually reviewed?
   □ Does the CI QA gate fail if there are high or critical severity security findings?

4. CODE REVIEW PHASE
   □ Is there a code review checklist with security items?
   □ Does at least one reviewer have application security knowledge?
   □ Were changes to authentication, authorization, and data handling reviewed?
   □ Were security assumptions in the code identified and documented?
   □ Were logs reviewed to confirm they do not include sensitive data?

5. CI/CD AND DEPLOYMENT PHASE
   □ Does the CI pipeline include security linting, SAST, and automated SCA?
   □ Are Docker images based on official and minimal versions (distroless, alpine)?
   □ Do containers run as a non-root user?
   □ Are production secrets managed with a dedicated system? (Vault, AWS Secrets Manager, etc.)
   □ Is least privilege applied to service permissions?
   □ Is there a tested rollback process for security-problematic deployments?
   □ Are build artifacts signed or verified with checksums?

6. OPERATIONS AND MONITORING PHASE
   □ Are security events recorded in structured logs?
     (failed logins, permission changes, sensitive data access)
   □ Are alerts configured for anomalous patterns?
   □ Is there a security incident response process? (see 11-04)
   □ Is periodic review of access and permissions performed?
   □ Are security patches applied in a reasonable timeframe?
     (critical: ≤24h, high: ≤7 days, medium: ≤30 days)
   □ Are periodic penetration tests or security reviews performed? (see 13-06)

7. MATURITY BY DOMAIN (simplified OWASP SAMM)
   Evaluate the current level for each domain on a 0-3 scale:
   - Governance (policies, training, compliance)
   - Design (threat modeling, security requirements)
   - Implementation (secure coding, defect management)
   - Verification (security testing, code review)
   - Operations (incident management, environment management)

Deliverables:
- complete checklist with status for each control (✅ compliant / ⚠️ partial / ❌ non-compliant / N/A),
- maturity level per phase (0-3),
- summary of critical gaps,
- prioritized improvement plan with owner and suggested timeline,
- maturity roadmap: what to achieve in the next sprint / quarter / semester.
```

---

## Standard formula usage

```text
Use the Secure SDLC review prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [MAIN BRANCH]
- current cycle phase: [DESIGN / IMPLEMENTATION / QA / PRE-RELEASE / OPERATIONS]
- available results: [SAST 13-01 / SCA 13-02 / Threat Model 13-04 / none]
- project type: [NEW / INCREMENTAL CHANGE / MAINTENANCE]
- target environment: [DEV / QA / STAGING / PROD]
- documents to review: architecture, CI/CD workflows, project security policies
- specific output goal: complete checklist + improvement plan with maturity levels
- depth level: high
```

---

## Expected output

### Checklist by phase

| Phase | Control | Status | Evidence / Note |
|---|---|---|---|
| Design | Threat modeling performed | ✅ / ⚠️ / ❌ | |
| Implementation | Secrets in vault, not in code | ✅ / ⚠️ / ❌ | |
| CI/CD | SAST in pipeline | ✅ / ⚠️ / ❌ | |

### Maturity level by domain (SAMM)

| Domain | Current level | Target level | Gap |
|---|---|---|---|
| Governance | 1 / 3 | 2 / 3 | No formal security policy |
| Design | 0 / 3 | 2 / 3 | No threat modeling performed |
| Implementation | 2 / 3 | 3 / 3 | Missing formal coding guidelines |
| Verification | 1 / 3 | 3 / 3 | SAST and DAST not integrated in CI |
| Operations | 2 / 3 | 3 / 3 | No security alerts in production |

### Improvement plan

| Priority | Gap | Action | Owner | Timeline |
|---|---|---|---|---|
| 1 | SAST not in CI | Integrate bandit/semgrep into pipeline | DevOps | Current sprint |
