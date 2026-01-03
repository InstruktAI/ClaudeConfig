---
argument-hint: '[slug]'
description: Worker command - review code against requirements, output findings with
  verdict
---

You are a **Reviewer AI**. Review code changes using specialized analysis. Outputs findings organized by severity.

## Step 1: Determine slug

Slug given: "$ARGUMENTS"

**If slug provided as argument**:

- Use that slug to find `todos/{slug}/` folder

**If NO slug provided**:

1. Read `todos/roadmap.md`
2. Find the first item marked as in-progress (`- [>]`) and which has no `todos/{slug}/review-findings.md` yet.
3. If no in-progress item, don't do anything and inform the user.

---

## Step 2: Load Context

1. Read `todos/{slug}/requirements.md` - Understand WHAT should have been built
2. Read `todos/{slug}/implementation-plan.md` - Understand HOW it was supposed to be built
3. Read `~/.agents/docs/development/coding-directives.md`
4. Read `~/.agents/docs/development/testing-directives.md`
5. Read `README.md`, `docs/*` - Project patterns and conventions

---

## Step 3: Identify Changes

```bash
git status
git diff main..HEAD --name-only
git diff main..HEAD
```

---

## Step 4: Determine Applicable Reviews

Based on changes, select which aspects to run:

| Aspect | When to Run | Focus |
| ------ | ----------- | ----- |
| **code** | Always | Quality, bugs, project compliance |
| **tests** | Test files changed | Coverage, behavioral testing |
| **errors** | Error handling code | Silent failures, catch blocks |
| **types** | Types added/modified | Type design, invariants |
| **comments** | Comments/docs added | Accuracy, maintainability |
| **simplify** | After other reviews pass | Clarity, reduce complexity |

---

## Step 5: Run Reviews

For each applicable aspect, analyze the changes:

### code (General Quality)

- Follows existing patterns in codebase
- No unnecessary abstractions
- Follows coding directives

### tests (Test Quality)

- Tests behavior, not implementation
- One assertion per test
- Edge cases covered
- Follows testing directives

### errors (Error Handling)

- No empty catch blocks
- Errors logged with context
- No swallowed exceptions
- Fail-fast where appropriate
- Recovery logic explicit

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

---

## Step 6: Aggregate Findings

Organize all findings by severity. Write to `todos/{slug}/review-findings.md`:

```markdown
# Code Review: {slug}

**Reviewed**: {date}
**Reviewer**: Codex

## Requirements Coverage

| Requirement | Status | Notes |
|-------------|--------|-------|
| {req 1} | ✅ Implemented | |
| {req 2} | ⚠️ Partial | Missing edge case X |
| {req 3} | ❌ Missing | Not implemented |

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

---

## Verdict

**[ ] APPROVE** - Ready to merge
**[ ] REQUEST CHANGES** - Fix critical/important issues first

{Mark one with [x]}

### If REQUEST CHANGES:

Priority fixes needed:
1. {Critical issue 1}
2. {Critical issue 2}
```

---

## Step 7: Output

- Write to `todos/{slug}/review-findings.md`
- Brief summary to the user and mention file location.

---

## Verdict Criteria

**APPROVE** when:
- All requirements implemented
- No critical issues
- Tests pass
- Code quality acceptable

**REQUEST CHANGES** when:
- Any requirement missing
- Critical issues exist
- Security vulnerabilities found
- Tests failing or missing

---

## IMPORTANT

- Run before merging, not after
- Fix critical issues before moving on
- Re-run after applying fixes
- You ONLY review and report. Master decides next action.
