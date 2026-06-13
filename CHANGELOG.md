# Changelog

All notable changes to Summ-AI-rize.

## [1.0.0] - 2026-06

### Added
- Content-aware summarization (math, tutorial, general)
- Depth control: concise, standard, deep
- TL;DR executive summary generation
- Keyword extraction from transcripts
- RAG chatbot with MMR retrieval and query rewriting
- Conversational memory in chat
- Multi-strategy YouTube transcript fetching with retries
- Manual transcript paste fallback for blocked IPs
- Transcript cleaning (removes [Music], timestamps, repeated words)
- In-memory summary cache
- Live progress bar during chunk processing
- Download summary as Markdown
- Export chat history as Markdown
- Regenerate summary at different depth without re-fetching
- Example transcripts dropdown with 9 samples
- Quick-action preset questions in chat
- Custom greenish-yellow themed UI with animations
- CLI mode (`cli.py`) for non-Streamlit usage
- Centralized configuration via `config.py` and `.env`
- Docker support with Dockerfile and .dockerignore
- GitHub Actions CI testing on Python 3.11 and 3.12
- 30+ unit tests across utils, content_detector, and keywords
- Comprehensive README, SETUP, CONTRIBUTING, Code of Conduct
- Issue templates for bug reports and feature requests

### Tech Stack
- Python 3.11
- Streamlit
- LangChain + LangChain Community
- Ollama (Llama 3.2, nomic-embed-text)
- FAISS
- youtube-transcript-api
