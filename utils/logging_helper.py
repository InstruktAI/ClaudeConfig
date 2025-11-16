"""
Unified logging helper for Claude Code hooks.
All log levels go to ~/.claude/logs/hooks.log

Usage:
    from utils.logging_helper import log

    log.debug("Starting hook", "stop")
    log.error("TTS failed", "stop", error=e)

Configuration:
    Set LOG_LEVEL in .env: debug, info, warn, error (default: info)
"""

import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

# Log level hierarchy: DEBUG < INFO < WARN < ERROR
_LEVELS = {"debug": 0, "info": 1, "warn": 2, "error": 3}


def _get_log_path() -> str:
    """Get the unified log file path at ~/.claude/logs/hooks.log"""
    log_dir = os.path.expanduser("~/.claude/logs")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, "hooks.log")


def _get_min_level() -> int:
    """Get minimum log level from env (lazy evaluation)."""
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    return _LEVELS.get(log_level, 1)


def _should_log(level: str) -> bool:
    """Check if this level should be logged based on LOG_LEVEL setting."""
    return _LEVELS.get(level, 0) >= _get_min_level()


def _write_log(
    level: str, message: str, hook_name: str, session_id: Optional[str] = None, error: Optional[Exception] = None
) -> None:
    """Write a log entry if level is enabled."""
    if not _should_log(level):
        return

    log_path = _get_log_path()
    timestamp = datetime.now().isoformat()

    log_entry = f"[{timestamp}] [{level.upper()}] [{hook_name}] {message}"

    if error:
        log_entry += f" | {type(error).__name__}: {error}"

    try:
        with open(log_path, "a") as f:
            f.write(log_entry + "\n")
    except Exception:
        pass  # Don't crash if logging fails


class _Logger:
    """Simple logger with level methods."""

    def debug(self, message: str, hook_name: str, session_id: Optional[str] = None) -> None:
        _write_log("DEBUG", message, hook_name, session_id)

    def info(self, message: str, hook_name: str, session_id: Optional[str] = None) -> None:
        _write_log("INFO", message, hook_name, session_id)

    def warn(
        self, message: str, hook_name: str, session_id: Optional[str] = None, error: Optional[Exception] = None
    ) -> None:
        _write_log("WARN", message, hook_name, session_id, error)

    def error(
        self, message: str, hook_name: str, session_id: Optional[str] = None, error: Optional[Exception] = None
    ) -> None:
        _write_log("ERROR", message, hook_name, session_id, error)


# Single global logger instance
log = _Logger()
