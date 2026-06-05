"""Summ-AI-rize main Streamlit application."""
import streamlit as st
from summarizer import YouTubeSummarizer
from chatbot import VideoChatbot
from utils import extract_video_id

st.set_page_config(page_title="Summ-AI-rize", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.app-title { font-size: 52px; font-weight: 800; background: linear-gradient(90deg, #d4ff00, #84cc16, #4ade80); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0; letter-spacing: -1px; }
.app-subtitle { color: #888; font-size: 16px; margin-top: 0; margin-bottom: 30px; }
.stTextInput input, .stTextArea textarea { background-color: #1a1a1a; color: #fff; border: 2px solid #4ade80; border-radius: 8px; }
.stTextInput input:focus, .stTextArea textarea:focus { box-shadow: 0 0 12px #84cc16; border-color: #d4ff00; }
.stButton button { background: linear-gradient(90deg, #84cc16, #d4ff00); color: #000; font-weight: 700; border: none; border-radius: 8px; padding: 10px 24px; transition: all 0.2s; }
.stButton button:hover { background: linear-gradient(90deg, #4ade80, #d4ff00); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(132, 204, 22, 0.3); }
.summary-card { background-color: rgba(132, 204, 22, 0.05); border-left: 4px solid #84cc16; border-radius: 8px; padding: 20px; margin: 20px 0; animation: fadeIn 0.6s ease-in; }
.stat-pill { display: inline-block; background: rgba(132, 204, 22, 0.15); color: #d4ff00; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; margin-right: 8px; font-family: 'JetBrains Mono', monospace; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

for key in ["summary", "video_id", "transcript", "chatbot", "stats"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("### Settings")
    depth = st.select_slider(
        "Summary depth",
        options=["concise", "standard", "deep"],
        value="standard",
        format_func=lambda x: x.capitalize(),
    )
    st.caption({
        "concise": "~200 words. Quick overview.",
        "standard": "~500 words. Balanced detail.",
        "deep": "~1000+ words. Exhaustive analysis.",
    }[depth])

    st.markdown("---")
    st.markdown("### About")
    st.write("Local YouTube summarizer with content-aware prompts for math, tutorial, and general content.")

    st.markdown("### If URL fetch fails")
    st.write("YouTube blocks transcript fetching from many IPs. Use manual paste mode as a guaranteed fallback.")

st.markdown('<h1 class="app-title">Summ-AI-rize</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Content-aware YouTube summarizer and chat assistant. Optimized for math, tutorials, and lectures.</p>', unsafe_allow_html=True)

mode = st.radio(
    "Input mode",
    ["YouTube URL (auto-fetch transcript)", "Paste transcript manually"],
    horizontal=True,
)

youtube_url = ""
manual_transcript = ""
manual_video_id = ""

if mode == "YouTube URL (auto-fetch transcript)":
    youtube_url = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...")
else:
    st.info("On YouTube: three-dot menu under the video → 'Show transcript' → select all → copy → paste below.")
    manual_video_id_input = st.text_input("YouTube URL (optional, for thumbnail)", placeholder="https://youtube.com/watch?v=...")
    manual_transcript = st.text_area("Paste transcript here", height=250, placeholder="Paste full transcript here...")
    if manual_video_id_input:
        manual_video_id = extract_video_id(manual_video_id_input) or manual_video_id_input.strip()

if st.button("Generate Summary", type="primary"):
    summarizer = YouTubeSummarizer(depth=depth)
    if mode == "YouTube URL (auto-fetch transcript)":
        if not youtube_url:
            st.warning("Please enter a YouTube URL.")
        else:
            with st.spinner(f"Generating {depth} summary... (check terminal for live progress)"):
                result = summarizer.summarize_video(youtube_url)
                if result["status"] == "success":
                    st.session_state.summary = result["summary"]
                    st.session_state.video_id = result["video_id"]
                    st.session_state.transcript = result["transcript"]
                    st.session_state.stats = {
                        "type_label": result["type_label"],
                        "chunks_processed": result["chunks_processed"],
                        "transcript_words": result["transcript_words"],
                        "summary_words": result["summary_words"],
                        "elapsed_seconds": result["elapsed_seconds"],
                    }
                    st.session_state.chatbot = None
                    st.session_state.messages = []
                else:
                    st.error(result["message"])
                    st.info("Try the 'Paste transcript manually' mode above instead.")
    else:
        if not manual_transcript.strip():
            st.warning("Please paste the transcript text.")
        else:
            with st.spinner(f"Generating {depth} summary from pasted transcript..."):
                try:
                    result = summarizer.summarize_text(manual_transcript)
                    st.session_state.summary = result["summary"]
                    st.session_state.transcript = manual_transcript
                    st.session_state.video_id = manual_video_id if manual_video_id else None
                    st.session_state.stats = {
                        "type_label": result["type_label"],
                        "chunks_processed": result["chunks_processed"],
                        "transcript_words": result["transcript_words"],
                        "summary_words": result["summary_words"],
                        "elapsed_seconds": result["elapsed_seconds"],
                    }
                    st.session_state.chatbot = None
                    st.session_state.messages = []
                except Exception as e:
                    st.error(f"Error generating summary: {str(e)}")

if st.session_state.summary:
    if st.session_state.stats:
        s = st.session_state.stats
        st.markdown(
            f'<div style="margin: 10px 0;">'
            f'<span class="stat-pill">Type: {s["type_label"]}</span>'
            f'<span class="stat-pill">{s["chunks_processed"]} chunk(s)</span>'
            f'<span class="stat-pill">{s["transcript_words"]} input words</span>'
            f'<span class="stat-pill">{s["summary_words"]} output words</span>'
            f'<span class="stat-pill">{s["elapsed_seconds"]}s</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    tab1, tab2 = st.tabs(["Summary", "Chat with Video"])
    with tab1:
        if st.session_state.video_id:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                st.markdown(st.session_state.summary)
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.image(f"https://img.youtube.com/vi/{st.session_state.video_id}/maxresdefault.jpg")
                st.video(f"https://youtube.com/watch?v={st.session_state.video_id}")
        else:
            st.markdown('<div class="summary-card">', unsafe_allow_html=True)
            st.markdown(st.session_state.summary)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        if st.session_state.chatbot is None:
            with st.spinner("Indexing transcript for chat..."):
                st.session_state.chatbot = VideoChatbot(st.session_state.transcript)
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        if prompt := st.chat_input("Ask a question about the video..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = st.session_state.chatbot.ask(prompt)
                    st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
