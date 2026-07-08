# 14.1 — Dependency and workspace auditing in monorepos

## Description

Prompt to map, audit, and document architectural boundaries, the local dependency graph, and couplings between subprojects or workspaces in a monorepo architecture.

**When to use it:** at the beginning of a major technical change or refactoring that affects shared libraries (`packages/`, `shared/`) inside a monorepo.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | low — maps the dependency graph read-only, does not modify code or workspace configuration |
| Required inputs | source workspace/subproject to analyze, monorepo configuration files (package.json, pnpm-workspace.yaml, go.work, lerna.json, turbo.json, tsconfig.json) |
| Allowed tools | reading of configuration files and workspace source code — no build execution or dependency installation |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if the monorepo configuration files are not accessible or are ambiguous, state the graph as incomplete instead of assuming unverified dependency relationships |
| Expected output | see `Output:` inside `## Complete prompt` |
| Minimum evidence | each reported local dependency (direct, transitive, or circular) references the configuration file where it is declared |
| Recommended next prompt | `05-01-plan-implementacion` to plan the isolation refactor; `04-04-adr-decisiones-arquitectura` to document the decision if it involves an architectural boundary change |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Map the monorepo dependency network and identify potential architecture violations (cycles, forbidden imports, phantom dependencies) after the suggested change.

Inputs:
- repository: [NAME OR URL]
- source workspace/subproject: [WORKSPACE/SUBPROJECT]
- configuration files (package.json, go.work, lerna.json, turbo.json, tsconfig.json): [READ OR PASTE DETAILS]

Activities:
1. Analyze the internal and external dependency graph of the indicated subproject/workspace.
2. Identify:
   - shared local dependencies (e.g. @repo/shared, common-utils),
   - external runtime dependencies vs development dependencies,
   - potential circular imports (package A imports B and B imports A).
3. Evaluate if the proposed change introduces unnecessary coupling.
4. Design an import relationship matrix.

Constraints:
- don't run the build, install dependencies, or execute any monorepo scripts — the analysis is strictly read-only over configuration and source code,
- if the configuration files are not accessible or are ambiguous, state the graph as incomplete instead of assuming unverified dependency relationships,
- every reported local dependency (direct, transitive, or circular) must reference the exact configuration file where it is declared,
- don't flag a coupling as "requires isolation" without concrete graph evidence — avoid speculative conclusions about build impact.

Output:
1. Dependency Graph Mapping (workspaces involved)
2. Potential Cycles and Conflicts Analysis
3. Build Speed Impact Assessment (Turbo/Lerna caching)
4. Isolation or Refactor Recommendation
```

---

## Use with standard formula

```text
Use the monorepo dependency audit prompt and adapt it to:
- repository: [NAME OR URL]
- workspace/subproject: [DIRECTORY/PACKAGE]
- standard/compliance: [NONE]
- issue or requirement: [REFERENCE]
- branch: [BRANCH]
- environment: DEV
- components: package.json, workspaces, common/
- documents to review: pnpm-workspace.yaml, package.json
- specific output objective: dependency graph with local impact matrix
- depth level: high
```

---

## Expected output

| Workspace | Depends on (local) | Dependency type | Key external dependency | Risk / Note |
|---|---|---|---|---|
| apps/web | @repo/ui, @repo/utils | runtime | react, next | low |
| apps/api | @repo/shared, @repo/db | runtime | express, prisma | medium — @repo/shared also imports from apps/api (cycle detected) |
| packages/shared | @repo/utils | runtime | zod | low |
| packages/ui | — | runtime | react | low |
| packages/db | @repo/utils | dev + runtime | prisma, pg | low |
