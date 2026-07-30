# 10.6 — End-user training materials and rollout plan

## Description

Prompt to design the training materials and communication rollout plan aimed at **end users** of a new system or feature: guides, training format matched to the audience profile, communication calendar, reinforced support strategy during launch, and an adoption metric. Distinct from `17-01-onboarding-tecnico`, which is exclusively for new engineers joining the team, not end users of the product.

**When to use it:** before launching a new feature or system to its non-technical end users, especially when it changes an existing workflow or affects a large user group.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | medium — insufficient training or a poorly communicated rollout can generate adoption resistance, avoidable support tickets, or incorrect use of a business-critical feature; the prompt does not send real communications or execute the rollout |
| Required inputs | description of the feature or system being launched, end-user audience (roles, technical level, approximate group size), available communication channel, launch date |
| Allowed tools | reading product documentation — no execution and no real communication sent |
| Permitted autonomy | A1 — Propose |
| Stop criteria | if the technical level or audience size is unknown, stop and request it before proposing the training format — a short video and a written guide don't work the same for 5 expert users as for 500 non-technical ones |
| Expected output | see `## Expected output` |
| Minimum evidence | each proposed material declares its target audience and chosen format with a reason; the rollout plan declares the date, channel, and owner of each communication |
| Recommended next prompt | `17-06-reporte-estado-stakeholders` to communicate rollout progress to internal stakeholders |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design the training materials and communication rollout plan for the end users of the described feature or system, with a support strategy during launch and an adoption metric.

Inputs:
- feature or system being launched: [DESCRIPTION]
- end-user audience: [ROLES, TECHNICAL LEVEL, APPROXIMATE GROUP SIZE]
- available communication channel: [EMAIL, IN-APP, LIVE MEETING, INTRANET, OR OTHER]
- launch date: [DATE OR APPROXIMATE WINDOW]

Activities:
1. AUDIENCE PROFILE
   Describe who the end users are, their technical level, and what concerns or resistance is expected against this change (e.g. fear of losing a familiar workflow, learning curve, change in responsibilities).

2. TRAINING MATERIALS
   Propose the training format (step-by-step written guide, short video, FAQ, live session) matched to the audience profile — never default to a format without justifying it against that profile.

3. ROLLOUT COMMUNICATION PLAN
   Define what gets communicated, at what point (before/during/after launch), through which channel, and who owns each message — a concrete calendar, not a generic intention.

4. SUPPORT STRATEGY DURING ROLLOUT
   Define the channel for questions during the launch window, who responds, and whether a reinforced-support window (higher-than-normal response capacity) is required given the change's impact.

5. ROLLBACK COMMUNICATION PLAN
   If the launch is delayed or reverted, define what gets communicated to end users and when — don't leave this scenario without a plan.

6. ADOPTION METRIC
   Define how it will be measured whether end users actually adopted the change (real use of the new feature), not just whether they received the communication.

Constraints:
- do not assume the same training format for audiences with different technical profiles without justifying the choice against the described profile,
- every communication plan must declare an owner and channel for each message — never leave it implicit or "will be communicated later",
- if the system or feature affects a business-critical workflow, a reinforced support strategy during rollout is mandatory, not optional — explicitly flag it if that capacity is missing,
- this prompt does not send any real communication or execute the rollout — it produces the materials and plan for the team to execute.

Output:
0. JSON metadata block (keys: status, audience_profile, materials_count, confidence_score [0.0 to 1.0]).
1. Audience profile and expected resistance.
2. Proposed training materials, with format and justification per audience.
3. Rollout communication plan (calendar with channel and owner).
4. Reinforced support strategy during rollout.
5. Rollback communication plan, if applicable.
6. Proposed adoption metric.
```

---

## Usage with standard formula

```text
Use the end-user training materials and rollout plan prompt and adapt it to:
- repository/project: [NAME OR URL]
- feature or system being launched: [DESCRIPTION]
- end-user audience: [ROLES AND TECHNICAL LEVEL]
- documents to review: product documentation, communications from similar prior launches if any
- specific output objective: complete training materials and rollout plan
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Structured, parseable JSON block with the plan summary |
| Audience profile (1) | Roles, technical level, and expected resistance |
| Training materials (2) | Proposed format per audience, with justification |
| Rollout plan (3) | Communication calendar with channel and owner |
| Support during rollout (4) | Question channel and reinforcement window if applicable |
| Rollback plan (5) | Communication in case of delay or reversal |
| Adoption metric (6) | How real usage will be measured, not just the notice sent |

### Example (excerpt)

```json
{
  "status": "plan_defined",
  "audience_profile": "300 internal sales users, low-to-medium technical level",
  "materials_count": 3,
  "confidence_score": 0.77
}
```

| Section | Example content |
|---|---|
| Training materials (2) | 1-page written guide with screenshots (preferred format given low time availability) + a 3-minute video for those who prefer watching the flow before using it — a mandatory live session was ruled out given the group size (300 people, unfeasible to coordinate) |
| Adoption metric (6) | % of users who complete at least one action with the new feature within the first 14 days post-launch, measured via the already-instrumented analytics event `feature_used:new_dashboard` — target: 60% adoption at 2 weeks |
