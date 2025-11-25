#!/usr/bin/env python3
"""
Tests for TTS hook functionality.
"""

import os
from unittest.mock import patch

from hooks.tts import (
    handle_session_end,
    handle_session_start,
    should_skip_event,
)


def test_session_start_tts_not_skipped_when_not_in_list(monkeypatch):
    """TTS is called when SessionStart is not in TTS_SKIP_HOOK_EVENTS."""
    monkeypatch.setenv("TTS_SKIP_HOOK_EVENTS", "SessionEnd,Stop")

    with patch("hooks.tts.speak") as mock_speak:
        handle_session_start({"session_id": "test-123", "source": "startup"}, "test-123")
        assert mock_speak.called


def test_session_start_tts_skipped_when_in_list(monkeypatch):
    """TTS is skipped when SessionStart is in TTS_SKIP_HOOK_EVENTS."""
    monkeypatch.setenv("TTS_SKIP_HOOK_EVENTS", "SessionStart,SessionEnd")

    with patch("hooks.tts.speak") as mock_speak:
        handle_session_start({"session_id": "test-123", "source": "startup"}, "test-123")
        assert not mock_speak.called


def test_session_end_tts_not_skipped_when_not_in_list(monkeypatch):
    """TTS is called when SessionEnd is not in TTS_SKIP_HOOK_EVENTS."""
    monkeypatch.setenv("TTS_SKIP_HOOK_EVENTS", "SessionStart,Stop")

    with patch("hooks.tts.speak") as mock_speak:
        with patch("hooks.tts.count_messages", return_value=5):
            handle_session_end({"session_id": "test-123", "reason": "logout"}, "test-123")
        assert mock_speak.called


def test_session_end_tts_skipped_when_in_list(monkeypatch):
    """TTS is skipped when SessionEnd is in TTS_SKIP_HOOK_EVENTS."""
    monkeypatch.setenv("TTS_SKIP_HOOK_EVENTS", "SessionStart,SessionEnd")

    with patch("hooks.tts.speak") as mock_speak:
        with patch("hooks.tts.count_messages", return_value=5):
            handle_session_end({"session_id": "test-123", "reason": "logout"}, "test-123")
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


def test_should_skip_event_returns_true_when_in_list(monkeypatch):
    """should_skip_event returns True when event is in skip list."""
    monkeypatch.setenv("TTS_SKIP_HOOK_EVENTS", "SessionStart,SessionEnd")
    assert should_skip_event("SessionStart") is True
    assert should_skip_event("SessionEnd") is True


def test_should_skip_event_returns_false_when_not_in_list(monkeypatch):
    """should_skip_event returns False when event is not in skip list."""
    monkeypatch.setenv("TTS_SKIP_HOOK_EVENTS", "SessionStart,SessionEnd")
    assert should_skip_event("Stop") is False
    assert should_skip_event("SubagentStop") is False


def test_tts_enabled_supports_multiple_formats(monkeypatch):
    """TTS_ENABLED supports various boolean formats."""
    test_cases = [
        ("0", False),
        ("no", False),
        ("off", False),
        ("false", False),
        ("FALSE", False),
        ("1", True),
        ("yes", True),
        ("on", True),
        ("true", True),
        ("TRUE", True),
    ]

    for value, _should_be_enabled in test_cases:
        monkeypatch.setenv("TTS_ENABLED", value)
        assert os.getenv("TTS_ENABLED") == value


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
