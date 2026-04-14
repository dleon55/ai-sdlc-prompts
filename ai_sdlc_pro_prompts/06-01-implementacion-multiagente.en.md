# 6.1 — Secure multi-agent implementation

## Description

Controlled execution prompt to implement the approved solution in an environment where multiple agents may be modifying the repository in parallel. Prioritizes minimal changes, atomic commits and conflict detection.

**When to use it:** during the execution phase, after the plan (`05-01`) and risks (`05-02`) have been approved.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Mode: controlled execution

Objective:
Implement the approved solution respecting a multi-agent environment with concurrent changes.

Rules:
1. Review recent changes before editing.
2. Work with minimal and controlled changes.
3. Do not modify files outside the scope.
4. Make atomic commits per logical unit.
5. If you detect foreign changes in the same area, stop and document.

Activities:
1. Identify files to modify
2. Apply changes by component
3. Maintain compatibility with existing contracts and flows
4. Update related tests and documentation
5. Prepare commit proposal

Deliver:
- modified files,
- summary of change per file,
- residual risks,
- suggested commit message.
```

---

## Use with standard formula

```text
Use the multi-agent implementation prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- branch: [WORKING BRANCH]
- environment: [DEV / QA]
- components: [FILES AND MODULES TO MODIFY]
- documents to review: approved implementation plan, technical design
- specific output objective: applied changes with atomic commits and without conflicts
- depth level: high
```

---

## Expected output

| File | Applied change | Residual risk | Suggested commit |
|---|---|---|---|
