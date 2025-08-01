# src/gemini_client.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINIAI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINIAI_API_KEY environment variable not set. Please add it to your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini(prompt):
    model = genai.GenerativeModel('models/gemini-1.0-pro-latest')
    response = model.generate_content(prompt)
    return response.text
