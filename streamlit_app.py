"""Summ-AI-rize main Streamlit application."""
import streamlit as st
from summarizer import YouTubeSummarizer

st.set_page_config(
    page_title="Summ-AI-rize",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state
if "summary" not in st.session_state:
    st.session_state.summary = None
if "video_id" not in st.session_state:
    st.session_state.video_id = None
if "transcript" not in st.session_state:
    st.session_state.transcript = None

with st.sidebar:
    st.markdown("### About")
    st.write("Paste a YouTube URL to generate a structured summary and chat with the video content.")

st.title("Summ-AI-rize")
st.write("YouTube video summarizer and chat assistant powered by Ollama.")

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
            else:
                st.error(result["message"])

if st.session_state.summary:
    st.markdown("### Summary")
    st.markdown(st.session_state.summary)
