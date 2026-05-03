# 7.12 — Accessibility (a11y) Audit and UX Compliance

## Description

Prompt geared towards QA Automation or Frontend Architect profiles. It examines HTML, React, Vue, or UI template code to verify compliance with WCAG 2.1 standards. It detects contrast issues, keyboard navigability, missing ARIA attributes, and semantic structure flaws.

**When to use it:** Before merging a Pull Request that introduces or modifies visual frontend components, or when auditing an existing system to meet accessibility regulations.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as a Web Accessibility (a11y) Auditor expert in WCAG 2.1 (Levels A and AA) standards. Analyze the source code of the provided component or UI view to identify accessibility barriers and recommend exact corrections.

Inputs:
- ui_framework: [React / Vue / HTML / Angular]
- frontend_code: [PASTE THE COMPONENT OR PAGE CODE HERE]

Analysis Activities:
1. HTML SEMANTICS: Verify the correct use of tags (`<nav>`, `<main>`, `<article>`, `<button>` vs `<div>` with `onClick`).
2. KEYBOARD NAVIGATION: Ensure all interactive elements are accessible via `Tab` and have clear `:focus-visible` states. There must be no "keyboard traps".
3. SCREEN READERS: Check the presence and correct use of `aria-*` tags, `alt` attributes on informative images, and ignoring (`aria-hidden="true"`) decorative images.
4. FORMS: Validate that `<input>` elements are correctly linked to their `<label>` (id/for) and that error messages are announced by screen readers (`aria-describedby`, `aria-live`).

Mandatory Output:
1. WCAG REPORT: List of detected violations categorized by Severity (Critical, High, Medium).
2. CORRECTED CODE: The same component refactored with the applied semantic tags and ARIA attributes.
3. QA CHECKLIST: Manual steps a QA tester must perform (e.g., "Navigate the component using only the Tab key").
```

---

## Use with standard formula

```text
Use the accessibility audit prompt and adapt it to:
- ui_framework: [FRAMEWORK]
- frontend_code: [CODE]
- specific output objective: find WCAG 2.1 AA errors and obtain refactored code.
- depth level: exhaustive
```

---

## Expected output

| Section | Expected content |
|---|---|
| WCAG Report | Violations grouped by severity and their impact on users |
| Corrected Code | Refactored frontend ready for copy-paste |
| QA Checklist | Manual accessibility testing steps |
