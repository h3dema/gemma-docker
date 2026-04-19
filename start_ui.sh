#!/bin/bash

ollama serve &
# sleep 5
until ollama list >/dev/null 2>&1; do sleep 1; done;

mkdir -p export /workspace/.ollama/models
export OLLAMA_MODELS=/workspace/.ollama/models
export LLM_MODEL=gemma4:e4b
ollama pull $LLM_MODEL &

python3 /workspace/code/run.py
