#!/Users/Morriz/.claude/.venv/bin/python

"""
Multi-Agent Observability Hook Script
Sends Claude Code hook events to the observability server.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime

from dotenv import load_dotenv

from utils.logging_helper import log
from utils.model_extractor import get_model_from_transcript
from utils.summarizer import generate_event_summary

load_dotenv()


def send_event_to_server(
    event_data: dict[str, object], server_url: str = "http://localhost:4000/events", hook_name: str = "send_event"
) -> bool:
    """Send event data to the observability server."""
    try:
        req = urllib.request.Request(
            server_url,
            data=json.dumps(event_data).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Claude-Code-Hook/1.0"},
        )

        with urllib.request.urlopen(req, timeout=1) as response:
            if response.status == 200:
                log.debug(
                    f"Event sent successfully: {event_data.get('hook_event_type')}",
                    hook_name,
                    event_data.get("session_id"),
                )
                return True
            else:
                log.warn(f"Server returned status {response.status}", hook_name, event_data.get("session_id"))
                return False

    except urllib.error.URLError as e:
        log.debug(f"Server not reachable: {e}", hook_name, event_data.get("session_id"))
        return False
    except Exception as e:
        log.error(f"Failed to send event: {e}", hook_name, event_data.get("session_id"), error=e)
        return False


def main() -> None:
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--source-app", required=True)
        parser.add_argument("--event-type", required=True)
        parser.add_argument("--server-url", default="http://localhost:4000/events")
        parser.add_argument("--add-chat", action="store_true")
        parser.add_argument("--summarize", action="store_true")
        args = parser.parse_args()

        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id")

        # Check if event sending is enabled
        if os.getenv("SEND_EVENTS", "false").lower() != "true":
            log.debug("Event sending disabled (SEND_EVENTS=false)", "send_event", session_id)
            sys.exit(0)

        log.debug(f"Sending {args.event_type} event to {args.source_app}", "send_event", session_id)

        transcript_path = input_data.get("transcript_path")
        model_name = ""
        if transcript_path:
            model_name = get_model_from_transcript(session_id, transcript_path)

        event_data = {
            "source_app": args.source_app,
            "session_id": session_id,
            "hook_event_type": args.event_type,
            "payload": input_data,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "model_name": model_name,
        }

        if args.add_chat and transcript_path and os.path.exists(transcript_path):
            chat_data = []
            try:
                with open(transcript_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                chat_data.append(json.loads(line))
                            except json.JSONDecodeError:
                                pass

                event_data["chat"] = chat_data
            except Exception:
                pass

        if args.summarize:
            summary = generate_event_summary(event_data)
            if summary:
                event_data["summary"] = summary

        send_event_to_server(event_data, args.server_url, "send_event")
        log.debug(f"{args.event_type} event sent", "send_event", session_id)
        sys.exit(0)

    except json.JSONDecodeError as e:
        log.error(f"Invalid JSON input: {e}", "send_event", error=e)
        sys.exit(0)
    except Exception as e:
        log.error(f"Unexpected error in send_event: {e}", "send_event", error=e)
        sys.exit(0)


if __name__ == "__main__":
    main()
