#!.venv/bin/python

import json
import os
import sys

from dotenv import load_dotenv

from utils.logging_helper import log
from utils.transcript_parser import count_messages
from utils.tts_manager import speak

load_dotenv()


def main() -> None:
    try:
        input_data = json.loads(sys.stdin.read())
        session_id = input_data.get("session_id")
        reason = input_data.get("reason")
        transcript_path = input_data.get("transcript_path")

        log.info(f"Session end hook triggered (reason: {reason})", "session_end", session_id)

        if transcript_path:
            message_count = count_messages(transcript_path)
            log.info(f"Session statistics: {message_count} messages, reason: {reason}", "session_end", session_id)

        # Check if TTS should be skipped for this event
        skip_events = os.getenv("TTS_SKIP_HOOK_EVENTS", "").split(",")
        skip_events = [e.strip() for e in skip_events if e.strip()]

        if "SessionEnd" not in skip_events:
            messages = {
                "clear": "Session cleared",
                "logout": "Logging out",
                "prompt_input_exit": "Session ended",
                "other": "Session ended",
            }
            message = messages.get(reason, "Session ended")
            speak(message, "session_end", session_id)
        else:
            log.debug("TTS skipped (SessionEnd in TTS_SKIP_HOOK_EVENTS)", "session_end", session_id)

        log.info("Session end hook completed", "session_end", session_id)
        sys.exit(0)

    except json.JSONDecodeError as e:
        log.error("JSON decode error", "session_end", error=e)
        sys.exit(0)
    except Exception as e:
        log.error("Unexpected error", "session_end", error=e)
        sys.exit(0)


if __name__ == "__main__":

    main()
