# test.py
import warnings
warnings.filterwarnings("ignore")
import os
from rag_pipeline.pipeline import RAGPipeline
from rag_pipeline.generator import Generator
from rag_pipeline.storage import ChromaDBStorage

def main():
    # Define the path to the document
    docx_file = "sample.docx"

    # Check if the .docx file exists in the directory
    if not os.path.exists(docx_file):
        print(f"Error: {docx_file} not found in the current directory.")
        return

    # Step 1: Initialize the ChromaDB storage
    chroma_storage = ChromaDBStorage(collection_name="my_document_embeddings")

    # Step 2: Initialize the generator with the updated model
    model_name = "t5-small"  
    generator = Generator(model_name=model_name)

    # Step 3: Initialize the RAG pipeline
    pipeline = RAGPipeline(generator=generator, chroma_storage=chroma_storage)

    # Step 4: Process and store the document embeddings with paragraph-based chunking
    print(f"Processing and storing document: {docx_file}")
    pipeline.process_and_store_document(docx_file)

    # Step 5: Define a list of queries
    queries = [
        "How does ML is used for crop disease prediction?"
    ]

    for query in queries:
        # Set generate_response to True for generated answers, False to retrieve chunks directly
        response = pipeline.run(query, generate_response=True)
        print(f"Question: {response['question']}")
        print(f"Answer: {response['answer']}")

if __name__ == "__main__":
    main()