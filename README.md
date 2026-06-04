# Summ-AI-rize

An AI-powered YouTube video summarizer with a built-in RAG chat assistant.
Built with Streamlit, LangChain, and Ollama (Llama 3.2) — runs fully locally.

## Features
- Generate structured summaries of any YouTube video with captions
- Chat with the video content using RAG (ask follow-up questions, get answers grounded in the transcript)
- Conversational memory — ask follow-ups like "explain that more"
- Custom greenish-yellow themed UI
- Runs fully locally — no API keys, no costs

## Tech Stack
- Python 3.10+
- Streamlit
- LangChain + LangChain Community
- Ollama (Llama 3.2 for generation, nomic-embed-text for embeddings)
- FAISS (in-memory vector store)
- youtube-transcript-api

## Project Structure
Summ-AI-rize/
├── streamlit_app.py    # Main Streamlit UI
├── summarizer.py       # Map-reduce summarization chain
├── chatbot.py          # RAG chatbot with FAISS + memory
├── utils.py            # URL parsing + transcript fetching
├── requirements.txt
└── README.md

## Setup

### 1. Install Ollama
Download from https://ollama.com/download

### 2. Pull the required models
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 3. Clone and install
```bash
git clone https://github.com/sreyashp07/Summ-AI-rize.git
cd Summ-AI-rize
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the app
Make sure Ollama is running, then:
```bash
streamlit run streamlit_app.py
```
Open http://localhost:8501

## How It Works
1. **Transcript extraction** — `youtube-transcript-api` pulls captions from the video
2. **Summarization** — LangChain `map_reduce` chain splits transcript into chunks, summarizes each, then combines into a structured final summary
3. **RAG chatbot** — Transcript is chunked, embedded with `nomic-embed-text`, stored in FAISS, and retrieved at query time with `ConversationalRetrievalChain`

## Notes
- The video must have captions enabled (auto or manual)
- First query is slow because the model loads into RAM
- Requires at least 8GB RAM (use `llama3.2:1b` for lower-end machines)

## License
MIT
