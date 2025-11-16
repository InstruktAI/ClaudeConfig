#!.venv/bin/python

"""Tests for transcript_parser module."""

import json
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))

from utils.transcript_parser import (
    count_messages,
    get_last_assistant_message,
    transcript_to_array,
)


def test_count_messages():
    """Counts all messages in transcript"""
    with NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(json.dumps({"type": "user", "message": {"role": "user"}}) + "\n")
        f.write(json.dumps({"type": "assistant", "message": {"role": "assistant"}}) + "\n")
        f.write(json.dumps({"type": "user", "message": {"role": "user"}}) + "\n")
        path = f.name

    try:
        count = count_messages(path)
        assert count == 3
    finally:
        Path(path).unlink()


def test_get_last_assistant_message_simple():
    """Extracts text from last assistant message"""
    with NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "Hello"}}) + "\n")
        f.write(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "role": "assistant",
                        "content": [{"type": "text", "text": "I completed the task successfully."}],
                    },
                }
            )
            + "\n"
        )
        path = f.name

    try:
        message = get_last_assistant_message(path)
        assert message == "I completed the task successfully."
    finally:
        Path(path).unlink()


def test_get_last_assistant_message_multiple_blocks():
    """Concatenates multiple text blocks"""
    with NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "role": "assistant",
                        "content": [{"type": "text", "text": "First part. "}, {"type": "text", "text": "Second part."}],
                    },
                }
            )
            + "\n"
        )
        path = f.name

    try:
        message = get_last_assistant_message(path)
        if message is None:
            raise AssertionError("Expected message, got None")
        assert "First part" in message  # pylint: disable=unsupported-membership-test
        assert "Second part" in message  # pylint: disable=unsupported-membership-test
    finally:
        Path(path).unlink()


def test_get_last_assistant_message_only_latest():
    """Returns only the last assistant message"""
    with NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {"role": "assistant", "content": [{"type": "text", "text": "Old message"}]},
                }
            )
            + "\n"
        )
        f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "More"}}) + "\n")
        f.write(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {"role": "assistant", "content": [{"type": "text", "text": "New message"}]},
                }
            )
            + "\n"
        )
        path = f.name

    try:
        message = get_last_assistant_message(path)
        assert message == "New message"
    finally:
        Path(path).unlink()


def test_get_last_assistant_message_with_last_only_flag():
    """Tests last_only flag to get only very last message"""
    with NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {"role": "assistant", "content": [{"type": "text", "text": "First response"}]},
                }
            )
            + "\n"
        )
        f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "Question"}}) + "\n")
        f.write(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {"role": "assistant", "content": [{"type": "text", "text": "Second response"}]},
                }
            )
            + "\n"
        )
        f.write(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {"role": "assistant", "content": [{"type": "text", "text": "Third response"}]},
                }
            )
            + "\n"
        )
        path = f.name

    try:
        message = get_last_assistant_message(path, last_only=True)
        assert message == "Third response"
    finally:
        Path(path).unlink()


def test_get_last_assistant_message_filters_project_root():
    """Filters out Project root: system metadata lines"""
    with NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "text",
                                "text": "Project root: /Users/test/.claude\n\nI'm ready to help you.",
                            }
                        ],
                    },
                }
            )
            + "\n"
        )
        path = f.name

    try:
        message = get_last_assistant_message(path, last_only=True)
        assert message == "I'm ready to help you."
        assert "Project root:" not in message
    finally:
        Path(path).unlink()


def test_get_last_assistant_message_filters_markdown_project_root():
    """Filters out **Project root:** markdown metadata lines"""
    with NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "text",
                                "text": "**Project root: /Users/test/.claude**\n\nReady to assist.",
                            }
                        ],
                    },
                }
            )
            + "\n"
        )
        path = f.name

    try:
        message = get_last_assistant_message(path, last_only=True)
        assert message == "Ready to assist."
        assert "Project root:" not in message
    finally:
        Path(path).unlink()


def test_transcript_to_array():
    """Converts JSONL to array"""
    with NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(json.dumps({"type": "user", "data": "first"}) + "\n")
        f.write(json.dumps({"type": "assistant", "data": "second"}) + "\n")
        path = f.name

    try:
        array = transcript_to_array(path)
        assert len(array) == 2
        assert array[0]["data"] == "first"
        assert array[1]["data"] == "second"
    finally:
        Path(path).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
