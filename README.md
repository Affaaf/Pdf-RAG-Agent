# PDF Knowledge Assistant - RAG Application

A Retrieval-Augmented Generation (RAG) application that allows you to upload PDF documents and ask questions about them using LLM-powered responses.

## Features

- 📤 **PDF Upload**: Upload and process PDF documents
- 🔍 **Semantic Search**: Search through documents using vector embeddings
- 🤖 **LLM Integration**: Get intelligent responses using Groq LLM
- 💾 **Vector Database**: Uses Qdrant for efficient vector storage and retrieval

## Architecture

- **FastAPI**: Backend API for PDF upload and search endpoints
- **Streamlit**: Frontend web interface
- **Qdrant**: Vector database for storing document embeddings
- **Sentence Transformers**: For generating embeddings
- **Groq**: LLM provider for generating responses

## Setup Instructions

### For Hugging Face Spaces Deployment

1. **Create a new Space** on Hugging Face:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose "Docker" as the SDK
   - Name your space (e.g., `your-username/pdf-knowledge-assistant`)

2. **Set Environment Variables** in your Space settings:
   - `GROQ_API_KEY`: Your Groq API key
   - `OPENAI_API_KEY`: Your OpenAI API key (if needed)
   - `QDRANT_URL`: Qdrant connection URL (default: `http://localhost:6333` for local Qdrant)
   - `API_SEARCH_URL`: FastAPI search endpoint (default: `http://localhost:8000/search`)
   - `API_UPLOAD_URL`: FastAPI upload endpoint (default: `http://localhost:8000/upload-pdf`)

3. **Upload your files** to the Space:
   - Upload all Python files
   - Upload `requirements.txt`
   - Upload `Dockerfile`
   - Upload this `README.md`

4. **Wait for build**: Hugging Face will automatically build and deploy your Docker container.

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd pdf_agent
   ```

2. **Set up environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Qdrant** (using Docker):
   ```bash
   docker pull qdrant/qdrant
   docker run -d -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
   ```

4. **Create `.env` file**:
   ```env
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=http://localhost:6333
   API_SEARCH_URL=http://localhost:8000/search
   API_UPLOAD_URL=http://localhost:8000/upload-pdf
   ```

5. **Run the application**:
   ```bash
   # Terminal 1: Start FastAPI
   uvicorn main:app --reload --port 8000
   
   # Terminal 2: Start Streamlit
   streamlit run app.py --server.port 8501
   ```

## API Endpoints

### POST `/upload-pdf`
Upload and process a PDF file.

**Request**: Multipart form data with `file` field containing PDF

**Response**:
```json
{
  "status": "ok",
  "saved_path": "data/example.pdf"
}
```

### POST `/search`
Search for information in uploaded documents.

**Request**:
```json
{
  "query": "What is the main topic?",
  "response_type": "agent"  // or "llm"
}
```

**Response**: String containing the LLM response

## Project Structure

```
pdf_agent/
├── main.py                 # FastAPI application
├── app.py                  # Streamlit entry point (for HF Spaces)
├── streamlit_app.py        # Original Streamlit app
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration for HF Spaces
├── README.md              # This file
├── configs/
│   └── constants.py       # Configuration constants
├── utils/
│   ├── models.py         # Pydantic models
│   ├── util.py           # Utility functions
│   ├── qdrant_setup.py   # Qdrant setup
│   └── llm_inference.py  # LLM inference functions
└── data/                  # Uploaded PDF files storage
```

## Notes for Hugging Face Spaces

- The Dockerfile runs both FastAPI and Streamlit in the same container
- Qdrant runs as a Docker-in-Docker container (requires Docker support in HF Spaces)
- For production, consider using Qdrant Cloud instead of local Qdrant
- The app uses port 7860 for Streamlit (HF Spaces default)
- FastAPI runs on port 8000 internally

## Troubleshooting

1. **Qdrant connection issues**: Make sure Qdrant is running and accessible at the configured URL
2. **API key errors**: Verify your API keys are set correctly in environment variables
3. **Port conflicts**: Ensure ports 8000 and 7860 are available
4. **Docker issues**: For HF Spaces, ensure Docker-in-Docker is supported or use Qdrant Cloud
