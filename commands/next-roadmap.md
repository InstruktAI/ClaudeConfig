---
argument-hint: '[subject]'
description: Roadmap grooming for todos/roadmap.md — add/refine/prioritize items before
  requirements exist; not for clarifying drafted requirements
---

You are in **roadmap discovery mode**. Output is a concise agreement summary plus next command.

## Step 1: Determine focus
- If an argument is provided, treat it as the subject candidate and derive slug (kebab-case, <=50 chars).
- If no argument, read `todos/roadmap.md`: use in-progress (`- [>]`) item; if none, first unchecked (`- [ ]`). Use its text as subject and slug.

If the chosen item doesn’t exist yet, you may add it to `todos/roadmap.md` after confirming with the user.

## Step 2: Quick context check
- Confirm priority/urgency and which user persona or environment (master vs non-master) it targets.
- Confirm whether this is a net-new item or a refinement of an existing roadmap entry.

## Step 3: Guided questions (ask, don’t assume)
Ask concise, focused questions to capture at least:
- Problem & why now
- Primary goals (must), secondary goals (nice-to-have)
- Non-goals / out-of-scope
- Users/personas and success outcomes
- Constraints (tech, UX, data, compliance, performance, rollout limits)
- Dependencies/risks and timeline/priority notes
- Any acceptance signals or metrics the user expects

Keep iterating until the user indicates “enough” or all fields are reasonably filled.

## Step 4: When to stop
- If answers are sufficient: summarize agreed details, update `todos/roadmap.md` with the refined/added item (keeping existing format/status markers), propose slug, and instruct: `Run /next-requirements {subject-slug}`.
- If the user declines or gaps remain: summarize what’s missing and stop; do **not** fabricate details.

## Step 5: Output format
- Brief recap bullet list (subject, slug, goals, non-goals, key constraints, blockers, open questions).
- Next step line: `Next: /next-requirements {subject-slug}` (only if ready), else “Need answers on: …”.

Guardrails:
- No files are written in this command.
- Do not invent requirements; only capture what the user confirms.
- Keep it short and decision-focused.
