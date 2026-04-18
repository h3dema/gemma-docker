This repo contains a simple implementation of a PDF question-answering system using LangChain, ChromaDB, and Ollama LLM model using the Gemma v4. It is designed to be run in a Docker container for easy setup and deployment.

> This implementation allows you to have a private and simple chatbot using your own PDF documents as the knowledge base.


## Installation

```bash
docker compose down
docker compose build --no-cache
```

```bash
docker-compose up
```

## Persistence

- `.db` stays on host → no reindex after restart

## Hot reload of code
- `./code` mounted → edit without rebuild

## Controlled reprocessing

- `LOAD_PDFS=true` → rebuild on startup
- `LOAD_PDFS=false` → just load DB
