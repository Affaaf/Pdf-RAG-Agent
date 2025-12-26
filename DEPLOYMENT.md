# Deployment Guide for Hugging Face Spaces

This guide will walk you through deploying your RAG application to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (sign up at https://huggingface.co)
2. API keys:
   - Groq API key (get it from https://console.groq.com)
   - OpenAI API key (if needed)
3. Optional: Qdrant Cloud account (recommended for production)

## Step-by-Step Deployment

### Step 1: Create a New Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in the details:
   - **Space name**: e.g., `pdf-knowledge-assistant`
   - **SDK**: Select **"Docker"**
   - **Hardware**: Choose based on your needs:
     - CPU basic (free tier)
     - CPU upgrade (for better performance)
     - GPU (if needed for embeddings)
   - **Visibility**: Public or Private
4. Click **"Create Space"**

### Step 2: Upload Your Files

You can upload files using:
- **Git**: Clone the space and push your files
- **Web UI**: Upload files directly through the Hugging Face interface

**Required files to upload:**
```
├── app.py                    # Streamlit entry point
├── main.py                   # FastAPI application
├── streamlit_app.py          # Original Streamlit app (optional)
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── start.sh                 # Startup script
├── qdrant_config.yaml       # Qdrant configuration
├── README.md                # Space description
├── configs/
│   └── constants.py
└── utils/
    ├── models.py
    ├── util.py
    ├── qdrant_setup.py
    └── llm_inference.py
```

### Step 3: Set Environment Variables

1. Go to your Space settings
2. Navigate to **"Variables and secrets"**
3. Add the following environment variables:

| Variable Name | Description | Example Value |
|--------------|-------------|---------------|
| `GROQ_API_KEY` | Your Groq API key | `gsk_...` |
| `OPENAI_API_KEY` | Your OpenAI API key (optional) | `sk-...` |
| `QDRANT_URL` | Qdrant connection URL | `http://localhost:6333` |
| `API_SEARCH_URL` | FastAPI search endpoint | `http://localhost:8000/search` |
| `API_UPLOAD_URL` | FastAPI upload endpoint | `http://localhost:8000/upload-pdf` |

**Note**: For local Qdrant (running in container), use `http://localhost:6333`. For Qdrant Cloud, use your cloud URL.

### Step 4: Using Qdrant Cloud (Recommended)

For production deployments, it's recommended to use Qdrant Cloud instead of running Qdrant locally:

1. **Sign up for Qdrant Cloud**: https://cloud.qdrant.io
2. **Create a cluster** (free tier available)
3. **Get your cluster URL** and API key
4. **Update environment variables**:
   - `QDRANT_URL`: Your Qdrant Cloud URL (e.g., `https://xyz-123.us-east-1-0.aws.cloud.qdrant.io:6333`)
   - `QDRANT_API_KEY`: Your Qdrant Cloud API key (if required)

5. **Update `utils/qdrant_setup.py`** to use API key if needed:
```python
from qdrant_client import QdrantClient

qdrant = QdrantClient(
    url=Const.QDRANT_URL,
    api_key=os.getenv("QDRANT_API_KEY")  # Add this if using Qdrant Cloud
)
```

### Step 5: Build and Deploy

1. After uploading files and setting environment variables, Hugging Face will automatically:
   - Build your Docker image
   - Start your container
   - Expose your Streamlit app on port 7860

2. **Monitor the build**:
   - Go to the "Logs" tab in your Space
   - Check for any build errors
   - Wait for the build to complete (usually 5-10 minutes)

3. **Test your deployment**:
   - Once built, your app will be available at: `https://your-username-pdf-knowledge-assistant.hf.space`
   - Try uploading a PDF
   - Test the search functionality

## Troubleshooting

### Build Fails

**Issue**: Docker build fails
- **Solution**: Check the logs for specific errors. Common issues:
  - Missing dependencies in `requirements.txt`
  - Syntax errors in Python files
  - Incorrect Dockerfile syntax

### Qdrant Connection Errors

**Issue**: Cannot connect to Qdrant
- **Solution**: 
  - Verify `QDRANT_URL` is set correctly
  - For local Qdrant, ensure it's started in the startup script
  - For Qdrant Cloud, verify your URL and API key

### FastAPI Not Responding

**Issue**: Streamlit can't reach FastAPI
- **Solution**:
  - Check that FastAPI is running on port 8000
  - Verify `API_SEARCH_URL` and `API_UPLOAD_URL` point to `http://localhost:8000`
  - Check FastAPI logs in the container logs

### Out of Memory

**Issue**: Container runs out of memory
- **Solution**:
  - Upgrade to a higher hardware tier
  - Optimize model loading (use smaller embedding models)
  - Reduce batch sizes

### Timeout Issues

**Issue**: Requests timeout
- **Solution**:
  - Increase timeout values in Streamlit app
  - Optimize PDF processing (smaller chunks)
  - Use faster models

## Alternative: Separate FastAPI and Streamlit

If you prefer to deploy FastAPI separately:

1. **Deploy FastAPI** to a separate service (e.g., Railway, Render, Fly.io)
2. **Update environment variables** in your Streamlit Space:
   - `API_SEARCH_URL`: Your FastAPI deployment URL
   - `API_UPLOAD_URL`: Your FastAPI deployment URL
3. **Deploy Streamlit** to Hugging Face Spaces (simpler Dockerfile, no FastAPI)

## Monitoring

- **Logs**: Check the "Logs" tab in your Space for runtime logs
- **Metrics**: Monitor CPU/Memory usage in the Space settings
- **Errors**: Check Streamlit error messages in the app interface

## Updating Your Deployment

1. **Make changes** to your code locally
2. **Push to Git** (if using Git) or **upload new files**
3. **Hugging Face will automatically rebuild** your Space
4. **Wait for the new build** to complete

## Best Practices

1. **Use Qdrant Cloud** for production (more reliable than local Qdrant)
2. **Set up proper error handling** in your code
3. **Add logging** for debugging
4. **Test locally** before deploying
5. **Monitor resource usage** and upgrade hardware if needed
6. **Keep API keys secure** (never commit them to Git)

## Support

- Hugging Face Spaces Docs: https://huggingface.co/docs/hub/spaces
- Qdrant Docs: https://qdrant.tech/documentation/
- FastAPI Docs: https://fastapi.tiangolo.com/
- Streamlit Docs: https://docs.streamlit.io/

