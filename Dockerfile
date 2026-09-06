FROM python:3.12-slim

# 1. Copy the uv binary from the official multi-platform image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. Set environment variables to optimize for container workflows
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_SYSTEM_PYTHON=1

WORKDIR /src

# 3. Copy configuration files first to exploit Docker layer caching
COPY pyproject.toml uv.lock ./

# 4. Install dependencies into the system environment (no virtualenv needed in a container)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# 5. Copy the rest of the application code
COPY . .

# 6. Install the project itself (if package-structured)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

CMD ["prefect", "server", "start", "--host", "0.0.0.0"]
