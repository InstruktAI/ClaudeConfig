---
argument-hint: '[scope|aspects]'
description: Review code changes for quality, bugs, and project compliance. Use before
  committing or as part of /next-work.
---

# Code Review

Review code changes using specialized analysis. Outputs findings organized by severity.

**Arguments:** "$ARGUMENTS"
- If scope (file/folder): review only those files
- If aspects (code, tests, errors, types, comments, simplify): run only those reviews
- Default: review all changed files with all applicable aspects

## Step 1: Identify Changes

```bash
git status
git diff --name-only HEAD
```

If scope provided, filter to those files. Otherwise review all changed files.

## Step 2: Load Project Context

Read project standards:
- `CLAUDE.md` or `AGENTS.md` - Project patterns and conventions
- Existing code in same modules - Match existing style

## Step 3: Determine Applicable Reviews

Based on changes, select which aspects to run:

| Aspect | When to Run | Focus |
|--------|-------------|-------|
| **code** | Always | Quality, bugs, project compliance |
| **tests** | Test files changed | Coverage, behavioral testing |
| **errors** | Error handling code | Silent failures, catch blocks |
| **types** | Types added/modified | Type design, invariants |
| **comments** | Comments/docs added | Accuracy, maintainability |
| **simplify** | After other reviews pass | Clarity, reduce complexity |

## Step 4: Run Reviews

For each applicable aspect, analyze the changes:

### code (General Quality)
- Follows existing patterns in codebase
- No unnecessary abstractions
- Functions are focused and small
- No code duplication
- Types explicit (no `Any`/`any`)
- Null/undefined handled properly
- Error cases handled, not swallowed

### tests (Test Quality)
- Tests behavior, not implementation
- One assertion per test
- Edge cases covered
- Mocks only at boundaries
- No testing of private methods

### errors (Error Handling)
- No empty catch blocks
- Errors logged with context
- No swallowed exceptions
- Fail-fast where appropriate
- Recovery logic explicit

### types (Type Design)
- Types express invariants
- No `any` or `Any`
- Illegal states unrepresentable
- Validation at boundaries

### comments (Documentation)
- Comments match code behavior
- No stale/misleading comments
- Complex logic explained
- API contracts documented

### simplify (Complexity Reduction)
- Can logic be simplified?
- Are abstractions necessary?
- Can functions be smaller?
- Is code self-documenting?

## Step 5: Aggregate Findings

Organize all findings by severity:

```markdown
# Code Review Findings

## Critical Issues (must fix)
- [aspect] `file:line` - Description
  - Suggested fix: ...

## Important Issues (should fix)
- [aspect] `file:line` - Description
  - Suggested fix: ...

## Suggestions (nice to have)
- [aspect] `file:line` - Minor improvement
  - Reason: ...

## Strengths
- Positive observations about the code

## Verdict
[ ] APPROVE - Ready to commit/merge
[ ] REQUEST CHANGES - Fix critical/important issues first
[ ] NEEDS DISCUSSION - Architectural concerns to resolve
```

## Step 6: Output

1. Print the findings summary to console
2. If `todos/{subject-slug}/` exists, also write to `todos/{subject-slug}/review-findings.md`

## Usage

**Review all changes:**
```
/next-review
```

**Review specific files:**
```
/next-review src/api/handler.py
```

**Run specific aspects:**
```
/next-review tests errors
```

**Review scope with aspects:**
```
/next-review src/api tests code
```

## Tips

- Run before committing, not after
- Fix critical issues before moving on
- Re-run after applying fixes
- Use with `/next-work` for full workflow integration
