# 13.9 — Data Privacy Impact Assessment (DPIA)

## Description

Prompt to assess the privacy impact of a new or significantly modified personal or sensitive data processing activity: data inventory, purpose and legal basis, minimization, third parties and international transfers, data-subject rights mechanism, retention, and residual risk. Complements `13-04-threat-modeling` (technical security threats) and `14-03-iso-moprosoft-compliance` (process conformance) — neither of them assesses legal basis or data-subject rights.

**When to use it:** when designing a feature that processes new personal or sensitive data, or before a significant change in how already-existing data is processed.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | high — an incomplete DPIA can let a data-processing activity reach production with no valid legal basis or no real mechanism for exercising data-subject rights, with real regulatory exposure (GDPR/CCPA/local data-protection law fines); the prompt does not execute or approve anything by itself |
| Required inputs | description of the personal/sensitive data processed, purpose of the processing, proposed legal basis, third parties involved (processors/sub-processors), geographic location of users and of storage |
| Allowed tools | reading existing documentation and design — no execution |
| Permitted autonomy | A0 — Analyze; A1 — Propose (suggested legal basis, mitigation controls) |
| Stop criteria | if a valid legal basis for the processing cannot be determined, do not assume one — report it as blocking, requiring a legal decision before proceeding |
| Expected output | see `## Expected output` |
| Minimum evidence | each personal data category declares purpose, legal basis, retention period, and a rights-exercise mechanism (access/rectification/deletion) |
| Recommended next prompt | `13-04-threat-modeling` for the technical security controls protecting the data identified here; `13-08-gestion-secretos-credenciales` if the processing involves credentials |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Assess the privacy impact of the described personal or sensitive data processing: what data, for what purpose, under what legal basis, with which third parties, with what data-subject rights mechanism, and with what residual risk.

Inputs:
- personal/sensitive data processed: [DESCRIPTION]
- purpose of the processing: [WHAT THAT DATA IS USED FOR]
- proposed legal basis: [CONSENT / CONTRACT / LEGITIMATE INTEREST / LEGAL OBLIGATION / NOT YET DEFINED]
- third parties involved: [PROCESSORS/SUB-PROCESSORS, OR "none"]
- geographic location: [COUNTRIES OF USERS AND OF STORAGE]

Activities:
1. DATA INVENTORY
   Identify what personal or sensitive data is processed, by category (identification, health, financial, biometric, location, behavioral, etc.) and its sensitivity level.

2. PURPOSE AND LEGAL BASIS
   For each data category, define what it's processed for and under what specific legal basis (consent, contract performance, legitimate interest, legal obligation) — never assume a legal basis without justifying it against the declared purpose.

3. MINIMIZATION
   Assess whether only what's necessary for the declared purpose is being collected, or whether there's over-collection of data that goes unused.

4. THIRD PARTIES AND TRANSFERS
   Identify which processors or sub-processors have access to the data, and whether there's an international transfer with the corresponding legal safeguards (standard contractual clauses, adequacy decision, or other).

5. DATA-SUBJECT RIGHTS
   Define the real mechanism (not just the declared intent) by which a user can access, correct, delete, or export their data.

6. RETENTION
   Define the retention period for each data category and the deletion mechanism once that period expires.

7. RESIDUAL RISK
   Given the design evaluated, identify whether any privacy risk remains unmitigated, and its severity.

Constraints:
- never assume a legal basis without explicit justification against the declared purpose — if unclear, mark it as "[PENDING LEGAL DECISION]" instead of choosing one on your own,
- do not declare "compliance" for a data-subject rights mechanism that only exists as stated intent with no verifiable real implementation,
- every international data transfer must declare the applicable legal safeguard or be explicitly flagged as an open risk — never assume it's safe without that cited safeguard,
- this prompt does not substitute formal legal advice — for legal-basis decisions in specific jurisdictions, explicitly flag that it requires validation from a legal team before proceeding.

Output:
0. JSON metadata block (keys: status, personal_data_categories, unmitigated_risks_count, confidence_score [0.0 to 1.0]).
1. Personal/sensitive data inventory by category.
2. Purpose and legal basis per category.
3. Minimization assessment.
4. Third parties and international transfers, with safeguards.
5. Real data-subject rights mechanism.
6. Retention policy per category.
7. Identified residual risk.
```

---

## Usage with standard formula

```text
Use the Data Privacy Impact Assessment (DPIA) prompt and adapt it to:
- repository/project: [NAME OR URL]
- feature that processes data: [DESCRIPTION]
- personal/sensitive data involved: [DESCRIPTION]
- documents to review: feature design, current privacy policy, contracts with third-party processors
- specific output objective: complete DPIA with legal basis and residual risk
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the assessment summary |
| Data inventory (1) | Identified personal/sensitive data categories |
| Purpose and legal basis (2) | Specific legal basis per category, justified |
| Minimization (3) | Over-collection assessment, if any |
| Third parties and transfers (4) | Processors and international-transfer safeguards |
| Data-subject rights (5) | Real access/rectification/deletion mechanism |
| Retention (6) | Period and deletion mechanism per category |
| Residual risk (7) | Unmitigated privacy risks, with severity |

### Example (excerpt)

```json
{
  "status": "assessed_with_pending_legal_item",
  "personal_data_categories": 4,
  "unmitigated_risks_count": 1,
  "confidence_score": 0.7
}
```

| Data category | Purpose | Legal basis | Retention | Data-subject rights |
|---|---|---|---|---|
| Device GPS location | Estimate delivery time | Contract performance (service requested by the user) | 90 days, automatic deletion via scheduled job | `DELETE /me/location-history` endpoint already implemented |
| Search history | Personalize recommendations | [PENDING LEGAL DECISION] — the team proposes "legitimate interest" but it hasn't been validated with legal given the volume of behavioral data collected | Not yet defined | Not implemented |

| Section | Example content |
|---|---|
| Residual risk (7) | High: search history is processed with no validated legal basis and no deletion mechanism — blocking for launching this feature until both points are resolved with the legal team |
