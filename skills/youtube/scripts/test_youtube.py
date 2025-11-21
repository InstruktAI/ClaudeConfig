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
"""Test script for YouTube search and transcript extraction."""

import asyncio
import sys
import traceback
from pathlib import Path

# Add parent to path to import youtube_helper
sys.path.insert(0, str(Path(__file__).parent))

from youtube_helper import youtube_search, youtube_transcripts


async def test_channel_search() -> None:
    """Test searching a specific channel with query."""
    print("\n=== Test 1: Channel Search with Query ===")
    videos = await youtube_search(
        channels="@indydevdan",
        query="multi-agent",
        period_days=90,
        max_videos_per_channel=3,
        get_transcripts=True,
    )

    print(f"Found {len(videos)} videos")
    for video in videos:
        print(f"\nTitle: {video.title}")
        print(f"URL: https://youtube.com{video.url_suffix}")
        print(f"Published: {video.publish_time}")
        print(f"Views: {video.views}")
        if video.transcript:
            print(f"Transcript (first 150 chars): {video.transcript[:150]}...")


async def test_recent_videos() -> None:
    """Test getting recent videos without query."""
    print("\n\n=== Test 2: Recent Videos (No Query) ===")
    videos = await youtube_search(
        channels="@indydevdan",
        period_days=7,
        max_videos_per_channel=2,
        get_transcripts=False,
    )

    print(f"Found {len(videos)} videos")
    for video in videos:
        print(f"\nTitle: {video.title}")
        print(f"URL: https://youtube.com{video.url_suffix}")
        print(f"Published: {video.publish_time}")


async def test_transcript_extraction() -> None:
    """Test extracting transcripts from known video IDs."""
    print("\n\n=== Test 3: Direct Transcript Extraction ===")
    # Using a known video ID (Rick Astley - Never Gonna Give You Up)
    transcripts = youtube_transcripts(ids="dQw4w9WgXcQ")

    for t in transcripts:
        print(f"\nVideo ID: {t.id}")
        print(f"URL: https://youtube.com/watch?v={t.id}")
        if t.text:
            print(f"Transcript (first 200 chars): {t.text[:200]}...")
        else:
            print("No transcript available")


async def test_multiple_channels() -> None:
    """Test searching multiple channels."""
    print("\n\n=== Test 4: Multiple Channels ===")
    videos = await youtube_search(
        channels="@indydevdan,@fireship",
        query="AI",
        period_days=14,
        max_videos_per_channel=2,
        get_transcripts=False,
    )

    print(f"Found {len(videos)} videos")
    for video in videos:
        print(f"\n[{video.channel}] {video.title}")
        print(f"URL: https://youtube.com{video.url_suffix}")
        print(f"Published: {video.publish_time}")


async def main() -> None:
    """Run all tests."""
    try:
        await test_channel_search()
        await test_recent_videos()
        await test_transcript_extraction()
        await test_multiple_channels()
        print("\n\n=== All tests completed successfully! ===\n")
    except Exception as e:
        print(f"\n\nError during testing: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
