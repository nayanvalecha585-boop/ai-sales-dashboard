# =====================================================
# utils/gemini_client.py
# Configures and exposes the Gemini model instance
# =====================================================

import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv


# Load .env file once on import
load_dotenv()


@st.cache_resource(show_spinner=False)
def get_gemini_model():
    """
    Initialises and returns the Gemini model.
    Cached so it's only created once per session.
    Raises a clear error if the API key is missing.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY not found. "
            "Please create a .env file with your key — see .env.example."
        )

    genai.configure(api_key=api_key)

    return genai.GenerativeModel("models/gemini-2.5-flash")


def generate_insight(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns the text response.
    Raises exceptions to be handled by the caller.
    """
    model = get_gemini_model()
    response = model.generate_content(prompt)
    return response.text
