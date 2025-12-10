---
argument-hint: '[subject]'
description: Find out what to do next and continue WIP or break down todo story into
  requirements + implementation plan. Use for queries like \"what's next\", \"next-work\",
  \"next\", \"work\", or \"start work\".
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
   - Commit ONCE with both code changes AND todo update: `/commit-commands:commit`

   **IMPORTANT**:

   - Use `/commit-commands:commit` while in worktree
   - Each commit = one completed task (code + todo checkbox)
   - Only use `/deploy` after merging to main branch

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

### 7.2 Run Specialized Code Review

Delegate to pr-review-toolkit: `/pr-review-toolkit:review-pr all`

This spawns specialized agents that auto-select based on changes:

- **code-reviewer**: Quality, bugs, CLAUDE.md compliance
- **pr-test-analyzer**: Test coverage, behavioral testing
- **silent-failure-hunter**: Error handling analysis
- **type-design-analyzer**: Type quality assessment
- **comment-analyzer**: Documentation accuracy

### 7.3 Capture Review Findings

1. Wait for all agents to complete
2. Aggregate agent reports into `todos/{subject-slug}/review-findings.md`
3. Parse findings to identify:
   - Critical issues (must fix)
   - Auto-fixable issues
   - Manual attention needed

### 7.4 Auto-Fix Issues

**For each auto-fixable issue**:

1. Apply fix using appropriate tools (Edit/Write)
2. Run linter and tests: `make lint && make test` (or `(pnpm|npm run|bun) test`)
3. If tests pass: continue to next fix
4. If tests fail: debug and retry

**After all fixes applied**:

1. Commit all fixes in one commit: `/commit-commands:commit` with message "fix: address review findings"
2. Update checkbox in `implementation-plan.md`: "Review feedback handled"

### 7.5 Quality Gate

**Before proceeding to merge**:

- ✅ All requirements addressed
- ✅ All critical issues resolved
- ✅ All tests passing
- ✅ "Review feedback handled" checked in implementation-plan.md

**If critical issues remain unresolved**:

- HALT - do NOT proceed to Step 8
- Report issues and wait for manual intervention

**If all clear**:

- Proceed to Step 8 (merge and deploy)

## Step 8: Merge Worktree and Deploy

**After all tasks complete and review feedback handled**:

1. **Ensure all changes committed in worktree**:

   - Verify `git status` is clean
   - All tasks should be committed (you've been doing `/commit-commands:commit` per task)

2. **Switch back to main branch**:

   - `cd` to project root (outside worktree): `cd ../..`
   - `git checkout main`

3. **Merge worktree branch to main**:

   - `git merge {subject-slug}`
   - Resolve any conflicts if needed

4. **Push to git**:

   - git push origin main
   - No new commit needed - merge already brought all commits to main

5. **Remove worktree**:

   - Run `/remove-worktree {subject-slug}`
   - This removes both the worktree directory and branch

6. **Verify cleanup**:
   - Run `/list-worktrees` to confirm worktree removed
   - Check main branch has all changes

## Important Notes

- **Worktree isolation**: ALWAYS work in a worktree to avoid conflicts with main branch
- **Parallel execution**: When possible, execute independent tasks simultaneously
- **Testing is mandatory**: All code changes must have passing tests
- **Commit per task**: One commit = code changes + checkbox update (NOT two separate commits)
- **Use /commit in worktree**: Create local commits with `/commit-commands:commit` (no deployment yet)
- **Use /deploy after merge**: Only push and deploy after merging to main
- **Check dependencies**: Always verify `**DEPENDS:**` requirements are met
- **Update roadmap**: Mark items in-progress (`[>]`) and complete (`[x]`)
- **Ask questions**: If requirements unclear, ask before implementing

## Work Session Template

For each work session:

1. ✅ Check bugs first
2. 🌳 Create/switch to worktree
3. 📖 Read requirements.md
4. 📋 Read implementation-plan.md
5. 🎯 Identify current task group
6. ⚡ Execute parallel tasks simultaneously

**Per task completion**:

7. 🧪 Run linter and tests
8. ✔️ Update checkbox in implementation-plan.md
9. 💾 `/commit-commands:commit` (one commit with code + checkbox)

**After all implementation tasks**:

10. 📋 Verify requirements alignment (Step 7.1)
11. 🔍 Code review: `/pr-review-toolkit:review-pr all` (Step 7.2)
12. 📝 Aggregate findings to review-findings.md (Step 7.3) 
13. 🔧 Auto-fix all issues (Step 7.4)
14. 14. ✅ Quality gate check (Step 7.5)
15. 🔀 Merge to main: `cd ../.. && git checkout main && git merge {subject-slug}`
16. 🚀 Push to git
17. 🧹 Cleanup: `/remove_worktree {subject-slug}`

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
