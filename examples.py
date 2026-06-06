"""Pre-loaded example transcripts for quick demos."""

EXAMPLES = {
    "(none)": "",
    "Math: Quick intro to derivatives": (
        "Today we're going to talk about derivatives. A derivative measures how a function "
        "changes as its input changes. If we have a function f of x equals x squared, then "
        "the derivative is two x. The way we get this is by taking the limit as h approaches "
        "zero of f of x plus h minus f of x, all divided by h. Let's do a dry run. Take f of "
        "x equals x squared at x equals three. The derivative is two times three, which is six. "
        "That means at x equals three, the function is increasing at a rate of six units per "
        "unit. This concept is foundational for calculus and shows up everywhere in physics, "
        "engineering, and machine learning. Common mistake: forgetting that the derivative of "
        "a constant is zero, not the constant itself."
    ),
    "Tutorial: Setting up a Python project": (
        "In this tutorial we'll set up a Python project from scratch. First, install Python "
        "3.11 from python.org. Then open your terminal and run python dash m venv venv to "
        "create a virtual environment. Activate it with source venv slash bin slash activate "
        "on Mac or Linux, or venv backslash Scripts backslash activate on Windows. Next, "
        "create a requirements dot txt file listing your dependencies, then run pip install "
        "dash r requirements dot txt. A common pitfall is forgetting to activate the venv "
        "before installing packages, which pollutes your global Python install. Always "
        "verify your prompt shows the venv name in parentheses."
    ),
    "General: Why sleep matters": (
        "Sleep is one of the most underrated aspects of human health. Adults need seven to "
        "nine hours of sleep per night for optimal cognitive function. During deep sleep, "
        "the brain clears out metabolic waste through the glymphatic system. Chronic sleep "
        "deprivation is linked to increased risk of heart disease, diabetes, depression, and "
        "even Alzheimer's. The most impactful thing you can do is keep a consistent sleep "
        "schedule, avoid screens for an hour before bed, and keep your room cool and dark. "
        "Caffeine has a half-life of around six hours, so avoid it after lunch if you "
        "struggle to fall asleep. Quality matters more than quantity."
    ),
}


def get_example_names():
    return list(EXAMPLES.keys())


def get_example_text(name: str) -> str:
    return EXAMPLES.get(name, "")
