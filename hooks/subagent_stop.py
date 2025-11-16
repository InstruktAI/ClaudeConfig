#!.venv/bin/python

import json
import os
import random
import sys
import time

from utils.llm_manager import summarize_text
from utils.logging_helper import log
from utils.transcript_parser import get_last_assistant_message
from utils.tts_manager import speak


def get_first_sentence(text: str) -> str:
    """Extract first sentence from text."""
    if not text:
        return ""
    # Split on common sentence terminators
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


def get_random_startup_message() -> str:
    """Return a random friendly startup message."""
    messages = [
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
    return random.choice(messages)


def should_debounce_tts(session_id: str, debounce_seconds: float = 10.0) -> bool:
    """Check if we should skip TTS due to recent activity (debouncing)."""
    timestamp_file = f"/tmp/subagent_tts_last_{session_id}"
    current_time = time.time()

    try:
        if os.path.exists(timestamp_file):
            with open(timestamp_file, "r", encoding="utf-8") as f:
                last_time = float(f.read().strip())
                time_diff = current_time - last_time

                if time_diff < debounce_seconds:
                    log.debug(f"Debouncing TTS - last spoke {time_diff:.1f}s ago", "subagent_stop", session_id)
                    return True

        return False
    except Exception as e:
        log.error(f"Error checking debounce: {e}", "subagent_stop", session_id)
        return False


def update_tts_timestamp(session_id: str) -> None:
    """Update the timestamp file after TTS is queued."""
    timestamp_file = f"/tmp/subagent_tts_last_{session_id}"
    try:
        with open(timestamp_file, "w", encoding="utf-8") as f:
            f.write(str(time.time()))
    except Exception as e:
        log.error(f"Error updating timestamp: {e}", "subagent_stop", session_id)


def main() -> None:
    try:
        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id")
        agent_transcript_path = input_data.get("agent_transcript_path")

        log.info("Subagent stop hook triggered", "subagent_stop", session_id)
        log.debug(f"Project: {input_data.get('cwd')}", "subagent_stop", session_id)
        log.debug(f"Full payload: {json.dumps(input_data, indent=2)}", "subagent_stop", session_id)
        log.debug(f"Agent ID: {input_data.get('agent_id')}", "subagent_stop", session_id)

        # Check debounce - skip if we spoke too recently
        if should_debounce_tts(session_id):
            log.info("Skipping TTS due to debounce", "subagent_stop", session_id)
            sys.exit(0)

        # Check if this is an initial/startup subagent
        if is_initial_subagent(agent_transcript_path):
            message = get_random_startup_message()
            log.debug(f"TTS: '{message}' (project: {input_data.get('cwd')})", "subagent_stop", session_id)
            speak(message, "subagent_stop", session_id)
            update_tts_timestamp(session_id)
        else:
            raw_message = (
                get_last_assistant_message(agent_transcript_path, last_only=True) if agent_transcript_path else None
            )

            if not raw_message:
                log.debug(f"TTS: 'Subagent Complete' (project: {input_data.get('cwd')})", "subagent_stop", session_id)
                speak("Subagent Complete", "subagent_stop", session_id)
            else:
                # Try to summarize using LLM if available
                summary = summarize_text(raw_message, "subagent_stop", max_words=15)
                if summary:
                    log.debug(f"TTS: '{summary}' (project: {input_data.get('cwd')})", "subagent_stop", session_id)
                    speak(summary, "subagent_stop", session_id)
                else:
                    # Fall back to first sentence
                    first_sentence = get_first_sentence(raw_message)
                    message = first_sentence or "Subagent Complete"
                    log.debug(f"TTS: '{message}' (project: {input_data.get('cwd')})", "subagent_stop", session_id)
                    speak(message, "subagent_stop", session_id)
            update_tts_timestamp(session_id)

        log.info("Subagent stop hook completed", "subagent_stop", session_id)
        sys.exit(0)

    except json.JSONDecodeError as e:
        log.error("JSON decode error", "subagent_stop", error=e)
        sys.exit(0)
    except Exception as e:
        log.error("Unexpected error", "subagent_stop", error=e)
        sys.exit(0)


if __name__ == "__main__":

    main()
