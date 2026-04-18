#!/bin/bash

ollama serve
# sleep 5
until ollama list >/dev/null 2>&1; do sleep 1; done;
ollama pull gemma-4-e4b-it
python3 /workspace/code/run.py
