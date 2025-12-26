# Use Python 3.9 base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install Qdrant binary
# Qdrant can run as a standalone binary without Docker
RUN QDRANT_VERSION=1.7.4 && \
    wget -q https://github.com/qdrant/qdrant/releases/download/v${QDRANT_VERSION}/qdrant-x86_64-unknown-linux-gnu.tar.gz && \
    tar -xzf qdrant-x86_64-unknown-linux-gnu.tar.gz && \
    mv qdrant /usr/local/bin/ && \
    rm qdrant-x86_64-unknown-linux-gnu.tar.gz && \
    chmod +x /usr/local/bin/qdrant

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data qdrant_storage

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose ports
# 7860 for Streamlit (Hugging Face Spaces default)
# 8000 for FastAPI
# 6333 for Qdrant
EXPOSE 7860 8000 6333

# Use the startup script
CMD ["/app/start.sh"]

