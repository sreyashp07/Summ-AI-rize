"""RAG chatbot with MMR retrieval, query rewriting, and conversational memory."""
import logging
import time
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger("chatbot")


class VideoChatbot:
    """Conversational RAG with MMR retrieval, query rewriting, and history."""

    def __init__(self, transcript: str, model: str = "llama3.2"):
        start = time.time()
        self.llm = ChatOllama(temperature=0.2, model=model)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

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

    def _invoke(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    def _rewrite_query(self, question: str) -> str:
        """Rewrite a follow-up question into a standalone search query."""
        if not self.history:
            return question

        last_q, last_a = self.history[-1]
        rewrite_prompt = (
            "Given the conversation, rewrite the current question into a clear "
            "standalone search query for finding relevant transcript passages. "
            "Output ONLY the rewritten query, nothing else.\n\n"
            f"Previous Q: {last_q}\n"
            f"Previous A: {last_a[:300]}...\n"
            f"Current Q: {question}\n\n"
            "Rewritten search query:"
        )
        try:
            rewritten = self._invoke(rewrite_prompt).strip()
            if 3 <= len(rewritten.split()) <= 30:
                logger.info(f"Query rewritten: '{question}' -> '{rewritten}'")
                return rewritten
        except Exception as e:
            logger.warning(f"Query rewrite failed, using original: {e}")
        return question

    def ask(self, question: str) -> str:
        start = time.time()

        # 1. Rewrite query for better retrieval
        search_query = self._rewrite_query(question)

        # 2. MMR retrieval for diverse, relevant chunks
        relevant_docs = self.vectorstore.max_marginal_relevance_search(
            search_query, k=4, fetch_k=20, lambda_mult=0.5
        )
        context = "\n\n".join(d.page_content for d in relevant_docs)
        logger.info(f"Retrieved {len(relevant_docs)} chunks for query")

        # 3. Build history block
        history_block = ""
        for q, a in self.history[-3:]:
            history_block += f"User: {q}\nAssistant: {a}\n\n"

        # 4. Generate answer
        prompt = (
            "You are a helpful assistant answering questions about a YouTube video. "
            "Use the transcript excerpts below to answer. If the answer is not in the "
            "excerpts, say so clearly. Be concise but thorough.\n\n"
            f"Transcript excerpts:\n{context}\n\n"
            f"{('Previous conversation:' + chr(10) + history_block) if history_block else ''}"
            f"Current question: {question}\n\nAnswer:"
        )
        answer = self._invoke(prompt)

        self.history.append((question, answer))
        elapsed = round(time.time() - start, 2)
        logger.info(f"Answered in {elapsed}s ({len(answer.split())} words)")
        return answer
