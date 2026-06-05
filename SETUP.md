# Detailed Setup Guide

This walks through every step to get Summ-AI-rize running. Pictures-free; copy-paste oriented.

## 1. System requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| OS | Windows 10, macOS 12, Ubuntu 20 | latest |
| Python | 3.10 | 3.11 |
| RAM | 8 GB | 16 GB |
| Disk | 5 GB free | 10 GB |
| Internet | Required for initial model download | |

## 2. Install Python 3.11

### Windows
1. Go to https://www.python.org/downloads/release/python-3119/
2. Download Windows installer (64-bit)
3. Run installer — CHECK "Add python.exe to PATH"
4. Verify: `py -3.11 --version`

### Mac (Homebrew)
```bash
brew install python@3.11
```

### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip
```

## 3. Install Git

Windows: https://git-scm.com/download/win
Mac: `brew install git`
Linux: `sudo apt install git`

## 4. Install Ollama

Go to https://ollama.com/download, get installer for your OS, run it. Ollama runs as a background service.

Verify:
```bash
ollama --version
```

Pull required models:
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Models combined are ~2.5 GB.

## 5. Clone repository

```bash
git clone https://github.com/sreyashp07/Summ-AI-rize.git
cd Summ-AI-rize
```

## 6. Create and activate virtual environment

### Windows (Git Bash or PowerShell)
```bash
py -3.11 -m venv venv
source venv/Scripts/activate
```

### Mac / Linux
```bash
python3.11 -m venv venv
source venv/bin/activate
```

Your prompt should now show `(venv)` prefix.

## 7. Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs Streamlit, LangChain, FAISS, and friends. Takes 2-5 minutes.

## 8. Run the app

Make sure Ollama is running. On Windows, check for the Ollama icon in the system tray near the clock. On Mac/Linux:

```bash
ollama serve   # in a separate terminal if not auto-started
```

Then in your project terminal (with venv active):

```bash
streamlit run streamlit_app.py
```

Browser opens at http://localhost:8501

## 9. First test

1. In sidebar, leave depth on **Standard**.
2. Switch to **Paste transcript manually** mode (most reliable).
3. Open any YouTube video, click the three-dot menu under it, click **Show transcript**.
4. Click in the transcript panel on the right, Ctrl+A to select all, Ctrl+C to copy.
5. Paste into the app's transcript box.
6. Click **Generate Summary**.

First run takes 30-90s because Llama 3.2 loads into RAM. Subsequent runs are faster.

## 10. Common issues

### "ollama: command not found"
Ollama not installed or not on PATH. Reinstall and restart terminal.

### "Could not retrieve transcript / no element found"
YouTube is blocking from your IP. This is a 2026-wide issue. Use manual paste mode.

### "Module not found: langchain_community"
Virtual environment not activated. Run `source venv/Scripts/activate` (Windows) or `source venv/bin/activate` (Mac/Linux).

### Streamlit doesn't open browser
Browser blocked? Open http://localhost:8501 manually.

### Out of memory
Use smaller model: `ollama pull llama3.2:1b`. Edit `summarizer.py`: change `model="llama3.2"` to `model="llama3.2:1b"`.

### App is slow
- First run: normal (model loading).
- After: check if other apps are using RAM. Close them.
- Still slow: switch to smaller model or use Groq API.

## 11. Stopping the app

In the terminal where Streamlit is running, press `Ctrl+C`.
