---
argument-hint: '[slug]'
description: Worker command - merge, archive, cleanup after review passes
---

# Finalize Worker

You are a **Worker AI** that handles post-review bookkeeping: merge, archive, cleanup.

**Prerequisites**: Review must have APPROVE verdict in `todos/{slug}/review-findings.md`.

Slug given: "$ARGUMENTS"

---

## Step 2: Verify Prerequisites

```
1. Read todos/{slug}/review-findings.md
2. Verify verdict is APPROVE
3. If not APPROVE, STOP and report: "Review not approved. Cannot finalize."
```

---

## Step 3: Final Tests

```
make test
```

Or equivalent test command. All tests must pass before proceeding.

---

## Step 4: Merge to Main (Fresh Main Required)

Use fast-forward only to keep local commits intact; do not overwrite local main.

```bash
git fetch origin main
git checkout main
git pull --ff-only origin main
git merge {slug} --no-edit
```

If merge conflicts:
1. Resolve conflicts
2. Run tests again
3. Commit resolution

---

## Step 5: Push to Remote

```bash
git push origin main
```

---

## Step 6: Archive Todo Folder

```
1. Determine next archive number:
   - Check done/ folder for existing {NNN}-* folders
   - Take highest NNN, add 1
   - Zero-pad to 3 digits (e.g., 001, 002, 042)

2. Create archive folder:
   mkdir -p done/{NNN}-{slug}

3. Move todo folder:
   mv todos/{slug}/ done/{NNN}-{slug}/
```

---

## Step 7: Log Delivery

Append to `todos/delivered.md`:

```
| {date} | {slug} | {title} | DELIVERED | {commit-hash} | done/{NNN}-{slug} |
```

Create file with header if it doesn't exist:

```markdown
# Delivered Items

| Date | Slug | Title | Outcome | Commit | Archive |
|------|------|-------|---------|--------|---------|
```

---

## Step 8: Update Roadmap

```
1. Read todos/roadmap.md
2. Find the item for {slug} (marked [>])
3. Remove item from roadmap
4. Save file
```

---

## Step 9: Final Commit and Push

```bash
git add -A
git commit -m "chore({slug}): finalize delivery

- Archived to done/{NNN}-{slug}
- Updated roadmap
- Logged to delivered.md

🤖 Generated with [TeleClaude](https://github.com/InstruktAI/TeleClaude)

Co-Authored-By: TeleClaude <noreply@instrukt.ai>"

git push origin main
```

---

## Step 10: Remove Worktree (Last)

If a worktree exists for this slug, remove it as the final cleanup step.

```
1. Check if trees/{slug} exists
2. If it exists, follow ~/.agents/commands/remove-worktree.md for safe removal
3. If it does not exist, continue
```

---

## Step 11: Report Completion

```
✅ Finalized: {slug}

- Merged to main: ✓
- Archived to: done/{NNN}-{slug}
- Reported in delivered.md: ✓
- Roadmap item removed

Item complete. Ready for next work.
```

---

## Error Handling

**If merge fails:**
- Report conflict details
- Do NOT force merge
- Wait for Master guidance

**If any step fails:**
- Document what failed
- Do NOT proceed to later steps
- Report to Master
