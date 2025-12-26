# Quick Start Guide - Hugging Face Spaces Deployment

## 🚀 Fast Deployment Steps

### 1. Create Space on Hugging Face
- Go to https://huggingface.co/spaces
- Click "Create new Space"
- Choose **Docker** as SDK
- Name it (e.g., `pdf-knowledge-assistant`)

### 2. Upload Files
Upload these files to your Space:
- ✅ `app.py`
- ✅ `main.py`
- ✅ `requirements.txt`
- ✅ `Dockerfile`
- ✅ `start.sh`
- ✅ `qdrant_config.yaml`
- ✅ `README.md`
- ✅ `configs/constants.py`
- ✅ All files in `utils/` folder

### 3. Set Environment Variables
In Space Settings → Variables and secrets, add:

```
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here
QDRANT_URL=http://localhost:6333
API_SEARCH_URL=http://localhost:8000/search
API_UPLOAD_URL=http://localhost:8000/upload-pdf
```

**Optional** (if using Qdrant Cloud):
```
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=https://your-cluster.qdrant.io:6333
```

### 4. Wait for Build
- Check the "Logs" tab
- Wait 5-10 minutes for build to complete
- Your app will be live at: `https://your-username-pdf-knowledge-assistant.hf.space`

## 📝 Important Notes

1. **Qdrant Options**:
   - **Local** (default): Qdrant runs in the container (free, but data is ephemeral)
   - **Qdrant Cloud** (recommended): Sign up at https://cloud.qdrant.io for persistent storage

2. **Hardware**: Start with CPU basic (free). Upgrade if you need more resources.

3. **First Upload**: The first PDF upload may take longer as it downloads the embedding model.

## 🔧 Troubleshooting

- **Build fails**: Check logs for missing dependencies
- **Qdrant errors**: Verify QDRANT_URL is correct
- **API errors**: Check your API keys are set correctly
- **Timeout**: Increase timeout in `app.py` or upgrade hardware

## 📚 Full Documentation

See `DEPLOYMENT.md` for detailed instructions and troubleshooting.

