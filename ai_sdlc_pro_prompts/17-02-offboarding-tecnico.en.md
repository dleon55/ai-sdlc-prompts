# 17.2 — Technical Offboarding Checklist

## Description

Prompt to generate the technical offboarding checklist when a team member leaves the team or the organization: which access needs to be revoked (repositories, cloud accounts, secrets manager, SSO, CI/CD pipelines), what knowledge needs to be transferred before the person leaves (document what only that person knew, reassign ownership of services, repositories, and on-call rotations), and which orphaned credentials need to be verified (personal access tokens, SSH keys, service accounts created under their name). The prompt does not revoke anything by itself: it produces the checklist for a human with administrative permissions (IAM, SSO, secrets manager) to execute, with explicit focus on the security risk that a forgotten access represents.

**When to use it:** as soon as a team member's departure date is confirmed (resignation, termination, contract end, team change resulting in loss of access), ideally with enough lead time to plan knowledge transfer before the last day. It is the symmetric counterpart of `17-01-onboarding-tecnico`: while that prompt manages onboarding and initial access grants, this one manages departure and complete access revocation. It does not replace the actual execution of revocation (which requires administrative permissions on each system) or an HR process: it is the technical layer that ensures no critical access, credential, or knowledge is left uncovered after departure.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | security |
| Expected risk | high — an incomplete technical offboarding leaves active access, valid tokens, or orphaned service accounts under the name of someone who should no longer have them, which is a direct path to data leakage or unauthorized access; the risk is high even though the prompt itself only generates the checklist, because the cost of missing an item is paid by the organization, not by the prompt |
| Required inputs | role of the person leaving the team and the access/systems known to be theirs, services/repositories/on-call rotations they own or maintain, confirmed departure date, list of the organization's access-managing systems (repos, cloud, secrets manager, SSO, CI/CD) |
| Allowed tools | reading access inventories, repository and ownership lists, existing documentation, and on-call records; the output is a text checklist — it does not execute revocations, does not delete keys, and does not disable accounts on any system |
| Permitted autonomy | A1 — Propose (generates the revocation, transfer, and verification checklist); never A2/A3 — actual access revocation requires human execution with administrative permissions on each system (IAM, SSO, secrets manager, CI/CD), and must be completed on or before the departure date |
| Stop criteria | stop and escalate if the complete list of access or systems the person had access to is not known — explicitly flag it as a residual risk instead of assuming the list is complete; stop if there is no confirmed departure date and use that gap as a blocker to set concrete deadlines in the checklist |
| Expected output | see `## Expected output` |
| Minimum evidence | each checklist item states the specific system or access affected, the responsible party for executing it (a role or person, not "the team"), the deadline (before/on/after the departure date), and whether it depends on a prior item (e.g., reassigning ownership before revoking the departing owner's access) |
| Recommended next prompt | `17-01-onboarding-tecnico` — its symmetric counterpart, for the person taking over the reassigned ownership or on-call rotation |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as the person responsible for access security and operations. Generate the complete technical offboarding checklist for the person leaving the team, covering access revocation, knowledge and ownership transfer, and verification of orphaned credentials. Do not execute any revocation: produce the checklist for a human with administrative permissions on each system to execute.

Inputs:
- person leaving the team (role/function): [ROLE OR FUNCTION]
- known access and systems they had access to: [REPOSITORIES / CLOUD ACCOUNTS / SECRETS MANAGER / SSO / CI-CD / OTHER — or "incomplete list, requires audit" if applicable]
- services, repositories, or on-call rotations they own or maintain: [KNOWN LIST]
- confirmed departure date: [DATE]
- organization systems that manage access: [REPO PROVIDER, CLOUD PROVIDER, SECRETS MANAGER, SSO PROVIDER, CI/CD TOOL]

Steps:

1. INVENTORY OF KNOWN ACCESS
   Based on the inputs, list all known systems and access the person has, grouped by category: code repositories, cloud accounts and roles, secrets manager, SSO/identity, CI/CD pipelines, internal tools (admin panels, dashboards, message queues, databases).
   - if the access list is incomplete or comes only from the team's memory (not from a centralized inventory), explicitly flag it as "residual risk — list not verified against an access inventory" instead of assuming it is complete.

2. ACCESS REVOCATION CHECKLIST
   For each access identified in step 1, generate an actionable checklist item: specific system/access, action to take (revoke role, disable account, remove from organization/team, rotate a shared credential if they knew it), suggested responsible party (whoever has administrative permissions on that system), and deadline (before the departure date, on the same day, or immediately after if the access is needed until the last day).

3. OWNERSHIP TRANSFER
   For each service, repository, or on-call rotation the person owns or maintains, generate a checklist item: what is being transferred, to whom (receiving person or team, to be defined by the responsible party if not yet identified), and the deadline to complete the transfer before the departing owner's access is revoked. Explicitly flag the dependency order: ownership transfer must be completed BEFORE the corresponding access is revoked, never after.

4. TRANSFER OF UNDOCUMENTED KNOWLEDGE
   Identify and list what critical knowledge might exist only in this person's head (undocumented design decisions, manual procedures, key external contacts, passwords or access not centrally managed, historical context on incidents or decisions). For each item, propose a concrete capture action (documented handover session, wiki/runbook entry, recorded walkthrough) with a responsible party and deadline before the departure date.

5. VERIFICATION OF ORPHANED CREDENTIALS
   Generate a specific verification checklist for credentials that could survive the person's departure if not actively reviewed: personal access tokens (PATs) issued under their name, SSH keys associated with their account or deployed on servers, service accounts or API keys created "under their name" or identity for automations, active SSO sessions not closed, shared credentials only they knew. For each category, indicate how to verify none remain orphaned (audit of active tokens, search for SSH keys in relevant servers' `authorized_keys`, review of service accounts without a clear owner).

6. ORDER AND DEPENDENCIES OF THE CHECKLIST
   Order the complete checklist respecting dependencies: first ownership transfer and knowledge capture (while the person is still available to consult), then access revocation (on or after the departure date), and finally orphaned credential verification (after revocation, as a closing control).

7. EXECUTIVE SUMMARY AND RESIDUAL RISKS
   Summarize how many items remain pending per category (revocation, transfer, verification), which are blocking before the departure date, and explicitly flag any residual risk: uninventoried access, ownership without an assigned receiver, or organization systems without a centralized revocation process.

Constraints:
- never execute or simulate having executed an access revocation, credential deletion, or ownership change: this prompt only produces the checklist, execution is the responsibility of a person with administrative permissions on each system.
- never assume the person's access list is complete unless it comes from a verified centralized inventory: flag incompleteness as an explicit residual risk.
- never reorder the checklist so that an access is revoked before its ownership has been transferred to a concrete receiver, unless there is an explicit security reason to do so (e.g., departure for disciplinary cause).
- if the departure date is not confirmed, say so explicitly and use a placeholder date marked "PENDING CONFIRMATION" instead of inventing one.
- always prioritize higher-sensitivity access (cloud with administrative permissions, secrets manager, SSO) over lower-sensitivity access when ordering the checklist, even if both share the same nominal deadline.
```

---

## Use with standard formula

```text
Use the technical offboarding prompt and adapt it to:
- person leaving the team (role/function): [ROLE]
- known access and systems: [REPOSITORIES / CLOUD / SECRETS MANAGER / SSO / CI-CD]
- services/repositories/on-call they own: [LIST]
- confirmed departure date: [DATE]
- organization systems to consider: [SPECIFIC PROVIDERS]
- documents to review: access inventory, repo/service ownership table, on-call calendar
- specific output objective: actionable checklist for revocation, transfer, and verification with a responsible party and deadline per item
- depth level: high
```

---

## Expected output

| Category | Item | Specific system/access | Responsible | Deadline | Depends on |
|---|---|---|---|---|---|
| Ownership transfer | Reassign ownership of the `payments-service` repository | GitHub — `acme` organization | Payments team tech lead | before the departure date | — |
| Knowledge transfer | Document the manual reconciliation procedure for failed payments (only known to this person) | Internal runbook / wiki | Departing person + receiving tech lead | before the departure date | — |
| Access revocation | Remove from GitHub organization and teams | GitHub — `acme` organization | GitHub org administrator | on the departure date | ownership of `payments-service` already reassigned |
| Access revocation | Revoke IAM role and disable user | AWS — production account | Cloud/IAM administrator | on the departure date | — |
| Access revocation | Disable SSO account and close active sessions | Okta / SSO provider | Identity administrator | on the departure date | — |
| Access revocation | Rotate shared secrets the person knew | Secrets manager (Vault/1Password) | Secrets manager administrator | on or before the departure date | — |
| Orphaned credential verification | Audit and revoke personal access tokens (PATs) issued under their name | GitHub / GitLab / CI-CD | Administrator of the corresponding platform | immediately after account revocation | account already disabled |
| Orphaned credential verification | Search for and remove associated SSH keys on relevant servers | Production servers / bastion hosts | Infrastructure team | immediately after account revocation | — |
| Orphaned credential verification | Identify service accounts or API keys created "under their name" and reassign or delete them | Cloud / CI-CD / internal integrations | Cloud administrator + receiving tech lead | within the week following departure | ownership reassigned |

> Note: the full table should include one row per access, transfer item, and verification identified, respecting the dependency order (ownership and knowledge transfer first, revocation next, orphaned credential verification last).

### Executive summary

- **Person and departure date:** [ROLE] — departure confirmed on [DATE].
- **Blocking items before the departure date:** [N] — mainly ownership transfer and undocumented knowledge capture.
- **High-sensitivity access to revoke on the departure day:** [LIST — e.g., cloud with admin permissions, secrets manager, SSO].
- **Residual risks:** [uninventoried access / access list not verified against a centralized inventory / ownership without an assigned receiver / systems without a centralized revocation process].
- **Recommended follow-up verification:** orphaned credential audit [N days] after the departure date, to confirm no active tokens, SSH keys, or service accounts remain under their name.
