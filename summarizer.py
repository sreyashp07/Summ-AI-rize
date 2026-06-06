"""YouTube video summarization with content-aware prompting, depth control, and timing."""
import time
import logging
from langchain_community.chat_models import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import extract_video_id, get_transcript
from content_detector import detect_content_type, get_type_label
from prompts import get_prompts

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("summarizer")


class YouTubeSummarizer:
    """Map-reduce summarization with content awareness, depth control, and timing."""

    def __init__(self, model: str = "llama3.2", depth: str = "standard"):
        self.llm = ChatOllama(temperature=0, model=model)
        self.depth = depth
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=1000,
            separators=["\n\n", "\n", " ", ""],
        )
        logger.info(f"Initialized summarizer with model={model}, depth={depth}")

    def _invoke(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    def _summarize_chunk(self, chunk: str, map_prompt: str) -> str:
        return self._invoke(map_prompt.format(text=chunk))

    def _combine(self, summaries: list, combine_prompt: str) -> str:
        combined = "\n\n".join(summaries)
        return self._invoke(combine_prompt.format(text=combined))

    def summarize_text(self, transcript: str) -> dict:
        if not transcript or not transcript.strip():
            raise Exception("Transcript is empty.")
        from utils import clean_transcript
        transcript = clean_transcript(transcript)

        start_time = time.time()

        content_type = detect_content_type(transcript)
        type_label = get_type_label(content_type)
        logger.info(f"Detected content type: {content_type} ({type_label})")

        map_prompt, combine_prompt = get_prompts(content_type, self.depth)
        chunks = self.text_splitter.split_text(transcript)
        logger.info(f"Split transcript into {len(chunks)} chunks; depth={self.depth}")

        if len(chunks) == 1:
            logger.info("Single-chunk summarization path")
            summary = self._summarize_chunk(chunks[0], map_prompt)
        else:
            logger.info(f"Running map-reduce over {len(chunks)} chunks")
            partials = []
            for i, chunk in enumerate(chunks, start=1):
                logger.info(f"  Summarizing chunk {i}/{len(chunks)}")
                partials.append(self._summarize_chunk(chunk, map_prompt))
            logger.info("Combining partial summaries")
            summary = self._combine(partials, combine_prompt)

        elapsed = round(time.time() - start_time, 2)
        word_count = len(summary.split())
        logger.info(f"Summary complete: {word_count} words in {elapsed}s")

        return {
            "summary": summary,
            "content_type": content_type,
            "type_label": type_label,
            "chunks_processed": len(chunks),
            "transcript_words": len(transcript.split()),
            "summary_words": word_count,
            "elapsed_seconds": elapsed,
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
                "video_id": video_id,
                "transcript": transcript,
                **result,
            }
        except Exception as e:
            logger.error(f"Summarization failed: {str(e)}")
            return {"status": "error", "message": str(e)}
