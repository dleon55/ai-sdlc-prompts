# 16.6 — Support knowledge base health audit

## Description

Prompt to audit the entire support knowledge base (KB) corpus as a collection — not to create a single article (`16-03-articulo-base-conocimiento`) nor to recommend updating documentation as a side effect of a ticket pattern (`16-05-analisis-tendencias-tickets`). Evaluates staleness (articles out of date relative to the current product version), duplicates or overlap, real coverage against recurring ticket categories, and unused articles.

**When to use it:** periodically (e.g. quarterly) as KB maintenance, or when the support team reports that existing articles no longer reflect the current product or that finding the right answer is difficult.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | low — the prompt only analyzes and recommends; it does not publish, edit, or delete articles on its own. The indirect risk is that an unaudited KB accumulates outdated articles that generate incorrect answers to customers if the support team trusts them without verifying |
| Required inputs | KB article inventory (title, last-updated date, category, usage/view metrics if any), current product version or recent changelog, recurring ticket categories (from `16-05` if available, or the ticket history directly) |
| Allowed tools | reading the KB inventory, product changelog/release notes, and the ticket trend analysis or history; does not publish, edit, or delete articles — produces the analysis and the list of recommended actions |
| Permitted autonomy | A0 — Analyze (staleness, duplicates, coverage, usage); A1 — Propose (what to update, merge, archive, or create); never A2/A3 — actually publishing or deleting articles requires human review and execution by the KB owner |
| Stop criteria | stop and flag if no last-updated date is available to evaluate staleness — do not assume an article is current just because there is no evidence it is outdated; if no usage/view metrics exist, limit the "unused" analysis to what can be inferred another way and state it as a proxy, not real usage data |
| Expected output | see `## Expected output` |
| Minimum evidence | every article flagged as outdated cites the product change (changelog/release) that makes it obsolete; every duplicate cites the two or more overlapping articles and the degree of overlap |
| Recommended next prompt | `16-03-articulo-base-conocimiento` to draft or update the articles prioritized by this audit; `16-05-analisis-tendencias-tickets` if the audit reveals recurring ticket categories with no article covering them |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Audit the entire support knowledge base corpus as a collection: identify articles outdated relative to the current product, duplicate or overlapping articles, coverage gaps against recurring ticket categories, and unused articles, with a prioritized list of actions.

Inputs:
- KB article inventory: [PASTE OR LINK — title, last-updated date, category, views/usage if any]
- recent product changelog or release notes: [PASTE OR LINK]
- recurring ticket categories: [PASTE 16-05 RESULT OR TICKET HISTORY DIRECTLY]
- period considered "recent": [e.g. LAST 6 MONTHS]

Steps:
1. STALENESS EVALUATION
   For each article, compare its last-updated date against the product changelog/release notes. If an article describes a flow, screen, or behavior that changed after its last update, mark it as outdated and cite the specific changelog entry that invalidates it. Do not mark an article as outdated just for its age if the flow it describes has not changed.

2. DUPLICATE AND OVERLAP DETECTION
   Identify articles that cover the same question or flow with redundant content (not related articles that complement each other, but ones competing for the same search). For each pair or group, state the degree of overlap and which should be the canonical article after merging.

3. COVERAGE ANALYSIS AGAINST RECURRING TICKETS
   Cross the provided recurring ticket categories against the KB inventory: does at least one current article exist for each high-volume category? If a recurring category has no article or only an outdated one, flag it as a priority coverage gap.

4. UNUSED ARTICLE IDENTIFICATION
   If view/usage metrics exist, identify articles with consistently low or zero usage in the period. If no usage metrics are available, use as a proxy the absence of mentions or links from recent tickets, and explicitly state that it is a proxy, not a direct usage measurement.

5. ACTION PRIORITIZATION
   For each finding, recommend an action: update (outdated article but the category is still relevant), merge (duplicates), create (coverage gap in a high-volume category), or archive (unused and with no associated ticket category). Prioritize by impact: coverage gaps in high-volume categories first, then outdated high-traffic articles, then duplicates, then low-priority archiving.

Constraints:
- do not mark an article as outdated without citing the specific product change (changelog/release) that invalidates it — age alone is not evidence of staleness,
- do not recommend archiving an article based only on apparent low usage if there are no real metrics and the proxy used (absence of ticket mentions) is weak — state it as a "candidate to review", not "archive directly",
- do not publish, edit, or delete any article — this prompt is analysis and recommendation only; actual execution is done by a human, supported by `16-03` to draft the updated content,
- if no last-updated date exists for an article, do not exclude it from the coverage/duplicate analysis, but explicitly flag that its staleness cannot be evaluated.

Output:
- table of outdated articles, with the product change that invalidates them
- table of duplicate/overlapping articles, with the recommended canonical one
- coverage gaps against recurring ticket categories
- candidate articles for archiving, with the strength of the "unused" evidence stated
- prioritized action list
```

---

## Use with standard formula

```text
Use the knowledge base audit prompt and adapt it to:
- repository/project: [NAME OR URL]
- KB inventory: [LINK TO THE ARTICLE INVENTORY]
- recent changelog: [LINK TO RELEASE NOTES]
- recurring ticket categories: [16-05 RESULT OR HISTORY]
- period considered "recent": [LAST 6 MONTHS]
- documents to review: KB inventory, changelog, ticket history
- specific output objective: prioritized action list for the KB corpus
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Outdated articles | Title, product change that invalidates it |
| Duplicate/overlapping | Involved articles, degree of overlap, recommended canonical one |
| Coverage gaps | Ticket category with no current article covering it |
| Archive candidates | Article, "unused" evidence (real or stated proxy) |
| Prioritized actions | Update/merge/create/archive, in order of impact |

### Example (excerpt)

| Article | Last updated | Detected problem |
|---|---|---|
| "How to reset your password" | 14 months ago | Outdated: release notes from 6 months ago show the reset flow now requires SMS verification, not just email — the article still describes the old flow |
| "Recover access to your account" | 3 months ago | ~80% duplicate of "How to reset your password"; both compete for the same user search — recommend merging into one canonical article, using the more recent one as the base |

**Priority coverage gap:** the "mobile app sync errors" ticket category represents 12% of tickets in the last 6 months (per `16-05`) and has no associated KB article — recommend creating a new article before updating articles in lower-volume categories.
