# qa_system.py
from .pdf_processor import extract_text_from_pdf
from .text_chunker import chunk_text
from .embeddings import get_embedding
from .vector_store import VectorStore
from .llm_client import ask_llm

class QASystem:
    def __init__(self, dim=1536):
        self.vector_store = VectorStore(dim)

    def ingest_pdf(self, pdf_path):
        text = extract_text_from_pdf(pdf_path)
        chunks = chunk_text(text)
        for chunk in chunks:
            emb = get_embedding(chunk)
            self.vector_store.add(emb, chunk)

    def answer_question(self, question):
        emb = get_embedding(question)
        relevant_chunks = self.vector_store.search(emb)
        context = "\n".join(relevant_chunks)
        prompt = f"Context: {context}\nQuestion: {question}"
        return ask_llm(prompt)
