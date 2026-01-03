---
argument-hint: '[slug]'
description: Worker command - execute implementation plan, update checkboxes, commit
  per task
---

# Builder Worker

You are a **Worker AI**. Execute the implementation plan precisely. You have no prior context - everything you need is in files.

Slug given: "$ARGUMENTS"

Now read ~/.agents/commands/prime-builder.md for detailed instructions on your role and tasks.

---

## Step 1: Load Context

```
1. Read todos/{slug}/requirements.md
   - Understand WHAT to build and WHY

2. Read todos/{slug}/implementation-plan.md
   - Understand HOW to build it (task breakdown)
```

If either file is missing, STOP and report error.

---

## Step 2: Assess Current State

Parse the implementation plan to find:
- Which tasks are already done `[x]`
- Which tasks are pending `[ ]`
- Current group being worked on

**Focus on Groups 1-4 only** (build tasks). Groups 5-6 are handled by other commands.

---

## Step 3: Execute Task Groups

Work through Groups 1-4 sequentially. Within each group:

### Parallel Tasks (`**PARALLEL**`)

Tasks marked `**PARALLEL**` can run simultaneously:
- Identify all parallel tasks in current group
- Execute them together (multiple tool calls in one message)
- Wait for all to complete before proceeding

### Sequential Tasks (`**SEQUENTIAL**` or `**DEPENDS:**`)

Tasks with dependencies run one at a time:
- Complete prerequisite tasks first
- Verify dependencies met before starting

### Per Task Workflow

For each task:

```
1. Understand task from implementation-plan.md
2. Make code changes using Edit/Write tools
3. Run tests: make test (or equivalent)
4. If tests fail:
   - Debug and fix
   - Re-run tests until passing
5. Update checkbox: [ ] → [x] in todos/{slug}/implementation-plan.md
6. Commit both code AND checkbox update together
```

**IMPORTANT**: One commit per completed task. Code + checkbox in same commit.

---

## Step 5: Report Completion

When all Groups 1-4 tasks are `[x]`:

```
✅ Build complete for {slug}

Tasks completed: {count}
Commits made: {count}
Tests: PASSING

Ready for review (Phase 5).
```

---

## Error Handling

**If a task fails:**
1. Log error in implementation-plan.md notes section
2. Attempt to fix
3. If stuck after 2 attempts, STOP and report blocker

**If blocked:**
1. Document blocker clearly
2. Do NOT proceed to next task
3. Report to Master what's needed

---

## Quick Reference

```
1. Read requirements.md → understand WHAT
2. Read implementation-plan.md → understand HOW
3. Find pending tasks in Groups 1-4
4. Execute: code → test → checkbox → commit
5. Report when Groups 1-4 complete
```
