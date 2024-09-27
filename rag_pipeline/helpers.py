# rag_pipeline/helpers.py

from typing import List
import docx
import numpy as np

def preprocess_text(text: str) -> str:
    """Basic text preprocessing: lowercasing and removing extra spaces."""
    return text.lower().strip()

def read_docx(file_path: str) -> str:
    """Reads a .docx file and returns the text."""
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def chunk_text(text: str) -> List[str]:
    """
    Splits text into paragraphs.

    Args:
        text (str): The input text to be chunked.

    Returns:
        List[str]: A list of paragraphs.
    """
    # Split the text by newline characters to identify paragraphs
    paragraphs = text.split('\n')
    
    # Clean and filter out empty paragraphs
    paragraphs = [para.strip() for para in paragraphs if para.strip()]
    
    return paragraphs

def compute_embeddings(texts: List[str], model_name: str = 'all-MiniLM-L6-v2') -> np.ndarray:
    """Computes embeddings using SentenceTransformers."""
    from sentence_transformers import SentenceTransformer
    import numpy as np

    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=True)
    return np.array(embeddings)