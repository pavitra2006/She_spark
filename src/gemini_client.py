# src/gemini_client.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

GEMINIAI_API_KEY = os.getenv("GEMINIAI_API_KEY")

# Configure generative AI client
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
