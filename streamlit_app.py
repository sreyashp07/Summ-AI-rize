"""Summ-AI-rize main Streamlit application."""
import streamlit as st
from summarizer import YouTubeSummarizer
from chatbot import VideoChatbot

st.set_page_config(page_title="Summ-AI-rize", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.app-title { font-size: 48px; font-weight: 800; background: linear-gradient(90deg, #d4ff00, #84cc16, #4ade80); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0; }
.app-subtitle { color: #888; font-size: 16px; margin-top: 0; margin-bottom: 30px; }
.stTextInput input { background-color: #1a1a1a; color: #fff; border: 2px solid #4ade80; border-radius: 8px; }
.stTextInput input:focus { box-shadow: 0 0 12px #84cc16; border-color: #d4ff00; }
.stButton button { background: linear-gradient(90deg, #84cc16, #d4ff00); color: #000; font-weight: 700; border: none; border-radius: 8px; padding: 10px 24px; }
.stButton button:hover { background: linear-gradient(90deg, #4ade80, #d4ff00); }
.summary-card { background-color: rgba(132, 204, 22, 0.05); border-left: 4px solid #84cc16; border-radius: 8px; padding: 20px; margin: 20px 0; animation: fadeIn 0.6s ease-in; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

for key in ["summary", "video_id", "transcript", "chatbot"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("### About")
    st.write("Paste a YouTube URL to generate a summary and chat with the video.")

st.markdown('<h1 class="app-title">Summ-AI-rize</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">YouTube summarizer and chat assistant powered by Ollama</p>', unsafe_allow_html=True)

youtube_url = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...")

if st.button("Generate Summary", type="primary"):
    if not youtube_url:
        st.warning("Please enter a YouTube URL.")
    else:
        with st.spinner("Fetching transcript and generating summary..."):
            summarizer = YouTubeSummarizer()
            result = summarizer.summarize_video(youtube_url)
            if result["status"] == "success":
                st.session_state.summary = result["summary"]
                st.session_state.video_id = result["video_id"]
                st.session_state.transcript = result["transcript"]
                st.session_state.chatbot = None
                st.session_state.messages = []
            else:
                st.error(result["message"])

if st.session_state.summary:
    tab1, tab2 = st.tabs(["Summary", "Chat with Video"])
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown('<div class="summary-card">', unsafe_allow_html=True)
            st.markdown(st.session_state.summary)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.image(f"https://img.youtube.com/vi/{st.session_state.video_id}/maxresdefault.jpg")
            st.video(f"https://youtube.com/watch?v={st.session_state.video_id}")
    with tab2:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        st.write("(Chat input coming next commit.)")
