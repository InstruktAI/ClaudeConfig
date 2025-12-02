#!/usr/bin/env python3

"""
TTS Queue Runner - ensures sequential FIFO TTS playback with fallback.
Uses exclusive file locking to ensure only one TTS plays at a time.
Supports fallback chain: tries each TTS service until one succeeds.
"""

import fcntl
import os
import subprocess
import sys
import time

from utils.logging_helper import log


def run_tts_script(text: str, script_path: str) -> bool:
    """Run a single TTS script, return True if successful."""
    python_path = os.path.expanduser("~/.claude/.venv/bin/python")
    result = subprocess.run([python_path, script_path, text], check=False, capture_output=True)
    return result.returncode == 0


def run_tts_with_lock(text: str, script_paths: list[str], lock_file: str) -> int:
    """
    Run TTS scripts with fallback while holding exclusive lock.
    Tries each script in order until one succeeds.
    """
    try:
        with open(lock_file, "a") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)

            for script_path in script_paths:
                service_name = os.path.basename(script_path).replace("_tts.py", "").replace("_simple", "")
                log.debug(f"Trying TTS: {service_name}", "tts_queue_runner")

                if run_tts_script(text, script_path):
                    log.debug(f"TTS succeeded: {service_name}", "tts_queue_runner")
                    time.sleep(0.5)
                    return 0

                log.debug(f"TTS failed: {service_name}, trying next...", "tts_queue_runner")

            log.error("All TTS services failed", "tts_queue_runner")
            return 1
    except Exception as e:
        log.error(f"TTS lock error: {e}", "tts_queue_runner")
        return 1


def main():
    # Usage: tts_queue_runner.py <script1> [script2] ... -- <text> <job_id>
    if len(sys.argv) < 4:
        sys.exit(1)

    # Parse args: scripts before --, text and job_id after
    if "--" in sys.argv:
        separator_idx = sys.argv.index("--")
        script_paths = sys.argv[1:separator_idx]
        text = sys.argv[separator_idx + 1]
        # job_id = sys.argv[separator_idx + 2]  # unused but kept for compatibility
    else:
        # Legacy single-script mode for backwards compatibility
        script_paths = [sys.argv[1]]
        text = sys.argv[2]
        # job_id = sys.argv[3]

    queue_dir = os.path.expanduser("~/.claude/.tmp/tts_queue")
    os.makedirs(queue_dir, exist_ok=True)

    playback_lock = os.path.join(queue_dir, ".playback.lock")
    exit_code = run_tts_with_lock(text, script_paths, playback_lock)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
