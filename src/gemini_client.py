# src/gemini_client.py
import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINIAI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text
