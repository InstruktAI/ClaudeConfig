---
argument-hint: '[scope]'
description: Inspect the codebase and update docs/ so it accurately reflects what
  the code does. Use when docs might be stale or missing details.
---

# Sync Docs

Keep documentation truthful to the codebase.

## Scope

ARGUMENT: "$ARGUMENTS"

- ARGUMENT: optional focus area (path, feature, or component). If omitted, cover the whole repo.
- Always operate from project root to keep paths correct.

## Process

### Phase 1: Inventory (run in parallel)

- **Code mapper** (`subagent_type=Explore`): crawl source directories (src/, app/, packages/, services/, bin/, scripts/). Capture modules, entrypoints, commands, APIs, jobs, and key config flags. Return JSON with `items` [{name, path, role, dependencies, notes}].
- **Docs mapper** (`subagent_type=Explore`): read `docs/**/*.md` (and README files) to extract documented components, claims, and assumptions. Return JSON with `items` [{name, path, claims, last_known_role}].

### Phase 2: Drift Detection

- Compare code vs docs inventories to find:
  - Implemented components missing from docs.
  - Docs describing code that no longer exists or changed behavior.
  - Config/flags/CLI commands without docs.
  - Tests covering behavior not documented.
- Decide target doc file per item (reuse existing file when possible).

### Phase 3: Update Docs

- Edit docs in place (no new abstractions). Keep sections concise, factual, path-anchored (`module: src/foo/bar.py`).
- For new components: add purpose, inputs/outputs, dependencies, invariants, and primary interactions.
- For changed components: rewrite statements to match current behavior; remove stale claims.
- When behavior is unclear, add a short **Open questions** list instead of guessing.

### Phase 4: Validate

- Re-read updated docs to ensure every claim is backed by code or tests you inspected.
- Ensure links/paths resolve and filenames are correct.
- Keep terminology consistent with code (function names, flags, env vars).

### Phase 5: Report

- Summarize edits with touched files and the drift resolved.
- If ambiguities remain, list them with the file/path to investigate next.

## Notes

- Do not push; offer a commit only if changes are complete.
- Keep writing style aligned with existing docs; no new format unless needed for clarity.
