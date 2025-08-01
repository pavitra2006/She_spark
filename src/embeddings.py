# embeddings.py
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']
