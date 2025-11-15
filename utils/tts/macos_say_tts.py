#!.venv/bin/python

import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
env_path = Path.home() / ".claude" / ".env"
load_dotenv(env_path)

# Import logging after .env is loaded
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logging_helper import log


def main():
    """macOS Say TTS - native text-to-speech using macOS say command."""
    hook_name = "macos_say_tts"

    try:
        # Get text from command line argument or use default
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])
        else:
            text = "Work complete!"

        # Truncate text for logging if too long
        log_text = text[:80] + "..." if len(text) > 80 else text

        # Get voice from env (optional)
        voice = os.getenv("MACOS_VOICE")

        if voice:
            log.debug(f"Speaking with voice '{voice}': {log_text}", hook_name)
            subprocess.run(["say", "-v", voice, text], check=True)
        else:
            log.debug(f"Speaking with system default voice: {log_text}", hook_name)
            subprocess.run(["say", text], check=True)

        log.debug("TTS playback completed successfully", hook_name)

    except subprocess.CalledProcessError as e:
        log.error("say command failed", hook_name, error=e)
        sys.exit(1)
    except FileNotFoundError as e:
        log.error("say command not found (not on macOS?)", hook_name, error=e)
        sys.exit(1)
    except Exception as e:
        log.error("Unexpected TTS error", hook_name, error=e)
        sys.exit(1)


if __name__ == "__main__":
    main()
