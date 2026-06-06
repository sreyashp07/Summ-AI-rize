"""RAG chatbot using direct retrieval + LLM call with logging."""
import logging
import time
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger("chatbot")


class VideoChatbot:
    """Conversational RAG with manual retrieval and sliding history."""

    def __init__(self, transcript: str, model: str = "llama3.2"):
        start = time.time()
        self.llm = ChatOllama(temperature=0.2, model=model)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

        # Smaller chunks with sentence-aware separators for precise retrieval
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=120,
            separators=[". ", "? ", "! ", "\n\n", "\n", " ", ""],
            length_function=len,
        )
        docs = splitter.create_documents([transcript])
        logger.info(f"Building FAISS index over {len(docs)} chunks")
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)

        self.history = []
        elapsed = round(time.time() - start, 2)
        logger.info(f"Chatbot ready in {elapsed}s with {len(docs)} chunks")

    def ask(self, question: str) -> str:
        start = time.time()
        relevant_docs = self.vectorstore.similarity_search(question, k=4)
        context = "\n\n".join(d.page_content for d in relevant_docs)
        logger.info(f"Retrieved {len(relevant_docs)} chunks for query")

        history_block = ""
        for q, a in self.history[-3:]:
            history_block += f"User: {q}\nAssistant: {a}\n\n"

        prompt = (
            "You are a helpful assistant answering questions about a YouTube video. "
            "Use the transcript excerpts below to answer. If the answer is not in the "
            "excerpts, say so clearly. Be concise but thorough.\n\n"
            f"Transcript excerpts:\n{context}\n\n"
            f"{('Previous conversation:' + chr(10) + history_block) if history_block else ''}"
            f"Current question: {question}\n\nAnswer:"
        )

        response = self.llm.invoke(prompt)
        answer = response.content if hasattr(response, "content") else str(response)
        self.history.append((question, answer))
        elapsed = round(time.time() - start, 2)
        logger.info(f"Answered in {elapsed}s ({len(answer.split())} words)")
        return answer
