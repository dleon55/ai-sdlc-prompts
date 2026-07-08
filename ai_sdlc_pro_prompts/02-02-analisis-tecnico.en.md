# 2.2 - Deep technical analysis of existing code

## Description

Static and traceable analysis prompt for reconstructing how code related to a requirement or incident actually works. It examines the end-to-end flow, contracts, data, dependencies, security, observability, tests, technical debt, and regression risks without modifying files.

**When to use it:** after functional analysis (`02-01`) and before cross-impact analysis (`02-03`) and solution design (`04-01`).

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — this is the foundation for cross-impact analysis (`02-03`) and design (`04-01`); an incorrect mapping of flow, contracts, or dependencies propagates errors into those phases, although the prompt does not modify files |
| Required inputs | output of `02-01`, repository or workspace, issue or requirement, target branch or commit, environment, documents and contracts to review |
| Allowed tools | reading of code, logs, and git history; non-destructive execution limited to inspections, builds, or focused tests already approved by the project (maximum three self-correction cycles) — no file edits or commits |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if behavior cannot be verified at runtime, label it as static analysis; if the JSON metadata `status` is `blocked`, stop and escalate instead of forcing conclusions |
| Expected output | see `## Expected output` |
| Minimum evidence | every finding and risk must cite path, symbol, and line; every executed verification must record command, result, and limitations |
| Recommended next prompt | `02-03-impacto-cruzado` |

---

## Mandatory previous context

> Include the block from `00-framework.en.md` before this prompt.

---

## Complete prompt

```text
Objective:
Analyze the existing code related to the requirement or incident and document, with verifiable evidence, how it actually works in the repository's current state.

Constraints:
- Work in analysis-only mode. Do not modify files, generate code, or create commits.
- Do not present assumptions as facts.
- Exclude from recursive searches: **/node_modules/**, **/venv/**, **/.git/**, **/dist/**, **/build/**, and **/*.log.
- Use exact paths and line references when supported by the tool.
- If runtime behavior cannot be verified, explicitly label the result as static analysis.

Inputs:
- repository or workspace: [NAME, URL, OR PATH]
- issue or requirement: [REFERENCE AND DESCRIPTION]
- target branch or commit: [BRANCH / SHA]
- environment: [LOCAL / DEV / QA / PROD]
- initial components or modules: [LIST OR UNKNOWN]
- documents and contracts to review: [PATHS OR UNKNOWN]
- depth level: [MEDIUM / HIGH / FORENSIC]

Activities:
1. Perform preflight and record:
   - branch, commit, and working tree state;
   - relevant recent changes, active branches, and worktrees;
   - uncommitted files and possible conflicts with other agents;
   - applicable policies, standards, documentation, and governance files.
2. Bound the scope:
   - translate the requirement into observable technical behaviors;
   - identify entry points, outputs, actors, data, and external systems;
   - state what is in and out of scope.
3. Locate the involved artifacts:
   - paths, modules, packages, layers, and owners;
   - classes, functions, endpoints, jobs, events, commands, and UI components;
   - models, tables, migrations, queries, caches, and storage;
   - configuration, environment variables, feature flags, referenced secrets, and permissions;
   - tests, fixtures, mocks, pipelines, and related documentation.
4. Reconstruct the current end-to-end flow from input to response or final effect:
   - UI or consumer;
   - routing/controller;
   - application or use case;
   - domain and business rules;
   - persistence, messaging, and integrations;
   - error handling, retries, transactions, idempotency, and concurrency;
   - logs, metrics, traces, and alerts.
5. Trace dependencies and boundaries:
   - relevant imports and internal calls;
   - dependencies between packages or workspaces;
   - API contracts, events, schemas, and compatibility;
   - external dependencies and versions when declared;
   - circular coupling, improper cross-layer access, or violated boundaries.
6. Assess behavior and quality:
   - validation, authorization, authentication, and sensitive-data handling;
   - empty, loading, error, and success states plus accessibility when UI exists;
   - technical debt, duplication, complexity, and dead code;
   - existing coverage and untested critical scenarios;
   - differences between documentation, configuration, tests, and executable code.
7. Verify non-destructively when feasible:
   - run only inspections, builds, or focused tests approved by the project;
   - record command, result, and limitations;
   - apply the framework's maximum three-cycle self-correction limit.
8. Classify every statement as:
   - CONFIRMED FACT: supported by code, configuration, a test, or execution;
   - FINDING: technical conclusion derived from cited evidence;
   - ASSUMPTION: hypothesis pending confirmation;
   - RISK: possible impact with probability and severity;
   - RECOMMENDATION: next action without implementing it.
9. Finish with open questions and missing evidence required to confirm runtime behavior.

Output format:
0. Valid JSON metadata without comments:
   {
     "status": "complete|partial|blocked",
     "analysis_mode": "static|static_and_runtime",
     "repository": "",
     "branch": "",
     "commit": "",
     "scope": [],
     "entry_points": [],
     "file_dependencies": [{"from": "", "to": "", "type": "import|call|data|event|config"}],
     "couplings": [{"source": "", "target": "", "evidence": "", "severity": "low|medium|high|critical"}],
     "risks": [{"id": "", "description": "", "probability": "low|medium|high", "impact": "low|medium|high|critical"}],
     "verification": [{"command": "", "result": "passed|failed|not_run", "evidence": ""}],
     "open_questions": []
   }
1. Executive summary
2. Scope, exclusions, and repository state
3. Current end-to-end flow
4. Component, layer, and dependency map
5. Contracts, data, security, and observability
6. Relevant files with path, symbol, lines, and purpose
7. Existing tests, observable coverage, and executed validations
8. Confirmed facts
9. Prioritized technical findings
10. Assumptions and open questions
11. Modification risks
12. Recommendations and suggested order for cross-impact analysis (`02-03`)

Quality criteria:
- Every finding and risk references concrete evidence.
- Current code is distinguished from legacy, generated, test-only, or unused code.
- The flow includes alternative paths and error handling, not only the happy path.
- Runtime behavior is not inferred from file names alone.
- The output enables `02-03` and `04-01` without repeating discovery.
```

---

## Use with standard formula

```text
Use the deep technical analysis prompt and adapt it to:
- repository: [NAME OR URL]
- workspace/subproject: [PATH OR NOT APPLICABLE]
- issue or requirement: [REFERENCE]
- branch or commit: [BRANCH / SHA]
- environment: [LOCAL / DEV / QA / PROD]
- components: [INVOLVED COMPONENTS]
- documents to review: [PATHS]
- specific output objective: verifiable current flow + dependency map + modification risks
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| JSON metadata (0) | Status, scope, dependencies, couplings, risks, and verification |
| Summary and scope (1-2) | Executive result, exclusions, and analyzed Git state |
| Current flow (3) | End-to-end sequence, variants, errors, and side effects |
| Technical architecture (4-5) | Layers, boundaries, contracts, data, security, and observability |
| Evidence (6-8) | Paths, symbols, lines, tests, and confirmed facts |
| Assessment (9-11) | Findings, assumptions, and prioritized risks |
| Continuity (12) | Recommendations for cross-impact analysis and subsequent design |
