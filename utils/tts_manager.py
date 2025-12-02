"""
TTS Manager - unified interface for text-to-speech across hooks.

Priority order: ElevenLabs > OpenAI > pyttsx3
"""

import os
import subprocess
import time
from typing import Optional

from dotenv import load_dotenv

from utils.logging_helper import log

load_dotenv()


def get_tts_script_path() -> Optional[str]:
    """
    Determine which TTS script to use based on available options.
    Priority order: macOS say > ElevenLabs > OpenAI > pyttsx3

    Returns:
        Path to TTS script, or None if none available
    """
    tts_dir = os.path.expanduser("~/.claude/utils/tts")

    # Check for macOS say (highest priority - native, reliable)
    macos_say_script = os.path.join(tts_dir, "macos_say_tts.py")
    if os.path.exists(macos_say_script):
        return macos_say_script

    # Check for ElevenLabs API key
    if os.getenv("ELEVENLABS_API_KEY"):
        elevenlabs_script = os.path.join(tts_dir, "elevenlabs_tts.py")
        if os.path.exists(elevenlabs_script):
            return elevenlabs_script

    # Check for OpenAI API key
    if os.getenv("OPENAI_API_KEY"):
        openai_script = os.path.join(tts_dir, "openai_tts.py")
        if os.path.exists(openai_script):
            return openai_script

    # Fall back to pyttsx3 (no API key required)
    pyttsx3_script = os.path.join(tts_dir, "pyttsx3_tts.py")
    if os.path.exists(pyttsx3_script):
        return pyttsx3_script

    return None


def speak(text: str, hook_name: str, session_id: Optional[str] = None, timeout: int = 10) -> bool:
    """
    Speak text using configured TTS service with fallback chain.

    Configure with TTS_SERVICE env var (comma-separated list):
    - macos (default, free, reliable)
    - openai (high quality, requires API key)
    - elevenlabs (premium quality, requires API key)
    - pyttsx3 (offline fallback)

    Example: TTS_SERVICE=elevenlabs,macos,pyttsx3
    Fallback happens in the queue runner if a service fails (e.g., quota exceeded).
    """
    tts_dir = os.path.expanduser("~/.claude/utils/tts")

    service_priority = os.getenv("TTS_SERVICE", "macos")
    service_names = [s.strip().lower() for s in service_priority.split(",")]

    service_map = {
        "macos": ("macOS say", os.path.join(tts_dir, "macos_say_tts.py")),
        "openai": ("OpenAI", os.path.join(tts_dir, "openai_tts_simple.py")),
        "elevenlabs": ("ElevenLabs", os.path.join(tts_dir, "elevenlabs_tts.py")),
        "pyttsx3": ("pyttsx3", os.path.join(tts_dir, "pyttsx3_tts.py")),
    }

    log.debug(f"Speaking: {text} (priority: {service_priority})", hook_name, session_id)

    # Build list of valid script paths for fallback chain
    script_paths = []
    service_labels = []
    for service in service_names:
        service_name, script_path = service_map.get(service, (None, None))
        if not service_name:
            continue

        # Skip if API key missing
        if service == "openai" and not os.getenv("OPENAI_API_KEY"):
            continue
        if service == "elevenlabs" and not os.getenv("ELEVENLABS_API_KEY"):
            continue

        if script_path and os.path.exists(script_path):
            script_paths.append(script_path)
            service_labels.append(service_name)

    if not script_paths:
        log.error("No TTS services available", hook_name, session_id)
        return False

    try:
        python_path = os.path.expanduser("~/.claude/.venv/bin/python")
        queue_runner = os.path.expanduser("~/.claude/utils/tts_queue_runner.py")
        job_id = f"{time.time_ns()}"

        # Pass all scripts as fallback chain: script1 script2 ... -- text job_id
        cmd = [python_path, queue_runner] + script_paths + ["--", text, job_id]
        log.debug(f"TTS fallback chain: {', '.join(service_labels)}", hook_name, session_id)

        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log.debug(f"TTS queued (pid: {result.pid})", hook_name, session_id)
        return True
    except Exception as e:
        log.error(f"TTS queue error: {e}", hook_name, session_id, error=e)
        return False
