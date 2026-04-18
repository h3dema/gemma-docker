# Ubuntu 24.04 base
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    curl \
    git \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# # Upgrade pip tooling
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install --upgrade pip setuptools wheel

# Install Python deps
RUN pip3 install --no-cache-dir \
    gradio \
    langchain \
    langchain-community \
    chromadb \
    pypdf \
    sentence-transformers \
    ollama

RUN pip3 install -U langchain-huggingface sentence-transformers langchain-chroma

# Create workspace
WORKDIR /workspace

# Create folders
RUN mkdir -p /workspace/code /workspace/pdfs /workspace/.db

# Copy code
COPY start_ui.sh /workspace/start_ui.sh

# Expose port (Gradio will run on 80)
EXPOSE 80

# Start Ollama + pull model + run app
CMD ["bash", "-c", "/workspace/start_ui.sh"]
# CMD ["tail", "-f", "/dev/null"]
