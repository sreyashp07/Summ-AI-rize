"""YouTube video summarization with progress callbacks, caching, content-aware prompts, depth control, TL;DR, and keywords."""
import time
import hashlib
import logging
from langchain_community.chat_models import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import extract_video_id, get_transcript, clean_transcript
from content_detector import detect_content_type, get_type_label
from prompts import get_prompts
from keywords import extract_keywords

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("summarizer")


TLDR_PROMPT = (
    "In 2-3 sentences, give a sharp executive summary of the following video summary. "
    "Be specific, no fluff. Start directly with the content - no 'this video discusses'.\n\n"
    "Summary:\n{summary}\n\nTL;DR:"
)


class YouTubeSummarizer:
    _cache: dict = {}

    def __init__(self, model: str = "llama3.2", depth: str = "standard"):
        self.llm = ChatOllama(temperature=0, model=model)
        self.depth = depth
        self.model_name = model
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

    def _generate_tldr(self, summary: str) -> str:
        try:
            tldr = self._invoke(TLDR_PROMPT.format(summary=summary[:3000]))
            return tldr.strip()
        except Exception as e:
            logger.warning(f"TL;DR generation failed: {e}")
            return ""

    def summarize_text(self, transcript: str, progress_callback=None) -> dict:
        if not transcript or not transcript.strip():
            raise Exception("Transcript is empty.")

        transcript = clean_transcript(transcript)
        cache_key = hashlib.md5(
            f"{transcript[:5000]}|{self.depth}|{self.model_name}".encode()
        ).hexdigest()
        if cache_key in self._cache:
            logger.info(f"Cache HIT for key {cache_key[:8]}...")
            if progress_callback:
                progress_callback(1, 1, "Loaded from cache")
            return self._cache[cache_key]

        logger.info(f"Cache MISS for key {cache_key[:8]}... generating")
        start_time = time.time()

        content_type = detect_content_type(transcript)
        type_label = get_type_label(content_type)
        if progress_callback:
            progress_callback(0, 100, f"Detected: {type_label}")

        map_prompt, combine_prompt = get_prompts(content_type, self.depth)
        chunks = self.text_splitter.split_text(transcript)
        total = len(chunks)
        logger.info(f"Split transcript into {total} chunks; depth={self.depth}")

        if total == 1:
            if progress_callback:
                progress_callback(0, 1, "Summarizing single chunk")
            summary = self._summarize_chunk(chunks[0], map_prompt)
            if progress_callback:
                progress_callback(1, 1, "Done")
        else:
            partials = []
            for i, chunk in enumerate(chunks, start=1):
                logger.info(f"  Summarizing chunk {i}/{total}")
                if progress_callback:
                    progress_callback(i - 1, total + 1, f"Summarizing chunk {i} of {total}")
                partials.append(self._summarize_chunk(chunk, map_prompt))
            if progress_callback:
                progress_callback(total, total + 1, "Combining summaries")
            summary = self._combine(partials, combine_prompt)

        if progress_callback:
            progress_callback(total, total + 1, "Generating TL;DR")
        tldr = self._generate_tldr(summary)
        if tldr:
            summary = f"## TL;DR\n\n{tldr}\n\n---\n\n{summary}"

        kws = extract_keywords(transcript, top_n=8)
        elapsed = round(time.time() - start_time, 2)
        word_count = len(summary.split())
        logger.info(f"Summary complete: {word_count} words in {elapsed}s")

        if progress_callback:
            progress_callback(total + 1, total + 1, "Done")

        result = {
            "summary": summary,
            "tldr": tldr,
            "keywords": kws,
            "content_type": content_type,
            "type_label": type_label,
            "chunks_processed": total,
            "transcript_words": len(transcript.split()),
            "summary_words": word_count,
            "elapsed_seconds": elapsed,
        }
        self._cache[cache_key] = result
        return result

    def summarize_video(self, youtube_url: str, progress_callback=None) -> dict:
        try:
            video_id = extract_video_id(youtube_url)
            if not video_id:
                return {"status": "error", "message": "Invalid YouTube URL"}
            if progress_callback:
                progress_callback(0, 100, "Fetching transcript")
            transcript = get_transcript(video_id)
            result = self.summarize_text(transcript, progress_callback=progress_callback)
            return {
                "status": "success",
                "video_id": video_id,
                "transcript": transcript,
                **result,
            }
        except Exception as e:
            logger.error(f"Summarization failed: {str(e)}")
            return {"status": "error", "message": str(e)}
