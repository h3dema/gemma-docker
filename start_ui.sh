#!/bin/bash

ollama serve &
# sleep 5
until ollama list >/dev/null 2>&1; do sleep 1; done;

mkdir -p export /workspace/.ollama/models
export OLLAMA_MODELS=/workspace/.ollama/models
ollama pull gemma4:e4b &

python3 /workspace/code/run.py
