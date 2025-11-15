#!.venv/bin/python

"""
TTS Queue Runner - ensures sequential FIFO TTS playback.
Uses filesystem-based FIFO queue with unique job files.
"""

import subprocess
import sys
import time
from pathlib import Path


def wait_for_turn(job_file: Path, queue_dir: Path, max_wait: int = 30) -> bool:
    """Wait until this job is the oldest in queue."""
    waited = 0
    while waited < max_wait:
        jobs = sorted(queue_dir.glob("*.job"))
        if not jobs or jobs[0] == job_file:
            return True
        time.sleep(0.1)
        waited += 0.1
    return False


def run_tts(text: str, script_path: str) -> int:
    """Run TTS script and return exit code."""
    try:
        result = subprocess.run([script_path, text], timeout=10, check=False)
        return result.returncode
    except Exception:
        return 1


def main():
    if len(sys.argv) < 4:
        sys.exit(1)

    script_path = sys.argv[1]
    text = sys.argv[2]
    job_id = sys.argv[3]

    queue_dir = Path.home() / ".claude" / ".tmp" / "tts_queue"
    queue_dir.mkdir(parents=True, exist_ok=True)

    job_file = queue_dir / f"{job_id}.job"
    job_file.touch()

    try:
        if wait_for_turn(job_file, queue_dir):
            exit_code = run_tts(text, script_path)
            sys.exit(exit_code)
        else:
            sys.exit(1)
    finally:
        job_file.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
