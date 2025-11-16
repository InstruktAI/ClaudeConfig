#!/usr/bin/env python3

import os
import sys

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

# Load .env from project root
env_path = os.path.expanduser("~/.claude/.env")
load_dotenv(env_path)

# Import logging after .env is loaded
sys.path.insert(0, os.path.expanduser("~/.claude"))
from utils.logging_helper import log


def main():
    """ElevenLabs TTS - Flash v2.5 model for ultra-low latency speech."""
    hook_name = "elevenlabs_tts"

    # Get API key from environment
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        log.error("ELEVENLABS_API_KEY not found in environment", hook_name)
        sys.exit(1)

    try:
        # Initialize client
        elevenlabs = ElevenLabs(api_key=api_key)

        # Get text from command line argument or use default
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])
        else:
            text = "The first move is what sets everything in motion."

        # Truncate text for logging if too long
        log_text = text[:80] + "..." if len(text) > 80 else text

        # Get voice ID from env or use default
        voice_id = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")

        log.debug(f"Generating with voice ID '{voice_id}': {log_text}", hook_name)

        # Generate and play audio directly
        audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_flash_v2_5",
            output_format="mp3_44100_128",
        )

        log.debug("Playing audio stream", hook_name)
        play(audio)

        log.debug("TTS playback completed successfully", hook_name)

    except Exception as e:
        log.error("ElevenLabs TTS failed", hook_name, error=e)
        sys.exit(1)


if __name__ == "__main__":
    main()
