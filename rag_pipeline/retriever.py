# rag_pipeline/retriever.py

from annoy import AnnoyIndex
import numpy as np
from typing import List

class Retriever:
    def __init__(self, vector_dim: int, num_trees: int = 10):
        """Initialize the Annoy index with the specified vector dimension and number of trees."""
        self.index = AnnoyIndex(vector_dim, 'angular')  # Use angular distance (cosine similarity)
        self.vector_dim = vector_dim
        self.num_trees = num_trees

    def build_index(self, embeddings: np.ndarray):
        """Build the Annoy index from the provided embeddings."""
        for i, embedding in enumerate(embeddings):
            self.index.add_item(i, embedding)

        # Build the index with the specified number of trees (more trees = more accuracy, slower queries)
        self.index.build(self.num_trees)

    def retrieve(self, query_embedding: np.ndarray, top_k: int = 5) -> List[int]:
        """Retrieve the top-k nearest neighbor indices for a given query embedding."""
        return self.index.get_nns_by_vector(query_embedding, top_k)
