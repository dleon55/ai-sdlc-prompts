# 7.0 — Test Stack Detection

## Description

Prompt to detect and document the active test stack in the repository. Produces a structured **test stack profile** that is attached as context to implementation prompts (`07-07` through `07-11`), eliminating the need for each agent to re-discover the project's tools and conventions.

**When to use:** once per project, or when the test stack changes. The generated profile is reused across all test implementation prompt executions.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | low — a read-only discovery of the repository, does not execute tests or modify files |
| Required inputs | read access to the repository: root configuration files (package.json, pyproject.toml, pom.xml, etc.), CI/CD workflows, existing tests directory |
| Allowed tools | read-only access to the repository; may non-destructively verify that a test command exists (e.g. inspecting the script in package.json), but does not run the full test suite as part of this prompt |
| Permitted autonomy | A0 — Analyze (reading and inventory); applies no changes and requires no approval |
| Stop criteria | explicitly mark a field "not detected" instead of assuming or inventing a framework, command, or convention not backed by a real file in the repository |
| Expected output | see `## Expected output — Test stack profile` |
| Minimum evidence | every field in the profile backed by an explicitly cited file path or verified command, not by an unsourced inference |
| Recommended next prompt | `07-01-pruebas-unitarias` (or directly `07-07-implementacion-pruebas-unitarias` using the profile as context) |

---

## Mandatory previous context

> Include the block from `00-framework.md` before this prompt.

---

## Complete prompt

```text
Objective:
Detect and document the repository's test stack to produce a reusable profile
that contextualizes test implementation prompts.

Detection steps:

1. PROJECT CONFIGURATION
   Review the root configuration files of the project:
   - package.json / package-lock.json / yarn.lock / pnpm-lock.yaml
   - pyproject.toml / setup.cfg / requirements*.txt / Pipfile
   - pom.xml / build.gradle / build.sbt
   - Gemfile / .ruby-version
   - go.mod / go.sum
   - Any detected framework configuration file

2. TEST FRAMEWORKS
   Identify the active framework for each type:

   a) Unit tests:
      - project's main language
      - unit test framework (pytest, Jest, Vitest, JUnit, RSpec, Go test, etc.)
      - mock/stub library (unittest.mock, pytest-mock, jest.mock, Sinon, Mockito, etc.)
      - coverage configuration (pytest-cov, nyc/c8, JaCoCo, SimpleCov, etc.)

   b) Integration tests:
      - integration strategy (DB fixtures, Testcontainers, docker-compose, etc.)
      - HTTP testing tool (supertest, httpx, RestAssured, etc.)
      - test data providers (factories, fixtures, seeders)

   c) E2E tests:
      - installed E2E framework (Playwright, Cypress, Selenium, Puppeteer, Robot Framework, etc.)
      - language of E2E scripts (if different from main language)
      - use of Page Object Model or other UI abstraction pattern

   d) Smoke tests:
      - existing smoke/healthcheck scripts
      - available health endpoints (/health, /ping, /status, etc.)
      - CI/CD pipeline integration

3. PROJECT CONVENTIONS
   Detect active conventions:
   - test directory: where tests live (tests/, __tests__/, spec/, src/**/*.test.*)
   - file naming pattern: test_*.py, *.test.ts, *_spec.rb, etc.
   - function/method naming pattern: test_*, it(), describe(), should_*, etc.
   - preferred internal structure: AAA (Arrange/Act/Assert), Given/When/Then, etc.

4. CI/CD PIPELINE
   Review existing workflows:
   - files in .github/workflows/, .gitlab-ci.yml, Jenkinsfile, etc.
   - steps that run tests: exact commands used
   - coverage reporting configuration and minimum threshold if present

5. CURRENT STATE
   Report:
   - Are there existing tests? How many and in what state?
   - Is active coverage configuration present? What is the current threshold?
   - Are there currently failing tests?

Constraints:
- this is a read-only detection: do not install dependencies, do not run the full test suite, and do not run any other command that changes the state of the repository or the environment,
- if a profile field cannot be backed by a real, cited file or command, mark it explicitly as "not detected" — never assume or invent a framework, version, or convention,
- always distinguish "not detected" (insufficient evidence was found; it may exist but was not located) from "not configured" or "not present" (actively confirmed that the element does not exist in the repository); do not treat these terms as synonyms,
- if the same test type appears to use two different tools (e.g., two unit test frameworks in the same repo), report it as an ambiguous finding instead of arbitrarily picking one.

Deliverables:
Produce the test stack profile in the standard format defined below.
```

---

## Standard formula usage

```text
Use the test stack detection prompt and adapt it to:
- repository: [NAME OR URL]
- branch: [MAIN OR WORKING BRANCH]
- documents to review: root configuration files, package.json/pyproject.toml,
  .github/workflows/, existing tests directory
- specific output goal: complete and verified test stack profile
- depth level: medium
```

---

## Expected output — Test stack profile

The agent must generate a block in this exact format, ready to be copied and pasted as context into prompts 07-07 through 07-11:

```
── TEST STACK PROFILE ──────────────────────────────────────────────────
Repository  : [name or URL]
Branch      : [analyzed branch]
Date        : [detection date]

MAIN LANGUAGE : [language]
RUNTIME / VER : [version]

── UNIT TESTS ──────────────────────────────────────────────────────────
Framework        : [name and version]
Mock library     : [name and version]
Coverage         : [tool] — minimum threshold: [X%] | not configured
Directory        : [relative path]
File name pattern: [pattern]
Run command:
  [full verified command]

── INTEGRATION TESTS ───────────────────────────────────────────────────
Strategy         : [fixtures / Testcontainers / docker-compose / not detected]
HTTP testing     : [tool or not detected]
Test data        : [factories / fixtures / seeders / not detected]
Directory        : [relative path]
Run command:
  [full verified command or not detected]

── E2E TESTS ───────────────────────────────────────────────────────────
Framework        : [name and version or not detected]
Script language  : [language]
UI pattern       : [Page Object / no pattern / not detected]
QA base URL      : [URL or environment variable]
Directory        : [relative path]
Commands:
  headless : [command]
  headed   : [command]

── SMOKE / HEALTHCHECK ─────────────────────────────────────────────────
Existing script  : [path or not detected]
Health endpoints : [list of endpoints or not detected]
CI integration   : [yes — step: X / no]

── CI/CD PIPELINE ──────────────────────────────────────────────────────
Platform         : [GitHub Actions / GitLab CI / Jenkins / not detected]
File             : [workflow path]
Test steps       : [exact workflow commands]
Coverage gate    : [threshold in CI or not configured]

── CONVENTIONS ─────────────────────────────────────────────────────────
Test structure   : [AAA / Given-When-Then / no explicit convention]
Function naming  : [detected pattern]
File naming      : [detected pattern]

── CURRENT STATE ───────────────────────────────────────────────────────
Existing tests   : [N files / N tests]
Failing tests    : [N or none]
Current coverage : [X% or unmeasured]

── NOTES AND ASSUMPTIONS ───────────────────────────────────────────────
[any relevant findings, ambiguities, or recommendations]
────────────────────────────────────────────────────────────────────────
```

> This block must be pasted at the beginning (after the `00-framework.md` block) of any
> test implementation prompt: `07-07`, `07-08`, `07-09`, `07-10`, `07-11`.

### Example of a completed profile (excerpt, this prompt library's own repository)

```
── TEST STACK PROFILE ──────────────────────────────────────────────────
Repository  : ai-sdlc-prompts
Branch      : main

MAIN LANGUAGE : Python
RUNTIME / VER : not pinned in a version file — not detected (verify against the CI runner)

── UNIT TESTS ──────────────────────────────────────────────────────────
Framework        : pytest — version not detected (no pyproject.toml/requirements.txt pins it; installed via `pip install pytest` in the workflow)
Mock library     : not detected (no use of unittest.mock or pytest-mock found in tests/)
Coverage         : not configured (no pytest-cov or coverage configuration detected)
Directory        : tests/
Run command:
  python -m pytest tests/ -q  (verified in .github/workflows/deploy.yml, build job)

── CI/CD PIPELINE ──────────────────────────────────────────────────────
Platform         : GitHub Actions
File             : .github/workflows/deploy.yml
Test steps       : `pip install pytest` followed by `python -m pytest tests/ -q` in the build job
Coverage gate    : not configured
```
