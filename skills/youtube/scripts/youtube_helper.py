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
"""YouTube search and transcript extraction helper.

Searches YouTube channels for videos and extracts transcripts.
"""

import asyncio
import json
import logging
import time
import urllib.parse
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

import dateparser  # pylint: disable=import-error
from aiohttp import ClientSession
from munch import munchify  # pylint: disable=import-error
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi  # pylint: disable=import-error

# Configure logging to youtube_helper.log
log_dir = Path.home() / ".claude" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "youtube_helper.log"

log = logging.getLogger("youtube_helper")
log.setLevel(logging.INFO)
if not any(isinstance(handler, RotatingFileHandler) for handler in log.handlers):
    handler = RotatingFileHandler(
        str(log_file),
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [youtube_helper] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    log.addHandler(handler)


class Transcript(BaseModel):
    """Transcript model."""

    text: str
    start: int
    duration: int


class VideoTranscript(BaseModel):
    """Video transcript model."""

    id: str
    text: str


class Video(BaseModel):
    """Video model."""

    id: str
    title: str
    short_desc: str
    channel: str
    duration: str
    views: str
    publish_time: str
    url_suffix: str
    long_desc: str | None = None
    transcript: str | None = None


def _get_since_date(period_days: int, end_date: str) -> tuple[str, str, str]:
    """Calculate start date from period and end date."""
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d")
    else:
        end = datetime.now()

    start = end - timedelta(days=period_days)
    return (
        str(start.year),
        str(start.month).zfill(2),
        str(start.day).zfill(2),
    )


def _parse_html_list(html: str, max_results: int) -> list[Video]:
    """Parse YouTube search results HTML."""
    results: list[Video] = []
    if "ytInitialData" not in html:
        return []
    start = html.index("ytInitialData") + len("ytInitialData") + 3
    end = html.index("};", start) + 1
    json_str = html[start:end]
    data = json.loads(json_str)
    if "twoColumnBrowseResultsRenderer" not in data["contents"]:
        return []
    tab = None
    for tab in data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]:
        if "expandableTabRenderer" in tab:
            break
    if tab is None:
        return []
    for contents in tab["expandableTabRenderer"]["content"]["sectionListRenderer"]["contents"]:
        if "itemSectionRenderer" in contents:
            for video in contents["itemSectionRenderer"]["contents"]:
                if "videoRenderer" not in video:
                    continue

                res: dict[str, str | list[str] | int | None] = {}
                video_data = video.get("videoRenderer", {})
                res["id"] = video_data.get("videoId", None)
                res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", "")
                res["short_desc"] = video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", "")
                res["channel"] = video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None)
                res["duration"] = video_data.get("lengthText", {}).get("simpleText", "")
                res["views"] = video_data.get("viewCountText", {}).get("simpleText", "")
                res["publish_time"] = video_data.get("publishedTimeText", {}).get(
                    "simpleText",
                    "",
                )
                res["url_suffix"] = (
                    video_data.get("navigationEndpoint", {})
                    .get("commandMetadata", {})
                    .get("webCommandMetadata", {})
                    .get("url", "")
                )
                results.append(Video(**res))
                if len(results) >= int(max_results):
                    break
        if len(results) >= int(max_results):
            break

    return results


def _parse_html_video(html: str) -> dict[str, str]:
    """Parse video page HTML to extract description."""
    result: dict[str, str] = {"long_desc": None}
    start = html.index("ytInitialData") + len("ytInitialData") + 3
    end = html.index("};", start) + 1
    json_str = html[start:end]
    data = json.loads(json_str)
    obj = munchify(data)
    try:
        result["long_desc"] = obj.contents.twoColumnWatchNextResults.results.results.contents[
            1
        ].videoSecondaryInfoRenderer.attributedDescription.content
    except (AttributeError, KeyError, IndexError, TypeError):
        log.warning("YouTube HTML structure changed, could not extract long description")
    return result


def _build_youtube_search_url(query: str | None, period_days: int, end_date: str) -> str:
    """Build YouTube search query URL with date filters."""
    year, month, day = _get_since_date(period_days, end_date)
    query_str = f"{query} " if query else ""
    before = f"{' ' if query else ''}before:{end_date} " if end_date else ""
    return urllib.parse.quote_plus(f"{query_str}{before}after:{year}-{month}-{day}")


def _filter_channels(channels: list[str]) -> list[str]:
    """Validate and normalize channel handles."""
    return [ch for ch in channels if ch and ch.lower() != "n/a"]


def _create_channel_tasks(
    channels_arr: list[str],
    encoded_search: str,
    max_videos_per_channel: int,
    get_descriptions: bool,
    get_transcripts: bool,
) -> list[Any]:
    """Create async tasks for fetching videos from each channel."""
    tasks = []
    for channel in channels_arr:
        if channel == "n/a":
            continue
        url = f"https://www.youtube.com/{channel}/search?hl=en&query={encoded_search}"
        tasks.append(
            _get_channel_videos(
                channel=channel,
                url=url,
                max_videos_per_channel=max_videos_per_channel,
                get_descriptions=get_descriptions,
                get_transcripts=get_transcripts,
            )
        )
    return tasks


def _process_video_results(results: list[list[Video]], query: str | None, char_cap: int | None) -> list[Video]:
    """Process and sort video results."""
    res: list[Video] = []
    for videos in results:
        if not query:
            videos.sort(key=_sort_by_publish_time)
            videos = videos[::-1]
        res.extend(videos)
    if char_cap:
        res = _filter_by_char_cap(res, char_cap)
    return res


async def youtube_search(
    channels: str,
    end_date: str = "",
    query: str | None = None,
    period_days: int = 3,
    max_videos_per_channel: int = 3,
    get_descriptions: bool = False,
    get_transcripts: bool = True,
    char_cap: int | None = None,
) -> list[Video]:
    """Search YouTube channels for videos with optional transcript extraction.

    Args:
        channels: Comma-separated list of channel handles (e.g., "@indydevdan,@someotherchannel")
        end_date: End date in YYYY-MM-DD format (defaults to today)
        query: Search query within channel
        period_days: Number of days back to search
        max_videos_per_channel: Maximum videos to return per channel
        get_descriptions: Extract full video descriptions
        get_transcripts: Extract video transcripts
        char_cap: Maximum total characters in results (for LLM context management)

    Returns:
        List of Video objects with metadata and optional transcripts
    """
    if not channels:
        raise ValueError("No channels specified")

    channels_arr = _filter_channels(["@" + channel.replace("@", "") for channel in channels.lower().split(",")])
    if len(channels_arr) == 0:
        return []

    log.debug(
        "Searching channels: %s, query: %s, period_days: %s, end_date: %s, max_videos_per_channel: %s",
        channels_arr,
        query,
        period_days,
        end_date,
        max_videos_per_channel,
    )

    encoded_search = _build_youtube_search_url(query, period_days, end_date)
    tasks = _create_channel_tasks(
        channels_arr,
        encoded_search,
        max_videos_per_channel,
        get_descriptions,
        get_transcripts,
    )

    try:
        results = await asyncio.gather(*tasks)
    except Exception as e:
        log.error("Error searching YouTube: %s", e, exc_info=True)
        raise

    return _process_video_results(results, query, char_cap)


def _filter_by_char_cap(videos: list[Video], char_cap: int) -> list[Video]:
    """Filter videos to fit within character cap by removing longest transcripts."""
    if char_cap is None:
        return videos
    while len(json.dumps([vid.model_dump_json() for vid in videos])) > char_cap:
        transcript_lengths = [len(video.transcript) for video in videos]
        max_index = transcript_lengths.index(max(transcript_lengths))
        videos.pop(max_index)
    return videos


def _sort_by_publish_time(video: Video) -> float:
    """Sort key function for videos by publish time."""
    now = datetime.now()
    d = dateparser.parse(
        video.publish_time.replace("Streamed ", ""),
        settings={"RELATIVE_BASE": now},
    )
    return time.mktime(d.timetuple())


def youtube_transcripts(ids: str) -> list[VideoTranscript]:
    """Extract transcripts from comma-separated video IDs.

    Args:
        ids: Comma-separated YouTube video IDs

    Returns:
        List of VideoTranscript objects
    """
    results: list[VideoTranscript] = []
    for video_id in ids.split(","):
        transcript = _get_video_transcript(video_id)
        results.append(VideoTranscript(id=video_id, text=transcript))
    return results


async def _get_channel_videos(
    channel: str,
    url: str,
    max_videos_per_channel: int,
    get_descriptions: bool,
    get_transcripts: bool,
) -> list[Video]:
    """Fetch and parse videos from a channel search page."""
    # Cookie to bypass YouTube consent page
    async with ClientSession() as session:
        response = await session.get(
            url,
            headers={"Cookie": "SOCS=CAESEwgDEgk0ODE3Nzk3MjQaAmVuIAEaBgiA_LyaBg"},
        )
        if response.status != 200:
            raise RuntimeError(
                f'Failed to fetch videos for channel "{channel}". '
                f"The handle is probably incorrect. Status: {response.status}"
            )
        html = await response.text()
        videos = _parse_html_list(html, max_results=max_videos_per_channel)
        for video in videos:
            if get_descriptions:
                video_info = await _get_video_info(session, video.id)
                video.long_desc = video_info.get("long_desc")
            if get_transcripts:
                transcript = _get_video_transcript(video.id)
                video.transcript = transcript
        return videos


async def _get_video_info(session: ClientSession, video_id: str) -> dict[str, str]:
    """Fetch video page to extract full description."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    response = await session.get(
        url,
        headers={"Cookie": "SOCS=CAESEwgDEgk0ODE3Nzk3MjQaAmVuIAEaBgiA_LyaBg"},
    )
    html = await response.text()
    return _parse_html_video(html)


def _get_video_transcript(video_id: str, strip_timestamps: bool = False) -> str:
    """Extract transcript from YouTube video using youtube-transcript-api.

    Args:
        video_id: YouTube video ID
        strip_timestamps: If True, remove timestamp markers

    Returns:
        Transcript text with or without timestamps
    """
    ytt_api = YouTubeTranscriptApi()
    try:
        transcripts = ytt_api.fetch(video_id, preserve_formatting=True)
        return " ".join(
            [
                (
                    "[" + str(t["start"]).split(".", maxsplit=1)[0] + "s] " + t["text"]
                    if not strip_timestamps
                    else t["text"]
                )
                for t in transcripts.to_raw_data()
            ],
        )
    except (KeyError, AttributeError, ValueError, ConnectionError, TimeoutError) as e:
        log.warning("Could not fetch transcript for %s: %s", video_id, e)
        return ""


async def main() -> None:
    """Example usage."""
    # Example: Search @indydevdan for multi-agent videos in last 30 days
    videos = await youtube_search(
        channels="@indydevdan",
        query="multi-agent orchestration",
        period_days=30,
        max_videos_per_channel=5,
        get_transcripts=True,
    )

    for video in videos:
        print(f"\nTitle: {video.title}")
        print(f"URL: https://youtube.com{video.url_suffix}")
        print(f"Published: {video.publish_time}")
        if video.transcript:
            print(f"Transcript (first 200 chars): {video.transcript[:200]}...")


if __name__ == "__main__":
    asyncio.run(main())
