# src/gemini_client.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINIAI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINIAI_API_KEY environment variable not set. Please add it to your .env file.")

genai.configure(api_key=GEMINI_API_KEY)


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
