# 11.2 — Security hardening and operations

## Description

Prompt to analyze the repository and operational configuration for security strengthening opportunities: hardening, secrets management, permissions, service exposure and deployment risks.

**When to use it:** periodically as security review, before a production deployment, or when security findings are detected in code review.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | security |
| Expected risk | high — can expose infrastructure configuration and secrets if used carelessly |
| Required inputs | docker-compose, nginx configuration, `.env` (structure, not values), workflows, GitHub permissions, read access to recent commit history (git log) |
| Allowed tools | reading configuration and infrastructure — never execute configuration changes in the same step |
| Permitted autonomy | A0 — Analyze (only delivers findings and mitigation plan, does not apply changes) |
| Stop criteria | never include real secret values in the output, even if found exposed; reference only location and type |
| Expected output | see `## Expected output` |
| Minimum evidence | each finding must indicate the exact file/component and justified criticality |
| Recommended next prompt | `13-08-gestion-secretos-credenciales` if exposed credentials are detected; `13-03-secure-sdlc-revision` for a broader review |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze the repository and operational configuration to detect security strengthening opportunities, hardening, secrets management, permissions, service exposure and deployment risks.

Steps:
1. Inventory the available operational configuration sources (docker-compose, nginx, `.env`, CI/CD workflows, GitHub permissions) and confirm which are accessible before continuing; if one is missing, flag it instead of assuming that area is safe.
2. Review secrets management: look for hardcoded credentials, tokens, or keys in code, configuration, or recent commit history. Report only location and type, never the real value.
3. Review permissions: identify service accounts, CI/CD tokens, or roles with broader privileges than their function requires (principle of least privilege).
4. Review service exposure: unnecessarily published ports, services without authentication, admin endpoints reachable from outside the internal network.
5. Review insecure configuration: active debug flags, permissive CORS, missing security headers (CSP, HSTS, X-Frame-Options), misconfigured or disabled TLS.
6. Review vulnerable dependencies: packages with known CVEs or outdated versions of critical components (web framework, auth/crypto libraries).
7. Review logging and auditing: confirm there is enough logging to detect incidents, without that logging capturing sensitive data (PII, secrets) in plain text.
8. Prioritize findings by exploitability and impact: a secret exposed in an accessible repository is more urgent than a missing security header on a low-risk internal endpoint.

Constraints:
- never include the real value of a secret, credential, or token in the output, even if found exposed — reference only file, approximate line, and type,
- this is a read-only audit: don't apply configuration changes, rotate credentials, or restart services as part of the same step,
- if you find a credential that may have already been compromised, flag the need for immediate rotation and follow the team's responsible disclosure process — don't publish or share it outside the designated reporting channel,
- every proposed mitigation requires human review and approval before it's applied; don't run automated remediations or fix-it scripts,
- if you lack access to a required input, flag the omission explicitly in the output instead of completing the matrix with assumptions.

Deliver:
- findings,
- criticality,
- mitigation,
- priority.
```

---

## Use with standard formula

```text
Use the hardening and security prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [MAIN BRANCH]
- environment: [PROD / STAGING]
- components: [INFRASTRUCTURE, SERVICES, CONFIGURATIONS]
- documents to review: docker-compose, nginx, .env, workflows, GitHub permissions
- specific output objective: security findings report with prioritized mitigation plan
- depth level: high
```

---

## Expected output

| Finding | Category | Criticality | Component | Mitigation | Priority |
|---|---|---|---|---|---|
| Third-party API key hardcoded as a default value (`STRIPE_KEY`) | exposed secrets | critical | `docker-compose.override.yml:14` | move to a secrets manager (Vault / GitHub Actions secrets), rotate the exposed key, and purge it from git history | P0 |
| CI/CD token with `repo` scope (full access) used only to publish releases | excessive permissions | high | `.github/workflows/release.yml` | replace with a GitHub App scoped to `contents:write` and `packages:write` | P1 |
| PostgreSQL port 5432 published directly to the host | exposed services | high | `docker-compose.yml`, `db` service | remove the public port mapping and expose it only on the internal Docker network | P1 |
| CORS configured with `Access-Control-Allow-Origin: *` | insecure configuration | medium | `nginx.conf` | restrict the origin to known frontend domains | P2 |
| `lodash@4.17.15` dependency with a known prototype-pollution CVE | vulnerable dependencies | medium | `package.json` | upgrade to `>=4.17.21` | P2 |
| Login endpoint doesn't log failed attempts | insufficient logging | low | `auth/login` handler | add structured logging for failed attempts without recording the password or other sensitive data | P3 |
