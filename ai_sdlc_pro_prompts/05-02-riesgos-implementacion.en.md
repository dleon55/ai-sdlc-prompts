# 5.2 — Implementation risk and impact analysis

## Description

Prompt to identify and classify implementation risks: functional, technical, data, security, operations, agent concurrency, integration and deployment. Generates a risk matrix with probability, impact and mitigation plan.

**When to use it:** in parallel with the implementation plan (`05-01`), before executing any change.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — does not execute changes, but an omitted or misclassified risk can reach the execution phase (`06-01`) without mitigation |
| Required inputs | approved design, architecture, incident history, implementation plan (`05-01`) in progress or approved |
| Allowed tools | read-only access to design, architecture, and incident history; does not execute commands or modify the repository |
| Permitted autonomy | A0 — Analyze risks and potential impact; A1 — Propose the risk matrix with mitigation and contingency |
| Stop criteria | stop if there is no reference design or plan; escalate to human review before moving on to `06-01` if any risk remains classified as high without a viable mitigation |
| Expected output | see `## Expected output` |
| Minimum evidence | each risk with explicit category, probability, impact, mitigation, and contingency; no high risk left without an associated mitigation plan |
| Recommended next prompt | `06-01-implementacion-multiagente`, once the plan (`05-01`) and this risk matrix are approved |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Identify and analyze implementation risks and the potential impact of the change on other modules, processes, services, pipelines, integrations and users, in parallel with the implementation plan (`05-01`).

Inputs:
- approved design: [PASTE OR REFERENCE]
- architecture: [REFERENCE]
- related incident history: [REFERENCE OR "none known"]
- implementation plan (`05-01`): [REFERENCE]

Steps:
1. Review the approved design, architecture, and implementation plan to identify every point of change and its dependencies.
2. For each point of change, identify risks in each of these categories where applicable: functional, technical, data, security, operations, agent concurrency, integration, deployment.
3. For each risk, estimate probability (low/medium/high) and impact (low/medium/high) based on cited incident history or design — not on unsupported intuition.
4. Define the proposed mitigation and contingency plan (what to do if the mitigation fails) for each risk.
5. If a risk is classified as high without a viable mitigation, do not downplay or leave it implicit: state it explicitly as a blocker for `06-01`.

Constraints:
- do not classify a risk as low just because there is no evidence against it — if there is not enough information to evaluate it, state it as "risk not evaluable with available information" instead of assuming it is low,
- no high risk may be left without an explicit mitigation and contingency in the output,
- do not execute commands or modify the repository or environment — this prompt is analysis and proposal only (A0/A1),
- distinguish in every matrix row what is a risk confirmed by cited evidence (design, architecture, incident history) versus your own inference — never mix them without marking the difference,
- if there is no reference design or implementation plan, stop and request one instead of building the matrix on your own assumptions.

Output:
- risk matrix: category, probability, impact, mitigation, contingency
- separate list of high risks without a viable mitigation (if any), flagged as blockers for `06-01`
```

---

## Use with standard formula

```text
Use the implementation risk analysis prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [TARGET BRANCH]
- environment: [DEV / QA / PROD]
- components: [COMPONENTS TO MODIFY]
- documents to review: approved design, architecture, incident history
- specific output objective: complete risk matrix with mitigation plan
- depth level: high
```

---

## Expected output

| Risk | Category | Probability | Impact | Mitigation | Contingency |
|---|---|---|---|---|---|
