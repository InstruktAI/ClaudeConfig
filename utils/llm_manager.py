"""
LLM Manager - unified interface for LLM calls with fallback chain.

Priority order: OpenAI > Anthropic
"""

import os
import random
import subprocess
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def prompt(text: str, hook_name: str = "llm_manager") -> Optional[str]:
    """Send prompt to LLM with fallback chain (OpenAI > Anthropic)."""

    llm_dir = os.path.expanduser("~/.claude/utils/llm")

    if os.getenv("OPENAI_API_KEY"):
        result = subprocess.run(
            [os.path.join(llm_dir, "oai.py"), text],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()

    if os.getenv("ANTHROPIC_API_KEY"):
        result = subprocess.run(
            [os.path.join(llm_dir, "anth.py"), text],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()

    return None


def generate_completion_message(hook_name: str = "llm_manager") -> Optional[str]:
    """Generate a completion message using LLM with fallback."""
    llm_dir = os.path.expanduser("~/.claude/utils/llm")

    if os.getenv("OPENAI_API_KEY"):
        result = subprocess.run(
            [os.path.join(llm_dir, "oai.py"), "--completion"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()

    if os.getenv("ANTHROPIC_API_KEY"):
        result = subprocess.run(
            [os.path.join(llm_dir, "anth.py"), "--completion"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()

    # Fallback to random message
    messages = [
        "Work complete!",
        "All done!",
        "Task finished!",
        "Job complete!",
        "Ready for next task!",
    ]
    return random.choice(messages)


def summarize_text(text: str, hook_name: str = "llm_manager", max_words: int = 20) -> Optional[str]:
    """Summarize text using LLM."""
    if not text:
        return None

    # Truncate if too long (keep last 2000 chars to focus on conclusion)
    if len(text) > 2000:
        text = "..." + text[-2000:]

    prompt_text = f"""You just completed some work. Summarize what you accomplished in {max_words} words or less, speaking in first person as if you just finished the task.

Your response:
{text}"""

    response = prompt(prompt_text, hook_name)
    if not response:
        return None

    # Clean up response
    response = response.strip().strip('"').strip("'").strip()
    response = response.split("\n")[0].strip()  # First line only

    return response
