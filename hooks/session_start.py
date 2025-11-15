#!.venv/bin/python

import json
import os
import sys

from dotenv import load_dotenv

from utils.logging_helper import log
from utils.tts_manager import speak

load_dotenv()


def main() -> None:
    try:
        input_data = json.loads(sys.stdin.read())
        session_id = input_data.get("session_id")
        source = input_data.get("source")

        log.info(f"Session start hook triggered (source: {source})", "session_start", session_id)

        # Check if TTS should be skipped for this event
        skip_events = os.getenv("TTS_SKIP_HOOK_EVENTS", "").split(",")
        skip_events = [e.strip() for e in skip_events if e.strip()]

        if "SessionStart" not in skip_events:
            messages = {
                "startup": "Claude Code session started",
                "resume": "Resuming previous session",
                "clear": "Starting fresh session",
            }
            message = messages.get(source, "Session started")
            speak(message, "session_start", session_id)
        else:
            log.debug("TTS skipped (SessionStart in TTS_SKIP_HOOK_EVENTS)", "session_start", session_id)

        log.info("Session start hook completed", "session_start", session_id)
        sys.exit(0)

    except json.JSONDecodeError as e:
        log.error("JSON decode error", "session_start", error=e)
        sys.exit(0)
    except Exception as e:
        log.error("Unexpected error", "session_start", error=e)
        sys.exit(0)


if __name__ == "__main__":

    main()
