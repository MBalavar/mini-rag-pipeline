# rag_pipeline/storage.py

import chromadb
import numpy as np
from typing import List

class ChromaDBStorage:
    def __init__(self, collection_name: str):
        import chromadb
        from chromadb.config import Settings
        self.client = chromadb.Client(Settings())
        self.collection = self.client.get_or_create_collection(name=collection_name)
    
    def store_embeddings(self, doc_ids: List[str], embeddings: np.ndarray, metadatas: List[dict]):
        # Convert embeddings to list of lists if they are NumPy arrays
        if isinstance(embeddings, np.ndarray):
            embeddings = embeddings.tolist()
        self.collection.add(ids=doc_ids, embeddings=embeddings, metadatas=metadatas)

    def query_embeddings(self, query_embedding: np.ndarray, top_k: int = 5):
        """Retrieve documents by querying with an embedding."""
        results = self.collection.query(query_embeddings=query_embedding, n_results=top_k)
        return results['ids'], results['embeddings'], results['metadatas']
