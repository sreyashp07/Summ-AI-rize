"""Unit tests for utils.py."""
from utils import extract_video_id, clean_transcript


# ----- extract_video_id -----

def test_extract_standard_url():
    assert extract_video_id("https://www.youtube.com/watch?v=abc123XYZ") == "abc123XYZ"


def test_extract_short_url():
    assert extract_video_id("https://youtu.be/abc123XYZ") == "abc123XYZ"


def test_extract_embed_url():
    assert extract_video_id("https://www.youtube.com/embed/abc123XYZ") == "abc123XYZ"


def test_extract_shorts_url():
    assert extract_video_id("https://youtube.com/shorts/abc123XYZ") == "abc123XYZ"


def test_extract_url_with_params():
    assert extract_video_id("https://www.youtube.com/watch?v=abc123&t=42") == "abc123"


def test_extract_invalid_url():
    assert extract_video_id("https://example.com/video") is None


def test_extract_empty_string():
    assert extract_video_id("") is None


# ----- clean_transcript -----

def test_remove_bracketed_annotations():
    result = clean_transcript("hello [Music] world")
    assert "[Music]" not in result
    assert "hello" in result and "world" in result


def test_remove_multiple_brackets():
    result = clean_transcript("[Music] hello [Applause] world [Laughter]")
    assert "[" not in result and "]" not in result


def test_remove_timestamps():
    result = clean_transcript("at 1:23 we see this and 12:34:56 later")
    assert "1:23" not in result
    assert "12:34:56" not in result


def test_collapse_repeated_words():
    result = clean_transcript("the the the the cat sat")
    assert result.count("the") == 1


def test_normalize_whitespace():
    result = clean_transcript("hello    world\n\n\nfoo\t\tbar")
    assert "  " not in result


def test_empty_input():
    assert clean_transcript("") == ""


def test_preserves_normal_text():
    result = clean_transcript("This is a normal sentence about machine learning.")
    assert "normal sentence" in result
    assert "machine learning" in result
