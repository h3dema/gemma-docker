
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
