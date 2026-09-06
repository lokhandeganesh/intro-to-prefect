# Intro to Prefect

This project is meant as an introduction to data engineering through Prefect.
This `main` branch is the starting point. For the completed version, see
the `complete` branch.

## Setup

```shell
uv sync --all-groups
uv run pre-commit install

docker-compose up -d

uv run prefect config set PREFECT_SERVER_ANALYTICS_ENABLED=false
uv run prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"

uv run prefect server start
```

## Running test cases

```shell
uv run pytest --cache-clear
```

## Teardown

```shell
docker-compose down
```
