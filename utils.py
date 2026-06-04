"""Utility functions for URL parsing and transcript fetching."""
import re
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi


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


def get_transcript(video_id: str) -> str:
    """Fetch the full transcript of a YouTube video as a single string."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript_list])
    except Exception as e:
        raise Exception(f"Error getting transcript: {str(e)}")
