"""Summ-AI-rize main Streamlit application."""
import streamlit as st

st.set_page_config(
    page_title="Summ-AI-rize",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Summ-AI-rize")
st.write("YouTube video summarizer and chat assistant powered by Ollama.")
