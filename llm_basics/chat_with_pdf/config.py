"""
Configuration file for RAG system.

WHY: Centralize all settings in one place
HOW: Define constants and API keys
RESULT: Easy to change settings later
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"  # For converting text to vectors
LLM_MODEL = "gpt-4"  # For generating answers

# PDF Processing
MAX_CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 50    # Characters overlap between chunks

# Vector Database
VECTOR_DB_PATH = "./vector_store"  # Where to store embeddings

# Retrieval
TOP_K = 3  # How many chunks to retrieve for each question

# LLM Parameters
TEMPERATURE = 0.2  # Low = consistent, High = creative
MAX_TOKENS = 500   # Max response length