"""YouTube video summarization with content-aware prompting and depth control."""
from langchain_community.chat_models import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import extract_video_id, get_transcript
from content_detector import detect_content_type, get_type_label
from prompts import get_prompts


class YouTubeSummarizer:
    """Map-reduce summarization that adapts to content type and depth."""

    def __init__(self, model: str = "llama3.2", depth: str = "standard"):
        self.llm = ChatOllama(temperature=0, model=model)
        self.depth = depth
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=1000,
            separators=["\n\n", "\n", " ", ""],
        )

    def _invoke(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    def _summarize_chunk(self, chunk: str, map_prompt: str) -> str:
        return self._invoke(map_prompt.format(text=chunk))

    def _combine(self, summaries: list, combine_prompt: str) -> str:
        combined = "\n\n".join(summaries)
        return self._invoke(combine_prompt.format(text=combined))

    def summarize_text(self, transcript: str) -> dict:
        """Summarize a transcript. Returns dict with summary, type label, and stats."""
        if not transcript or not transcript.strip():
            raise Exception("Transcript is empty.")

        content_type = detect_content_type(transcript)
        type_label = get_type_label(content_type)
        map_prompt, combine_prompt = get_prompts(content_type, self.depth)

        chunks = self.text_splitter.split_text(transcript)
        if len(chunks) == 1:
            summary = self._summarize_chunk(chunks[0], map_prompt)
        else:
            partials = [self._summarize_chunk(c, map_prompt) for c in chunks]
            summary = self._combine(partials, combine_prompt)

        return {
            "summary": summary,
            "content_type": content_type,
            "type_label": type_label,
            "chunks_processed": len(chunks),
            "transcript_words": len(transcript.split()),
        }

    def summarize_video(self, youtube_url: str) -> dict:
        try:
            video_id = extract_video_id(youtube_url)
            if not video_id:
                return {"status": "error", "message": "Invalid YouTube URL"}
            transcript = get_transcript(video_id)
            result = self.summarize_text(transcript)
            return {
                "status": "success",
                "summary": result["summary"],
                "content_type": result["content_type"],
                "type_label": result["type_label"],
                "chunks_processed": result["chunks_processed"],
                "transcript_words": result["transcript_words"],
                "video_id": video_id,
                "transcript": transcript,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
