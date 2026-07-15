# 17.1 — Technical Onboarding Checklist

## Description

Prompt to generate a concrete, actionable technical onboarding checklist for a new engineering team member: access to provision (repositories, cloud, CI/CD tooling, secrets manager), tools to install/configure locally, and documentation/context to review during the first week. The checklist is tailored to the role and the team's tech stack, distinguishes what is blocking for day 1 from what is expected during week 1, and assigns an owner to each item. It does not grant access or create accounts: it generates the checklist for a human with the corresponding permissions (tech lead, IT, IAM administrator) to execute.

**When to use it:** when bringing a new member onto the engineering team, before or during their first day. Complements `17-02-offboarding-tecnico` as its symmetric counterpart: this prompt generates the checklist of what to grant and configure on the way in; `17-02-offboarding-tecnico` generates the checklist of what to revoke and deactivate on the way out.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation/planning |
| Expected risk | medium — an incomplete access checklist delays the new member's productivity; an excessive checklist (extra access, elevated permissions without justification) carries security implications, even though the prompt itself never grants any real access |
| Required inputs | role and seniority of the new team member, team tech stack and tooling (repos, cloud provider, CI/CD tooling, secrets manager), access level required by the role, start date, assigned mentor/buddy if any, available internal documentation (wiki, runbooks, architecture guides) |
| Allowed tools | reading existing internal documentation about the team's stack, processes, and access structure; the output is a text checklist — it does not create accounts, does not grant IAM permissions, does not configure tooling; execution of the actual access provisioning is delegated to whoever holds IAM permissions, not to this prompt |
| Permitted autonomy | A0 — Analyze (survey the role, stack, and the team's existing access setup); A1 — Propose (the checklist of access, tools, and documentation to review); never A2/A3 — this prompt does not create accounts, grant permissions, or make changes to identity/access systems |
| Stop criteria | stop and ask for clarification if the role or the team's stack is not specified — never fabricate a generic checklist without context; escalate to whoever holds IAM permissions before any listed access is granted; if information about the team's secrets manager or least-privilege policy is missing, state this explicitly instead of assuming it |
| Expected output | see `## Expected output` |
| Minimum evidence | each checklist item states the specific system or tool, the owner responsible for granting or configuring it, and whether it is blocking for day 1 or expected during week 1 |
| Recommended next prompt | `17-02-offboarding-tecnico` as its symmetric counterpart, so both flows are documented consistently |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as the Tech Lead responsible for onboarding. Generate a concrete, actionable technical onboarding checklist for the described new team member, tailored to their role and the team's stack, covering access to provision, tools to install/configure, and documentation to review during their first week. Do not grant any access or execute any configuration: the resulting checklist must be executed by a person with the corresponding permissions (tech lead, IT, IAM administrator).

Inputs:
- role and seniority of the new team member: [ex: Backend Engineer Mid-Senior / SRE / Data Engineer]
- team tech stack: [LANGUAGES, FRAMEWORKS, DATABASES]
- relevant repositories: [LIST OF REPOS OR "to define with the team lead"]
- cloud provider(s): [AWS / GCP / AZURE / OTHER]
- CI/CD tooling: [ex: GitHub Actions, Jenkins, CircleCI, GitLab CI]
- secrets manager: [ex: HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, 1Password — or "not defined"]
- access level required by the role: [MINIMUM NECESSARY / ELEVATED WITH JUSTIFICATION]
- start date: [DATE]
- assigned mentor/buddy: [NAME OR "to be assigned"]
- available internal documentation: [WIKI, RUNBOOKS, ARCHITECTURE GUIDES — or "not available"]

Steps:

1. ROLE AND STACK SURVEY
   Confirm the role, seniority, and the specific tools that role needs to touch given the team's stack. If critical information is missing (role or stack not specified), stop and ask for clarification instead of generating a generic checklist.

2. REPOSITORY ACCESS
   List the repositories the new team member needs access to, the required permission level (read, write, protected-branch administration) based on their role, and who is responsible for granting it (ex: organization administrator in GitHub/GitLab).

3. CLOUD ACCESS
   List the accounts and IAM roles needed in the indicated cloud provider(s), applying the least-privilege principle by default. Explicitly flag any elevated access (admin, production permissions) and require it to be justified by the role before being granted.

4. CI/CD TOOLING ACCESS
   List the access needed in the team's CI/CD tooling (view pipelines, trigger builds, manage pipeline secrets), distinguishing read-only permissions from those that allow modifying or triggering deployments.

5. SECRETS MANAGER ACCESS
   List which secrets or namespaces in the secrets manager the role needs, at what access level (reading specific secrets vs. administration), and who approves granting it. If the team has no formalized secrets manager, flag this as a risk to resolve before continuing with ad-hoc access.

6. COMMUNICATION AND MANAGEMENT TOOLS
   List access to the team's communication and management tools (chat, ticketing/project tool, collaborative documentation) needed to operate from day 1.

7. LOCAL TOOLS AND ENVIRONMENT
   List what the new team member must install/configure locally: IDE and recommended extensions, package manager and language/runtime version, the team's linters/formatters, local containers/orchestration if applicable, VPN client if the team requires it, SSH/GPG key generation and registration.

8. DOCUMENTATION AND CONTEXT TO REVIEW IN THE FIRST WEEK
   List the internal documentation to review before contributing code autonomously: architecture overview, code style/conventions guide, the team's code review and deployment process, on-call/incident policy if applicable, product domain glossary. If any document does not exist, flag it as a gap to resolve instead of silently omitting it.

9. PRIORITY AND OWNER CLASSIFICATION
   For each checklist item (access, tools, documentation), state: (a) whether it is blocking for day 1 or expected during week 1, and (b) who is the owner responsible for granting, installing, or sharing it.

10. EXECUTIVE SUMMARY
    Summarize how many day-1 blocking access items exist, who the key owners are to coordinate before the start date, and any documentation or secrets-manager gap detected.

Constraints:
- this prompt generates the checklist; it never creates accounts, grants IAM permissions, generates credentials, or executes provisioning commands (`aws iam`, `gcloud projects add-iam-policy-binding`, Git provider organization invitations, etc.) — that execution always remains the responsibility of a human with the corresponding permissions.
- apply the least-privilege principle by default: do not include administrative or production access unless the role explicitly justifies it, and flag such items so they receive additional approval.
- never include passwords, tokens, API keys, or any real credential (nor a plausible-looking sample one) in the checklist.
- always distinguish access/tasks blocking for day 1 from those expected during week 1; do not treat the entire checklist as equally urgent.
- if information about the role, the stack, or the team's secrets manager is missing, say so explicitly and ask for it instead of inventing a generic checklist or assuming tools the team does not use.
```

---

## Use with standard formula

```text
Use the technical onboarding checklist prompt and adapt it to:
- repository/team: [NAME OR URL]
- role and seniority of the new team member: [ex: Backend Engineer Mid-Senior]
- tech stack: [LANGUAGES, FRAMEWORKS, DATABASES]
- cloud provider: [AWS / GCP / AZURE]
- CI/CD tooling: [ex: GitHub Actions]
- secrets manager: [ex: AWS Secrets Manager or "not defined"]
- access level required: [MINIMUM NECESSARY / ELEVATED WITH JUSTIFICATION]
- start date: [DATE]
- documents to review: internal wiki, runbooks, architecture guide
- specific output objective: checklist of access, tools, and documentation prioritized by day 1 / week 1, with an owner per item
- depth level: high
```

---

## Expected output

| Category | Item | Access level / detail | Owner | Priority |
|---|---|---|---|---|
| Repository | Read/write access to `org/payments-service` | write on feature branches, no direct push to `main` | GitHub organization admin | Day 1 blocking |
| Cloud | `developer-readonly` IAM role in staging AWS account | read-only, no production access | Tech lead / IAM administrator | Day 1 blocking |
| CI/CD | Read access to the repo's GitHub Actions pipelines | view builds and logs, no permission to modify workflows | Tech lead | Day 1 blocking |
| Secrets manager | Access to the `payments/staging` namespace in Vault | read staging secrets only | Security lead / DevOps | Week 1 |
| Communication | Added to team Slack channel and Jira board | standard member access | Direct manager | Day 1 blocking |
| Local environment | Install Docker, project's LTS Node version, team linter | per repo setup guide | New team member (with buddy support) | Day 1 blocking |
| Documentation | Review architecture guide and code review process | reading and confirming understanding with the buddy | Assigned buddy | Week 1 |

> Note: the full checklist should cover every category relevant to the given role and stack (repos, cloud, CI/CD, secrets manager, communication/management, local environment, documentation), one row per item, avoiding elevated access without explicit justification.

### Executive summary

- **Day 1 blocking access items:** [N] items — key owners to coordinate before the start date: [LIST].
- **Access/tasks expected during week 1:** [N] items.
- **Gaps detected:** [missing documentation, non-formalized secrets manager, or another risk flagged during the survey].
- **Elevated access requiring additional approval:** [LIST OR "none"].
