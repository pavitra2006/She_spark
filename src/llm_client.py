# llm_client.py
import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINIAI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINIAI_API_KEY environment variable not set. Please add it to your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

def ask_llm(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text
