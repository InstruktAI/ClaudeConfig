#!/usr/bin/env python3
"""Summarizer utility - generates summary and title from transcript.

Can be imported as a module or run as a script.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI

from utils.file_log import append_line

# Load .env from ~/.claude/ since hooks run from project directories
load_dotenv(Path.home() / ".claude" / ".env")

LOG_FILE = Path.home() / ".claude" / "logs" / "summarizer.log"


def log(message: str) -> None:
    """Write log message to file."""
    try:
        append_line(LOG_FILE, f"[{datetime.now().isoformat()}] {message}")
    except Exception:
        pass


def extract_assistant_since_last_user(transcript_path: Path) -> str:
    """Extract assistant text messages since the last user input.

    This captures exactly what the AI did between Stop events - the work done
    after the user's last message. Filters out tool_use blocks.

    Args:
        transcript_path: Path to Claude session .jsonl file

    Returns:
        Plain text of assistant messages since last user input
    """
    assistant_texts: list[str] = []

    try:
        with open(transcript_path) as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)

                # Skip non-message entries
                if entry.get("type") == "summary":
                    continue

                message = entry.get("message", {})
                role = message.get("role")
                content = message.get("content", [])

                if not role:
                    continue

                if role == "user" and isinstance(content, str):
                    # User message - reset assistant texts (start fresh)
                    assistant_texts = []

                elif role == "assistant" and isinstance(content, list):
                    # Extract only text blocks, skip tool_use
                    for block in content:
                        if block.get("type") == "text":
                            text = block.get("text", "").strip()
                            if text:
                                assistant_texts.append(text)

    except Exception:
        return ""

    # Join all assistant texts since last user input
    combined = "\n\n".join(assistant_texts)

    # Truncate if too long (keep last 3000 chars)
    if len(combined) > 3000:
        combined = combined[-3000:]

    return combined


def _parse_response(text: str) -> tuple[str, str | None]:
    """Parse LLM response into summary and title."""
    summary = "Work complete!"
    title = None

    for line in text.strip().split("\n"):
        if line.startswith("SUMMARY:"):
            summary = line[8:].strip()
        elif line.startswith("TITLE:"):
            title = line[6:].strip()[:50]  # Max 50 chars

    return summary, title


def generate_summary_and_title(conversation: str) -> tuple[str, str | None]:
    """Generate summary and title using Claude API (with OpenAI fallback).

    Returns:
        Tuple of (summary_message, title) where title may be None if extraction fails.
    """
    if not conversation.strip():
        return "Work complete!", None

    prompt = f"""Summarize what an AI assistant reported in its last messages. Write for humans tracking progress.

Rules:
- First person ("I...")
- 1-2 sentences
- Accurately reflect what the AI said it did or observed
- Preserve the subject: if AI said "the worker did X", say "I delegated X" or "My worker did X" - not "I did X"
- Also provide a short title (max 50 chars)

Format:
SUMMARY: <your summary>
TITLE: <short title>

AI's recent messages:
{conversation}"""

    # Try Anthropic first
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        try:
            client = Anthropic(api_key=anthropic_key)
            response = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}],
            )
            return _parse_response(response.content[0].text)
        except Exception as e:
            log(f"Anthropic API failed: {e}")

    # Try OpenAI as fallback
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}],
            )
            return _parse_response(response.choices[0].message.content or "")
        except Exception as e:
            log(f"OpenAI API failed: {e}")

    # No API keys or all failed
    if not anthropic_key and not openai_key:
        log("No API keys found (ANTHROPIC_API_KEY or OPENAI_API_KEY)")

    return "Work complete!", None


def summarize_transcript(transcript_path: str) -> dict:
    """Generate summary and title from transcript file.

    Args:
        transcript_path: Path to Claude session .jsonl file

    Returns:
        Dict with "summary" and "title" keys, or "error" key on failure.
    """
    path = Path(transcript_path)

    if not path.exists():
        return {"error": f"Transcript not found: {transcript_path}"}

    assistant_output = extract_assistant_since_last_user(path)
    summary, title = generate_summary_and_title(assistant_output)

    return {"summary": summary, "title": title}


def main() -> int:
    """CLI entry point - read transcript, generate summary/title, output JSON to stdout."""
    if len(sys.argv) != 2:
        print(json.dumps({"error": f"Usage: {sys.argv[0]} <transcript_path>"}))
        return 1

    result = summarize_transcript(sys.argv[1])
    print(json.dumps(result))
    return 1 if "error" in result else 0


if __name__ == "__main__":
    sys.exit(main())
