# src/gemini_client.py

import os
import google.generativeai as genai

# Try to get API key from Streamlit secrets first, fallback to .env or environment variable

GEMINIAI_API_KEY = None
try:
    import streamlit as st
    try:
        GEMINIAI_API_KEY = st.secrets["GEMINIAI_API_KEY"]
    except (st.runtime.secrets.StreamlitSecretNotFoundError, KeyError, AttributeError):
        GEMINIAI_API_KEY = None
except ImportError:
    GEMINIAI_API_KEY = None

if not GEMINIAI_API_KEY:
    from dotenv import load_dotenv
    load_dotenv()
    GEMINIAI_API_KEY = os.getenv("GEMINIAI_API_KEY")

if not GEMINIAI_API_KEY:
    raise ValueError("GEMINIAI_API_KEY not set. Please add it to Streamlit secrets or your .env file.")

genai.configure(api_key=GEMINIAI_API_KEY)


def list_gemini_models():
    try:
        models = genai.list_models()
        return [m.name for m in models]
    except Exception as e:
        return f"Gemini API error: {e}"

def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API error: {e}"
