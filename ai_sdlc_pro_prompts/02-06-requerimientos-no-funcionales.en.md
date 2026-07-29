# 2.6 — Non-functional requirements specification

## Description

Prompt to catalog and formally document the system or change's **non-functional requirements (NFR)**: performance, availability, scalability, security, usability, maintainability, portability, and compliance — each numbered, with a measurable threshold and a verification method. Complements the functional requirements catalog already produced by `02-05`/`04-03`, which does not cover this category.

**When to use it:** after functional requirements are defined (`02-05`) or the tentative architecture exists (`00-D-02`), and before solution design (`04-01`) — NFRs condition design decisions that are expensive to reverse if discovered late.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — an omitted or poorly quantified NFR (e.g. "must be fast" with no number) leaves design and the test plan without a verifiable criterion, propagating ambiguity to `04-01`/`07-06`, although this prompt does not execute or commit anything by itself |
| Required inputs | system or change context, functional requirements already defined (from `02-05`/`04-03`) if they exist, known business constraints (contractual SLA, compliance, infrastructure budget), tentative architecture or stack if it exists (`00-D-02`) |
| Allowed tools | reading existing documentation and code — no execution or changes |
| Permitted autonomy | A0 — Analyze (catalog NFRs already stated or inferable from context); A1 — Propose (suggested thresholds when the business hasn't set them, always explicitly marked as a proposal to validate) |
| Stop criteria | if an NFR cannot be expressed with a measurable threshold (number, unit, test condition), do not declare it as defined — register it as "pending quantification" instead of inventing a figure |
| Expected output | see `## Expected output` |
| Minimum evidence | each numbered NFR (NFR-XXX) declares category, measurable threshold or "pending quantification", verification method, and if it's a business constraint, where that constraint comes from |
| Recommended next prompt | `04-01-diseno-solucion` (NFRs feed the design constraints); `07-06-pruebas-performance-carga` for performance/load NFRs |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Catalog and formally document the system or change's non-functional requirements, with a measurable threshold and a verification method for each one.

Inputs:
- system or change context: [DESCRIPTION]
- functional requirements already defined: [PASTE OR "not yet defined"]
- known business constraints: [contractual SLA, compliance (GDPR/HIPAA/PCI/ISO), infrastructure budget, or "none declared"]
- tentative architecture or stack: [PASTE OR "not yet defined"]
- categories to prioritize: [e.g. ALL, or a subset: performance, availability, scalability, security, usability, maintainability, portability, compliance]

Activities:
1. For each applicable NFR category (performance, availability/reliability, scalability, security, usability/accessibility, maintainability, portability, compliance/regulatory, observability), determine whether the context makes it relevant — omit non-applicable categories with a one-line explanation of why, do not silently ignore them.
2. For each relevant NFR, define: identifier (NFR-XXX), category, description, measurable threshold (number + unit + condition), verification method (what test or metric confirms it), priority (critical/high/medium/low), and origin (declared by business / inferred from FR / inferred from applicable compliance).
3. If an NFR has no threshold set by the business, propose one based on industry standards for this type of system, mark it explicitly as "[PROPOSED THRESHOLD — validate with business]", and justify the proposed figure.
4. Detect conflicts between NFRs (e.g. maximum security vs. minimum UX friction, high availability vs. limited infrastructure budget) and declare them explicitly with the trade-off options, without resolving the conflict on your own.
5. Relate each NFR to the functional requirements it constrains or conditions, if functional requirements are already defined.

Constraints:
- never declare an NFR as "defined" if it only has a qualitative description with no measurable threshold — report it as pending quantification,
- always distinguish an NFR explicitly declared by the business from one you infer or propose — never present them with the same level of certainty,
- do not invent regulatory compliance thresholds (e.g. figures from a specific standard) unless you can cite the exact standard — if you don't know it with certainty, mark it as "[VERIFY AGAINST THE APPLICABLE STANDARD]",
- do not resolve conflicts between NFRs on your own (e.g. choosing security over UX) — report them as a pending decision for the business or the architecture.

Output:
0. JSON metadata block (keys: status, nfr_count, categories_covered, unquantified_count, confidence_score [0.0 to 1.0]).
1. NFR catalog: ID | Category | Description | Measurable threshold | Verification method | Priority | Origin
2. NFRs pending quantification, with the reason a threshold could not be set.
3. Conflicts detected between NFRs: Conflicting NFRs | Nature of the trade-off | Options | Decision required from
4. NFR ↔ FR relationship: which functional requirements are constrained by each critical NFR.
5. Categories omitted and why.
```

---

## Usage with standard formula

```text
Use the non-functional requirements prompt and adapt it to:
- repository/project: [NAME OR URL]
- system or change context: [DESCRIPTION]
- functional requirements already defined: [PASTE OR REFERENCE]
- documents to review: Project Charter, architecture (00-D-02), applicable compliance
- specific output objective: NFR catalog with measurable thresholds and verification method
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the NFR count and its status |
| NFR catalog (1) | Complete table, one NFR per row, with measurable threshold and verification method |
| Pending NFRs (2) | List of NFRs with no defined threshold, with the reason |
| Conflicts (3) | Trade-offs detected between NFRs, not resolved on its own |
| NFR ↔ FR relationship (4) | Which functionality is conditioned by each critical NFR |
| Omitted categories (5) | Justification of which categories don't apply to this system |

### Example (excerpt)

```json
{
  "status": "cataloged_with_pending_items",
  "nfr_count": 9,
  "categories_covered": ["performance", "availability", "security", "scalability"],
  "unquantified_count": 2,
  "confidence_score": 0.72
}
```

| Section | Example content |
|---|---|
| NFR catalog (1) | NFR-003 \| Performance \| Response time of the search endpoint \| ≤300ms at the 95th percentile, under 200 req/s \| Load test with `07-06-pruebas-performance-carga` \| High \| Declared by business (SLA with Premium customer) |
| Conflicts (3) | NFR-005 (99.95% availability) vs. NFR-011 (infrastructure budget ≤$500 USD/month) \| High availability usually requires multi-zone redundancy, which exceeds the declared budget \| Options: (a) lower the target SLA, (b) increase budget, (c) accept single-zone risk with a manual DR plan \| Decision required from the project sponsor |
