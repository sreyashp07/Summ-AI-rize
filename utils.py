"""Utility functions for URL parsing and transcript fetching."""
import re
import time
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(youtube_url: str) -> Optional[str]:
    """Extract the video ID from any common YouTube URL format."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?]*)',
        r'(?:youtube\.com\/shorts\/)([^&\n?]*)',
    ]
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    return None


def _extract_text(fetched) -> str:
    """Convert any transcript return type into a single text string."""
    parts = []
    for item in fetched:
        if hasattr(item, "text"):
            parts.append(item.text)
        elif isinstance(item, dict) and "text" in item:
            parts.append(item["text"])
    return " ".join(parts).strip()


def get_transcript(video_id: str, max_retries: int = 3) -> str:
    """
    Fetch transcript using multiple API strategies for compatibility
    across youtube-transcript-api versions, with retries.
    """
    languages = ["en", "en-US", "en-GB", "hi", "es"]
    last_error = None

    for attempt in range(max_retries):
        # Strategy 1: New v1.x instance .fetch() method
        try:
            api = YouTubeTranscriptApi()
            if hasattr(api, "fetch"):
                fetched = api.fetch(video_id, languages=languages)
                text = _extract_text(fetched)
                if text:
                    return text
        except Exception as e:
            last_error = e

        # Strategy 2: Old static get_transcript() method
        try:
            if hasattr(YouTubeTranscriptApi, "get_transcript"):
                fetched = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
                text = _extract_text(fetched)
                if text:
                    return text
        except Exception as e:
            last_error = e

        # Strategy 3: list_transcripts + find_transcript + fetch
        try:
            if hasattr(YouTubeTranscriptApi, "list_transcripts"):
                ts_list = YouTubeTranscriptApi.list_transcripts(video_id)
                ts = ts_list.find_transcript(languages)
                fetched = ts.fetch()
                text = _extract_text(fetched)
                if text:
                    return text
        except Exception as e:
            last_error = e

        if attempt < max_retries - 1:
            time.sleep(1.5 * (attempt + 1))

    raise Exception(
        f"Could not fetch transcript. YouTube is likely blocking your IP "
        f"(PO-token issue affecting most users in 2026). "
        f"Use 'Paste transcript manually' mode instead. "
        f"Last error: {str(last_error)}"
    )
