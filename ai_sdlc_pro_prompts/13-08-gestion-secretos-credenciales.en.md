# 13.8 — Secrets and Credentials Management

## Description

Prompt to audit, classify, and remediate secrets management in source code, infrastructure, CI/CD pipelines, and runtime environments: detects hardcoded credentials, exposed tokens, insecure configurations, and establishes secure secrets management practices with rotation and centralized storage.

**When to use:** as a preventive review before a PR, after receiving secret scanning alerts (GitHub Secret Scanning, Gitleaks, truffleHog), when onboarding to a project to audit historical state, or as part of the Secure SDLC review (`13-03`).

---

## Required prior context

> Include the block from `00-framework.md` before this prompt.
> If a result from `13-03` (Secure SDLC review) exists, use it to identify prior secrets management findings.

---

## Full prompt

```text
Objective:
Audit, classify, and remediate secrets and credentials management in source code,
Git history, infrastructure, CI/CD pipelines, and runtime environments;
establish secure storage, access, rotation, and auditing practices for secrets.

Steps:

1. EXPOSED SECRETS INVENTORY AND DETECTION
   Analyze the following exposure surfaces:
   
   a) Current source code:
      - hardcoded credentials: passwords, API keys, tokens, private keys
      - connection strings with embedded credentials (DSN, JDBC, MongoDB URI)
      - fixed encryption keys or salts in code
      - committed certificates or private keys (.pem, .key, .pfx)
      - test payloads with real data or real secrets
   
   b) Git history (previous commits):
      - secrets removed from code but remaining in history
      - commits with "remove secret" or "fix credentials" messages (past exposure indicators)
      - branches or tags with secrets no longer in main
      ⚠️ Secrets in Git history must be considered compromised until rotated
   
   c) Configuration files:
      - `.env`, `.env.local`, `.env.production` committed to the repository
      - `config.yml`, `settings.json`, `application.properties` with real values
      - Terraform, Ansible, Helm files with secrets directly interpolated
      - `docker-compose.yml` with hardcoded environment variables
   
   d) CI/CD and automation:
      - secrets embedded in workflow files (GitHub Actions, GitLab CI, Jenkins)
      - environment variables visible in CI/CD logs
      - deployment scripts with inline credentials
   
   e) Dependencies and packages:
      - npm/pip/composer packages including keys in their default configuration
      - `package.json`, `composer.json` files with private registry tokens

2. CLASSIFICATION AND CRITICALITY
   For each secret found, classify:
   
   Secret type:
   - Database credential (critical — data access)
   - External service API key (high — depends on service)
   - OAuth token / JWT secret (high — can impersonate users)
   - SSH / TLS private key (critical — infrastructure access)
   - Symmetric encryption key (critical — data decryption)
   - Webhook secret (medium — depends on scope)
   - Cloud service key (critical — full infrastructure access)
   
   Status:
   - ACTIVE: secret is still valid and in use → rotate immediately
   - EXPIRED: no longer valid → document and suppress alert
   - REVOKED: invalidated after detection → verify rotation is complete
   - UNKNOWN: validity cannot be determined → assume active, rotate

3. CURRENT MANAGEMENT PRACTICES ASSESSMENT
   Audit the existing secrets management infrastructure:
   
   a) Storage:
      - is a centralized secrets manager used? (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, Doppler)
      - are environment secrets injected at runtime or stored in files?
      - are `.env` files correctly listed in `.gitignore`?
   
   b) Access and control:
      - who has access to production secrets?
      - is the principle of least privilege applied? (each service only accesses its own secrets)
      - is there an audit trail for secrets access?
      - do API keys have scope reduced to the minimum necessary?
   
   c) Rotation:
      - is there a credential rotation policy? (frequency by type)
      - is rotation automated or manual?
      - do secrets have expiration dates configured?
   
   d) CI/CD:
      - are provider-encrypted environment variables used? (GitHub Secrets, GitLab CI Variables, Jenkins Credentials)
      - do CI/CD logs mask sensitive environment variables?
      - are secrets passed between jobs without unnecessary exposure?

4. PREVENTIVE DETECTION VERIFICATION
   Evaluate whether preventive controls are active:
   - is there a pre-commit hook to detect secrets? (gitleaks, detect-secrets, git-secrets)
   - is GitHub Secret Scanning enabled (if using GitHub)?
   - is there secrets scanning in the CI/CD pipeline?
   - are secret detection alerts reviewed and closed systematically?
   - do developers know how to report an accidental exposure?

5. REMEDIATION PLAN
   For each active secret found:
   
   a) Immediate action (within the first hours):
      - revoke / rotate the secret at the service provider
      - update the secret in the secrets manager or target system
      - verify the application works with the new secret
      - if the secret was exposed → review access logs of the affected service for unauthorized use
   
   b) Repository cleanup:
      - if the secret is only in current code: remove and commit with a clear message
      - if the secret is in Git history: use `git filter-repo` to rewrite history
        ⚠️ This requires a force push — coordinate with the team, everyone must re-clone
      - add the secret to `.gitignore` to prevent accidental recommit
   
   c) Structural improvements:
      - migrate secrets to a centralized manager if none exists
      - implement runtime secret injection (environment variables from Vault/AWS SSM)
      - install pre-commit hook in the repository
      - train the team on secrets handling practices

6. STANDARDS AND BEST PRACTICES
   Define or verify the project's secrets policies:
   
   a) Naming and documentation:
      - inventory of all secrets with: name, service, owner, rotation date, expiration
      - document which secrets exist (not their values)
   
   b) Rotation policy by type:
      - DB credentials: every 90 days or after any personnel change with access
      - External service API keys: per provider policy, minimum every 180 days
      - SSH keys: every 12 months or when a team member leaves
      - Encryption keys: versioning policy; rotation implies data re-encryption
      - CI/CD tokens: every 90 days
   
   c) Response to exposure:
      - procedure: detect → revoke → rotate → audit logs → document
      - maximum response time: 1 hour for critical, 24 hours for high

Recommended tools:
- Detection in code: gitleaks, truffleHog, detect-secrets, semgrep (secrets rules)
- Detection in CI/CD: GitHub Secret Scanning, GitLab Secret Detection, Snyk
- Centralized management: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Doppler
- History cleanup: git-filter-repo (replacement for git-filter-branch)
- Pre-commit hooks: pre-commit framework with gitleaks or detect-secrets

Deliverables:
- inventory of detected secrets with classification and status (active/expired/revoked),
- prioritized remediation plan by criticality with rotation SLA,
- current assessment of secrets management practices (checklist),
- architecture recommendations for centralized secure management,
- checklist of preventive controls to implement.
```

---

## Standard formula usage

```text
Use the secrets management prompt and adapt it to:
- repository: [NAME OR URL]
- technology stack: [language, framework, cloud provider]
- current secrets manager: [none / .env files / Vault / AWS Secrets Manager / other]
- CI/CD used: [GitHub Actions / GitLab CI / Jenkins / other]
- service providers with credentials: [AWS / GCP / Stripe / SendGrid / etc.]
- depth of Git history analysis: [recent commits only / full history]
- documents to review: .env.example, CI/CD workflows, infrastructure files (Terraform, Helm, docker-compose)
- specific output goal: exposed secrets inventory + remediation plan + controls checklist
- depth level: high
```

---

## Expected output

### Detected secrets inventory

| ID | Type | Location | Status | Severity | Required action | SLA |
|---|---|---|---|---|---|---|
| SEC-001 | DB credential | `config/database.yml:12` | ACTIVE | CRITICAL | Rotate + migrate to Vault | 1 hour |
| SEC-002 | Stripe API key | `git log —commit a3f2b1` (history) | UNKNOWN | HIGH | Revoke in Stripe dashboard + clean history | 2 hours |
| SEC-003 | AWS Access Key | `.github/workflows/deploy.yml:34` | ACTIVE | CRITICAL | Revoke IAM, migrate to GitHub Secrets + OIDC | 1 hour |

### Current practices assessment

| Control | Status | Recommendation |
|---|---|---|
| Centralized secrets manager | ❌ Not implemented | Implement HashiCorp Vault or AWS Secrets Manager |
| Pre-commit detection hook | ❌ Not implemented | Install gitleaks as pre-commit hook |
| GitHub Secret Scanning | ⚠️ Not verified | Enable in repository settings |
| `.env` in `.gitignore` | ✅ Correct | Verify all environments (.env.*) |
| Documented rotation policy | ❌ Does not exist | Create policy and assign owners per secret |
