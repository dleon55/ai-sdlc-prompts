# 9.5 — Feature Flag / Kill-Switch Strategy

## Description

Prompt to design the feature flag and kill-switch strategy for a change: flag type and lifecycle, naming convention and evaluation point, ring-based rollout progression with promotion criteria, kill-switch design for fast rollback without a deploy, session consistency, evaluation fail-safe, cleanup plan, and rollout-specific monitoring.

**When to use it:** when a change needs a progressive or controlled rollout instead of an all-at-once deployment — for example, a high-risk feature, a significant UX change, or a change to a critical business flow. It is complementary to `09-04-promotion-checklist`: that prompt is the promotion gate between environments (DEV→QA→PROD) that decides whether the code gets deployed; this prompt designs how a feature behaves and is gradually activated once deployed, within one environment or across several, over days or weeks, independently of the deployment itself.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | design |
| Expected risk | medium — a poorly designed flag strategy (e.g. no kill-switch, or a flag that cannot be safely toggled off) increases the blast radius of a failed rollout, but this prompt itself only designs: it does not toggle or modify flags in a real environment |
| Required inputs | feature or change to flag, expected flag type (release/ops/experiment), feature flag platform, layers where it is evaluated (client/server/edge), whether there is an associated A/B experiment, target date or milestone for full rollout |
| Allowed tools | reading code, architecture, and feature flag platform documentation to design the strategy — no creating, enabling, disabling, or modifying flags on the real platform |
| Permitted autonomy | A1 — Propose (complete strategy design without applying it); creating and enabling flags on the real platform requires explicit A2/A3 by the team that owns the feature |
| Stop criteria | stop and escalate if the proposed kill-switch depends on the same deploy pipeline it is meant to bypass in an emergency; do not propose a rollout progression without measurable promotion/pause criteria; do not leave any flag without an owner or a removal plan |
| Expected output | see `## Expected output` |
| Minimum evidence | each flag documented with type, naming convention, evaluation point, rollout rings with % and promotion criteria, kill-switch design, and cleanup plan with a concrete date or trigger |
| Recommended next prompt | `09-06-coordinacion-breaking-changes` if the flagged feature is itself a breaking change requiring coordination with consumers |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design the feature flag and kill-switch strategy for the progressive, safe rollout of this change.

Required inputs:
- repository: [NAME OR URL]
- feature or change to flag: [REFERENCE TO ISSUE OR PR]
- expected flag type: [RELEASE / OPS / EXPERIMENT / COMBINATION]
- feature flag platform: [LaunchDarkly / Unleash / Flagsmith / GrowthBook / in-house solution / other]
- layers where it is evaluated: [CLIENT / SERVER / EDGE]
- associated A/B experiment: [YES / NO]
- target date or milestone for full rollout: [DATE]

Steps:

1. DEFINE THE FLAG'S PURPOSE AND LIFECYCLE
   Classify each needed flag into one of these types and justify the choice:
   - release flag: temporary, wraps code under development/rollout; removed as soon as rollout reaches 100% and stabilizes (expected life: days-weeks).
   - ops flag / kill-switch: permanent, does not wrap a new feature but gives operational control to switch a capability off if it fails (expected life: indefinite, as long as the capability exists).
   - experiment flag: temporary, tied to an A/B experiment with a defined hypothesis and success metric; removed once the experiment concludes and a winner is declared.
   The same change may need more than one flag (e.g. a release flag for the rollout plus a permanent emergency ops flag).

2. DEFINE THE NAMING CONVENTION AND EVALUATION POINT
   - proposed naming convention: [domain]-[feature]-[type] (e.g. checkout-new-payment-flow-release).
   - where the flag is evaluated: client (app/SPA), server (backend/API), or edge (CDN/gateway) — justify based on where the changing logic lives and the acceptable propagation latency.
   - if evaluated on the client: what happens to cached or stale clients that don't receive the flag's updated value.
   - flag owner: the person or team responsible for its full lifecycle.

3. DESIGN THE ROLLOUT PROGRESSION
   Define concrete rings with user %, target audience, and minimum duration before promoting to the next one:
   - ring 0 — internal/dogfooding: internal team, 0% external users, minimum [X] days.
   - ring 1 — canary: [X]% of external users (low-risk segment), minimum [X] hours/days.
   - ring 2 — partial rollout: [X]% of users, minimum [X] days.
   - ring 3 — full rollout: 100%.
   For each transition between rings, define the promotion criterion (which metric and threshold must be met) and the pause/rollback criterion, automatic or manual (e.g. error rate > X%, P95 latency > Yms, conversion drop > Z%).

4. DESIGN THE KILL-SWITCH
   Specifically for the emergency scenario, not for the normal rollout progression:
   - it must be toggleable without going through the deploy pipeline (a toggle in the flag platform's panel or in remote config, never a code change that requires a build).
   - who has permission to activate it (define the role, not an individual person) and how that change gets audited.
   - expected propagation time from activation until 100% of traffic stops seeing the feature.
   - what happens to requests already in flight at the moment it is activated.

5. DEFINE SESSION CONSISTENCY
   - should users keep the same flag state for their entire session (sticky assignment by user ID/session ID), or can they see a behavior change mid-session — decide and justify based on the feature type (a checkout flow requires strict consistency; an informational banner can tolerate a mid-session change).
   - if there is an associated A/B experiment, how deterministic bucketing of each user into their variant is guaranteed.

6. DEFINE THE EVALUATION FAIL-SAFE
   - what value the flag takes if the flag service is unreachable — it must always fall back to the stable/known behavior, never enable the new feature by default.
   - evaluation timeout and local cache behavior on the flag client.

7. DEFINE THE CLEANUP PLAN
   - concrete date or trigger to remove the flag and the dead code from the old branch (e.g. "30 days after reaching 100% with no incidents").
   - who is responsible for creating and following up on the cleanup ticket.
   - what happens if the flag never reaches 100% (final rollback of the flag vs. explicit reclassification as a permanent ops flag).

8. DEFINE ROLLOUT-SPECIFIC MONITORING AND ALERTS
   - metrics to watch at each ring (error rate, latency, conversion, support complaint volume).
   - dashboard or segmentation that allows comparing cohorts with and without the flag active.
   - alert that fires an automatic notification when the pause criterion defined in step 3 is met.

Constraints:
- the kill-switch must never depend on the same deploy pipeline it is meant to bypass in an emergency — if activating it requires a build or a deploy, it is not a kill-switch.
- no flag may remain in the code without an explicit owner and a removal plan or date — a flag "forever" with no owner is undeclared technical debt.
- flag evaluation must fail safe: if the flag service does not respond, the system must fall back to the known stable behavior, never silently enable a half-tested feature.
- if there is an associated A/B experiment, the rollout strategy must not contaminate variant assignment; the emergency kill-switch must be able to switch the whole feature off without retroactively invalidating data already collected (it is marked as truncated, not silently discarded).
- this prompt designs the strategy; it does not create, enable, disable, or modify flag configuration in any real environment — those actions require explicit A2/A3 execution outside this prompt.

Deliver:
1. Flag table (name, type, evaluation point, owner)
2. Ring-based rollout progression with promotion and pause criteria
3. Kill-switch design (mechanism, permissions, propagation time)
4. Session consistency definition
5. Evaluation fail-safe
6. Cleanup plan with a concrete date or trigger
7. Monitoring and alerting plan
```

---

## Use with standard formula

```text
Use the feature flag / kill-switch strategy prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- feature to flag: [BRIEF DESCRIPTION]
- expected flag type: [RELEASE / OPS / EXPERIMENT]
- feature flag platform: [LaunchDarkly / Unleash / Flagsmith / GrowthBook / other]
- environment(s) where it applies: [DEV / QA / PROD]
- documents to review: architecture, feature flag platform documentation, current metrics for the affected flow
- specific output objective: complete flag strategy + rollout progression + kill-switch design + cleanup plan
- depth level: high
```

---

## Expected output

### Flag strategy

| Flag | Type (release/ops/experiment) | Rollout (rings/%) | Promotion criterion | Kill-switch | Cleanup plan |
|---|---|---|---|---|---|
| [flag-name] | [release / ops / experiment] | [ring 0 → 1 → 2 → 3 with %] | [metric and threshold per ring] | [mechanism, permissions, propagation time] | [removal date or trigger] |

### Example applied

Feature: new single-page checkout flow (replaces the current multi-step checkout).

| Flag | Type | Rollout (rings/%) | Promotion criterion | Kill-switch | Cleanup plan |
|---|---|---|---|---|---|
| `checkout-spa-release` | release | Ring 0 internal 0% → Ring 1 canary 5% → Ring 2 partial 25% → Ring 3 full 100% | error rate < 0.5%, P95 < 400ms, conversion drop no more than 2% vs. control; each ring stable for at least 48h before promoting | inherits `checkout-spa-kill` — turning it off returns 100% of traffic to the multi-step checkout in < 2 min | remove flag and multi-step checkout code 30 days after reaching 100% with no incidents; ticket assigned to Checkout Team |
| `checkout-spa-kill` | ops (permanent) | N/A — global 0%/100%, no rings | activated manually on incident; activation criterion: error rate > 2% sustained for 5 min, or confirmed payment degradation | direct toggle in the LaunchDarkly panel, no build/deploy; permission restricted to the `on-call-checkout` role; propagation < 2 min to all clients | not removed — lives as long as the SPA flow exists; ownership reviewed quarterly |
| `checkout-spa-experiment` | experiment | 50/50 split within Ring 2 (25% of total traffic) | winning variant declared with statistical significance p < 0.05 after a minimum of 2 weeks and 10,000 sessions per variant | inherits `checkout-spa-kill` — turning off the kill-switch also stops the experiment and marks in-progress data as truncated | removed once the winning variant is declared and its code is merged as the sole behavior |
