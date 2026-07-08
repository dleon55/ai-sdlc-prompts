# 2.3 — Cross-impact analysis

## Description

Prompt to evaluate the impact of the change on all modules, processes, data, integrations, environments and pipelines of the system. Detects direct and indirect impacts and generates a severity matrix.

**When to use it:** after deep technical analysis (`02-02`) and before solution design (`04-01`).

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — although read-only, it has a wide blast radius (modules, data, integrations, environments, pipelines, semver); underestimating an impact can let a breaking change or an undetected production risk slip through |
| Required inputs | output of `02-02` (technical flow and dependencies), architecture, API contracts, database schema, involved components |
| Allowed tools | reading of code, architecture, contracts, and configuration — no execution or changes |
| Permitted autonomy | A0 — Analyze |
| Stop criteria | if there is not enough evidence to rule out impact on a critical component (security, data, production, semver), classify it as an unconfirmed high risk instead of omitting it from the matrix |
| Expected output | see `## Expected output` |
| Minimum evidence | every row of the impact matrix must cite the verified component or contract, not just one assumed by name or convention |
| Recommended next prompt | `04-01-diseno-solucion` |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Analyze the impact of the requested change on other modules, processes, data, integrations, environments, pipelines, monorepo workspaces/subprojects, and versioning policies (semver).

Activities:
1. Evaluate impact on:
   - monorepo workspaces / subprojects (for example, shared dependencies, common utility packages),
   - API contracts and semantic versioning (semver) of local packages,
   - frontend,
   - backend,
   - database,
   - integrations,
   - infrastructure,
   - CI/CD (independent or shared build pipelines),
   - security and regulatory compliance (ISO, MAAGTICSI, etc.),
   - monitoring,
   - documentation.
2. Detect direct and indirect impacts.
3. Evaluate affectation to other use cases.

Constraints:
- this is a read-only analysis: don't modify code, configuration, or API contracts to evaluate the impact,
- for every component marked as impacted, trace the actual dependency or import chain that connects it to the change (the file that imports it, the function that calls it, the contract it consumes) — don't mark it by name similarity or architectural intuition,
- if you cannot verify the dependency chain of a critical component (security, data, production, semver) due to missing visibility (inaccessible code, an unversioned contract, absent documentation), classify it as an unconfirmed high risk and explicitly flag the visibility gap — never omit it from the matrix or treat it as safe without evidence,
- don't close the impact matrix with "low" severity on components you could not inspect directly.

Output:
- impact matrix (including monorepo workspaces and packages),
- severity,
- affected component/workspace,
- impact type (direct/indirect, breaking changes in local dependencies),
- risk,
- mitigation recommendation.
```

---

## Use with standard formula

```text
Use the cross-impact analysis prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [CURRENT BRANCH]
- environment: [DEV / QA / PROD]
- components: [INVOLVED COMPONENTS]
- documents to review: architecture, API contracts, DB schema
- specific output objective: cross-impact matrix with severity by component
- depth level: high
```

---

## Expected output

| Component | Impact type | Severity | Risk | Recommendation |
|---|---|---|---|---|
| CI/CD | Direct — `deploy.yml` invokes `build.py` on every push to `main`; if `build.py` changes its validation signature, the `python build.py` step can fail the pipeline | High | The workflow has no automatic rollback step if `build.py` errors out mid-way through generating the index | Add a verification step (`pytest tests/test_build.py`) before generating `index.html` in the pipeline |
| documentation | Indirect — every prompt modified in `ai_sdlc_pro_prompts/*.md` requires updating its `.en.md` pair; verified by cross-checking `tests/test_i18n.py` | Medium | Risk that the build publishes an out-of-sync ES/EN pair if the parity test doesn't run in CI | Confirm `test_i18n.py` runs in `deploy.yml` before the build, not only locally |
| frontend | | | | |
| backend | | | | |
| database | | | | |
| integrations | | | | |
| infrastructure | | | | |
| security | | | | |
| monitoring | | | | |
