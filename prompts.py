"""Specialized prompt templates for different content types."""

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
State the main mathematical concept, theorem, or problem being discussed.

## 2. Key Equations and Formulas
List every important equation or formula. Format with proper notation. For each, explain what each variable represents.

## 3. Step-by-Step Reasoning
Walk through the logical derivation or argument. For each step:
- WHAT is being done
- WHY it's being done (the underlying reasoning)
- The mathematical transformation involved

## 4. Worked Example / Dry Run
If specific numerical examples are discussed, reproduce them step by step with actual values. Show each calculation clearly.

## 5. Intuition
Explain the intuitive understanding. What does this mean conceptually, beyond just the symbols?

## 6. Common Pitfalls
Mistakes, edge cases, or misconceptions the speaker warned about.

## 7. Applications
Real-world uses or related problems where this technique applies.

DETAILED MATHEMATICAL SUMMARY:"""
