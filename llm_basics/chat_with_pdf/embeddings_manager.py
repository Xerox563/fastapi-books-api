"""
Create embeddings (vectors) from text chunks.

WHY: Convert text to vectors for similarity search
HOW: Use OpenAI embedding API
RESULT: Can find relevant chunks based on meaning
"""

from openai import OpenAI
from typing import List
import os
from config import OPENAI_API_KEY, EMBEDDING_MODEL

class EmbeddingsManager:
    """Create and manage text embeddings."""
    
    def __init__(self):
        """
        Initialize embeddings manager.
        
        WHY: Set up OpenAI client
        HOW: Use API key from environment
        """
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = EMBEDDING_MODEL
    
    def embed_text(self, text: str) -> List[float]:
        """
        Convert single text to embedding (vector).
        
        Args:
            text: Text to embed
        
        Returns:
            List of numbers (embedding vector)
        
        HOW:
        1. Send text to OpenAI
        2. OpenAI returns vector (list of 1536 numbers)
        3. Return the vector
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            # response.data[0].embedding is the vector
            return response.data[0].embedding
        
        except Exception as e:
            print(f" Error embedding text: {e}")
            return []
    
    def embed_chunks(self, chunks: List[str]) -> List[dict]:
        """
        Convert multiple chunks to embeddings.
        
        Args:
            chunks: List of text chunks
        
        Returns:
            List of dicts with chunk and embedding
        
        WHY: Embed all chunks at once
        HOW: Loop through all the chunks and create vector of each inorder to store in chromadb 
        """
        embedded_chunks = []
        
        print(f"🔀 Embedding {len(chunks)} chunks...")
        
        for i, chunk in enumerate(chunks):
            embedding = self.embed_text(chunk)
            
            if embedding:  # Only add if successful
                embedded_chunks.append({
                    "chunk_id": i,
                    "text": chunk,
                    "embedding": embedding
                })
                print(f"   Embedded chunk {i+1}/{len(chunks)}")
            else:
                print(f"   Failed to embed chunk {i+1}")
        
        print(f"✓ Successfully embedded {len(embedded_chunks)} chunks\n")
        return embedded_chunks


# Test embeddings
if __name__ == "__main__":
    manager = EmbeddingsManager()
    
    # Test single embedding
    text = "Machine learning is a type of artificial intelligence"
    embedding = manager.embed_text(text)
    
    print(f"Text: {text}")
    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")