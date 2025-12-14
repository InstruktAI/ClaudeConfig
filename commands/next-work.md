---
argument-hint: '[subject]'
description: Find out what to do next and continue WIP or break down todo story into
  requirements + implementation plan. Use for queries like "what's next", "next-work",
  "next", "work", or "start work".
---

You are now in **WORK mode**. Your output is ALWAYS working code that is covered by tests.

Follow these steps to find out what to do next:

## Step 1: Fix Bugs FIRST

1. Open `todos/bugs.md` to see if there are any open bugs (unchecked items).
2. If there are open bugs, pick the first one and work on fixing it.
3. Work on fixing all open bugs before moving on.

## Step 2: Determine Subject

ARGUMENT GIVEN: "$ARGUMENTS"

**If subject provided as argument**:

- Use that subject to find `todos/{subject-slug}/` folder

**If NO subject provided**:

1. Read `todos/roadmap.md`
2. Find the item marked as in-progress (`- [>]`)
3. If no in-progress item, find first unchecked item (`- [ ]`) that is clear to you (mark `[~]` if unsure and ask for input)
4. Extract description and generate slug
5. Use that as the subject

## Step 3: Create or Switch to Worktree

**CRITICAL**: All work must be done in an isolated worktree to avoid conflicts.

1. **Check if worktree already exists**:

   - Run `/list-worktrees`
   - Look for worktree with branch name matching `{subject-slug}`

2. **If worktree exists**:

   - Switch to existing worktree directory: `cd worktrees/{subject-slug}`
   - **Sync with main** (critical to avoid stale branches):
     - `git fetch origin`
     - `git merge origin/main`
     - If conflicts occur: resolve them before continuing, or ask user for guidance
     - If merge brought changes: run `make install` to update dependencies
   - Continue with existing work

3. **If worktree does NOT exist**:
   - Run `/create-worktree {subject-slug}` (no port offset needed)
   - This will:
     - Create `worktrees/{subject-slug}/` directory
     - Create git branch `{subject-slug}`
     - Set up isolated environment
     - Switch to the worktree directory
   - Run `make install` first to get all the tools to work
   - Continue with new work

**Important**: Always verify you're in the worktree directory before proceeding with implementation tasks.

## Step 4: Check Requirements & Implementation Plan Exist

1. Check if `todos/{subject-slug}/requirements.md` exists

   - If NOT: Run `/next-requirements {subject}`
   - Wait for it to complete, then continue

2. Check if `todos/{subject-slug}/implementation-plan.md` exists
   - If NOT: Run `/next-implementation {subject-slug}`
   - Wait for it to complete, then continue

If neither requirements nor a clear roadmap item exist (or info is unclear), run `/next-roadmap` to gather details before continuing.

## Step 5: Assess Current State

1. Read `todos/{subject-slug}/implementation-plan.md`
2. Count unchecked boxes in each section
3. Determine what's actually incomplete

**If only deployment/cleanup tasks remain** → Skip to Step 8
**If implementation tasks remain** → Continue to Step 6

## Step 6: Execute Implementation Plan

1. Read `todos/{subject-slug}/requirements.md` to understand the goals
2. Read `todos/{subject-slug}/implementation-plan.md` to see the task breakdown
3. Determine outstanding tasks

### Task Execution Strategy

**For each task group** (sequentially):

1. **Identify parallel vs sequential tasks**:

   - Tasks marked with `**PARALLEL**` can run simultaneously
   - Tasks marked with `**SEQUENTIAL**` or `**DEPENDS:**` must run in order

2. **Execute parallel tasks**:

   ```
   If multiple tasks in group are marked **PARALLEL**:
   - Create separate tool calls for each parallel task
   - Execute all tool calls in a single message
   - Wait for all to complete before continuing
   ```

3. **Execute sequential tasks**:

   - Run one at a time
   - Wait for completion before next task

4. **Complete task workflow** (per task):

   - Make code changes
   - **Delegate to `debugger` subagent**: Run tests and fix issues
   - Update checkbox from `- [ ]` to `- [x]` in `todos/{subject-slug}/implementation-plan.md`
   - Commit with both code changes AND todo update: `git add -A && git commit -m "type(scope): description"`

   **IMPORTANT**:

   - Each commit = one completed task (code + todo checkbox)
   - Only push after merging to main branch

### Parallel Execution Example

```markdown
### Group 2: Core Implementation

- [ ] **PARALLEL** Create handler.py
- [ ] **PARALLEL** Create validator.py
- [ ] **DEPENDS: Group 1** Integrate components
```

**Execution**:

1. Run "Create handler.py" AND "Create validator.py" in parallel (single message, multiple tool calls)
2. Wait for both to complete
3. Run "Integrate components" sequentially

## Step 7: Comprehensive Review & Auto-Fix

**After completing all implementation tasks (Groups 1-4)**:

### 7.1 Verify Requirements Alignment

1. Read `todos/{subject-slug}/requirements.md`
2. Get code changes: `git diff main..{subject-slug}`
3. Confirm all requirements are addressed in the implementation
4. Report any missing requirements

### 7.2 Run Code Review

1. **Mark checkbox in-progress**: Update `- [ ] Review created` → `- [>]` in `todos/{subject-slug}/implementation-plan.md`
2. **Run review**: `/next-review`
3. Review outputs findings to `todos/{subject-slug}/review-findings.md`

### 7.3 Process Review Findings

1. Parse `todos/{subject-slug}/review-findings.md` to identify:
   - Critical issues (must fix)
   - Important issues (should fix)
   - Suggestions (nice to have)
2. **Mark checkbox complete**: Update `- [>] Review created` → `- [x]` in `todos/{subject-slug}/implementation-plan.md`
3. **Commit**: `git add -A && git commit -m "docs: capture review findings"`

### 7.4 Auto-Fix Issues

1. **Mark checkbox in-progress**: Update `- [ ] Review feedback handled` → `- [>]` in `todos/{subject-slug}/implementation-plan.md`

**For each auto-fixable issue**:

2. Apply fix using appropriate tools (Edit/Write)
3. Run linter and tests: `make lint && make test` (or `(pnpm|npm run|bun) test`)
4. If tests pass: continue to next fix
5. If tests fail: debug and retry

**After all fixes applied**:

6. **Mark checkbox complete**: Update `- [>] Review feedback handled` → `- [x]` in `todos/{subject-slug}/implementation-plan.md`
7. **Commit**: `git add -A && git commit -m "fix: address review findings"`

### 7.5 Quality Gate

**Before proceeding to merge**:

- All requirements addressed
- All critical issues resolved
- All tests passing
- "Review feedback handled" checked in implementation-plan.md

**If critical issues remain unresolved**:

- HALT - do NOT proceed to Step 8
- Report issues and wait for manual intervention

**If all clear**:

- Proceed to Step 8 (merge and deploy)

## Step 8: Merge Worktree and Deploy

**Execute Group 6 checkboxes with full checkbox discipline.**

### 8.1 Pre-Merge (in worktree)

1. **Mark checkbox in-progress**: `- [ ] Tests pass locally` → `- [>]`
2. Run final tests: `make test` (or equivalent)
3. **Mark checkbox complete**: `- [>]` → `- [x]`

4. **Mark checkbox in-progress**: `- [ ] All Groups 1-5 complete` → `- [>]`
5. Verify all prior group checkboxes are `[x]`
6. **Mark checkbox complete**: `- [>]` → `- [x]`

7. **Commit pre-merge checkboxes**: `git add -A && git commit -m "docs: mark pre-merge tasks complete"`

### 8.2 Merge to Main

1. Switch to project root: `cd ../..`
2. Checkout main: `git checkout main`
3. Merge: `git merge {subject-slug}`
4. Push: `git push origin main`

### 8.3 Post-Merge (on main)

1. **Mark checkbox in-progress**: `- [ ] Merged to main and pushed` → `- [>]`
2. Verify merge succeeded (check `git log`)
3. **Mark checkbox complete**: `- [>]` → `- [x]`
4. **Commit**: `git add -A && git commit -m "docs: mark merge complete"`

5. **Mark checkbox in-progress**: `- [ ] Deployment verified` → `- [>]`
6. Verify deployment on all computers
7. **Mark checkbox complete**: `- [>]` → `- [x]`
8. **Commit**: `git add -A && git commit -m "docs: mark deployment verified"`

9. **Mark checkbox in-progress**: `- [ ] Worktree cleaned up` → `- [>]`
10. Run `/remove-worktree {subject-slug}`
11. Verify with `/list-worktrees`
12. **Mark checkbox complete**: `- [>]` → `- [x]`
13. **Commit**: `git add -A && git commit -m "docs: mark worktree cleanup complete"`

14. **Mark checkbox in-progress**: `- [ ] Roadmap item marked complete` → `- [>]`
15. Update `todos/roadmap.md`: Change `- [>]` → `- [x]` for this item
16. **Mark checkbox complete**: `- [>]` → `- [x]`
17. **Commit**: `git add -A && git commit -m "docs: mark roadmap item complete"`

18. **Push final changes**: `git push origin main`

## Important Notes

- **Worktree isolation**: ALWAYS work in a worktree to avoid conflicts with main branch
- **Parallel execution**: When possible, execute independent tasks simultaneously
- **Testing is mandatory**: All code changes must have passing tests
- **Commit per task**: One commit = code changes + checkbox update (NOT two separate commits)
- **Commit in worktree**: Create local commits while in worktree (no push yet)
- **Push after merge**: Only push after merging to main
- **Check dependencies**: Always verify `**DEPENDS:**` requirements are met
- **Update roadmap**: Mark items in-progress (`[>]`) and complete (`[x]`)
- **Ask questions**: If requirements unclear, ask before implementing

## Work Session Template

For each work session:

1. Check bugs first
2. Create/switch to worktree
3. Read requirements.md
4. Read implementation-plan.md
5. Identify current task group
6. Execute parallel tasks simultaneously

**Per task completion**:

7. Run linter and tests
8. Update checkbox in implementation-plan.md
9. Commit (one commit with code + checkbox)

**After all implementation tasks (Group 5: Review)**:

10. Verify requirements alignment (Step 7.1)
11. Mark "Review created" in-progress → run `/next-review` → complete + commit
12. Mark "Review feedback handled" in-progress → fix issues → complete + commit
13. Quality gate check (Step 7.5)

**Group 6: Pre-merge (in worktree)**:

14. Mark "Tests pass locally" in-progress → test → complete
15. Mark "All Groups 1-5 complete" in-progress → verify → complete
16. Commit pre-merge checkboxes

**Group 6: Merge**:

17. Switch to main, merge, push

**Group 6: Post-merge (on main)**:

18. Mark "Merged to main" complete + commit
19. Mark "Deployment verified" in-progress → verify → complete + commit
20. Mark "Worktree cleaned up" in-progress → cleanup → complete + commit
21. Mark "Roadmap item complete" in-progress → update roadmap → complete + commit
22. Push final changes

## Error Handling

If a task fails:

1. Log the error in implementation-plan.md notes section
2. Fix the issue
3. Re-run the task
4. Only mark complete when successful

If blocked:

1. Document blocker in implementation-plan.md
2. Ask user for clarification
3. Don't proceed until unblocked
