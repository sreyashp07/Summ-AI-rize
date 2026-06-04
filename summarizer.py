"""YouTube video summarization using direct LLM calls (no legacy chains)."""
from langchain_community.chat_models import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import extract_video_id, get_transcript


class YouTubeSummarizer:
    """Map-reduce summarization without load_summarize_chain."""

    def __init__(self, model: str = "llama3.2"):
        self.llm = ChatOllama(temperature=0, model=model)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=1000,
            separators=["\n\n", "\n", " ", ""],
        )
        self.map_prompt = (
            'Summarize the following part of a YouTube video transcript. '
            'Focus on key points and takeaways:\n\n'
            '"{text}"\n\nSUMMARY:'
        )
        self.combine_prompt = (
            'Create a detailed summary of the YouTube video based on these '
            'partial summaries:\n\n"{text}"\n\n'
            'Structure the summary as:\n'
            '1. Main Topic/Theme\n'
            '2. Key Points\n'
            '3. Important Details\n'
            '4. Conclusions/Takeaways\n\n'
            'DETAILED SUMMARY:'
        )

    def _invoke(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    def _summarize_chunk(self, chunk: str) -> str:
        return self._invoke(self.map_prompt.format(text=chunk))

    def _combine(self, summaries: list) -> str:
        combined = "\n\n".join(summaries)
        return self._invoke(self.combine_prompt.format(text=combined))

    def summarize_text(self, transcript: str) -> str:
        """Summarize a transcript string directly (used by both URL and paste modes)."""
        chunks = self.text_splitter.split_text(transcript)
        if not chunks:
            raise Exception("Transcript is empty.")
        if len(chunks) == 1:
            return self._summarize_chunk(chunks[0])
        partials = [self._summarize_chunk(c) for c in chunks]
        return self._combine(partials)

    def summarize_video(self, youtube_url: str) -> dict:
        try:
            video_id = extract_video_id(youtube_url)
            if not video_id:
                return {"status": "error", "message": "Invalid YouTube URL"}
            transcript = get_transcript(video_id)
            summary = self.summarize_text(transcript)
            return {
                "status": "success",
                "summary": summary,
                "video_id": video_id,
                "transcript": transcript,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
