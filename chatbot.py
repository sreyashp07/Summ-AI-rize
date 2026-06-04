"""RAG chatbot using direct retrieval + LLM call (no legacy chains)."""
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


class VideoChatbot:
    """Conversational RAG with manual retrieval and a sliding history window."""

    def __init__(self, transcript: str, model: str = "llama3.2"):
        self.llm = ChatOllama(temperature=0.2, model=model)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = splitter.create_documents([transcript])
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)

        self.history = []  # list of (question, answer) tuples

    def ask(self, question: str) -> str:
        # Retrieve relevant transcript chunks
        relevant_docs = self.vectorstore.similarity_search(question, k=4)
        context = "\n\n".join(d.page_content for d in relevant_docs)

        # Build a short history window
        history_block = ""
        for q, a in self.history[-3:]:
            history_block += f"User: {q}\nAssistant: {a}\n\n"

        prompt = (
            "You are a helpful assistant answering questions about a YouTube video. "
            "Use the transcript excerpts below to answer. If the answer is not in the "
            "excerpts, say so clearly.\n\n"
            f"Transcript excerpts:\n{context}\n\n"
            f"{('Previous conversation:' + chr(10) + history_block) if history_block else ''}"
            f"Current question: {question}\n\nAnswer:"
        )

        response = self.llm.invoke(prompt)
        answer = response.content if hasattr(response, "content") else str(response)
        self.history.append((question, answer))
        return answer
