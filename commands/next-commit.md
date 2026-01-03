---
argument-hint: '[slug]'
description: Worker command - commit uncommitted changes in worktree
---

# Commit Worker

You are a **Worker AI**. Commit any uncommitted changes in the worktree for the given slug.

Slug given: "$ARGUMENTS"

---

## Step 1: Verify Location

```
Verify you are in the correct worktree: trees/{slug}
Run: git status
```

If not in a git repository or wrong location, STOP and report error.

---

## Step 2: Check for Changes

```bash
git status
git diff --stat
```

If no changes (working tree clean), report "No changes to commit" and stop.

---

## Step 3: Review Changes

Before committing:

1. Review what changed with `git diff`
2. Ensure changes are intentional (not debug code, temp files, etc.)
3. If suspicious changes found, report them and ask for guidance

---

## Step 4: Stage and Commit

```bash
git add -A
git commit -m "wip({slug}): checkpoint uncommitted work

🤖 Generated with [TeleClaude](https://github.com/InstruktAI/TeleClaude)

Co-Authored-By: TeleClaude <noreply@instrukt.ai>"
```

Use a more specific commit message if the changes are clear:
- `fix({slug}): ...` for bug fixes
- `feat({slug}): ...` for features
- `refactor({slug}): ...` for refactoring

---

## Step 5: Report Completion

```
✅ Changes committed

Files changed: {count}
Commit: {hash}

Ready to continue work.
```

---

## Error Handling

**If commit fails (pre-commit hooks):**
- Fix the issues (lint, format, etc.)
- Re-run `git add -A && git commit`

**If merge conflict markers found:**
- Report the conflict
- Do NOT commit conflict markers
- Stop and report to Master

---

## What You Do NOT Do

- ❌ Push to remote (Master handles merging)
- ❌ Modify code beyond fixing lint/format issues
- ❌ Delete or reset changes without explicit approval
