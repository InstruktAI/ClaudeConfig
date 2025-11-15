#!.venv/bin/python
# pylint: disable=import-outside-toplevel
# Rationale: These tests require dynamic imports with importlib.reload()
# to test different LOG_LEVEL environment variable settings.

"""Tests for logging_helper module."""

import sys
from pathlib import Path

import pytest

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))


def test_log_level_filtering_debug(monkeypatch):
    """DEBUG level logs all levels"""
    monkeypatch.setenv("LOG_LEVEL", "debug")

    import importlib

    import utils.logging_helper

    importlib.reload(utils.logging_helper)

    from utils.logging_helper import _should_log

    assert _should_log("debug") is True
    assert _should_log("info") is True
    assert _should_log("warn") is True
    assert _should_log("error") is True


def test_log_level_filtering_info(monkeypatch):
    """INFO level filters DEBUG"""
    monkeypatch.setenv("LOG_LEVEL", "info")

    import importlib

    import utils.logging_helper

    importlib.reload(utils.logging_helper)

    from utils.logging_helper import _should_log

    assert _should_log("debug") is False
    assert _should_log("info") is True
    assert _should_log("warn") is True
    assert _should_log("error") is True


def test_log_level_filtering_error(monkeypatch):
    """ERROR level only logs ERROR"""
    monkeypatch.setenv("LOG_LEVEL", "error")

    import importlib

    import utils.logging_helper

    importlib.reload(utils.logging_helper)

    from utils.logging_helper import _should_log

    assert _should_log("debug") is False
    assert _should_log("info") is False
    assert _should_log("warn") is False
    assert _should_log("error") is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
