# 15.1 — User stories and Gherkin acceptance criteria

## Description

Prompt for business analysts and product owners. Converts raw business requests and requirements into structured user stories and incorporates acceptance criteria in Gherkin format (Given / When / Then).

**When to use:** when defining detailed business requirements, prior to technical design or architectural definitions.

---

## Mandatory prior context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a Senior Business Analyst & Product Owner. Convert the attached functional description or business requirement into detailed user stories with their respective acceptance criteria structured in Gherkin format.

Inputs:
- requirement or business request: [PASTE]
- affected module or process: [MODULE]
- standard/compliance: [NONE / ISO 29110 / MOPROSOFT]

Activities:
1. Analyze the business request and identify the main goals.
2. Identify:
   - user roles (actors) involved,
   - the functional need (the "what"),
   - the business value (the "why").
3. Write user stories under the classic template: "As a [Role], I want [Action], so that [Benefit]".
4. Write detailed acceptance criteria in Gherkin format:
   - Scenario: description of the case,
   - Given [Context or precondition],
   - When [Action or trigger event],
   - Then [Expected result or system behavior].
5. Specify critical business rules, alternate flows, and special User Experience (UX) guidelines.

Output:
1. User stories (standard template)
2. Acceptance criteria (Gherkin format for happy path, alternate, and validation failure scenarios)
3. Business rules and functional implications
4. UI/UX design considerations (accessibility, visual validation feedback)
```

---

## Standard formula usage

```text
Use the user stories prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [PASTE FUNCTIONAL REQUIREMENT]
- branch: main
- environment: DEV
- components: registration module
- documents to review: business rules, mockups
- specific output goal: detailed user stories with Gherkin acceptance criteria
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| User story | "As a [User], I want [Feature], so that [Value]" |
| Gherkin criteria | Given / When / Then of successful and failure scenarios |
| Business rules | Validation constraints, business limits, and policies |
| UI/UX considerations | Visual guidelines, accessibility, and component behaviors |
