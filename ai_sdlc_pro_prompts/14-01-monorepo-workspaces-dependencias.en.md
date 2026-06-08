# 14.1 — Dependency and workspace auditing in monorepos

## Description

Prompt to map, audit, and document architectural boundaries, the local dependency graph, and couplings between subprojects or workspaces in a monorepo architecture.

**When to use it:** at the beginning of a major technical change or refactoring that affects shared libraries (`packages/`, `shared/`) inside a monorepo.

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
