#!/usr/bin/env python3
"""
Configuration test script - validates installation and hook setup.
Called at the end of installation to verify everything works.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Fun messages for each test
MESSAGES = {
    "session_start": "🎬 Session start hook",
    "session_end": "🎭 Session end hook",
    "stop": "🛑 Stop hook",
    "subagent_stop": "🤖 Subagent stop hook",
    "notification": "🔔 Notification hook",
}

EMOJI_PASS = "✓"
EMOJI_SKIP = "⊘"


def print_header():
    """Print test header."""
    print("\n" + "=" * 50)
    print("  🧪 Configuration Test Suite")
    print("=" * 50)
    print()


def print_result(name: str, passed: bool, message: str = ""):
    """Print a test result."""
    emoji = EMOJI_PASS if passed else "✗"
    status = "PASS" if passed else "FAIL"
    msg = f"  {emoji} {name}: {status}"
    if message:
        msg += f" - {message}"
    print(msg)


def test_hook(hook_name: str, input_data: dict, project_root: Path) -> bool:
    """Test a hook by calling it with sample data."""
    hook_file = project_root / "hooks" / f"{hook_name}.py"
    if not hook_file.exists():
        return False

    try:
        result = subprocess.run(
            [str(hook_file)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def test_env_vars() -> tuple[bool, str]:
    """Test that required environment variables are set."""
    required = ["ENGINEER_NAME", "ENGINEER_EMAIL"]
    missing = [var for var in required if not os.getenv(var)]

    if missing:
        return False, f"Missing: {', '.join(missing)}"
    return True, "All required vars set"


def test_tts_config() -> tuple[bool, str]:
    """Test TTS configuration."""
    tts_service = os.getenv("TTS_SERVICE", "")
    if not tts_service:
        return False, "TTS_SERVICE not set"

    # Check if skip events is configured
    skip_events = os.getenv("TTS_SKIP_HOOK_EVENTS", "")
    if skip_events:
        return True, f"TTS configured (skipping: {skip_events})"
    return True, "TTS configured"


def main() -> int:
    """Run configuration tests."""
    print_header()

    project_root = Path(__file__).parent.parent

    # Test 1: Environment variables
    passed, msg = test_env_vars()
    print_result("Environment variables", passed, msg)
    if not passed:
        print("\n  ⚠️  Please configure .env with your details")
        return 1

    # Test 2: TTS configuration
    passed, msg = test_tts_config()
    print_result("TTS configuration", passed, msg)

    # Test 3: Test hooks
    print()
    hooks_tested = 0
    hooks_passed = 0

    # SessionStart
    passed = test_hook(
        "session_start",
        {"session_id": "test-config", "source": "startup"},
        project_root,
    )
    hooks_tested += 1
    if passed:
        hooks_passed += 1
    print_result(MESSAGES["session_start"], passed, "Hook executed")

    # SessionEnd
    passed = test_hook(
        "session_end",
        {"session_id": "test-config", "reason": "test"},
        project_root,
    )
    hooks_tested += 1
    if passed:
        hooks_passed += 1
    print_result(MESSAGES["session_end"], passed, "Hook executed")

    # Stop
    passed = test_hook(
        "stop",
        {"session_id": "test-config", "transcript_path": None},
        project_root,
    )
    hooks_tested += 1
    if passed:
        hooks_passed += 1
    print_result(MESSAGES["stop"], passed, "Hook executed")

    # SubagentStop
    passed = test_hook(
        "subagent_stop",
        {"session_id": "test-config"},
        project_root,
    )
    hooks_tested += 1
    if passed:
        hooks_passed += 1
    print_result(MESSAGES["subagent_stop"], passed, "Hook executed")

    # Notification
    passed = test_hook(
        "notification",
        {"session_id": "test-config", "message": "Test"},
        project_root,
    )
    hooks_tested += 1
    if passed:
        hooks_passed += 1
    print_result(MESSAGES["notification"], passed, "Hook executed")

    # Summary
    print()
    print("=" * 50)
    if hooks_passed == hooks_tested:
        print(f"  🎉 All {hooks_tested} hooks tested successfully!")
        print("  🚀 Your Claude Code setup is ready!")
    else:
        print(f"  ⚠️  {hooks_passed}/{hooks_tested} hooks passed")
        print("  Some hooks may need attention")
    print("=" * 50)
    print()

    return 0 if hooks_passed == hooks_tested else 1


if __name__ == "__main__":
    sys.exit(main())
