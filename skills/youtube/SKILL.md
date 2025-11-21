---
name: YouTube Search & Transcripts
description: Search YouTube channels for videos and extract transcripts. Use when user asks to find YouTube videos, get video transcripts, search specific channels, analyze YouTube content by topic or date range, or needs video URLs and content for research.
---

# YouTube Search & Transcripts

Search YouTube channels for videos matching specific queries or date ranges, and extract full transcripts with timestamps for analysis.

## Instructions

### Prerequisites

The helper script uses **PEP 723 inline dependencies** - no separate requirements.txt needed. Dependencies are declared in the script header and auto-install when you run with `uv`:

- `youtube-transcript-api` - Extract transcripts from YouTube videos
- `aiohttp` - Async HTTP client for parallel channel searches
- `dateparser` - Parse relative and absolute dates
- `munch` - Dot-notation access to dicts (for HTML parsing)
- `pydantic` - Data validation and models

### Workflow

**1. Understand the Query**

Identify what the user needs:
- Specific channel(s) to search (e.g., "@indydevdan")
- Search query/keywords (e.g., "multi-agent orchestration")
- Time period (e.g., "last 30 days", "this year", specific date range)
- What to extract: just URLs, metadata, transcripts, or full descriptions

**2. Run the Search**

Use the `youtube_helper.py` script with appropriate parameters:

```python
from skills.youtube.scripts.youtube_helper import youtube_search
import asyncio

videos = await youtube_search(
    channels="@channelhandle",           # Required: comma-separated handles
    query="search terms",                # Optional: keywords to search
    period_days=30,                      # Optional: days back to search (default: 3)
    end_date="2025-11-17",              # Optional: YYYY-MM-DD end date (default: today)
    max_videos_per_channel=5,           # Optional: videos per channel (default: 3)
    get_descriptions=False,              # Optional: extract full descriptions (default: False)
    get_transcripts=True,                # Optional: extract transcripts (default: True)
    char_cap=50000,                      # Optional: max total chars for LLM context
)
```

**3. Extract Transcripts from Video IDs**

If you already have video IDs and just need transcripts:

```python
from skills.youtube.scripts.youtube_helper import youtube_transcripts

transcripts = youtube_transcripts(ids="video_id1,video_id2,video_id3")
```

**4. Process Results**

Each `Video` object contains:
- `id` - YouTube video ID
- `title` - Video title
- `short_desc` - Short description from search results
- `long_desc` - Full description (if `get_descriptions=True`)
- `channel` - Channel name
- `duration` - Video duration (e.g., "12:34")
- `views` - View count (e.g., "1.2K views")
- `publish_time` - Relative publish time (e.g., "2 weeks ago")
- `url_suffix` - URL path (prefix with `https://youtube.com`)
- `transcript` - Full transcript with timestamps (if `get_transcripts=True`)

**5. Answer the Question**

Analyze the transcripts and metadata to answer the user's question:
- Search for specific topics/keywords in transcripts
- Find first mentions of concepts
- Summarize video content
- Extract relevant quotes with timestamps

### Technical Details

**How It Works:**
- **No API required** - Parses YouTube HTML directly to bypass rate limits
- **Parallel searches** - Uses asyncio to search multiple channels simultaneously
- **Timestamp preservation** - Transcripts include `[123s]` markers for reference
- **Smart filtering** - Character cap removes longest transcripts first to fit LLM context
- **Date filtering** - Uses YouTube's native `after:YYYY-MM-DD` and `before:YYYY-MM-DD` syntax

**Logging:**
All activity is logged to `~/.claude/logs/youtube_helper.log` for debugging.

**Channel Handles:**
- Always use `@` prefix (e.g., `@indydevdan`)
- Multiple channels: comma-separated (e.g., `@channel1,@channel2`)
- Invalid handles will raise `RuntimeError`

**Limitations:**
- HTML parsing may break if YouTube changes page structure
- Transcripts only available for videos with captions (auto or manual)
- Search limited to channel-level searches (not global YouTube search)

## Examples

### Example 1: Find First Mention of a Topic

**User Query:** "Get me @indydevdan's video URLs where he talks about multi-agent orchestration for the first time"

**Approach:**
1. Search the channel with query "multi-agent orchestration"
2. Search a broad time period (e.g., last 365 days)
3. Get transcripts for all matching videos
4. Analyze timestamps to find earliest mentions
5. Return video URLs with context

```python
import asyncio
from skills.youtube.scripts.youtube_helper import youtube_search

videos = await youtube_search(
    channels="@indydevdan",
    query="multi-agent orchestration",
    period_days=365,
    max_videos_per_channel=10,
    get_transcripts=True,
)

# Sort by publish date to find earliest
videos.sort(key=lambda v: v.publish_time)

for video in videos:
    if "multi-agent" in video.transcript.lower():
        print(f"Title: {video.title}")
        print(f"URL: https://youtube.com{video.url_suffix}")
        print(f"Published: {video.publish_time}")
        # Find first mention in transcript
        for line in video.transcript.split("["):
            if "multi-agent" in line.lower():
                print(f"First mention: {line[:200]}...")
                break
```

### Example 2: Recent Videos from Multiple Channels

**User Query:** "What have @indydevdan and @swyx posted about AI agents in the last week?"

```python
import asyncio
from skills.youtube.scripts.youtube_helper import youtube_search

videos = await youtube_search(
    channels="@indydevdan,@swyx",
    query="AI agents",
    period_days=7,
    max_videos_per_channel=5,
    get_transcripts=True,
)

for video in videos:
    print(f"\n[{video.channel}] {video.title}")
    print(f"URL: https://youtube.com{video.url_suffix}")
    print(f"Views: {video.views} | Published: {video.publish_time}")
    if video.transcript:
        print(f"Transcript preview: {video.transcript[:300]}...")
```

### Example 3: Get Transcripts from Specific Video IDs

**User Query:** "Get me the transcripts for these videos: dQw4w9WgXcQ, jNQXAC9IVRw"

```python
from skills.youtube.scripts.youtube_helper import youtube_transcripts

transcripts = youtube_transcripts(ids="dQw4w9WgXcQ,jNQXAC9IVRw")

for t in transcripts:
    print(f"\nVideo ID: {t.id}")
    print(f"URL: https://youtube.com/watch?v={t.id}")
    print(f"Transcript:\n{t.text}")
```

### Example 4: Deep Analysis with Full Descriptions

**User Query:** "Find @channelname's videos about Python testing from the last 3 months and summarize the key points"

```python
import asyncio
from skills.youtube.scripts.youtube_helper import youtube_search

videos = await youtube_search(
    channels="@channelname",
    query="Python testing",
    period_days=90,
    max_videos_per_channel=10,
    get_descriptions=True,  # Get full descriptions too
    get_transcripts=True,
    char_cap=100000,  # Limit total context to 100k chars
)

# Now analyze videos:
# - video.long_desc contains full description
# - video.transcript contains full transcript with timestamps
# - Use LLM to extract key testing strategies, tools mentioned, etc.
```

## Supporting Files

- [youtube_helper.py](scripts/youtube_helper.py) - Main search and transcript extraction script

## Tips

1. **Start broad, then narrow**: If unsure about date range, start with 30-90 days
2. **Use char_cap for large queries**: Prevent context overflow when searching multiple channels
3. **Check transcript availability**: Not all videos have transcripts - the script returns empty string if unavailable
4. **Timestamps are useful**: Use `[123s]` markers to reference specific moments in videos
5. **Parallel searches are fast**: Multiple channels searched simultaneously via asyncio
