"""Unit tests for keywords.py."""
from keywords import extract_keywords


def test_basic_extraction():
    text = "python python python javascript javascript java"
    result = extract_keywords(text, top_n=3)
    assert "python" in result
    assert "javascript" in result


def test_returns_list():
    assert isinstance(extract_keywords("hello world example"), list)


def test_empty_input():
    assert extract_keywords("") == []


def test_excludes_stopwords():
    text = "the the the the the cat sat"
    result = extract_keywords(text)
    assert "the" not in result


def test_excludes_short_words():
    text = "ab abc test testing example"
    result = extract_keywords(text)
    assert "ab" not in result
    assert "abc" not in result


def test_top_n_limit():
    text = "apple apple banana cherry date elderberry fig grape"
    result = extract_keywords(text, top_n=2)
    assert len(result) <= 2
    assert "apple" in result  # most frequent


def test_case_insensitive():
    text = "Python python PYTHON Java"
    result = extract_keywords(text, top_n=2)
    assert "python" in result


def test_orders_by_frequency():
    text = "apple " * 10 + "banana " * 5 + "cherry"
    result = extract_keywords(text, top_n=3)
    assert result[0] == "apple"
    assert result[1] == "banana"
