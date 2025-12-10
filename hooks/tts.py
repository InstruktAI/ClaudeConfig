#!/usr/bin/env python3
"""
Unified TTS hook for all Claude Code events.
Usage: tts.py --event-type <EventType>
"""

import argparse
import json
import os
import random
import sys
import time

from utils.llm_manager import generate_completion_message, summarize_text
from utils.logging_helper import log
from utils.transcript_parser import count_messages, get_last_assistant_message
from utils.tts_manager import speak

# Message templates
NOTIFICATION_MESSAGES = [
    "I need your input",
    "Your attention is needed",
    "I am waiting for your input",
    "Ready for your next instruction",
    "Standing by for input",
]

STARTUP_MESSAGES = [
    "Standing by with grep patterns locked and loaded. What can I find?",
    "Warmed up and ready to hunt down that bug!",
    "Cache cleared, mind fresh. What's the task?",
    "All systems nominal, ready to ship some code!",
    "Initialized and ready to make those tests pass. What needs fixing?",
    "Compiled with optimism and ready to refactor!",
    "Ready to turn coffee into code. Where do we start?",
    "Standing by like a well-indexed database!",
    "Alert and ready to parse whatever you need. What's up?",
    "Primed to help you ship that feature!",
    "Spun up and ready to debug. What's broken?",
    "Loaded and eager to make things work!",
    "Ready to dig into the details. What should I investigate?",
    "All systems go for some serious coding!",
    "Prepared to tackle whatever you throw at me. What's the challenge?",
    "Standing by to help ship something awesome!",
    "Ready to make the build green. What needs attention?",
    "Warmed up and waiting to assist!",
    "Initialized and ready to solve problems. What's the issue?",
    "All set to help you build something great!",
]

SESSION_START_MESSAGES = {
    "startup": "Claude Code session started",
    "resume": "Resuming previous session",
    "clear": "Starting fresh session",
}

SESSION_END_MESSAGES = {
    "clear": "Session cleared",
    "logout": "Logging out",
    "prompt_input_exit": "Session ended",
    "other": "Session ended",
}


def should_skip_event(event_type: str) -> bool:
    """Check if TTS should be skipped for this event type."""
    skip_events = os.getenv("TTS_SKIP_HOOK_EVENTS", "").split(",")
    skip_events = [e.strip() for e in skip_events if e.strip()]
    return event_type in skip_events


def get_first_sentence(text: str) -> str:
    """Extract first sentence from text."""
    if not text:
        return ""
    for terminator in [". ", "! ", "? ", "\n"]:
        if terminator in text:
            return text.split(terminator)[0] + terminator.strip()
    return text


def is_initial_subagent(agent_transcript_path: str) -> bool:
    """Check if this is an initial/startup subagent with no user interaction."""
    if not agent_transcript_path or not os.path.exists(agent_transcript_path):
        return True
    try:
        with open(agent_transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                if entry.get("type") == "user":
                    return False
        return True
    except Exception:
        return True


def should_debounce_tts(session_id: str, debounce_seconds: float = 10.0) -> bool:
    """Check if we should skip TTS due to recent activity."""
    timestamp_file = f"/tmp/subagent_tts_last_{session_id}"
    current_time = time.time()
    try:
        if os.path.exists(timestamp_file):
            with open(timestamp_file, "r", encoding="utf-8") as f:
                last_time = float(f.read().strip())
                time_diff = current_time - last_time
                if time_diff < debounce_seconds:
                    log.debug(f"Debouncing TTS - last spoke {time_diff:.1f}s ago", "tts", session_id)
                    return True
        return False
    except Exception as e:
        log.error(f"Error checking debounce: {e}", "tts", session_id)
        return False


def update_tts_timestamp(session_id: str) -> None:
    """Update the timestamp file after TTS is queued."""
    timestamp_file = f"/tmp/subagent_tts_last_{session_id}"
    try:
        with open(timestamp_file, "w", encoding="utf-8") as f:
            f.write(str(time.time()))
    except Exception as e:
        log.error(f"Error updating timestamp: {e}", "tts", session_id)


def handle_notification(input_data: dict, session_id: str) -> None:
    """Handle Notification event."""
    if input_data.get("message") == "Claude is waiting for your input":
        return

    engineer_name = os.getenv("ENGINEER_NAME", "").strip()
    base_message = random.choice(NOTIFICATION_MESSAGES)

    if engineer_name and random.random() < 0.5:
        message = f"{engineer_name}, {base_message.lower()}"
    else:
        message = base_message

    log.debug(f"Speaking notification: {message}", "tts", session_id)
    speak(message, "tts", session_id)


def handle_session_start(input_data: dict, session_id: str) -> None:
    """Handle SessionStart event."""
    if should_skip_event("SessionStart"):
        log.debug("TTS skipped (SessionStart in TTS_SKIP_HOOK_EVENTS)", "tts", session_id)
        return

    source = input_data.get("source", "startup")
    message = SESSION_START_MESSAGES.get(source, "Session started")
    speak(message, "tts", session_id)


def handle_session_end(input_data: dict, session_id: str) -> None:
    """Handle SessionEnd event."""
    transcript_path = input_data.get("transcript_path")
    if transcript_path:
        message_count = count_messages(transcript_path)
        reason = input_data.get("reason")
        log.info(f"Session statistics: {message_count} messages, reason: {reason}", "tts", session_id)

    if should_skip_event("SessionEnd"):
        log.debug("TTS skipped (SessionEnd in TTS_SKIP_HOOK_EVENTS)", "tts", session_id)
        return

    reason = input_data.get("reason", "other")
    message = SESSION_END_MESSAGES.get(reason, "Session ended")
    speak(message, "tts", session_id)


def handle_stop(input_data: dict, session_id: str) -> None:
    """Handle Stop event."""
    transcript_path = input_data.get("transcript_path")

    summary = None
    if transcript_path:
        last_message = get_last_assistant_message(transcript_path)
        log.debug(f"Last assistant message length: {len(last_message) if last_message else 0}", "tts", session_id)
        if last_message:
            summary = summarize_text(last_message, "tts")
            log.debug(f"Summary generated: {summary}", "tts", session_id)

    completion_message = generate_completion_message("tts")

    if summary:
        speak(summary, "tts", session_id)

    speak(completion_message, "tts", session_id)


def handle_subagent_stop(input_data: dict, session_id: str) -> None:
    """Handle SubagentStop event."""
    agent_transcript_path = input_data.get("agent_transcript_path")

    log.debug(f"Project: {input_data.get('cwd')}", "tts", session_id)
    log.debug(f"Agent ID: {input_data.get('agent_id')}", "tts", session_id)

    if should_debounce_tts(session_id):
        log.info("Skipping TTS due to debounce", "tts", session_id)
        return

    if is_initial_subagent(agent_transcript_path):
        message = random.choice(STARTUP_MESSAGES)
        log.debug(f"TTS: '{message}'", "tts", session_id)
        speak(message, "tts", session_id)
        update_tts_timestamp(session_id)
        return

    raw_message = get_last_assistant_message(agent_transcript_path, last_only=True) if agent_transcript_path else None

    if not raw_message:
        log.debug("TTS: 'Subagent Complete'", "tts", session_id)
        speak("Subagent Complete", "tts", session_id)
    else:
        summary = summarize_text(raw_message, "tts", max_words=15)
        if summary:
            log.debug(f"TTS: '{summary}'", "tts", session_id)
            speak(summary, "tts", session_id)
        else:
            first_sentence = get_first_sentence(raw_message)
            message = first_sentence or "Subagent Complete"
            log.debug(f"TTS: '{message}'", "tts", session_id)
            speak(message, "tts", session_id)

    update_tts_timestamp(session_id)


EVENT_HANDLERS = {
    "Notification": handle_notification,
    "SessionStart": handle_session_start,
    "SessionEnd": handle_session_end,
    "Stop": handle_stop,
    "SubagentStop": handle_subagent_stop,
}


def main() -> None:
    try:
        parser = argparse.ArgumentParser(description="Unified TTS hook")
        parser.add_argument("--event-type", required=True, choices=EVENT_HANDLERS.keys())
        args = parser.parse_args()

        # Early exit if TTS is disabled
        if os.getenv("TTS_ENABLED", "false").lower() != "true":
            sys.exit(0)

        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id")

        log.info(f"TTS hook triggered ({args.event_type})", "tts", session_id)

        handler = EVENT_HANDLERS.get(args.event_type)
        if handler:
            handler(input_data, session_id)

        log.info(f"TTS hook completed ({args.event_type})", "tts", session_id)
        sys.exit(0)

    except json.JSONDecodeError as e:
        log.error("JSON decode error", "tts", error=e)
        sys.exit(0)
    except Exception as e:
        log.error(f"Unexpected error: {e}", "tts", error=e)
        sys.exit(0)


if __name__ == "__main__":
    main()
