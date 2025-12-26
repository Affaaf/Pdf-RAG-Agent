import os
import openai
from dotenv import load_dotenv
from configs.constants import Const
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance 

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Qdrant client with optional API key (for Qdrant Cloud)
qdrant_api_key = os.getenv("QDRANT_API_KEY")
if qdrant_api_key:
    qdrant = QdrantClient(url=Const.QDRANT_URL, api_key=qdrant_api_key)
else:
    qdrant = QdrantClient(url=Const.QDRANT_URL)

combined_collection_name = Const.PDF_COLLECTION


def create_collection():
    existing = qdrant.get_collections()
    names = [c.name for c in existing.collections]

    if combined_collection_name in names:
        print(f"Collection '{combined_collection_name}' already exists.")
        return

    qdrant.create_collection(
        collection_name=combined_collection_name,
        vectors_config=VectorParams(
            size=384,       
            distance=Distance.COSINE
        )
    )

    print(f"Collection '{combined_collection_name}' created with dimension 384.")
