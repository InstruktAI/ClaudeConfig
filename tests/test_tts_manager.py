#!.venv/bin/python

"""Tests for tts_manager module."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))

from utils.tts_manager import speak


def test_speak_respects_service_priority(monkeypatch):
    """Tries services in TTS_SERVICE order"""
    monkeypatch.setenv("TTS_ENABLED", "true")
    monkeypatch.setenv("TTS_SERVICE", "macos,openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    with patch("subprocess.Popen") as mock_popen:
        speak("Test", "test_hook")

        # Should call python with queue runner and macos script path
        assert mock_popen.called
        args = mock_popen.call_args[0][0]
        assert "python" in str(args[0])
        assert "tts_queue_runner.py" in str(args[1])
        assert "macos_say_tts.py" in str(args[2])


def test_speak_passes_text_to_subprocess(monkeypatch):
    """Passes text as argument to TTS script"""
    monkeypatch.setenv("TTS_ENABLED", "true")
    monkeypatch.setenv("TTS_SERVICE", "macos")

    with patch("subprocess.Popen") as mock_popen:
        speak("Hello world", "test_hook")

        # Text should be passed to queue runner
        args = mock_popen.call_args[0][0]
        assert "Hello world" in args


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
