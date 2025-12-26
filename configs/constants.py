import os
from dotenv import load_dotenv

load_dotenv()

class Const:
    QDRANT_URL = os.getenv("QDRANT_URL")
    PDF_COLLECTION = "pdf-collection"
    MODEL_NAME = "llama-3.3-70b-versatile"
    DATA_DIR = "data"
    EMBEDDINGS_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    