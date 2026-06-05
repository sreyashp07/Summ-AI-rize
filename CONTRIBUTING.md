# Contributing to Summ-AI-rize

Contributions are welcome.

## Development setup

```bash
git clone https://github.com/sreyashp07/Summ-AI-rize.git
cd Summ-AI-rize
python -m venv venv
source venv/Scripts/activate   # or venv/bin/activate on Mac/Linux
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Ways to contribute

- Improve specialized prompts in `prompts.py`
- Add a new content-type detector (e.g., interview, podcast) in `content_detector.py`
- Add file/PDF support
- Improve the UI in `streamlit_app.py`
- Add unit tests
- Improve documentation

## Commit message style

Use clear, imperative commit messages:

- Good: `Add Groq backend option to summarizer`
- Bad: `update`, `fix stuff`, `wip`

## Pull request process

1. Fork the repo
2. Create a feature branch from `main`
3. Make your changes with meaningful commits
4. Open a PR with a clear description of what changed and why
