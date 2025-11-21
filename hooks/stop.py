#!/Users/Morriz/.claude/.venv/bin/python

import json
import sys

from utils.llm_manager import generate_completion_message, summarize_text
from utils.logging_helper import log
from utils.transcript_parser import get_last_assistant_message
from utils.tts_manager import speak


def main() -> None:
    try:
        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id")
        transcript_path = input_data.get("transcript_path")

        log.info("Stop hook triggered", "stop", session_id)

        summary = None
        if transcript_path:
            last_message = get_last_assistant_message(transcript_path)
            log.debug(f"Last assistant message length: {len(last_message) if last_message else 0}", "stop", session_id)
            if last_message:
                summary = summarize_text(last_message, "stop")
                log.debug(f"Summary generated: {summary}", "stop", session_id)
            else:
                log.debug("No assistant message found in transcript", "stop", session_id)
        else:
            log.debug("No transcript path provided", "stop", session_id)

        completion_message = generate_completion_message("stop")

        if summary:
            speak(summary, "stop", session_id)
        else:
            log.debug("No summary to speak", "stop", session_id)

        speak(completion_message, "stop", session_id)

        log.info("Stop hook completed", "stop", session_id)
        sys.exit(0)

    except Exception as e:
        log.error(f"Stop hook failed: {e}", "stop", session_id, error=e)
        sys.exit(0)


if __name__ == "__main__":
    main()
