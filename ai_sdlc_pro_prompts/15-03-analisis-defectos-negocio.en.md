# 15.3 — Defect reporting and business impact analysis

## Description

Prompt for manual testers and functional analysts. Helps structure professional bug reports, translating technical errors (console messages, failed HTTP responses) into business consequences and user impact, facilitating prioritization by the development team.

**When to use:** when reporting a bug in the incident backlog, ensuring it contains all the necessary information for developers.

---

## Mandatory prior context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a QA Defect Analyst. Help the tester document and analyze a defect, translating visual symptoms and potential technical errors into clear business impacts and precise reproduction steps for development.

Inputs:
- description of the observed error: [INDICATE]
- steps you were performing: [INDICATE]
- expected behavior: [INDICATE]
- technical error (screenshot, console log, or HTTP code if available): [PASTE IF APPLICABLE]

Activities:
1. Analyze the reported anomalous behavior and identify which business rule or user flow is failing.
2. Translate any technical error logs or codes provided into readable functional language (e.g.: "Error 500 when saving" -> "Critical failure in persistence when saving customer data").
3. Structure the bug report according to industry best practices:
   - defect title (clear and informative),
   - technical severity vs business priority,
   - precise steps to reproduce (repro steps),
   - actual vs expected behavior,
   - test data used,
   - business impact (e.g.: prevents the user from paying, degrades visual experience, breaks accessibility).

Output:
Generate a structured defect report form with the following sections:
1. Defect Title
2. Severity (Blocker / Critical / Major / Minor) and Business Impact
3. Steps to Reproduce
4. Actual vs Expected Behavior
5. Test Data and Environment
6. Technical Diagnosis for Developers (functional translation of logs)
```

---

## Standard formula usage

```text
Use the defect analysis prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [LOG OR INCIDENT DESCRIPTION]
- branch: main
- environment: QA
- components: payment gateway
- documents to review: payment policies, console screenshot
- specific output goal: structured bug report with business impact
- depth level: high
```

---

## Expected output

An organized card ready to copy into Jira or GitHub Issues:

### 1. Defect Title
`[ERROR] Finish purchase button freezes and order is not submitted`

### 2. Severity and Business Impact
*   **Severity:** Blocker.
*   **Impact:** Customers cannot complete purchases. Directly affects sales conversion and stops the billing operational workflow.

### 3. Steps to Reproduce
1. Add any product to the shopping cart.
2. Go to the checkout screen.
3. Fill in valid shipping fields.
4. Click the "Finish purchase" button.

### 4. Actual vs Expected Behavior
*   **Actual Behavior:** The button shows an infinite spinner, a `POST /api/orders 500` error is observed in the console, and it does not advance to confirmation.
*   **Expected Behavior:** The order should be processed, redirect to the thank you screen, and clear the cart.

### 5. Test Data and Environment
*   **Environment:** QA (https://qa.prompts.lionsystems.com.mx/)
*   **Browser:** Chrome v120 / Windows 11
*   **Data:** Test buyer account `test_buyer@lionsystems.com`

### 6. Technical Diagnosis for Developers
*   **Origin:** The server returns `HTTP 500 (Internal Server Error)` when calling the order creation endpoint, possibly due to a mismatch in shipping database fields mapping.
