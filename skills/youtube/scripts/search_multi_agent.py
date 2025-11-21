#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "youtube-transcript-api",
#     "aiohttp",
#     "dateparser",
#     "munch",
#     "pydantic",
# ]
# ///
"""Search @indydevdan for multi-agent orchestration videos."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from youtube_helper import youtube_search


async def main() -> None:
    """Find videos where @indydevdan talks about multi-agent orchestration."""
    print("Searching @indydevdan for 'multi-agent orchestration' videos...\n")

    videos = await youtube_search(
        channels="@indydevdan",
        query="multi-agent orchestration",
        period_days=365,
        max_videos_per_channel=20,
        get_transcripts=True,
    )

    # Find videos that actually mention multi-agent
    relevant_videos = []
    for video in videos:
        if video.transcript and "multi-agent" in video.transcript.lower():
            relevant_videos.append(video)

    # Sort by publish time (oldest first to find earliest mentions)
    relevant_videos.sort(key=lambda v: v.publish_time, reverse=True)

    print(f"Found {len(relevant_videos)} videos mentioning multi-agent orchestration:\n")

    for i, video in enumerate(relevant_videos, 1):
        print(f"{i}. {video.title}")
        print(f"   URL: https://youtube.com{video.url_suffix}")
        print(f"   Published: {video.publish_time}")
        print(f"   Views: {video.views}")

        # Find first mention in transcript
        transcript_lower = video.transcript.lower()
        idx = transcript_lower.find("multi-agent")
        if idx >= 0:
            # Find timestamp before this mention
            timestamp_start = transcript_lower.rfind("[", 0, idx)
            timestamp_end = transcript_lower.find("]", timestamp_start)
            if timestamp_start >= 0 and timestamp_end >= 0:
                timestamp = video.transcript[timestamp_start : timestamp_end + 1]
                context_start = max(0, idx - 30)
                context_end = min(len(video.transcript), idx + 120)
                context = video.transcript[context_start:context_end].strip()
                print(f"   First mention at {timestamp}: ...{context}...")
        print()


if __name__ == "__main__":
    asyncio.run(main())
