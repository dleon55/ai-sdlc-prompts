# 15.2 — Design of manual and functional test cases

## Description

Prompt for manual testers and functional QAs. Generates detailed manual test cases (step-by-step, test data, expected results) from user stories or functional specifications without requiring programming skills.

**When to use:** when planning the testing phase of a feature, before starting exploratory or manual tests.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | documentation |
| Expected risk | low — generates a test case matrix as documentation, does not execute tests or modify code; a missed edge case can leave a scenario without QA coverage |
| Required inputs | user story or requirement to validate, acceptance criteria or business rules if they exist (ideally from `15-01`) |
| Allowed tools | no execution or system access — only drafting of the test case matrix based on the information provided |
| Permitted autonomy | A1 — Propose the manual test case suite as an artifact ready for QA execution |
| Stop criteria | do not invent business rules or system behaviors not described in the requirement; if acceptance criteria are missing, state this and limit coverage to what is verifiable with the available information |
| Expected output | see `## Expected output` |
| Minimum evidence | each test case includes ID, precondition, execution steps, test data, and a verifiable expected result; the suite covers happy path, alternate, negative, and at least one edge case |
| Recommended next prompt | `07-05-automatizacion-antigravity` to automate the critical cases in the suite; `07-03-pruebas-e2e` if formal end-to-end test design is required |

---

## Mandatory prior context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a Functional QA Tester. Generate a suite of detailed manual test cases to functionally validate the attached requirement or user story.

Inputs:
- user story or requirement: [PASTE]
- acceptance criteria or business rules: [PASTE IF APPLICABLE]

Activities:
1. Analyze the user flows described in the feature specification.
2. Identify primary test scenarios:
   - happy path,
   - alternate scenarios,
   - validation or error flows (negative paths),
   - edge cases (limit values, empty fields, etc.).
3. Write each test case detailed in a tabular structure.
4. For each test case specify:
   - test case ID,
   - short descriptive title,
   - precondition (prior system state),
   - execution steps (sequential actions),
   - suggested test data (specific inputs),
   - expected result (observable correct behavior).

Constraints:
- explicitly distinguish "must-test" cases (critical path, business rules, security) from "nice-to-test" cases (cosmetic or low-probability variations), and prioritize the former if QA time is limited,
- do not design test cases that depend on real production data (customer accounts, real financial information, PII) — always use synthetic data or data from a controlled test environment,
- each test case must be traceable to the specific requirement or acceptance criterion it validates; do not include cases without that reference,
- do not invent business rules or system behaviors that are not described in the requirement or the provided acceptance criteria; if they are missing, state this and limit coverage to what is verifiable with the available information.

Output:
Present a structured table with the following fields for each test case:
| ID | Title | Precondition | Execution Steps | Input Data | Expected Result |
```

---

## Standard formula usage

```text
Use the manual test cases prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [FUNCTIONAL REFERENCE]
- branch: main
- environment: QA
- components: checkout module
- documents to review: user stories, business rules
- specific output goal: complete matrix of step-by-step manual test cases
- depth level: high
```

---

## Expected output

A clear table with numbered test cases covering successful and error flows:

| ID | Title | Precondition | Execution Steps | Input Data | Expected Result |
|---|---|---|---|---|---|
| TC-01 | Successful Login | Registered user exists | 1. Navigate to login<br>2. Enter credentials<br>3. Click enter | User: admin<br>Pass: admin123 | Redirection to Home and welcome banner visible |
| TC-02 | Login with Invalid Password | Registered user exists | 1. Navigate to login<br>2. Enter incorrect password<br>3. Click enter | User: admin<br>Pass: wrongpass | Error message "Incorrect password" and stays on login page |
| TC-03 | Required email field validation on registration | Registration form loaded and empty | 1. Navigate to registration form<br>2. Leave the "Email" field empty<br>3. Fill the rest of the fields with valid data<br>4. Click "Register" | Email: (empty)<br>Other fields: valid | The form is not submitted, "Email is required" is shown next to the field and it is highlighted in red — validates the required-fields acceptance criterion of the registration story |
