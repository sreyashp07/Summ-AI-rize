"""YouTube video summarization using LangChain map-reduce chain."""
from langchain_community.chat_models import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter


class YouTubeSummarizer:
    """Summarize YouTube videos using a local Ollama LLM."""

    def __init__(self, model: str = "llama3.2"):
        self.llm = ChatOllama(temperature=0, model=model)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=1000,
            separators=["\n\n", "\n", " ", ""]
        )
