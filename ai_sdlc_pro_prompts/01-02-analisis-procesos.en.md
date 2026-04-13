# 1.2 — Locate processes, procedures and project policies

## Description

Startup prompt to map all project governance: processes, procedures, policies, standards, branching strategy, QA strategy, CI/CD and engineering rules. Establishes what exists, what is incomplete and what does not exist.

**When to use it:** before any analysis or implementation work, to understand the project governance framework and avoid violating already defined rules.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
I want you to identify within the repository all documents, files or sections that correspond to processes, procedures, policies, standards, guidelines, coding guides, workflows, branch definition, QA strategy, CI/CD strategy and software engineering rules.

Activities:
1. Search in README, docs, exported wiki, documentation folders, markdowns, ADRs, contribution files and workflows.
2. Classify what is found by category:
   - processes,
   - procedures,
   - policies,
   - standards,
   - architecture,
   - QA,
   - security,
   - branching,
   - deployment,
   - operations.
3. Indicate what exists, what is incomplete and what does not exist.

Output format:
- matrix by category,
- found file/path,
- description,
- completeness level,
- observations.
```

---

## Use with standard formula

```text
Use the process and policy location prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [CURRENT BRANCH]
- documents to review: README, docs/, .github/, workflows/
- specific output objective: project governance matrix with completeness status
- depth level: medium
```

---

## Expected output

Matrix with the following columns:

| Category | File/Path | Description | Completeness | Observations |
|---|---|---|---|---|
| processes | | | | |
| procedures | | | | |
| policies | | | | |
| standards | | | | |
| architecture | | | | |
| QA | | | | |
| security | | | | |
| branching | | | | |
| deployment | | | | |
| operations | | | | |
