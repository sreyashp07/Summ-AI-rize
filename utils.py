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


def get_transcript(video_id: str, max_retries: int = 3) -> str:
    """
    Fetch transcript using youtube-transcript-api v1.x with retries
    and language fallbacks. Handles YouTube's new PO-token blocking
    gracefully by retrying and trying multiple language codes.
    """
    languages = ["en", "en-US", "en-GB", "hi", "es"]
    last_error = None

    for attempt in range(max_retries):
        try:
            api = YouTubeTranscriptApi()
            fetched = api.fetch(video_id, languages=languages)

            # v1.x returns an iterable of snippet objects with .text attribute
            text_parts = []
            for snippet in fetched:
                if hasattr(snippet, "text"):
                    text_parts.append(snippet.text)
                elif isinstance(snippet, dict):
                    text_parts.append(snippet.get("text", ""))

            full_text = " ".join(text_parts).strip()
            if not full_text:
                raise Exception("Empty transcript returned from YouTube")
            return full_text

        except Exception as e:
            last_error = e
            error_msg = str(e).lower()

            # Permanent failures - don't retry
            if any(x in error_msg for x in [
                "transcripts disabled",
                "no transcript",
                "video unavailable",
                "not available",
                "no captions",
            ]):
                raise Exception(
                    f"This video has no available captions. ({str(e)})"
                )

            # Retry on transient/blocking errors
            if attempt < max_retries - 1:
                time.sleep(1.5 * (attempt + 1))
                continue

    raise Exception(
        f"Could not fetch transcript after {max_retries} attempts. "
        f"YouTube is likely blocking requests from your IP (PO-token issue). "
        f"Use the 'Paste transcript manually' option below, or try a different video. "
        f"Last error: {str(last_error)}"
    )
