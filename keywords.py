"""Simple keyword extraction using term frequency with stopword filtering."""
import re
from collections import Counter
from typing import List


STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "of", "to", "in", "on", "at",
    "for", "with", "by", "from", "up", "as", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "can", "this", "that", "these", "those",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
    "my", "your", "his", "its", "our", "their", "what", "which", "who", "whom",
    "where", "when", "why", "how", "all", "any", "both", "each", "few", "more",
    "most", "other", "some", "such", "no", "not", "only", "own", "same", "so",
    "than", "too", "very", "just", "really", "actually", "basically", "literally",
    "kind", "sort", "thing", "things", "stuff", "going", "gonna", "got", "get",
    "gets", "getting", "say", "said", "says", "saying", "like", "see", "look",
    "know", "think", "thought", "want", "need", "make", "made", "way", "lot",
    "okay", "ok", "yeah", "yes", "right", "well", "now", "then", "here",
    "there", "also", "even", "still", "back", "first", "two", "one", "about",
    "into", "out", "over", "again", "down", "off", "after", "before", "while",
}


def extract_keywords(text: str, top_n: int = 8) -> List[str]:
    """Extract top N keywords by lowercase term frequency, filtered."""
    if not text:
        return []
    words = re.findall(r"[a-zA-Z][a-zA-Z'-]{2,}", text.lower())
    filtered = [w for w in words if w not in STOPWORDS and len(w) >= 4]
    counter = Counter(filtered)
    return [word for word, _ in counter.most_common(top_n)]
