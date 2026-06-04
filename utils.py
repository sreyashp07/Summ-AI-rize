"""Utility functions for URL parsing and transcript fetching."""
import re
from typing import Optional


def extract_video_id(youtube_url: str) -> Optional[str]:
    """Extract the video ID from any common YouTube URL format."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?]*)',
        r'(?:youtube\.com\/shorts\/)([^&\n?]*)'
    ]
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    return None
