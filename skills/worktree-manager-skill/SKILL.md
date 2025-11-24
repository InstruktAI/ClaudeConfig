---
name: worktree-manager-skill
description: Manage git worktrees with consistent conventions. Use when the user wants to create, list, or remove worktrees in any git repository.
allowed-tools: SlashCommand
---

# Worktree Manager Skill

Manage git worktrees with enforced conventions for consistent directory structure across all projects.

## Purpose

Ensure all worktrees are created in a standardized `trees/` directory, preventing inconsistency across sessions and projects.

## When to Use

Use this skill when the user wants to:
- **Create** a new worktree for parallel development
- **List** existing worktrees and their status
- **Remove** a worktree (with optional branch deletion)

## Operations

### Create Worktree
**Keywords:** create, new, setup, make, add worktree

**Action:** Use `/create_worktree <branch-name>`

**What it does:**
- Creates worktree in `trees/<branch-name>`
- Creates branch if it doesn't exist
- Ensures `trees/` is in .gitignore
- Reports location and next steps

### List Worktrees
**Keywords:** list, show, display, status, which worktrees

**Action:** Use `/list_worktrees`

**What it does:**
- Shows main repository status
- Lists all worktrees in `trees/`
- Displays branch and commit info
- Provides quick command references

### Remove Worktree
**Keywords:** remove, delete, cleanup, destroy worktree

**Action:** Use `/remove_worktree <branch-name>`

**What it does:**
- Removes worktree from `trees/`
- Checks for uncommitted changes
- Optionally deletes the branch
- Safe with confirmation prompts

## Examples

**User:** "Create a worktree for feature-auth"
**Action:** `/create_worktree feature-auth`

**User:** "Show me all my worktrees"
**Action:** `/list_worktrees`

**User:** "Remove the feature-auth worktree"
**Action:** `/remove_worktree feature-auth`

## Important Notes

- All worktrees are created in `trees/` directory (convention enforced)
- After creating a worktree, users can install dependencies and start services as needed
- This skill works in ANY git repository
- No project-specific assumptions are made
