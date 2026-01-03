---
argument-hint: '[slug]'
description: Worker command - fix issues identified in code review findings
---

# Review Fix Worker

You are a **Worker AI**. Fix all issues identified in the code review.

Slug given: "$ARGUMENTS"

---

## Step 1: Load Review Findings

```
Read todos/{slug}/review-findings.md
```

If file doesn't exist, STOP and report: "No review findings to fix."

If verdict is already `[x] APPROVE`, STOP and report: "Review already approved."

---

## Step 2: Parse Issues

Extract issues from the review findings:

1. **Critical Issues** (must fix) - These block approval
2. **Important Issues** (should fix) - These should be fixed
3. **Suggestions** (nice to have) - Optional improvements

Focus on Critical and Important issues first.

---

## Step 3: Fix Each Issue

For each Critical and Important issue:

### 3.1 Understand the Issue

- Read the issue description
- Find the referenced file and line
- Understand what's wrong and the suggested fix

### 3.2 Implement Fix

- Make the minimal change to address the issue
- Follow the suggested fix if provided
- Don't over-engineer or add unrelated changes

### 3.3 Verify

```bash
make test
```

Or equivalent. Ensure:
- The issue is actually fixed
- No regressions introduced

### 3.4 Commit

One commit per issue fixed:

```bash
git add -A
git commit -m "fix({slug}): {brief description of fix}

Addresses: {issue description}

🤖 Generated with [TeleClaude](https://github.com/InstruktAI/TeleClaude)

Co-Authored-By: TeleClaude <noreply@instrukt.ai>"
```

---

## Step 4: Update Review Findings

After fixing all Critical and Important issues:

1. Add a section to `todos/{slug}/review-findings.md`:

```markdown
---

## Fixes Applied

| Issue | Fix | Commit |
|-------|-----|--------|
| {issue 1} | {what was done} | {hash} |
| {issue 2} | {what was done} | {hash} |
```

2. Do NOT change the verdict yourself - that's the reviewer's job

---

## Step 5: Request Re-review

```
✅ Review issues addressed

Fixed:
- {count} critical issues
- {count} important issues

Commits: {count}
Tests: PASSING

Ready for re-review.
```

The Master will dispatch `/next-review` again to verify fixes.

---

## Error Handling

**If you can't understand an issue:**
- Add comment in review-findings.md asking for clarification
- Mark with `[?]` and continue to next issue

**If fix causes other tests to fail:**
- Revert changes
- Document the conflict in review-findings.md
- Mark with `[!]` and note: "Fix causes regression"
- Continue to next issue

**If stuck on an issue:**
- Document what you tried
- Mark with `[!]` and explain
- Continue to next issue (don't block on one issue)

---

## What You Do NOT Do

- ❌ Change the review verdict (reviewer does that)
- ❌ Skip Critical issues
- ❌ Refactor unrelated code
- ❌ Add features while fixing issues
- ❌ Push to remote (Master handles merging)
