#!/bin/bash

# Startup script for Hugging Face Spaces deployment
# This script starts Qdrant, FastAPI, and Streamlit

echo " Starting PDF Knowledge Assistant..."

# Start Qdrant in background
echo " Starting Qdrant..."
if command -v qdrant &> /dev/null; then
    # Create Qdrant config if it doesn't exist
    if [ ! -f /app/qdrant_config.yaml ]; then
        cat > /app/qdrant_config.yaml << EOF
storage:
  storage_path: /app/qdrant_storage

service:
  http_port: 6333
  grpc_port: 6334
EOF
    fi
    qdrant --config-path /app/qdrant_config.yaml &
    QDRANT_PID=$!
    echo "Qdrant started with PID: $QDRANT_PID"
else
    echo " Warning: Qdrant binary not found. Make sure QDRANT_URL points to an external Qdrant instance."
fi

# Wait for Qdrant to be ready
echo " Waiting for Qdrant to be ready..."
sleep 5

# Start FastAPI in background
echo "🔌 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info &
FASTAPI_PID=$!
echo "FastAPI started with PID: $FASTAPI_PID"

# Wait for FastAPI to be ready
echo " Waiting for FastAPI to be ready..."
sleep 3

# Health check for FastAPI
for i in {1..10}; do
    if curl -s http://localhost:8000/docs > /dev/null; then
        echo " FastAPI is ready!"
        break
    fi
    echo "Waiting for FastAPI... ($i/10)"
    sleep 2
done

# Start Streamlit (main process - keeps container alive)
echo " Starting Streamlit app..."
streamlit run app.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false

