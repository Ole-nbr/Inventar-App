# Development image: the source code is mounted by docker-compose.yml for hot reload.
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Keep the venv outside /app, so the mounted source (with the host's .venv) cannot hide it.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy

WORKDIR /app

# Dependencies first, so this layer is only rebuilt when the lockfile changes.
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uv run alembic upgrade head && uv run fastapi dev app/main.py --host 0.0.0.0"]
