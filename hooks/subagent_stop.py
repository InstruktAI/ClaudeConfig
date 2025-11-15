#!.venv/bin/python

import json
import sys

from utils.logging_helper import log
from utils.tts_manager import speak


def main() -> None:
    try:
        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id")

        log.info("Subagent stop hook triggered", "subagent_stop", session_id)

        speak("Subagent Complete", "subagent_stop", session_id)

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
