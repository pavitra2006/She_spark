# src/gemini_client.py

import os
import google.generativeai as genai

# Try to get API key from Streamlit secrets first, fallback to .env or environment variable
GEMINIAI_API_KEY = None
try:
    import streamlit as st
    GEMINIAI_API_KEY = st.secrets["GEMINIAI_API_KEY"] if "GEMINIAI_API_KEY" in st.secrets else None
except ImportError:
    pass
if not GEMINIAI_API_KEY:
    from dotenv import load_dotenv
    load_dotenv()
    GEMINIAI_API_KEY = os.getenv("GEMINIAI_API_KEY")

genai.configure(api_key=GEMINIAI_API_KEY)

def list_gemini_models():
    try:
        models = genai.list_models()
        return [m.name for m in models]
    except Exception as e:
        return f"Gemini API error: {e}"

def ask_gemini(prompt):
    if not GEMINIAI_API_KEY:
        return "Error: Gemini API key not set. Please ensure 'GEMINIAI_API_KEY' is defined in your .env file."
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API error: {e}"
