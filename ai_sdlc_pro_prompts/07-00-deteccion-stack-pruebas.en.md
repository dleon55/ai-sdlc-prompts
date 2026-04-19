# 7.0 — Test Stack Detection

## Description

Prompt to detect and document the active test stack in the repository. Produces a structured **test stack profile** that is attached as context to implementation prompts (`07-07` through `07-10`), eliminating the need for each agent to re-discover the project's tools and conventions.

**When to use:** once per project, or when the test stack changes. The generated profile is reused across all test implementation prompt executions.

---

## Required prior context

> Include the block from `00-framework.md` before this prompt.

---

## Full prompt

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

The agent must generate a block in this exact format, ready to be copied and pasted as context into prompts 07-07 through 07-10:

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
> test implementation prompt: `07-07`, `07-08`, `07-09`, `07-10`.
