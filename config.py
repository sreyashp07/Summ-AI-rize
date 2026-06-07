"""Centralized configuration loaded from environment variables with sensible defaults.

To override any setting, create a .env file in the project root or set the
environment variable before running the app.
"""
import os

# Try to load .env if python-dotenv is available (installed transitively via pydantic-settings)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ===== LLM Configuration =====
LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.2")
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0"))
CHAT_TEMPERATURE: float = float(os.getenv("CHAT_TEMPERATURE", "0.2"))

# ===== Chunking Configuration =====
SUMMARY_CHUNK_SIZE: int = int(os.getenv("SUMMARY_CHUNK_SIZE", "10000"))
SUMMARY_CHUNK_OVERLAP: int = int(os.getenv("SUMMARY_CHUNK_OVERLAP", "1000"))
CHAT_CHUNK_SIZE: int = int(os.getenv("CHAT_CHUNK_SIZE", "600"))
CHAT_CHUNK_OVERLAP: int = int(os.getenv("CHAT_CHUNK_OVERLAP", "120"))

# ===== Retrieval Configuration (MMR) =====
RETRIEVAL_K: int = int(os.getenv("RETRIEVAL_K", "4"))
RETRIEVAL_FETCH_K: int = int(os.getenv("RETRIEVAL_FETCH_K", "20"))
RETRIEVAL_LAMBDA: float = float(os.getenv("RETRIEVAL_LAMBDA", "0.5"))

# ===== App Defaults =====
DEFAULT_DEPTH: str = os.getenv("DEFAULT_DEPTH", "standard")
TRANSCRIPT_FETCH_RETRIES: int = int(os.getenv("TRANSCRIPT_FETCH_RETRIES", "3"))


def get_all() -> dict:
    """Return all config values as a dict (useful for debugging)."""
    return {
        "LLM_MODEL": LLM_MODEL,
        "EMBEDDING_MODEL": EMBEDDING_MODEL,
        "LLM_TEMPERATURE": LLM_TEMPERATURE,
        "CHAT_TEMPERATURE": CHAT_TEMPERATURE,
        "SUMMARY_CHUNK_SIZE": SUMMARY_CHUNK_SIZE,
        "SUMMARY_CHUNK_OVERLAP": SUMMARY_CHUNK_OVERLAP,
        "CHAT_CHUNK_SIZE": CHAT_CHUNK_SIZE,
        "CHAT_CHUNK_OVERLAP": CHAT_CHUNK_OVERLAP,
        "RETRIEVAL_K": RETRIEVAL_K,
        "RETRIEVAL_FETCH_K": RETRIEVAL_FETCH_K,
        "RETRIEVAL_LAMBDA": RETRIEVAL_LAMBDA,
        "DEFAULT_DEPTH": DEFAULT_DEPTH,
        "TRANSCRIPT_FETCH_RETRIES": TRANSCRIPT_FETCH_RETRIES,
    }
