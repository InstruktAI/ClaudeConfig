#!/bin/bash
# Fast cleanup script for Signal AI sessions across Claude, Codex, and Gemini stores.
# Uses exact fixed-string matching and does NOT create backups.
set -euo pipefail

SCRIPT_NAME="$(basename "$0")"

PROJECT_DIR="/Users/morriz/.claude/projects/-Users-morriz-Workspace-InstruktAI-crypto-ai"
CODEX_SESSIONS_DIR="${HOME}/.codex/sessions"
GEMINI_TMP_DIR="${HOME}/.gemini/tmp"

# Exact string to match (fixed-string search)
SEARCH_STRINGS=(
  "system: You are Signal AI"
)

DRY_RUN=false

usage() {
  cat <<USAGE
Usage: ${SCRIPT_NAME} [--dry-run]

Options:
  --dry-run  Show what would be deleted, but do not modify anything
  -h, --help Show this help
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Error: Unknown option '$1'" >&2
      usage
      exit 1
      ;;
  esac
done

echo "Signal AI Session Cleanup"
echo "======================================"
echo ""

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

claude_matches="${tmp_dir}/claude_matches.txt"
codex_matches="${tmp_dir}/codex_matches.txt"
gemini_matches="${tmp_dir}/gemini_matches.txt"
tool_results="${tmp_dir}/tool_results.txt"
all_items="${tmp_dir}/all_items.txt"

> "$claude_matches"
> "$codex_matches"
> "$gemini_matches"
> "$tool_results"
> "$all_items"

find_matches() {
  local root_dir="$1"
  local glob="$2"
  local out_file="$3"

  if [[ ! -d "$root_dir" ]]; then
    return
  fi

  if command -v rg >/dev/null 2>&1; then
    rg -l -F \
      -e "${SEARCH_STRINGS[0]}" \
      "$root_dir" -g "$glob" --no-messages > "$out_file" || true
  else
    grep -rl -F \
      -e "${SEARCH_STRINGS[0]}" \
      "$root_dir" --include "$glob" > "$out_file" || true
  fi
}

extract_session_id() {
  local file="$1"
  local base
  base="$(basename "$file" .jsonl)"
  if [[ "$base" =~ ^[0-9a-fA-F-]{8,}$ ]]; then
    echo "$base"
    return
  fi

  local sid=""
  if command -v rg >/dev/null 2>&1; then
    sid=$(rg -m1 -o --pcre2 '"sessionId":"[^"]+"' "$file" --no-messages \
      | head -n1 \
      | sed -e 's/^"sessionId":"//' -e 's/"$//')
  else
    sid=$(grep -m1 -oE '"sessionId":"[^"]+"' "$file" \
      | head -n1 \
      | sed -e 's/^"sessionId":"//' -e 's/"$//')
  fi

  if [[ -n "$sid" ]]; then
    echo "$sid"
  fi
}

safe_delete() {
  local target="$1"
  if [[ -z "$target" ]]; then
    echo "Error: Refusing to delete empty path" >&2
    exit 1
  fi

  if [[ "$target" != "$PROJECT_DIR"* && "$target" != "$CODEX_SESSIONS_DIR"* && "$target" != "$GEMINI_TMP_DIR"* ]]; then
    echo "Error: Refusing to delete unexpected path: $target" >&2
    exit 1
  fi

  if [[ -d "$target" ]]; then
    rm -rf "$target"
  else
    rm -f "$target"
  fi
}

echo "Searching for Signal AI session files (exact string match)..."
find_matches "$PROJECT_DIR" "*.jsonl" "$claude_matches"
find_matches "$CODEX_SESSIONS_DIR" "*.jsonl" "$codex_matches"
find_matches "$GEMINI_TMP_DIR" "*.json" "$gemini_matches"

# Identify tool-results directories related to matched Claude sessions
if [[ -s "$claude_matches" ]]; then
  while IFS= read -r file; do
    session_id="$(extract_session_id "$file" || true)"
    if [[ -n "$session_id" ]]; then
      tool_dir="${PROJECT_DIR}/${session_id}/tool-results"
      if [[ -d "$tool_dir" ]]; then
        echo "$tool_dir" >> "$tool_results"
      fi
    fi
  done < "$claude_matches"
fi

if [[ -s "$tool_results" ]]; then
  sort -u "$tool_results" -o "$tool_results" || true
fi

cat "$claude_matches" "$codex_matches" "$gemini_matches" "$tool_results" | sort -u > "$all_items"

claude_count="$(wc -l < "$claude_matches" | tr -d ' ')"
codex_count="$(wc -l < "$codex_matches" | tr -d ' ')"
gemini_count="$(wc -l < "$gemini_matches" | tr -d ' ')"
tool_count="$(wc -l < "$tool_results" | tr -d ' ')"
total_count="$(wc -l < "$all_items" | tr -d ' ')"

if [[ "$total_count" -eq 0 ]]; then
  echo "No files found"
  exit 0
fi

echo "Found:"
echo "  - Claude sessions: $claude_count"
echo "  - Codex sessions:  $codex_count"
echo "  - Gemini sessions: $gemini_count"
echo "  - Tool results:    $tool_count"
echo "  - Total items:     $total_count"
echo ""

if [[ "$DRY_RUN" == true ]]; then
  echo "Dry run only. No files deleted."
  exit 0
fi

echo "Deleting..."
delete_count=0
while IFS= read -r item; do
  if [[ -z "$item" ]]; then
    continue
  fi
  safe_delete "$item"
  delete_count=$((delete_count + 1))
done < "$all_items"

echo ""
echo "✓ Deleted $delete_count items"
echo "Done!"
