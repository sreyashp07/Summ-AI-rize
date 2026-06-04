"""YouTube video summarization using LangChain map-reduce chain."""
from langchain_community.chat_models import ChatOllama


class YouTubeSummarizer:
    """Summarize YouTube videos using a local Ollama LLM."""

    def __init__(self, model: str = "llama3.2"):
        self.llm = ChatOllama(temperature=0, model=model)
