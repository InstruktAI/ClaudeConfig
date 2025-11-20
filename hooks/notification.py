#!/Users/Morriz/.claude/.venv/bin/python

import json
import os
import random
import sys

from utils.logging_helper import log
from utils.tts_manager import speak

# Random notification messages
NOTIFICATION_MESSAGES = [
    "I need your input",
    "Your attention is needed",
    "I am waiting for your input",
    "Ready for your next instruction",
    "Standing by for input",
]


def main() -> None:
    try:
        input_data = json.loads(sys.stdin.read())
        session_id = input_data.get("session_id")

        log.info("Notification hook triggered", "notification", session_id)

        # Skip TTS for the generic "Claude is waiting for your input" message
        if input_data.get("message") != "Claude is waiting for your input":
            # Get engineer name if available
            engineer_name = os.getenv("ENGINEER_NAME", "").strip()

            # Select a random notification message
            base_message = random.choice(NOTIFICATION_MESSAGES)

            # Create notification message with 30% chance to include name
            if engineer_name and random.random() < 0.5:
                notification_message = f"{engineer_name}, {base_message.lower()}"
            else:
                notification_message = base_message

            log.debug(f"Speaking notification: {notification_message}", "notification", session_id)
            speak(notification_message, "notification", session_id)

        log.info("Notification hook completed", "notification", session_id)
        sys.exit(0)

    except json.JSONDecodeError as e:
        log.error("JSON decode error", "notification", error=e)
        sys.exit(0)
    except Exception as e:
        log.error("Unexpected error", "notification", error=e)
        sys.exit(0)


if __name__ == "__main__":
    main()
