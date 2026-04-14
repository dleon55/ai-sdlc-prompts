# 3.2 — Root cause analysis

## Description

Prompt to investigate a defect or incident and determine the real root cause, not just the symptom. Includes formulation of hypotheses, validation with evidence and remediation recommendation.

**When to use it:** when investigating defects in QA or production, when the symptom is clear but the cause is not.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze a defect or incident and determine the real root cause, not just the symptom.

Activities:
1. Define the observed symptom.
2. Review evidence:
   - logs,
   - code,
   - configurations,
   - queries,
   - recent commits,
   - recent deployments.
3. Formulate hypotheses.
4. Validate hypotheses with evidence.
5. Determine:
   - root cause,
   - contributing factors,
   - impact,
   - affected modules.
6. If it cannot be fully confirmed, indicate missing evidence and confidence level.

Output:
1. Symptom
2. Evidence
3. Hypotheses
4. Confirmed or probable root cause
5. Contributing factors
6. Associated risk
7. Remediation recommendation
```

---

## Use with standard formula

```text
Use the root cause analysis prompt and adapt it to:
- repository: [NAME OR URL]
- issue: [NUMBER OR REFERENCE]
- branch: [AFFECTED BRANCH]
- environment: [QA / STAGING / PROD]
- components: [INVOLVED COMPONENTS]
- documents to review: logs, code, recent commits, configurations
- specific objective: confirm root cause and propose solution plan
- depth level: high
```

### Real example

```text
Use the root cause analysis prompt and adapt it to:
- repository: urgemy-api
- issue: #842
- branch: urgemy-test
- environment: QA
- components: api, push notifications, postgres
- documents to review: README, docs/notifications, workflows, related issues
- specific objective: confirm root cause and propose solution plan
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Symptom | Observed behavior with evidence |
| Evidence reviewed | Logs, code, commits, configurations |
| Hypotheses | Possible causes ordered by probability |
| Root cause | Confirmed or probable with confidence level |
| Contributing factors | Conditions that allowed the problem |
| Risk | Impact if not corrected |
| Remediation | Recommended correction plan |
