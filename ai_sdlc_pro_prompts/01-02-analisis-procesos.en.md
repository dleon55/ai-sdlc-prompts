# 1.2 — Locate processes, procedures and project policies

## Description

Startup prompt to map all project governance: processes, procedures, policies, standards, branching strategy, QA strategy, CI/CD and engineering rules. Establishes what exists, what is incomplete and what does not exist.

**When to use it:** before any analysis or implementation work, to understand the project governance framework and avoid violating already defined rules.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | low — this is a read-only location of governance documents; it does not execute changes, although missing an existing policy can lead to violating it in later work |
| Required inputs | read access to README, docs/, exported wiki, ADRs, contribution files, and workflows in the repository |
| Allowed tools | reading of documentation, markdown files, and configuration files — no execution or changes |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if no documentary evidence is found for a governance category (e.g., security or branching), state it as "does not exist" instead of assuming an implicit policy |
| Expected output | see `## Expected output` |
| Minimum evidence | every row of the matrix must cite the file or path found; categories marked incomplete or nonexistent must state what was searched and not found |
| Recommended next prompt | `01-01-arranque-comprension-repositorio` if the technical inventory has not been done yet; `02-01-analisis-issue` to start the functional analysis of the concrete work |

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

Constraints:
- base every finding on observable evidence (the file, section, or commit where it is documented); don't base it on assumptions about how a team "should" work,
- explicitly distinguish between "not documented" and "the process does not exist" — the absence of a document doesn't prove the practice isn't followed informally, so flag it as a documentation gap, not as a missing process,
- don't execute changes or create new documentation; this prompt only locates and classifies what already exists,
- if a governance category has no documentary evidence found, mark it "does not exist" in the matrix instead of assuming an implicit policy.

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
| processes | `CONTRIBUTING.md` | Defines the contribution flow: mandatory ES/EN structure, how to run `build.py`, and pre-PR validations | Complete | References the Editorial Contract but doesn't detail the post-agent human review process |
| QA | `tests/test_build.py`, `tests/test_i18n.py` | Pytest suite that validates index generation, ES/EN parity, and each prompt's structure | Complete | No QA strategy document exists apart from the tests themselves; it should be made explicit in text |
| deployment | `.github/workflows/deploy.yml` | GitHub Actions pipeline that builds and publishes `index.html` | Incomplete | Doesn't document rollback conditions or a staging environment prior to production |
| procedures | | | | |
| policies | | | | |
| standards | | | | |
| architecture | | | | |
| security | | | | |
| branching | | | | |
| operations | | | | |
