#!/usr/bin/env python3

import os
import random
import sys

import pyttsx3
from dotenv import load_dotenv

# Load .env from project root
env_path = os.path.expanduser("~/.claude/.env")
load_dotenv(env_path)

# Import logging after .env is loaded
sys.path.insert(0, os.path.expanduser("~/.claude"))
from utils.logging_helper import log


def main():
    """pyttsx3 TTS - offline text-to-speech synthesis."""
    hook_name = "pyttsx3_tts"

    try:
        # Initialize TTS engine
        engine = pyttsx3.init()

        # Configure engine settings
        engine.setProperty("rate", 180)  # Speech rate (words per minute)
        engine.setProperty("volume", 0.8)  # Volume (0.0 to 1.0)

        # Get text from command line argument or use default
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])
        else:
            # Default completion messages
            completion_messages = [
                "Work complete!",
                "All done!",
                "Task finished!",
                "Job complete!",
                "Ready for next task!",
            ]
            text = random.choice(completion_messages)

        # Truncate text for logging if too long
        log_text = text[:80] + "..." if len(text) > 80 else text

        log.debug(f"Speaking offline (rate=180, volume=0.8): {log_text}", hook_name)

        # Speak the text
        engine.say(text)
        engine.runAndWait()

        log.debug("TTS playback completed successfully", hook_name)

    except Exception as e:
        log.error("pyttsx3 TTS failed", hook_name, error=e)
        sys.exit(1)


if __name__ == "__main__":
    main()
