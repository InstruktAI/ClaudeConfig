"""
Transcript parser utilities for Claude Code hooks.
Handles reading and parsing JSONL transcript files.
"""

import json
import os
from typing import Optional

from utils.logging_helper import log


def count_messages(transcript_path: str) -> int:
    """
    Count total messages in a transcript.

    Args:
        transcript_path: Path to JSONL transcript file

    Returns:
        Number of messages, or 0 if error
    """
    if not transcript_path or not os.path.exists(transcript_path):
        return 0

    try:
        with open(transcript_path, "r") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def get_last_assistant_message(transcript_path: str, last_only: bool = False) -> Optional[str]:
    """
    Extract assistant text responses since the last user input.

    Args:
        transcript_path: Path to JSONL transcript file
        last_only: If True, return only the very last assistant message.
                   If False, return all assistant messages since last user input.

    Returns:
        Assistant text(s), or None if not found
    """
    if not transcript_path or not os.path.exists(transcript_path):
        return None

    def clean_text(text: str) -> str:
        """Remove system metadata lines from assistant messages."""
        lines = text.split("\n")
        cleaned_lines = []
        for line in lines:
            # Skip lines that are just system metadata
            stripped = line.strip()
            if stripped.startswith("Project root:"):
                continue
            if stripped.startswith("**Project root:"):
                continue
            cleaned_lines.append(line)
        return "\n".join(cleaned_lines).strip()

    try:
        entries = []
        with open(transcript_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    entries.append(entry)
                except json.JSONDecodeError:
                    continue

        if last_only:
            # Just get the very last assistant message
            for i in range(len(entries) - 1, -1, -1):
                entry = entries[i]
                if entry.get("type") == "assistant":
                    message = entry.get("message", {})
                    content = message.get("content", [])
                    if isinstance(content, list):
                        text_parts = [block.get("text", "") for block in content if block.get("type") == "text"]
                        if text_parts:
                            full_text = " ".join(text_parts)
                            cleaned = clean_text(full_text)
                            if cleaned:
                                return cleaned
            return None

        # Find the last user message
        last_user_idx = -1
        for i in range(len(entries) - 1, -1, -1):
            if entries[i].get("type") == "user":
                last_user_idx = i
                break

        # Collect all assistant text responses after the last user message
        assistant_texts = []
        start_idx = last_user_idx + 1 if last_user_idx >= 0 else 0

        for i in range(start_idx, len(entries)):
            entry = entries[i]
            if entry.get("type") == "assistant":
                message = entry.get("message", {})
                content = message.get("content", [])
                if isinstance(content, list):
                    # Extract only text blocks (skip tool_use blocks)
                    text_parts = [block.get("text", "") for block in content if block.get("type") == "text"]
                    if text_parts:
                        assistant_texts.append(" ".join(text_parts))

        return " ".join(assistant_texts) if assistant_texts else None
    except Exception as e:
        log.error("Failed to parse transcript", "transcript_parser", error=e)
        return None


def transcript_to_array(transcript_path: str) -> list[dict[str, object]]:
    """
    Convert JSONL transcript to array of entries.

    Args:
        transcript_path: Path to JSONL transcript file

    Returns:
        List of transcript entries, or empty list if error
    """
    if not transcript_path or not os.path.exists(transcript_path):
        return []

    chat_data = []
    try:
        with open(transcript_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        chat_data.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass  # Skip invalid lines
    except Exception as e:
        log.error("Failed to read transcript", "transcript_parser", error=e)

    return chat_data
