# embeddings.py
import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINIAI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINIAI_API_KEY environment variable not set. Please add it to your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

def get_embedding(text):
    model = genai.GenerativeModel('gemini-pro-embeddings')
    response = model.embed_content([text])
    return response['embeddings'][0]
