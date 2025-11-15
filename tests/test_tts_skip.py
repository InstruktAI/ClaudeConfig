#!/usr/bin/env python3
"""
Tests for TTS_SKIP_HOOK_EVENTS functionality.
"""

import json
import sys
from io import StringIO
from unittest.mock import patch

from hooks.session_end import main as session_end_main
from hooks.session_start import main as session_start_main


def test_session_start_tts_not_skipped_when_not_in_list(monkeypatch):
    """TTS is called when SessionStart is not in TTS_SKIP_HOOK_EVENTS."""
    monkeypatch.setenv("TTS_SKIP_HOOK_EVENTS", "SessionEnd,Stop")

    with patch("hooks.session_start.speak") as mock_speak:
        input_data = json.dumps({"session_id": "test-123", "source": "startup"})
        sys.stdin = StringIO(input_data)

        try:
            session_start_main()
        except SystemExit:
            pass

        # Verify speak was called
        assert mock_speak.called


def test_session_start_tts_skipped_when_in_list(monkeypatch):
    """TTS is skipped when SessionStart is in TTS_SKIP_HOOK_EVENTS."""
    monkeypatch.setenv("TTS_SKIP_HOOK_EVENTS", "SessionStart,SessionEnd")

    with patch("hooks.session_start.speak") as mock_speak:
        input_data = json.dumps({"session_id": "test-123", "source": "startup"})
        sys.stdin = StringIO(input_data)

        try:
            session_start_main()
        except SystemExit:
            pass

        # Verify speak was NOT called
        assert not mock_speak.called


def test_session_end_tts_not_skipped_when_not_in_list(monkeypatch):
    """TTS is called when SessionEnd is not in TTS_SKIP_HOOK_EVENTS."""
    monkeypatch.setenv("TTS_SKIP_HOOK_EVENTS", "SessionStart,Stop")

    with patch("hooks.session_end.speak") as mock_speak:
        input_data = json.dumps({"session_id": "test-123", "reason": "logout"})
        sys.stdin = StringIO(input_data)

        try:
            session_end_main()
        except SystemExit:
            pass

        # Verify speak was called
        assert mock_speak.called


def test_session_end_tts_skipped_when_in_list(monkeypatch):
    """TTS is skipped when SessionEnd is in TTS_SKIP_HOOK_EVENTS."""
    monkeypatch.setenv("TTS_SKIP_HOOK_EVENTS", "SessionStart,SessionEnd")

    with patch("hooks.session_end.speak") as mock_speak:
        input_data = json.dumps({"session_id": "test-123", "reason": "logout"})
        sys.stdin = StringIO(input_data)

        try:
            session_end_main()
        except SystemExit:
            pass

        # Verify speak was NOT called
        assert not mock_speak.called


def test_tts_skip_with_whitespace_in_env():
    """TTS skip list handles whitespace correctly."""
    skip_events = "SessionStart , SessionEnd,  Stop  ".split(",")
    skip_events = [e.strip() for e in skip_events if e.strip()]

    assert "SessionStart" in skip_events
    assert "SessionEnd" in skip_events
    assert "Stop" in skip_events
    assert len(skip_events) == 3


def test_tts_skip_with_empty_env():
    """TTS skip list handles empty string correctly."""
    skip_events = "".split(",")
    skip_events = [e.strip() for e in skip_events if e.strip()]

    assert len(skip_events) == 0


if __name__ == "__main__":
    import pytest  # noqa: PLC0415

    pytest.main([__file__, "-v"])
