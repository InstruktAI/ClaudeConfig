#!.venv/bin/python

import os
import subprocess
import sys
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load .env from project root
env_path = Path.home() / ".claude" / ".env"
load_dotenv(env_path)

# Import logging after .env is loaded
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logging_helper import log


def main():
    """OpenAI TTS - file-based text-to-speech using OpenAI API."""
    hook_name = "openai_tts"

    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        log.error("OPENAI_API_KEY not found in environment", hook_name)
        sys.exit(1)

    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        # Get text from command line argument or use default
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])
        else:
            text = "Work complete!"

        # Truncate text for logging if too long
        log_text = text[:80] + "..." if len(text) > 80 else text

        # Get voice from env or use default
        voice = os.getenv("OPENAI_VOICE", "nova")

        log.debug(f"Generating with voice '{voice}': {log_text}", hook_name)

        # Create temp file for audio
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            # Generate audio and save to file
            response = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=text,
            )

            # Write audio to temp file
            response.write_to_file(temp_path)

            log.debug("Playing audio with afplay", hook_name)

            # Play with afplay (macOS native audio player)
            subprocess.run(["afplay", temp_path], check=True)

            log.debug("TTS playback completed successfully", hook_name)

        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    except Exception as e:
        log.error("OpenAI TTS failed", hook_name, error=e)
        sys.exit(1)


if __name__ == "__main__":
    main()
