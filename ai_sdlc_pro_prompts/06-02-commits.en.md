# 6.2 — Quality commit message generation

## Description

Prompt to generate small, clear and traceable commit messages, aligned with the project standard. Includes alternatives if the change should be divided into multiple commits.

**When to use it:** before committing any change, to guarantee traceability and consistency with the repository history.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Generate small, clear, traceable commit messages aligned with the project standard.

Inputs:
- issue,
- change type,
- component,
- brief description.

Deliver:
1. suggested main commit
2. alternative commits if the change should be divided
3. justification of why it is convenient to divide the work
```

---

## Use with standard formula

```text
Use the commit messages prompt and adapt it to:
- issue: [NUMBER OR REFERENCE]
- change type: [feat / fix / refactor / docs / test / chore]
- component: [AFFECTED MODULE OR FILE]
- brief description: [WHAT WAS DONE IN ONE LINE]
- specific output objective: main commit + alternatives if applicable to divide
```

### Real example

```text
Use the commit messages prompt and adapt it to:
- issue: #842
- change type: fix
- component: api/notifications
- brief description: fixes duplicate push notification sending when updating order
```

---

## Recommended commit formats

```text
fix(api/notifications): fixes duplicate sending when updating order #842

feat(auth): adds token expiration validation in middleware #123

refactor(db): extracts user query to separate repository #456

docs(readme): updates deployment instructions in Docker #78

test(payments): adds edge cases for negative amount in processor #99
```

## Expected output

| Commit | Description | Justification |
|---|---|---|
| Main | | |
| Alternative 1 | | |
| Alternative 2 | | |
