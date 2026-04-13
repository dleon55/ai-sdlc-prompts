# 4.2 — Generate Mermaid diagrams

## Description

Prompt to generate Mermaid diagrams that document the solution: current and proposed flow, sequence, components and entity-relationship. Diagrams must be consistent with the code and real architecture.

**When to use it:** during or after solution design (`04-01`), to document and visually communicate the changes.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Based on the analysis and design of the change, generate clear and useful Mermaid diagrams to document the solution.

I need:
1. Flow diagram of current and proposed process
2. Sequence diagram
3. Component diagram
4. If applicable, simplified entity-relationship diagram

Rules:
- Diagrams must be consistent with the code and real architecture.
- Do not invent non-existent components.
- Clearly label actors, services, modules and data.

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
