# 15.2 — Design of manual and functional test cases

## Description

Prompt for manual testers and functional QAs. Generates detailed manual test cases (step-by-step, test data, expected results) from user stories or functional specifications without requiring programming skills.

**When to use:** when planning the testing phase of a feature, before starting exploratory or manual tests.

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
