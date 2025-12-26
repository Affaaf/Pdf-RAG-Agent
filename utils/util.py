import os
import logging
import pdfplumber

from uuid import uuid4
from typing import List
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from langchain.text_splitter import CharacterTextSplitter
from utils.models import SearchResponse
from configs.constants import Const
from groq import Groq


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
embedding_model = SentenceTransformer(Const.EMBEDDINGS_MODEL)

# Qdrant client with optional API key (for Qdrant Cloud)
qdrant_api_key = os.getenv("QDRANT_API_KEY")
if qdrant_api_key:
    qdrant = QdrantClient(url=Const.QDRANT_URL, api_key=qdrant_api_key)
else:
    qdrant = QdrantClient(url=Const.QDRANT_URL)

collection_name = Const.PDF_COLLECTION


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    splitter = CharacterTextSplitter(
        separator="",
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len
    )
    return splitter.split_text(text)


def get_text_embedding(text: str):
    if not text or not text.strip():
        return []
    embedding = embedding_model.encode(text, normalize_embeddings=True)
    return embedding.tolist()

# def get_text_embedding(text: str):
#     if not text or not text.strip():
#         return []

#     response = client.embeddings.create(
#         model="llama-embed-derivative",
#         input=text
#     )

#     return response.data[0].embedding


def extract_and_store_pdf(file_path: str, chunk_size: int = 500, overlap: int = 100):
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_num = page.page_number
            logging.info("Processing page %d of '%s'", page_num, file_path)

            text = page.extract_text() or ""
            chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

            for chunk in chunks:
                if not chunk.strip():
                    continue

                embedding = get_text_embedding(chunk)

                point = PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "file_name": os.path.basename(file_path),
                        "page_number": page_num,
                        "content": chunk
                    }
                )

                qdrant.upsert(
                    collection_name=collection_name,
                    points=[point]
                )

                logging.info("Upserted chunk from page %d into Qdrant", page_num)

    logging.info("Finished processing file: %s", file_path)


def extract_results(query: str) -> List[SearchResponse]:
    query_embedding = get_text_embedding(query)

    search_results = qdrant.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=5,
        with_payload=True,
        with_vectors=False
    )

    output = []
    for r in search_results:
        payload = r.payload or {}
        output.append(
            SearchResponse(
                content=payload.get("content", ""),
                score=r.score,
                page_number=payload.get("page_number", -1),
                file_name=payload.get("file_name", "")
            )
        )

    return output
