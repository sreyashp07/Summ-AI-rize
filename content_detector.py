"""Detect the type of content in a YouTube transcript to pick the right prompt."""
import re
from typing import Literal

ContentType = Literal["math", "tutorial", "general"]


# Keyword sets with weights
MATH_KEYWORDS = {
    "equation", "theorem", "proof", "derivative", "integral", "matrix",
    "vector", "formula", "calculate", "solve for", "function f", "limit",
    "summation", "differentiation", "polynomial", "logarithm", "exponential",
    "sine", "cosine", "tangent", "probability", "statistics", "calculus",
    "algebra", "geometry", "trigonometry", "factorial", "binomial",
    "linear algebra", "eigenvalue", "determinant", "gradient",
}

TUTORIAL_KEYWORDS = {
    "install", "import ", "function", "variable", "method", "class",
    "library", "package", "npm install", "pip install", "github",
    "repository", "commit", "deploy", "framework", "api", "endpoint",
    "database", "query", "debug", "error", "exception", "syntax",
    "compile", "runtime", "tutorial", "step by step", "code editor",
    "terminal", "command line", "docker", "container",
}


def detect_content_type(transcript: str) -> ContentType:
    """
    Classify a transcript as math/tutorial/general based on keyword frequency.
    Uses lowercase substring matching for robustness.
    """
    text = transcript.lower()
    word_count = max(len(text.split()), 1)

    math_hits = sum(1 for kw in MATH_KEYWORDS if kw in text)
    tutorial_hits = sum(1 for kw in TUTORIAL_KEYWORDS if kw in text)

    # Normalize by transcript length (per 1000 words)
    math_score = (math_hits / word_count) * 1000
    tutorial_score = (tutorial_hits / word_count) * 1000

    # Look for equation-like patterns to boost math score
    equation_patterns = re.findall(r'[a-zA-Z]\s*=\s*[a-zA-Z0-9]', text)
    math_score += len(equation_patterns) * 0.5

    if math_score >= 3 and math_score > tutorial_score:
        return "math"
    if tutorial_score >= 4 and tutorial_score > math_score:
        return "tutorial"
    return "general"


def get_type_label(content_type: ContentType) -> str:
    """Human-readable label for UI display."""
    return {
        "math": "Mathematics / Scientific",
        "tutorial": "Tutorial / Coding",
        "general": "General Content",
    }.get(content_type, "General Content")
