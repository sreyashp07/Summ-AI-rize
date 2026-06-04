"""RAG chatbot for chatting with the video transcript."""
from langchain_community.chat_models import ChatOllama


class VideoChatbot:
    """Conversational RAG over a YouTube transcript."""

    def __init__(self, transcript: str, model: str = "llama3.2"):
        self.transcript = transcript
        self.llm = ChatOllama(temperature=0.2, model=model)
