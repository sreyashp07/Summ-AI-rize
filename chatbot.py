"""RAG chatbot for chatting with the video transcript."""
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


class VideoChatbot:
    """Conversational RAG over a YouTube transcript."""

    def __init__(self, transcript: str, model: str = "llama3.2"):
        self.transcript = transcript
        self.llm = ChatOllama(temperature=0.2, model=model)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
        )
        docs = splitter.create_documents([transcript])
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
