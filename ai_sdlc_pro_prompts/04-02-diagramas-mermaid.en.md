# 4.2 — Generate Mermaid diagrams

## Description

Prompt to generate Mermaid diagrams that document the solution: current and proposed flow, sequence, components and entity-relationship. Diagrams must be consistent with the code and real architecture.

**When to use it:** during or after solution design (`04-01`), to document and visually communicate the changes.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | low — produces visual documentation artifacts, does not modify code or configuration |
| Required inputs | approved design (`04-01`), real system architecture, source code or components involved in the change |
| Allowed tools | read-only access to code, design and architecture; no execution or repository writes required, only generates Mermaid blocks as text |
| Permitted autonomy | A0 — Analyze the existing design and code; A1 — Propose the diagrams as a documentation artifact |
| Stop criteria | stop if there is no approved design (`04-01`) to derive the diagrams from; never invent components, actors, or flows that do not exist in the real code or design |
| Expected output | see `## Expected output` |
| Minimum evidence | each diagram corresponds to components/flows verifiable in the cited code or design; valid Mermaid syntax (special characters escaped, no unquoted `end` used as node text) |
| Recommended next prompt | `04-03-casos-de-uso` to complete the functional documentation of the solution |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Based on the analysis and design of the change, generate clear and useful Mermaid diagrams to document the solution.

Inputs:
- approved design: [PASTE OR REFERENCE TO 04-01, OR "does not exist yet"]
- real architecture / relevant source code: [PATHS OR UNKNOWN]

I need:
1. Flow diagram of current and proposed process
2. Sequence diagram
3. Component diagram
4. If applicable, simplified entity-relationship diagram

Mermaid diagram type to use for each one:
- Flow: use `flowchart TD` or `flowchart LR`.
- Sequence: use `sequenceDiagram`.
- Components: Mermaid has no native component-diagram type; use `flowchart LR` with subgraphs per module.
- Entity-relationship: use `erDiagram`.

Rules:
- If no approved design (`04-01`) or verifiable code/architecture is referenced, stop and request it before generating any diagram.
- Diagrams must be consistent with the code and real architecture.
- Do not invent non-existent components.
- Clearly label actors, services, modules and data.
- Strict Syntax Rule: Always escape special characters (such as parentheses, brackets, or commas) inside node labels by wrapping them in double quotes (e.g., id["Node Name (Detail)"]). NEVER use HTML tags (such as <br> or <b>) inside Mermaid node text to avoid rendering failures.
- Never use the word "end" as a node ID or as unquoted node text: it is a reserved keyword and breaks flowchart parsing.

Deliver:
- Mermaid block per diagram,
- brief explanation of each one.
```

---

## Use with standard formula

```text
Use the Mermaid diagrams prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- components: [INVOLVED COMPONENTS]
- documents to review: approved design, architecture, source code
- specific output objective: set of Mermaid diagrams for technical documentation
- depth level: medium
```

---

## Expected output

One Mermaid block for each diagram with its explanation:

| Diagram | Description |
|---|---|
| Current flow | How the flow works today |
| Proposed flow | How it will work after the change |
| Sequence | Interaction between actors and services |
| Components | Relationship between system modules |
| ER (if applicable) | Entities and data relationships involved |
