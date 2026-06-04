"""YouTube video summarization using LangChain map-reduce chain."""
from langchain_community.chat_models import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate


class YouTubeSummarizer:
    """Summarize YouTube videos using a local Ollama LLM."""

    def __init__(self, model: str = "llama3.2"):
        self.llm = ChatOllama(temperature=0, model=model)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=1000,
            separators=["\n\n", "\n", " ", ""]
        )

        self.map_prompt = PromptTemplate(
            template=(
                'Summarize the following part of a YouTube video transcript:\n'
                '"{text}"\n\n'
                'KEY POINTS AND TAKEAWAYS:'
            ),
            input_variables=["text"]
        )

        self.combine_prompt = PromptTemplate(
            template=(
                'Create a detailed summary of the YouTube video based on '
                'these transcript summaries:\n"{text}"\n\n'
                'Structure the summary as:\n'
                '1. Main Topic/Theme\n'
                '2. Key Points\n'
                '3. Important Details\n'
                '4. Conclusions/Takeaways\n\n'
                'DETAILED SUMMARY:'
            ),
            input_variables=["text"]
        )

        self.chain = load_summarize_chain(
            llm=self.llm,
            chain_type="map_reduce",
            map_prompt=self.map_prompt,
            combine_prompt=self.combine_prompt,
            verbose=False
        )
