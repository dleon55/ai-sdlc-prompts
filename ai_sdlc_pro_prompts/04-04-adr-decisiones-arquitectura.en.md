# 4.4 — Architecture Decision Records (ADR)

## Description

Prompt to document architectural decisions in a structured way: problem context, evaluated options, decision made, consequences and status. Generates numbered and versioned ADRs that remain as a permanent record of the why of the design.

**When to use it:** when making a significant architectural decision (technology choice, design pattern, integration strategy, data structure), when documenting past decisions that were not recorded, or as a review at the beginning of a project.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Document the architectural decision of this project as a numbered and traceable Architecture Decision Record (ADR).

Required inputs:
- ADR number: [ADR-NNN]
- short title of the decision: [TITLE]
- date: [DATE]
- status: [proposed / accepted / deprecated / superseded by ADR-NNN]
- author(s): [NAME OR AGENT]

Generate a complete ADR with the following sections:

## 1. Context
Describe the situation, problem or need that required making a decision.
Include:
- system or team constraints
- forces at play (performance, cost, time, security, maintainability)
- what would happen if NO decision is made

## 2. Decision
The decision made, expressed directly and unambiguously.
A single clear sentence: "We have decided to use X for Y."

## 3. Options evaluated
For each option considered (including the rejected one):
- option name
- brief description
- concrete pros
- concrete cons
- why it was rejected (if applicable)

## 4. Consequences
### Positive
- what improves with this decision

### Negative or accepted trade-offs
- what is sacrificed or complicated

### Neutral
- process or convention changes that derive

## 5. Compliance and validation
- how it is verified that the decision was implemented correctly
- what metrics or evidence confirm it was the correct decision

## 6. References
- related documents
- issues or PRs that motivated the decision
- related ADRs

Output file format: docs/decisions/ADR-NNN-short-title.md
```

---

## Use with standard formula

```text
Use the Architecture Decision Records prompt and adapt it to:
- repository: [NAME OR URL]
- ADR number: [ADR-NNN]
- title: [DECISION TITLE]
- project context: [STACK, RESTRICTIONS, TEAM]
- evaluated options: [LIST OF CONSIDERED ALTERNATIVES]
- documents to review: README, existing architecture, related issues
- specific output objective: complete ADR ready to save in docs/decisions/
- depth level: high
```

---

## Expected output

```markdown
# ADR-001: Use of GitHub Pages + GCP dual-deploy for the prompts portal

**Date:** 2026-04-10
**Status:** Accepted
**Author:** David León / GitHub Copilot Agent

## Context
The AI-SDLC Pro portal needs to be publicly accessible for the entire team...

## Decision
We have decided to use GitHub Pages for the public URL and GCP with Nginx for the
corporate domain `prompts.lionsystems.com.mx`.

## Options evaluated
| Option | Pros | Cons | Result |
|---|---|---|---|
| GitHub Pages only | Free, automatic CI/CD | No custom domain without external DNS | Partially chosen |
| GCP Nginx only | Corporate domain, total control | Manual deployment, VM cost | Partially chosen |
| Vercel / Netlify | CI/CD + easy domain | Third-party dependency, usage restrictions | Rejected |
| Dual GitHub Pages + GCP | Best of both | Greater synchronization complexity | **Chosen** |

## Positive consequences
- Free public URL for external team
- Corporate URL with TLS for internal use
...
```

---

## Recommended ADR index (`docs/decisions/README.md`)

| ADR | Title | Status | Date |
|---|---|---|---|
| ADR-001 | [First ADR] | proposed | |
| ADR-002 | [Second ADR] | accepted | |
