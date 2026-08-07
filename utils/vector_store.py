"""
vector_store.py

Creates embeddings, builds a FAISS index,
and retrieves relevant document chunks.
"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:

    def __init__(self, model_name="all-MiniLM-L6-v2"):

        self.embedding_model = SentenceTransformer(model_name)

        self.index = faiss.IndexFlatL2(384)

        self.document_chunks = []

        self.chunk_metadata = []


    def build_index(self, document_chunks, chunk_metadata):

        self.document_chunks = document_chunks

        self.chunk_metadata = chunk_metadata

        embeddings = self.embedding_model.encode(
            document_chunks,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        embeddings = embeddings.astype("float32")

        self.index.reset()

        self.index.add(embeddings)


    def retrieve(self, question, top_k=3):

        question_embedding = self.embedding_model.encode(
            [question],
            convert_to_numpy=True
        ).astype("float32")

        distances, indices = self.index.search(
            question_embedding,
            top_k
        )

        retrieved_chunks = []

        for idx in indices[0]:

            if idx != -1:

                retrieved_chunks.append({
                    "text": self.document_chunks[idx],
                    "metadata": self.chunk_metadata[idx]
                })

        return retrieved_chunks
