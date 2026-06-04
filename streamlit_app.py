"""Summ-AI-rize main Streamlit application."""
import streamlit as st

st.set_page_config(
    page_title="Summ-AI-rize",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.markdown("### About")
    st.write("Paste a YouTube URL to generate a structured summary and chat with the video content.")
    st.markdown("### Requirements")
    st.write("- Ollama running locally")
    st.write("- llama3.2 model pulled")
    st.write("- nomic-embed-text model pulled")
    st.write("- Video must have captions")

st.title("Summ-AI-rize")
st.write("YouTube video summarizer and chat assistant powered by Ollama.")

youtube_url = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...")
generate = st.button("Generate Summary", type="primary")
