import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ-API-KEY")
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")