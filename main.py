import os
import shutil

from utils.qdrant_setup import create_collection
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from utils.models import QueryRequest
from utils.util import extract_results
from utils.util import extract_and_store_pdf
from utils.llm_inference import llm_agent,llm_response
from configs.constants import Const
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# List the domains allowed to visit your API
# origins = [
#     "http://localhost:3000",
#     "http://localhost:5173",
#     "https://your-frontend-domain.com",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"],        
)

os.makedirs(Const.DATA_DIR, exist_ok=True)


@app.post("/search", response_model=str)
def search_endpoint(request: QueryRequest):
    """
    Receives user query → returns response.
    """
    if request.response_type == "llm":
        response = llm_response(request.query)
        return response
    
    extracted_chunks = extract_results(request.query)

    response=llm_agent(request.query, extracted_chunks)

    return response


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
        Uploads a PDF file, stores it on disk, and processes it into the vector database.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF.")

    save_path = os.path.join(Const.DATA_DIR, file.filename)

    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    try:
        create_collection()
        extract_and_store_pdf(save_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")

    return JSONResponse({"status": "ok", "saved_path": save_path})
