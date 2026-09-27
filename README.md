# Intro to Prefect

This project is meant as an introduction to data engineering through Prefect.
This `main` branch is the starting point. For the completed version, see
the `complete` branch.

## Setup

```shell
uv sync --all-extras
uv run pre-commit install

docker compose up -d

uv run prefect config set PREFECT_SERVER_ANALYTICS_ENABLED=false
uv run prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"

uv run prefect server start
```

## Running Code/Deployment

Check the script section in `.toml` file
```shell
pipeline
```

## Running test cases

```shell
uv run pytest --cache-clear
```

## Teardown

```shell
docker compose down
```

## Logging Architecture & Observability

This repository implements a production-grade, dual-mode logging system designed to support both local development and
containerized Kubernetes / Rancher environments (ingested by Grafana Loki).

### Core Features

- **Context-Aware Metadata:** Injects active Prefect metadata (`flow_run_id`, `flow_name`, `task_run_id`) using `PrefectLogFilter`.
- **Dual-Mode Output:**
  - **Local Development:** Color-coded Rich terminal output (`cyan` for `INFO`, `red3` for `ERROR`) with millisecond timestamps.
  - **Production / Kubernetes:** Single-line structured JSON logs with zero broken tracebacks.
- **Prefect Cloud / Server Sync:** Integrates `APILogHandler` to route application logs to the Prefect UI.
- **Hierarchical Scoping:** Supports granular sub-loggers using Python dot notation (`auto_sys_app.<module_or_service>`) for targeted log filtering.
- **Dynamic Log Level:** Configurable at runtime via the `LOG_LEVEL` environment variable (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

---

### How to Use the Logger

Import `get_logger` from `src.core.logger` in any task, flow, or service module:

```python
from prefect import flow, task
from src.core.logger import get_logger

# 1. Automatic file-based naming: produces "auto_sys_app.07_retry_logger"
logger = get_logger(__name__)

# 2. Or semantic domain naming: produces "auto_sys_app.billing_service"
# logger = get_logger("billing_service")


@task(retries=3, retry_delay_seconds=5)
def process_data(item_id: int):
    logger.info(f"Processing item: {item_id}")
    try:
        # task logic
        pass
    except Exception as exc:
        logger.error(f"Processing failed for item {item_id}: {exc}")
        raise exc
```

Running Workflows Locally
Always execute workflows as Python modules using the -m flag
to ensure consistent module resolution from the repository root:

```bash
# Standard local run (human-readable, colorized output)
uv run python -m src.c_retry_logic.07_retry_logger

# Test JSON format locally (simulates production Loki output)
PREFECT_LOGGING_HANDLERS_CONSOLE_FORMATTER=json uv run python -m src.c_retry_logic.07_retry_logger

# Enable debug logging locally
LOG_LEVEL=DEBUG uv run python -m src.c_retry_logic.07_retry_logger
```

## Production Deployment (Docker/ Kubernetes / Rancher) In containerized deployments

set `PREFECT_LOGGING_HANDLERS_CONSOLE_FORMATTER="json"` to switch stdout to structured JSON:

Pod / Deployment template:
```yaml
spec:
  template:
    spec:
      containers:
        - name: prefect-worker
          image: your-registry/prefect-worker:latest
          env:
            # Enable single-line JSON formatting for Loki
            - name: PREFECT_LOGGING_HANDLERS_CONSOLE_FORMATTER
              value: "json"

            # Optional: adjust logging verbosity on the fly
            - name: LOG_LEVEL
              value: "INFO"
```
