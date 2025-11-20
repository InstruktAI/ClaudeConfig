#!/usr/bin/env python3

"""
TTS Queue Runner - ensures sequential FIFO TTS playback.
Uses exclusive file locking to ensure only one TTS plays at a time.
"""

import fcntl
import os
import subprocess
import sys
import time


def run_tts_with_lock(text: str, script_path: str, lock_file: str) -> int:
    """
    Run TTS script while holding exclusive lock.
    This ensures only one TTS plays at a time, regardless of queue state.
    """
    try:
        # Acquire exclusive lock - blocks until available
        with open(lock_file, "a") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)

            # Now we have exclusive access - run TTS
            python_path = os.path.expanduser("~/.claude/.venv/bin/python")
            result = subprocess.run([python_path, script_path, text], check=False)

            # Small delay to ensure audio device is released
            time.sleep(0.5)

            # Lock automatically released when context exits
            return result.returncode
    except Exception:
        return 1


def main():
    if len(sys.argv) < 4:
        sys.exit(1)

    script_path = sys.argv[1]
    text = sys.argv[2]
    job_id = sys.argv[3]

    queue_dir = os.path.expanduser("~/.claude/.tmp/tts_queue")
    os.makedirs(queue_dir, exist_ok=True)

    # Single playback lock ensures sequential execution
    playback_lock = os.path.join(queue_dir, ".playback.lock")

    # Run TTS with exclusive lock - this blocks if another TTS is playing
    exit_code = run_tts_with_lock(text, script_path, playback_lock)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
