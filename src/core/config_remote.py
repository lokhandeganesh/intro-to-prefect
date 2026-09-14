import requests
from pydantic_settings import BaseSettings, SettingsConfigDict

"""
CONFIGURATION LOADING STRATEGY:

This application uses a remote config store to fetch runtime settings.
The bootstrap credentials (CONFIG_STORE_URL, CONFIG_STORE_TOKEN) can be provided
without keeping a local .env file.

Order of precedence:
1. System/Container Environment Variables (Highest)
2. Local .env file (Fallback for local dev)

HOW TO PASS VARIABLES WITHOUT A .env FILE:

1. Docker run:
    docker run -e CONFIG_STORE_URL="https://config.internal/api/v1/app-config" \
        -e CONFIG_STORE_TOKEN="secret-token" \
        my-app-image

2. Docker Compose (compose.yml):
    services:
        app:
            image: my-app-image
        environment:
            - CONFIG_STORE_URL=https://config.internal/api/v1/app-config
            - CONFIG_STORE_TOKEN=secret-token

3. Kubernetes Deployment:
    env:
        - name: CONFIG_STORE_URL
        value: "https://config.internal/api/v1/app-config"
        - name: CONFIG_STORE_TOKEN
        valueFrom:
            secretKeyRef:
                name: app-secrets
                key: config-store-token

4. Local terminal session:
   export CONFIG_STORE_URL="https://config.internal/api/v1/app-config"
   export CONFIG_STORE_TOKEN="secret-token"
   uv run <script_path>
"""


# Reads only the bootstrap credentials from .env
class BootstrapSettings(BaseSettings):
    config_store_url: str
    config_store_token: str | None = None

    model_config = SettingsConfigDict(
        # Checks container/system environment variables first.
        # Falls back to .env only if present locally; silently ignores if absent.
        env_file=".env",
        extra="ignore",
    )


# Main settings that load from the remote JSON store
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    model_config = SettingsConfigDict(extra="ignore")


def load_settings() -> Settings:
    bootstrap = BootstrapSettings()

    headers = {}
    if bootstrap.config_store_token:
        headers["Authorization"] = f"Bearer {bootstrap.config_store_token}"

    try:
        response = requests.get(bootstrap.config_store_url, headers=headers, timeout=10)
        response.raise_for_status()
        return Settings(**response.json())
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Failed to fetch configuration from {bootstrap.config_store_url}: {exc}"
        ) from exc


settings = load_settings()