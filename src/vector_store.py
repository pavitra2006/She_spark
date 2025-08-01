# vector_store.py
import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embedding, text):
        self.index.add(np.array([embedding]).astype('float32'))
        self.texts.append(text)

    def search(self, embedding, k=5):
        D, I = self.index.search(np.array([embedding]).astype('float32'), k)
        return [self.texts[i] for i in I[0] if i < len(self.texts)]
