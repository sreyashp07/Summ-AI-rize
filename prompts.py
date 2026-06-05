"""Specialized prompt templates for different content types."""

# ==================== MATH ====================

MATH_MAP_PROMPT = """You are analyzing PART of a math/science video transcript. Summarize this section, preserving:
- Any equations or formulas mentioned (write them out clearly)
- The reasoning or logic being explained
- Numerical examples or worked calculations
- Definitions of new terms

Transcript section:
"{text}"

PARTIAL SUMMARY (preserve math content):"""

MATH_COMBINE_PROMPT = """You are creating a comprehensive summary of a math/science YouTube video. Use the partial summaries below to produce a deeply structured summary.

Partial summaries:
"{text}"

Produce a detailed summary with these sections:

## 1. Core Concept
State the main mathematical concept, theorem, or problem.

## 2. Key Equations and Formulas
List every important equation. Format with proper notation. Explain what each variable represents.

## 3. Step-by-Step Reasoning
For each step: WHAT is being done, WHY (the underlying reasoning), and the mathematical transformation.

## 4. Worked Example / Dry Run
Reproduce any numerical examples step by step with actual values.

## 5. Intuition
Explain the conceptual meaning beyond the symbols.

## 6. Common Pitfalls
Mistakes, edge cases, or misconceptions the speaker warned about.

## 7. Applications
Real-world uses or related problems.

DETAILED MATHEMATICAL SUMMARY:"""


# ==================== TUTORIAL ====================

TUTORIAL_MAP_PROMPT = """You are analyzing PART of a coding tutorial transcript. Summarize this section, preserving:
- Tools, libraries, or frameworks mentioned
- Code patterns, commands, or syntax
- Errors and how they were solved
- Configuration steps

Transcript section:
"{text}"

PARTIAL SUMMARY (preserve technical content):"""

TUTORIAL_COMBINE_PROMPT = """You are creating a comprehensive summary of a coding/technical YouTube tutorial. Use the partial summaries below.

Partial summaries:
"{text}"

Produce a detailed summary with these sections:

## 1. What We're Building
Goal of the tutorial, the end result.

## 2. Prerequisites
Tools, libraries, prior knowledge required.

## 3. Setup / Environment
Installation commands, configuration, initial project structure.

## 4. Step-by-Step Walkthrough
Numbered steps. For each:
- What is done
- Why this approach
- Key code patterns, functions, or commands used

## 5. Core Code Concepts
Important libraries, syntax, design patterns introduced.

## 6. Debugging Notes & Pitfalls
Common errors, "gotchas," debugging tips mentioned.

## 7. Final Result & Next Steps
What's built at the end and what could be added or learned next.

DETAILED TUTORIAL SUMMARY:"""


# ==================== GENERAL ====================

GENERAL_MAP_PROMPT = """Summarize this part of a YouTube video transcript, capturing key points, arguments, and important details.

Transcript section:
"{text}"

PARTIAL SUMMARY:"""

GENERAL_COMBINE_PROMPT = """Create a comprehensive summary of the YouTube video from these partial summaries.

Partial summaries:
"{text}"

Produce a detailed summary with these sections:

## 1. Main Topic
Central theme or subject of the video.

## 2. Key Points
The most important points, each with a brief explanation.

## 3. Supporting Details
Examples, statistics, anecdotes, or evidence that back up the key points.

## 4. Reasoning and Arguments
Capture the speaker's logic and how their points connect.

## 5. Notable Statements
Especially impactful or memorable claims.

## 6. Conclusions and Takeaways
Final conclusions, recommendations, or action items for the viewer.

DETAILED SUMMARY:"""


# ==================== DEPTH MODIFIERS ====================

DEPTH_MODIFIERS = {
    "concise": "\n\nIMPORTANT: Keep the summary CONCISE. Target around 200 words total. Be brief but cover all sections.",
    "standard": "\n\nTarget around 500-600 words. Be thorough but focused.",
    "deep": "\n\nIMPORTANT: This is a DEEP-DIVE summary. Be exhaustive. Target 1000+ words. Include all nuances, examples, and reasoning. Do not skip details.",
}


def get_prompts(content_type: str, depth: str = "standard"):
    """Return (map_prompt, combine_prompt) tuned for content type and depth."""
    mapping = {
        "math": (MATH_MAP_PROMPT, MATH_COMBINE_PROMPT),
        "tutorial": (TUTORIAL_MAP_PROMPT, TUTORIAL_COMBINE_PROMPT),
        "general": (GENERAL_MAP_PROMPT, GENERAL_COMBINE_PROMPT),
    }
    map_p, combine_p = mapping.get(content_type, mapping["general"])
    modifier = DEPTH_MODIFIERS.get(depth, DEPTH_MODIFIERS["standard"])
    return map_p, combine_p + modifier
