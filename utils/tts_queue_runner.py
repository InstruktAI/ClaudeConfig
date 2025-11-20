#!/usr/bin/env python3

"""
TTS Queue Runner - ensures sequential FIFO TTS playback.
Uses filesystem-based FIFO queue with unique job files and file locking.
"""

import fcntl
import glob
import os
import subprocess
import sys
import time


def wait_for_turn(job_file: str, queue_dir: str, max_wait: int = 30) -> bool:
    """Wait until this job is the oldest in queue."""
    lock_file = os.path.join(queue_dir, ".queue.lock")
    waited = 0
    job_name = os.path.basename(job_file)

    while waited < max_wait:
        # Use file lock to ensure atomic queue inspection
        with open(lock_file, "w") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            jobs = sorted(glob.glob(os.path.join(queue_dir, "*.job")))
            is_my_turn = not jobs or jobs[0] == job_file

            # Debug: Log queue state if waiting
            if not is_my_turn and waited < 0.5:
                queue_jobs = [os.path.basename(j) for j in jobs]
                print(
                    f"[TTS Queue] {job_name} waiting, queue: {queue_jobs[:3]}",
                    file=sys.stderr,
                )

            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)

        if is_my_turn:
            return True

        time.sleep(0.1)
        waited += 0.1
    return False


def run_tts(text: str, script_path: str) -> int:
    """Run TTS script and return exit code."""
    try:
        python_path = os.path.expanduser("~/.claude/.venv/bin/python")
        result = subprocess.run([python_path, script_path, text], check=False)
        # Small delay after playback to ensure audio fully completes before next item
        time.sleep(0.5)
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
    lock_file = os.path.join(queue_dir, ".queue.lock")

    # Atomically create job file under lock to prevent race conditions
    with open(lock_file, "w") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        open(job_file, "a").close()
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)

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
