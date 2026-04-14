"""
Configuration - Load environment variables
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate it exists
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file!")


# ============================================================================
# This creates a client object that knows how to talk to OpenAI servers
# The client automatically uses OPENAI_API_KEY from environment
client = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=OPENAI_API_KEY)