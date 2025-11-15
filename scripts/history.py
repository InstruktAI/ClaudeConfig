#!.venv/bin/python

"""
Parse and display Claude Code conversation history from history.jsonl
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def load_history(file_path: Path) -> list[dict]:
    """Load all entries from history.jsonl."""
    entries = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def format_timestamp(ts: int) -> str:
    """Convert millisecond timestamp to human readable format."""
    dt = datetime.fromtimestamp(ts / 1000)
    return dt.strftime("%b %d, %Y %H:%M")


def extract_project_name(project_path: str) -> str:
    """Extract just the folder name from full path."""
    return Path(project_path).name if project_path else "unknown"


def truncate_display(text: str, max_len: int = 70) -> str:
    """Truncate text to max length."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def search_entry(entry: dict, term: str) -> str | None:
    """
    Search entry for term in display or pasted contents.
    Returns 'topic' or 'content' if found, None otherwise.
    """
    term_lower = term.lower()

    display = entry.get("display", "").lower()
    if term_lower in display:
        return "topic"

    pasted = entry.get("pastedContents", {})
    for content in pasted.values():
        if isinstance(content, str) and term_lower in content.lower():
            return "content"

    return None


def format_table_row(
    num: int, timestamp: str, project: str, topic: str, session_id: str = "", match_type: str = ""
) -> str:
    """Format a single row with proper column widths."""
    num_str = f"{num:>4}"
    ts_str = f"{timestamp:<17}"
    proj_str = f"{project:<30}"
    topic_str = f"{topic:<70}"
    session_str = f"{session_id:<10}" if session_id else " " * 10
    match_str = f" [{match_type}]" if match_type else ""

    return f"{num_str} | {ts_str} | {proj_str} | {topic_str} | {session_str}{match_str}"


def print_header(show_match: bool = False) -> None:
    """Print table header."""
    match_suffix = " | Match" if show_match else ""
    print(f"{'Num':>4} | {'Date/Time':<17} | {'Project':<30} | {'Topic':<70} | {'Session':<10}{match_suffix}")
    print("-" * (4 + 3 + 17 + 3 + 30 + 3 + 70 + 3 + 10 + (9 if show_match else 0)))


def display_history(entries: list[dict], search_term: str = "") -> None:
    """Display conversation history."""
    # Reverse to show most recent first
    entries = list(reversed(entries))

    # Apply search filter if provided
    filtered = []
    if search_term:
        for entry in entries:
            match_type = search_entry(entry, search_term)
            if match_type:
                filtered.append((entry, match_type))
    else:
        filtered = [(entry, "") for entry in entries]

    if not filtered:
        print(f"No conversations found matching '{search_term}'")
        return

    # Show results
    show_match = bool(search_term)

    if search_term:
        print(f"\nSearch results for '{search_term}' ({len(filtered)} found):\n")
    else:
        print("\nRecent Conversations:\n")

    print_header(show_match)

    # First batch (most recent 10 or all search results if < 10)
    first_batch = filtered[:10]
    for i, (entry, match_type) in enumerate(first_batch, 1):
        timestamp = format_timestamp(entry.get("timestamp", 0))
        project = extract_project_name(entry.get("project", ""))
        topic = truncate_display(entry.get("display", ""))
        session_id = entry.get("sessionId", "")

        print(format_table_row(i, timestamp, project, topic, session_id, match_type))

    # Additional batch if more exist and not searching
    if not search_term and len(filtered) > 10:
        remaining = filtered[10:17]
        if remaining:
            print("\nAdditional Recent Conversations:\n")
            print_header()
            for i, (entry, _) in enumerate(remaining, 11):
                timestamp = format_timestamp(entry.get("timestamp", 0))
                project = extract_project_name(entry.get("project", ""))
                topic = truncate_display(entry.get("display", ""))
                session_id = entry.get("sessionId", "")

                print(format_table_row(i, timestamp, project, topic, session_id))

    # Show all search results if > 10
    if search_term and len(filtered) > 10:
        print(f"\n... and {len(filtered) - 10} more results\n")
        print("(showing first 10 matches)")

    # Tips
    print("\n" + "-" * 80)
    print("💡 Tip: Resume any conversation by running:")
    print("- claude --resume <session-id>")
    print("- claude --resume to see an interactive list of recent sessions")


def main() -> None:
    history_file = Path.home() / ".claude" / "history.jsonl"

    if not history_file.exists():
        print(f"History file not found: {history_file}")
        sys.exit(1)

    # Get search term from args if provided
    search_term = sys.argv[1] if len(sys.argv) > 1 else ""

    entries = load_history(history_file)
    display_history(entries, search_term)


if __name__ == "__main__":
    main()
