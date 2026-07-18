# 11.12 — Alert noise audit (alert fatigue)

## Description

Prompt to audit the real history of alerts fired in an already-deployed monitoring system — distinct from designing new SLOs/alerts, which is covered by `10-04-observabilidad-instrumentacion`. Classifies each alert as noise (false positives, no action taken, duplicate, recurrently silenced) or real signal, quantifies the noise rate and its relationship to on-call team fatigue, and recommends tuning, consolidation, or removal per alert.

**When to use it:** when the team reports alert fatigue (too many notifications, alerts habitually ignored), or periodically as a health check of an already-in-production monitoring system.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — silencing or removing an alert that looks like noise but actually detects a rare real problem can leave a real incident undetected in the future; the prompt only analyzes and recommends, it does not modify alert configuration on its own |
| Required inputs | history of alerts fired in the period (name, timestamp, severity, whether action was taken, whether silenced), access to current dashboards/alert rules, definition of what constitutes "action taken", if any |
| Allowed tools | reading the alert history, configured alert rules, and associated response/action logs; does not modify alert configuration or silence alerts — produces the analysis and recommendation |
| Permitted autonomy | A0 — Analyze (classify alerts as noise/signal); A1 — Propose (tuning, consolidation, or removal recommendation); never A2/A3 — actually modifying alert rules requires a human to apply it after reviewing the recommendation |
| Stop criteria | stop and flag if the alert history does not record whether action was taken — do not assume "no visible action" is equivalent to "confirmed noise" without verifying with the team; if the analyzed period is too short for low-frequency alerts, flag the limitation instead of concluding it is noise |
| Expected output | see `## Expected output` |
| Minimum evidence | every alert classified as noise cites the pattern that supports it (never led to action in N occurrences, duplicates another alert, is recurrently silenced without investigation); every removal recommendation identifies what real scenario would stop being detected |
| Recommended next prompt | `10-04-observabilidad-instrumentacion` if the analysis reveals missing SLOs/alerts for a blind spot, not just noise in existing ones; `11-13-salud-rotacion-oncall` if the noise volume correlates with on-call team fatigue |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Audit the real history of alerts fired in the indicated period to classify each as noise or real signal, quantify the noise rate, and recommend tuning, consolidation, or removal per alert.

Inputs:
- period's alert history: [PASTE OR LINK — name, timestamp, severity, action taken, whether silenced]
- current alert rules: [PASTE OR LINK TO CONFIGURATION]
- definition of "action taken": [e.g. TICKET OPENED, RESPONSE IN INCIDENT CHANNEL, RUNBOOK FOLLOWED — OR "not yet defined"]
- period to analyze: [e.g. LAST QUARTER]
- alerting channel/system: [e.g. PagerDuty / Opsgenie / Slack / other]

Steps:
1. PER-ALERT CLASSIFICATION
   For each distinct alert rule in the history, count how many times it fired in the period, in how many a logged action was taken (per the provided definition), in how many it was silenced without investigation, and whether it duplicates the same symptom as another alert already counted.

2. NOISE RATE CALCULATION
   For each alert, calculate the proportion of firings with no action taken versus the total. If the definition of "action taken" was not provided, flag it explicitly and use as a conservative proxy only the cases with direct evidence of investigation (comment, ticket, channel response) — never assume "no record" means "not investigated".

3. DUPLICATE AND CORRELATION DETECTION
   Identify alerts that always fire together or cascade from the same root symptom (e.g. a CPU alert and a latency alert that always coincide) — these are candidates for consolidation into a single signal with enriched context instead of generating N separate notifications.

4. FINAL CLASSIFICATION: NOISE VS. SIGNAL
   Classify each alert as: real signal (action taken consistently, detects a real problem), confirmed noise (never led to action in the full period, or is systematically silenced without investigation), or "needs more data" (frequency too low to conclude with the analyzed period — do not classify it as noise just because of this).

5. PER-ALERT RECOMMENDATION
   - Confirmed noise: recommend adjusting the threshold, changing the trigger condition, or removing the alert — explicitly stating what real scenario (even if unlikely) would stop being detected if removed.
   - Duplicate/correlated: recommend consolidating into a composite alert.
   - Real signal but high frequency: evaluate whether the threshold is miscalibrated (fires before the problem is actually actionable) instead of just accepting the volume.

6. RELATIONSHIP WITH TEAM FATIGUE
   If data on who received each alert is available, flag whether the noise concentrates in certain hours (night/weekend) or on certain people, which worsens fatigue beyond the total volume.

Constraints:
- never classify an alert as "confirmed noise" just because there is no explicit record of action — if the definition of "action taken" is unclear or the record is incomplete, classify it as "needs more data" instead of recommending removal,
- every recommendation to remove or raise an alert's threshold must explicitly state what real scenario would stop being detected — never recommend removal without that risk analysis,
- do not execute or modify any alert rule, silencing, or configuration — this prompt is analysis and recommendation only,
- if the analyzed period is too short for an expected low-frequency alert (e.g. once per quarter and the period is one month), do not classify it as noise — explicitly flag the data limitation.

Output:
- alert table: name, firings in the period, noise rate, classification (signal/noise/needs more data)
- consolidation candidates (duplicate/correlated alerts)
- tuning/consolidation/removal recommendation per alert, with the scenario that would stop being detected if applicable
- observed relationship between noise and receiving hour/person, if data exists
- summary: overall noise rate for the period, expected volume change if recommendations are applied
```

---

## Use with standard formula

```text
Use the alert noise audit prompt and adapt it to:
- repository/project: [NAME OR URL]
- alert history: [LINK TO THE PERIOD'S HISTORY]
- current alert rules: [LINK TO CONFIGURATION]
- definition of "action taken": [e.g. TICKET OPENED OR "not yet defined"]
- period to analyze: [LAST QUARTER]
- alerting channel/system: [PagerDuty / Opsgenie / Slack / other]
- documents to review: alert history, configuration rules
- specific output objective: noise vs. signal classification with tuning recommendations
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Alert table | Name, firings, noise rate, classification |
| Consolidation | Duplicate or correlated alerts to merge |
| Recommendations | Tuning/consolidation/removal, with risk scenario if applicable |
| Team fatigue | Noise concentration by hour or person, if data exists |
| Summary | Overall noise rate and expected volume change |

### Example (excerpt)

| Alert | Firings (quarter) | Noise rate | Classification |
|---|---|---|---|
| CPU > 80% for 5 min | 47 | 91% with no recorded action | Confirmed noise |
| P99 latency > 2s | 12 | 25% with no action | Real signal, well-calibrated threshold |
| Disk space < 10% (nightly backup) | 3 | 100% with no action, always coincides with the scheduled backup job | Needs more data — only 3 occurrences, but correlates with a known process; candidate for threshold adjustment or excluding the backup window, not removal without more evidence |

**Recommendation:** the CPU alert fires 47 times in the quarter with no occurrence leading to a logged action or incident-channel comment — raise the threshold to 90% sustained for 10 min instead of 5. Risk of removing without adjusting: a real CPU spike preceding a service outage would stop being notified; threshold adjustment is recommended, not removal.
