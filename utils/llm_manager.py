"""
LLM Manager - unified interface for LLM calls with fallback chain.

Priority order: OpenAI > Anthropic
"""

import os
import random
import subprocess
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from utils.logging_helper import log

# Load .env from ~/.claude/ since hooks run from project directories
load_dotenv(Path.home() / ".claude" / ".env")


def prompt(text: str, hook_name: str = "llm_manager") -> Optional[str]:
    """Send prompt to LLM with fallback chain (OpenAI > Anthropic)."""

    llm_dir = os.path.expanduser("~/.claude/utils/llm")

    if os.getenv("OPENAI_API_KEY"):
        try:
            result = subprocess.run(
                [os.path.join(llm_dir, "oai.py"), text],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            log.debug("OpenAI call failed, trying Anthropic", hook_name)
        except subprocess.TimeoutExpired:
            log.warn("OpenAI call timed out after 15s", hook_name)
        except Exception as e:
            log.error(f"OpenAI call error: {e}", hook_name, error=e)

    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            result = subprocess.run(
                [os.path.join(llm_dir, "anth.py"), text],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            log.debug("Anthropic call failed", hook_name)
        except subprocess.TimeoutExpired:
            log.warn("Anthropic call timed out after 15s", hook_name)
        except Exception as e:
            log.error(f"Anthropic call error: {e}", hook_name, error=e)

    log.error("All LLM providers failed", hook_name)
    return None


def generate_completion_message(hook_name: str = "llm_manager") -> Optional[str]:
    """Generate a completion message using LLM with fallback."""
    llm_dir = os.path.expanduser("~/.claude/utils/llm")

    if os.getenv("OPENAI_API_KEY"):
        try:
            result = subprocess.run(
                [os.path.join(llm_dir, "oai.py"), "--completion"],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except subprocess.TimeoutExpired:
            log.warn("OpenAI completion timed out", hook_name)
        except Exception as e:
            log.error(f"OpenAI completion error: {e}", hook_name, error=e)

    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            result = subprocess.run(
                [os.path.join(llm_dir, "anth.py"), "--completion"],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except subprocess.TimeoutExpired:
            log.warn("Anthropic completion timed out", hook_name)
        except Exception as e:
            log.error(f"Anthropic completion error: {e}", hook_name, error=e)

    # Fallback to random message
    log.debug("Using fallback completion message", hook_name)
    messages = [
        "Work complete!",
        "All done!",
        "Task finished!",
        "Job complete!",
        "Ready for next task!",
    ]
    return random.choice(messages)


def summarize_text(text: str, hook_name: str = "llm_manager", max_words: int = 10) -> Optional[str]:
    """Summarize text using LLM."""
    if not text:
        return None

    # Truncate if too long (keep last 2000 chars to focus on conclusion)
    if len(text) > 2000:
        text = "..." + text[-2000:]

    # Detect activity type from content
    lower_text = text.lower()
    is_planning = any(
        phrase in lower_text
        for phrase in [
            "i'll",
            "let me",
            "i'm going to",
            "here's the plan",
            "we can",
            "we should",
            "we need to",
            "first",
            "next step",
        ]
    )
    is_analysis = any(
        phrase in lower_text for phrase in ["analysis", "investigating", "found that", "it appears", "the issue is"]
    )

    if is_planning:
        verb_phrase = "what you proposed"
    elif is_analysis:
        verb_phrase = "what you found"
    else:
        verb_phrase = "what you accomplished"

    prompt_text = f"""Summarize {verb_phrase} in {max_words} words or less, speaking in first person. Be concise and focus on the key outcome only.

Your response:
{text}"""

    response = prompt(prompt_text, hook_name)
    if not response:
        return None

    # Clean up response
    response = response.strip().strip('"').strip("'").strip()
    response = response.split("\n")[0].strip()  # First line only

    return response
