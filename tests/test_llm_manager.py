#!.venv/bin/python

"""Tests for llm_manager module."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))

from utils.llm_manager import summarize_text


def test_summarize_text_truncates_long_text():
    """Truncates text longer than 2000 chars and keeps last part"""
    long_text = "x" * 3000

    with patch("utils.llm_manager.prompt") as mock_prompt:
        mock_prompt.return_value = "Summary"

        summarize_text(long_text, "test_hook")

        # Check that prompt was called with truncated text
        call_args = mock_prompt.call_args[0][0]
        assert "..." in call_args
        assert len(call_args) < 3000


def test_summarize_text_strips_quotes():
    """Strips quotes from LLM response"""
    with patch("utils.llm_manager.prompt") as mock_prompt:
        mock_prompt.return_value = '"Summary with quotes"'

        result = summarize_text("Test text", "test_hook")

        assert result == "Summary with quotes"


def test_summarize_text_takes_first_line_only():
    """Uses only first line of LLM response"""
    with patch("utils.llm_manager.prompt") as mock_prompt:
        mock_prompt.return_value = "First line\nSecond line"

        result = summarize_text("Test text", "test_hook")

        assert result == "First line"


def test_summarize_text_respects_max_words_parameter():
    """Includes max_words in prompt"""
    with patch("utils.llm_manager.prompt") as mock_prompt:
        mock_prompt.return_value = "Summary"

        summarize_text("Test text", "test_hook", max_words=15)

        call_args = mock_prompt.call_args[0][0]
        assert "15 words" in call_args


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
