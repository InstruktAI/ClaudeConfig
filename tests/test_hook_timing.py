#!.venv/bin/python
"""
Test that hooks return immediately and work continues in background.
"""

import json
import subprocess
import time
from pathlib import Path


def test_stop_hook_timing():
    """Test that stop hook returns immediately when not notifying."""
    hook_path = Path.home() / ".claude" / "hooks" / "stop.py"

    test_input = {"session_id": "test-session", "transcript_path": ""}

    start = time.time()

    result = subprocess.run(
        [str(hook_path)],  # Without --notify, no LLM calls
        input=json.dumps(test_input).encode(),
        capture_output=True,
        timeout=5,
        check=False,
    )

    elapsed = time.time() - start

    print(f"Hook returned in {elapsed:.3f} seconds")
    print(f"Exit code: {result.returncode}")

    # Hook should return immediately when just logging
    assert elapsed < 0.5, f"Hook took {elapsed:.3f}s - should return immediately"

    print(f"✅ PASSED: Hook returned in {elapsed:.3f}s")

    # Wait a bit to see if background work happens
    print("Waiting 3s for background work...")
    time.sleep(3)

    # Check logs to see if work completed
    log_path = Path.home() / ".claude" / "logs" / "hooks.log"
    if log_path.exists():
        with open(log_path, "r") as f:
            recent_logs = f.read().split("\n")[-10:]
            for line in recent_logs:
                if "test-session" in line:
                    print(f"Found log entry: {line}")


if __name__ == "__main__":
    test_stop_hook_timing()
