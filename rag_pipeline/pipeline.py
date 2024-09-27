# rag_pipeline/pipeline.py

from .retriever import Retriever
from .generator import Generator
from .helpers import preprocess_text, read_docx, chunk_text, compute_embeddings
from .storage import ChromaDBStorage
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGPipeline:
    def __init__(self, generator: Generator, chroma_storage: ChromaDBStorage, retriever: Retriever = None, embedding_model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize the RAG pipeline with generator, retriever, and ChromaDB storage."""
        self.generator = generator
        self.chroma_storage = chroma_storage
        self.retriever = retriever
        self.embedding_model = SentenceTransformer(embedding_model_name)

    def process_and_store_document(self, docx_file_path: str):
        """
        Process a document, perform paragraph-based chunking, compute embeddings, and store them in ChromaDB.

        Args:
            docx_file_path (str): Path to the .docx file.
        """
        # Step 1: Read the document
        document_text = read_docx(docx_file_path)
        
        # Step 2: Perform paragraph-based chunking
        chunks = chunk_text(document_text)
        
        # Step 3: Compute embeddings for each chunk
        embeddings = compute_embeddings(chunks, model_name='all-MiniLM-L6-v2')
        
        # Step 4: Store embeddings and metadatas in ChromaDB
        doc_ids = [str(i) for i in range(len(chunks))]  # Use string IDs to match Annoy indices
        metadatas = [{'text': chunk} for chunk in chunks]
        self.chroma_storage.store_embeddings(doc_ids, embeddings, metadatas=metadatas)
        
        # Step 5: Initialize the Annoy retriever with the stored embeddings
        self.retriever = Retriever(vector_dim=embeddings.shape[1])
        self.retriever.build_index(embeddings)
        
        return doc_ids

    def run(self, query: str, top_k: int = 5, generate_response: bool = True) -> dict:
        """Run the RAG pipeline: retrieve relevant documents and generate a response or return the chunks directly.

        Args:
            query (str): The user's question.
            top_k (int): Number of top relevant chunks to retrieve.
            generate_response (bool): Whether to generate a response or return retrieved chunks.

        Returns:
            dict: A dictionary containing 'question', 'context', and 'answer'.
        """
        try:
            # Preprocess the query
            preprocessed_query = preprocess_text(query)

            # Generate query embedding using SentenceTransformers
            query_embedding = compute_embeddings([preprocessed_query], model_name='all-MiniLM-L6-v2')[0]

            # Retrieve top-k relevant documents using Annoy
            retrieved_ids = self.retriever.retrieve(query_embedding, top_k)

            if not retrieved_ids:
                print("No relevant documents found for the query.")
                return {
                    "question": query,
                    "context": "",
                    "answer": "I'm sorry, I don't have information on that topic."
                }

            # Convert integer IDs to strings to match ChromaDB IDs
            retrieved_ids_str = [str(id) for id in retrieved_ids]

            # Concatenate relevant document chunks
            relevant_docs = []
            for id in retrieved_ids_str:
                result = self.chroma_storage.collection.get(ids=[id])
                if result['metadatas']:
                    metadata = result['metadatas'][0]  # Get the first metadata entry
                    text = metadata.get('text', '')
                    relevant_docs.append(text)
                else:
                    print(f"Warning: No metadata found for ID {id}")

            context = " ".join(relevant_docs)

            if not context.strip():
                print("Warning: No relevant documents found. Using empty context.")

            if generate_response:
                # Create a comprehensive prompt for the generator
                prompt = f"Question: {query}\nContext: {context}\nAnswer:"

                # Generate response based on the prompt
                answer = self.generator.generate(prompt, max_new_tokens=150)  # Increased tokens

                return {
                    "question": query,
                    "context": context,
                    "answer": answer
                }
            else:
                # Return the retrieved chunks directly
                return {
                    "question": query,
                    "context": context,
                    "answer": "\n\n".join(relevant_docs)
                }

        except Exception as e:
            print(f"An error occurred during pipeline execution: {e}")
            return {
                "question": query,
                "context": "",
                "answer": "I'm sorry, something went wrong while processing your request."
            }