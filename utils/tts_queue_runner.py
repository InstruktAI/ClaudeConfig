#!/usr/bin/env python3

"""
TTS Queue Runner - ensures sequential FIFO TTS playback.
Uses filesystem-based FIFO queue with unique job files.
"""

import glob
import os
import subprocess
import sys
import time


def wait_for_turn(job_file: str, queue_dir: str, max_wait: int = 30) -> bool:
    """Wait until this job is the oldest in queue."""
    waited = 0
    while waited < max_wait:
        jobs = sorted(glob.glob(os.path.join(queue_dir, "*.job")))
        if not jobs or jobs[0] == job_file:
            return True
        time.sleep(0.1)
        waited += 0.1
    return False


def run_tts(text: str, script_path: str) -> int:
    """Run TTS script and return exit code."""
    try:
        python_path = os.path.expanduser("~/.claude/.venv/bin/python")
        result = subprocess.run([python_path, script_path, text], timeout=10, check=False)
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

    job_file = os.path.join(queue_dir, f"{job_id}.job")
    open(job_file, "a").close()

    try:
        if wait_for_turn(job_file, queue_dir):
            exit_code = run_tts(text, script_path)
            sys.exit(exit_code)
        else:
            sys.exit(1)
    finally:
        if os.path.exists(job_file):
            os.unlink(job_file)


if __name__ == "__main__":
    main()
