#!/usr/bin/env python3
# TeleClaude bridge hook - forwards Claude Code events to TeleClaude daemon
#
# This is the ONLY place that communicates with TeleClaude.
# All Claude Code events flow through here via teleclaude__handle_claude_event.
#
# NOTE: This hook only processes events for TeleClaude sessions (TELECLAUDE_SESSION_ID set).
# For local terminal sessions, events are ignored.
#
# GLOBAL CONFIG: This hook gracefully no-ops when TeleClaude is not installed.
import json
import os
import random
import sys
import traceback
from datetime import datetime
from pathlib import Path

from utils.file_log import append_line
from utils.mcp_send import mcp_send
from utils.transcript_summarizer import summarize_transcript

LOG_DIR = Path.home() / ".claude" / "logs"
LOG_FILE = LOG_DIR / "teleclaude_bridge.log"
# State file tracks last processed transcript mtime per session to dedupe Stop events
STATE_FILE = LOG_DIR / "bridge_state.json"

NOTIFICATION_MESSAGES = [
    "Your agent needs your input",
    "Ready for your next instruction",
    "Waiting for guidance",
    "Standing by for input",
    "Input needed to proceed",
]


def log(message: str) -> None:
    """Write log message to file."""
    try:
        append_line(LOG_FILE, f"[{datetime.now().isoformat()}] {message}")
    except Exception:  # noqa: S110
        pass


def load_state() -> dict:
    """Load bridge state from file."""
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
    except Exception:
        pass
    return {}


def save_state(state: dict) -> None:
    """Save bridge state to file."""
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state))
    except Exception:
        pass


# def should_skip_summary(transcript_path: str) -> bool:
#     """Check if this Stop event should be skipped (transcript unchanged since last summary).

#     Claude Code fires multiple Stop events even when Claude hasn't done any new work.
#     This causes duplicate "Work complete!" messages to pile up in Telegram.

#     We track the transcript file's mtime and skip if unchanged since last summary.
#     Key is the transcript path itself (not TeleClaude session ID) because:
#     - Same Claude Code session = same transcript file
#     - TeleClaude session IDs change on restart but transcript stays the same
#     """
#     if not transcript_path:
#         return False

#     try:
#         transcript = Path(transcript_path)
#         if not transcript.exists():
#             return False

#         current_mtime = transcript.stat().st_mtime

#         state = load_state()
#         # Use transcript path as key - this is what actually tracks if work changed
#         last_mtime = state.get(transcript_path, {}).get("last_summary_mtime")

#         if last_mtime is not None and current_mtime == last_mtime:
#             log(f"Skipping duplicate summary - transcript unchanged (mtime={current_mtime})")
#             return True

#         # Update state with current mtime
#         state[transcript_path] = {"last_summary_mtime": current_mtime}
#         save_state(state)

#         return False

#     except Exception as e:
#         log(f"Error checking transcript mtime: {e}")
#         return False


def send_event(teleclaude_session_id: str, event_type: str, data: dict) -> None:
    """Send event to TeleClaude daemon via MCP."""
    mcp_send(
        "teleclaude__handle_claude_event",
        {"session_id": teleclaude_session_id, "event_type": event_type, "data": data},
    )
    log(f"Sent {event_type} event to daemon")


def handle_notification(teleclaude_session_id: str, message: str | None, notification_type: str | None) -> None:
    """Handle notification event - forward to daemon for listener notification and Telegram feedback.

    For AskUserQuestion and other input-required notifications, the original message contains
    the actual question content. This is forwarded to registered listeners (calling AIs) so they
    can respond to what the remote session is asking.

    Skip for 'Claude is waiting for your input' (60s idle prompt) - we already sent a summary.
    """
    if message == "Claude is waiting for your input":
        log("Skipping notification for 'Claude is waiting for your input'")
        return

    # For user-facing feedback in Telegram, use a friendly message
    # The original message goes in original_message for listener forwarding
    engineer_name = os.getenv("ENGINEER_NAME", "").strip()
    prefix = f"{engineer_name}, " if engineer_name and random.random() < 0.3 else ""
    random_message = random.choice(NOTIFICATION_MESSAGES)
    friendly_message = prefix + (random_message[0].lower() + random_message[1:]) if prefix else random_message

    log(f"Notification type: {notification_type}, original message: {message}")
    log(f"Friendly message for Telegram: {friendly_message}")

    # Send event with both messages:
    # - message: friendly message for Telegram feedback
    # - original_message: actual question/notification for listener forwarding
    send_event(
        teleclaude_session_id,
        "notification",
        {
            "message": friendly_message,
            "original_message": message,
            "notification_type": notification_type,
        },
    )


def run_summarizer(transcript_path: str) -> dict:
    """Run summarizer and return result.

    Returns:
        Dict with "summary" and "title" keys, or "error" key on failure.
    """
    log(f"Running summarizer for: {transcript_path}")
    try:
        result = summarize_transcript(transcript_path)
        log(f"Summarizer output: {result}")
        return result
    except Exception as e:
        log(f"Summarizer error: {e}")
        return {"error": str(e)}


def handle_stop(teleclaude_session_id: str, transcript_path: str, original_data: dict) -> None:
    """Handle stop event - run summarizer and send single enriched stop event.

    Deduplicates Stop events by tracking transcript file mtime.
    Claude Code fires multiple Stop events even when no new work was done,
    which would cause duplicate "Work complete!" messages in Telegram.

    The stop event includes both title and summary from summarizer so that:
    - Listener notifications include the title (for AI-to-AI workflows)
    - Telegram notifications include the summary
    - Title updates work as expected

    We send ONE stop event with all data, not separate stop + summary events.
    """
    # Run summarizer first (if applicable) - check mtime to deduplicate
    if transcript_path:  # and not should_skip_summary(transcript_path):
        summary_result = run_summarizer(transcript_path)
        if "error" in summary_result:
            log(f"Summarizer failed: {summary_result['error']}")
            summary_result = {"summary": "Work complete!", "title": None}
    else:
        # Skipped (duplicate) or no transcript - send minimal stop event
        summary_result = {}

    # Build enriched stop event with all data
    stop_data = dict(original_data)
    if summary_result.get("title"):
        stop_data["title"] = summary_result["title"]
    if summary_result.get("summary"):
        stop_data["summary"] = summary_result["summary"]

    # Send single enriched stop event (daemon handles everything from this one event)
    send_event(teleclaude_session_id, "stop", stop_data)


def main() -> None:
    """Forward Claude Code events to TeleClaude daemon via MCP.

    Only processes events for TeleClaude sessions (TELECLAUDE_SESSION_ID set).
    Events from local terminal sessions are ignored.
    """
    try:
        log("=== Hook triggered ===")

        # Read input
        data = json.load(sys.stdin)
        log(f"Received data: {json.dumps(data)}")

        # Get TeleClaude session ID from environment (set by tmux)
        teleclaude_session_id = os.getenv("TELECLAUDE_SESSION_ID")

        if not teleclaude_session_id:
            # Local terminal session - ignore events
            log("No TELECLAUDE_SESSION_ID, ignoring event (local terminal session)")
            log("=== Hook finished (local) ===\n")
            sys.exit(0)

        # Extract event type from hook data
        # Claude Code uses "hook_event_name" for the event type field
        event_type = data.get("hook_event_name", "unknown")

        # Normalize event type to match TeleClaude conventions
        # Claude Code: "SessionStart" -> TeleClaude: "session_start"
        if event_type:
            event_type = event_type.lower()
            if event_type == "sessionstart":
                event_type = "session_start"

        log(f"Event type: {event_type}, TeleClaude session: {teleclaude_session_id[:8]}")

        # Route to appropriate handler
        if event_type == "notification":
            handle_notification(
                teleclaude_session_id,
                data.get("message", None),
                data.get("notification_type", None),
            )
        elif event_type == "stop":
            transcript_path = data.get("transcript_path", "")
            handle_stop(teleclaude_session_id, transcript_path, data)
        else:
            # Forward other events directly
            send_event(teleclaude_session_id, event_type, data)

    except Exception as e:
        log(f"ERROR: {str(e)}")
        log(f"Traceback: {traceback.format_exc()}")

    log("=== Hook finished ===\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
