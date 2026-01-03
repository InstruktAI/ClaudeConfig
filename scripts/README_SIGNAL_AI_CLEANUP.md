# Signal AI Session Cleanup Documentation

## Investigation Summary

### What Was Found

- **Location**: `~/.claude/projects/-Users-morriz-Workspace-InstruktAI-crypto-ai/`
- **Files Found**: 7,909 session files (.jsonl)
- **Total Size**: 122 MB
- **Pattern**: All files contain "system: You are Signal AI"

### What These Files Are

These are Claude Code conversation history files from the crypto-ai project. Each `.jsonl` file represents a single AI session where the AI was configured with the "Signal AI" system prompt. The files contain:

- User messages
- Assistant responses
- Tool calls and results
- Session metadata (working directory, git branch, timestamps)

### Why It's Safe to Delete

1. **Session files are standalone**: Each `.jsonl` file is an independent session log
2. **History references are harmless**: The `~/.claude/history.jsonl` file contains 643 references to the crypto-ai project, but these are just historical records - they don't break if the session files are deleted
3. **No active sessions**: These appear to be completed/closed sessions
4. **Backup is created**: The cleanup script creates a backup before deletion

### Index/Reference Analysis

- **history.jsonl**: Contains chronological references but doesn't depend on session files existing
- **No database**: Claude Code doesn't use a database to index session files
- **Projects directory**: Organized by project path, session files are self-contained

## Using the Cleanup Script

### Dry Run (Recommended First Step)

```bash
~/.claude/scripts/cleanup_signal_ai_sessions.sh --dry-run
```

This shows what would be deleted without actually deleting anything.

### Actual Cleanup

```bash
~/.claude/scripts/cleanup_signal_ai_sessions.sh
```

This will:
1. Find all files containing "system: You are Signal AI"
2. Create a timestamped backup in `/tmp/`
3. Delete the files
4. Report freed disk space

### Custom Backup Location

```bash
~/.claude/scripts/cleanup_signal_ai_sessions.sh --backup-dir ~/backups/signal-ai-sessions
```

## What Happens After Deletion

### What Changes
- Session files removed from `projects/-Users-morriz-Workspace-InstruktAI-crypto-ai/`
- Disk space freed (122 MB)
- Backup created in specified location

### What Stays the Same
- `history.jsonl` still contains references (this is normal and harmless)
- Other project session files remain untouched
- Claude Code configuration unchanged
- No impact on current or future sessions

## Restoration (If Needed)

If you need to restore the deleted files:

```bash
# The backup location is shown in the cleanup script output
# Example:
cp /tmp/signal_ai_backup_20260101_123456/* ~/.claude/projects/-Users-morriz-Workspace-InstruktAI-crypto-ai/
```

## How This System Works

### Claude Code Session Management

```
~/.claude/
├── projects/
│   └── -Users-morriz-Workspace-InstruktAI-crypto-ai/
│       ├── <uuid>.jsonl           # Individual session files
│       ├── agent-<hash>.jsonl     # Agent subproject sessions
│       └── ...
├── history.jsonl                  # Global chronological history
└── settings.json                  # Configuration
```

### Session File Lifecycle

1. **Creation**: When you start a Claude Code session in a project
2. **Updates**: Each turn (user message + AI response) appends to the file
3. **Completion**: File remains after session ends
4. **Retention**: Files persist indefinitely unless manually cleaned up

### Why Files Accumulate

- Each crypto trading evaluation created a new session
- 7,909 sessions = likely automated/high-frequency usage
- Claude Code doesn't auto-delete old sessions
- Useful for auditing/debugging but can consume disk space

## Reusable Script Pattern

This script pattern can be adapted for other cleanup needs:

```bash
# Example: Clean up all sessions from a specific project
find ~/.claude/projects/-Users-morriz-Workspace-<project-name>/ \
  -type f -name "*.jsonl" \
  -exec grep -l "<pattern>" {} \; | \
  xargs -I {} cp {} /backup/dir/
```

## Safety Features

1. **Backup before delete**: Always creates a backup first
2. **Dry-run mode**: Preview changes without executing
3. **Verification**: Counts files before and after
4. **Error handling**: Stops if backup fails
5. **Non-destructive to config**: Only removes session files

## When to Run This

- When disk space is low
- After completing a project phase
- Before archiving/backing up your system
- When you want to clean up old session logs

## Best Practices

1. **Always run dry-run first**: `--dry-run` to preview
2. **Verify backup**: Check backup directory after cleanup
3. **Keep backup temporarily**: Don't delete backup immediately
4. **Document what you cleaned**: Note what was removed and when

## Questions?

- Session files can be safely deleted without breaking Claude Code
- history.jsonl references are historical records only
- Backup is created automatically for safety
- No impact on future sessions or Claude Code functionality
