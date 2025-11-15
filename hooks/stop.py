#!.venv/bin/python

import argparse
import json
import sys

from utils.llm_manager import generate_completion_message, summarize_text
from utils.logging_helper import log
from utils.transcript_parser import get_last_assistant_message
from utils.tts_manager import speak


def main() -> None:
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--notify", action="store_true")
        parser.add_argument("--summarize", action="store_true")
        args = parser.parse_args()

        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id")
        transcript_path = input_data.get("transcript_path")

        log.info("Stop hook triggered", "stop", session_id)

        if args.notify:
            summary = None
            if args.summarize and transcript_path:
                last_message = get_last_assistant_message(transcript_path)
                if last_message:
                    summary = summarize_text(last_message, "stop")

            completion_message = generate_completion_message("stop")

            if summary:
                speak(summary, "stop", session_id)

            speak(completion_message, "stop", session_id)

        log.info("Stop hook completed", "stop", session_id)
        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
