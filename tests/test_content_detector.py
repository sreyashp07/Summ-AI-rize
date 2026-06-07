"""Unit tests for content_detector.py."""
from content_detector import detect_content_type, get_type_label


def test_returns_valid_type():
    result = detect_content_type("some random short text")
    assert result in ["math", "tutorial", "general"]


def test_empty_defaults_to_general():
    assert detect_content_type("") == "general"


def test_math_heavy_text():
    # Lots of math keywords -> should classify as math
    text = (
        "Today we look at the derivative of a function. The derivative "
        "of x squared is two x. We compute the limit, the integral, and "
        "the matrix product. The theorem states this formula. Proof: "
        "we differentiate the polynomial step by step. The equation "
        "shows the relationship between vectors in linear algebra."
    )
    assert detect_content_type(text) == "math"


def test_tutorial_heavy_text():
    # Lots of code-tutorial keywords -> tutorial
    text = (
        "Let's install python and then import the library. We create a "
        "function and run pip install requests. Import the os module, "
        "then create a class. The framework will compile and the api "
        "endpoint will respond. Run npm install to set up the package. "
        "Debug the error in the terminal command line."
    )
    assert detect_content_type(text) == "tutorial"


def test_general_neutral_text():
    text = (
        "The history of ancient civilizations shows how trade routes "
        "influenced cultural exchange across continents. Many empires "
        "rose and fell over centuries."
    )
    assert detect_content_type(text) == "general"


def test_get_type_label_known():
    assert "Math" in get_type_label("math")
    assert "Tutorial" in get_type_label("tutorial")


def test_get_type_label_unknown_defaults_to_general():
    assert "General" in get_type_label("nonsense")
