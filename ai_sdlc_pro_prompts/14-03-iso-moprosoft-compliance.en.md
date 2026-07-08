# 14.3 — ISO 29110 / MOPROSOFT process compliance audit

## Description

Structured quality assurance (QA / Audit) prompt to certify that functional, design, and technical deliverables of the development cycle strictly comply with the requirements of ISO/IEC 29110 basic profiles and the MOPROSOFT process model.

**When to use it:** before deployment to controlled environments (Staging / Prod), as part of the quality gates in the release process.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | validation |
| Expected risk | medium — this is a read-only audit, but an unwarranted "Approved" verdict can authorize the release of a non-compliant deliverable to production |
| Required inputs | workspace/subproject and compliance standard to audit (ISO 29110 / MOPROSOFT / MAAGTICSI), generated artifacts (Implementation Plan, Test Cases, Test Code, Technical Memory) |
| Allowed tools | reading of project artifacts, code, and documentation — no test execution or repository changes |
| Permitted autonomy | A0 — Analyze the conformity of each artifact; A1 — Propose the verdict and the mandatory remediation actions |
| Stop criteria | do not issue an "Approved" verdict if bidirectional requirement-design-code-test traceability is missing; mark as "Rejected" or "Approved with Reservations" for any non-conformity without evidence of mitigation |
| Expected output | see `Output:` inside `## Complete prompt` |
| Minimum evidence | each reported non-conformity references the specific artifact or control that was not met and its associated mandatory remediation action |
| Recommended next prompt | `08-03-remediacion-maestro` if the verdict is "Rejected" or "Approved with Reservations"; `09-04-promotion-checklist` if the verdict is "Approved," to continue with promoting the change |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Audit the current software engineering deliverable to verify its conformity with the practices required by the ISO 29110 (Basic Profile) and MOPROSOFT standards.

Inputs:
- workspace/subproject: [WORKSPACE/SUBPROJECT]
- generated artifacts (Implementation Plan, Test Cases, Test Code, Technical Memory): [READ OR PASTE DETAILS]
- standard/compliance: [ISO 29110 / MOPROSOFT / MAAGTICSI]

Activities:
1. Review the artifacts against the basic quality checklist:
   - Is the requirement mapped to a formal technical design (ADR/Use Cases)?
   - Were verification and validation tests (Unit, Integration, Smoke) designed and implemented?
   - Is there bidirectional traceability between requirement, design, code, and tests?
   - Was the technical memory of the change recorded and user/operational documentation updated?
2. Identify non-conformities and deviations.
3. Evaluate if the code complies with the project's information security guidelines (ISO 27001).

Output:
1. Regulatory Compliance Report (Approved/Missing Checklist)
2. Traceability Matrix from Requirement to Tests
3. List of Detected Non-Conformities (Mandatory Remediation Action)
4. Final Release Approval Verdict (Approved / Approved with Reservations / Rejected)
```

---

## Use with standard formula

```text
Use the ISO/MOPROSOFT compliance audit prompt and adapt it to:
- repository: [NAME OR URL]
- workspace/subproject: [IF APPLICABLE]
- standard/compliance: ISO 29110
- issue or requirement: [REFERENCE]
- branch: [BRANCH]
- environment: STAGING
- components: technical memory, test plans, source code
- documents to review: plan_implementacion, walkthrough, test_build
- specific output objective: formal release audit and traceability report
- depth level: high
```
