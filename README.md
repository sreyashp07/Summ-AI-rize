<div align="center">

# Summ-AI-rize

<a href="https://github.com/sreyashp07/Summ-AI-rize">
  <img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=26&duration=2800&pause=900&color=84CC16&center=true&vCenter=true&width=720&lines=AI-Powered+YouTube+Summarizer;Local+LLMs.+No+API+Keys.+Free+Forever.;Specialized+for+Math%2C+Tutorials+%26+Lectures;Built-in+RAG+Chatbot+for+Any+Video" alt="Animated banner"/>
</a>

### A content-aware YouTube summarizer and conversational RAG assistant. Built for students, researchers, and creators who want fast, structured insight from long videos.

<br>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&logo=meta&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-84CC16?style=for-the-badge)

</div>

---

## Highlights

- **Content-aware prompts** — automatically detects whether the video is math, a coding tutorial, or general content, and adapts the summary structure accordingly.
- **Math mode** — extracts equations, walks through reasoning step-by-step, includes worked numerical examples (dry runs), and explains intuition + common pitfalls.
- **Tutorial mode** — surfaces prerequisites, setup commands, step-by-step walkthrough, key code patterns, and debugging tips.
- **Depth control** — Concise (~200 words), Standard (~500 words), or Deep-Dive (1000+ words).
- **RAG chatbot** — built-in conversational interface to ask follow-up questions about the video, grounded in the actual transcript with conversational memory.
- **Manual paste fallback** — when YouTube blocks the transcript fetch (common in 2026 due to PO-token verification), paste the transcript directly.
- **Fully local** — runs on your machine via Ollama. No API keys, no usage limits, no data leaving your computer.

---

## Demo

> Add screenshots or a GIF here:
> ```markdown
> ![Demo](docs/demo.gif)
> ```

---

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| UI | Streamlit | Fast, Python-only web framework |
| LLM | Ollama + Llama 3.2 | Runs locally, no API costs |
| Orchestration | LangChain + LangChain-Community | LLM chains, prompts, document handling |
| Embeddings | nomic-embed-text (via Ollama) | Fast, accurate, runs locally |
| Vector Store | FAISS | In-memory, fast similarity search |
| Transcripts | youtube-transcript-api | Caption extraction |
| Lang | Python 3.11 | Stable, broad library support |

---

## Architecture
             ┌─────────────────┐
             │  YouTube URL    │
             │ or pasted text  │
             └────────┬────────┘
                      │
            ┌─────────▼─────────┐
            │  Transcript fetch │
            │  (multi-strategy) │
            └─────────┬─────────┘
                      │
            ┌─────────▼─────────┐
            │ Content-type      │
            │ detector          │
            │ (math/tut/gen)    │
            └─────────┬─────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
 ┌──────▼──────┐ ┌────▼────┐  ┌─────▼─────┐
 │ Map-reduce  │ │  FAISS  │  │ Streamlit │
 │  summarizer │ │ index   │  │     UI    │
 │ (Llama 3.2) │ │         │  │           │
 └──────┬──────┘ └────┬────┘  └─────┬─────┘
        │             │             │
        └──────┬──────┘             │
               │                    │
        ┌──────▼──────┐             │
        │   Summary   │◄────────────┤
        │  +  Chat    │             │
        └─────────────┘             │
               │                    │
               └────────────────────┘

---

## Setup

### Prerequisites

- Python 3.11 (3.12 also works; avoid 3.13/3.14 — too new for some ML wheels)
- Git
- 8 GB RAM minimum (16 GB recommended for Llama 3.2)
- ~3 GB free disk for Ollama models

### 1. Install Ollama

Download the installer for your OS from [ollama.com/download](https://ollama.com/download). After install, Ollama runs as a background service.

Pull the required models:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 2. Clone and set up Python

```bash
git clone https://github.com/sreyashp07/Summ-AI-rize.git
cd Summ-AI-rize

# Create virtual environment
python -m venv venv

# Activate (Windows Git Bash)
source venv/Scripts/activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run

Make sure Ollama is running (system tray icon), then:

```bash
streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## Usage

1. **Pick depth** in the sidebar (Concise / Standard / Deep).
2. **Choose input mode**:
   - *YouTube URL* — auto-fetches the transcript.
   - *Paste transcript manually* — for videos where YouTube blocks the API (use the "Show transcript" button on the YouTube page, select all, copy, paste).
3. Click **Generate Summary**.
4. The app detects whether it's a math, tutorial, or general video and produces a structured summary.
5. Switch to the **Chat with Video** tab to ask follow-up questions.

---

## Project Structure
Summ-AI-rize/
├── streamlit_app.py      # Main UI
├── summarizer.py         # Content-aware map-reduce summarization
├── chatbot.py            # RAG chatbot (FAISS + Llama)
├── content_detector.py   # Math / tutorial / general classifier
├── prompts.py            # Specialized prompt templates
├── utils.py              # URL parsing + transcript fetching
├── requirements.txt
└── README.md

---

## Troubleshooting

**"Could not fetch transcript / no element found"**
YouTube blocks transcript API calls from many IPs in 2026 (PO-token). Use the manual paste mode in the app.

**"ollama: command not found"**
Ollama isn't installed or not in PATH. Reinstall from [ollama.com/download](https://ollama.com/download) and restart your terminal.

**Slow on first run**
The first summary takes 30–90s because Llama 3.2 loads into RAM. Subsequent runs are much faster.

**Out of memory**
Switch to the smaller model: `ollama pull llama3.2:1b` and edit `summarizer.py` to use `model="llama3.2:1b"`.

**Want a cloud LLM instead?**
Swap `ChatOllama` for `ChatGroq` (free tier with Llama 3.3 70B). Get a key at [console.groq.com](https://console.groq.com).

---

## Roadmap

- [ ] PDF / web article support
- [ ] Multi-language summary output
- [ ] Whisper-based transcription for videos without captions
- [ ] Export summary as PDF
- [ ] Optional Groq backend toggle

---

## License

MIT

---

<div align="center">

Built with care for the open-source community.

</div>
