"""RAG chatbot for chatting with the video transcript."""
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


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

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
        )

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=False,
        )

    def ask(self, question: str) -> str:
        """Ask a question; chain handles retrieval + memory."""
        result = self.chain.invoke({"question": question})
        return result["answer"]
