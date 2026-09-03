# syntax=docker/dockerfile:1
# Build from the repo root so the workspace files are in context:
#   docker build -f services/api/Dockerfile -t ai-ta-api:dev .

# ---------- stage 1: build the virtualenv ----------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Dependency manifests first: this layer only rebuilds when they change.
COPY pyproject.toml uv.lock ./
COPY services/api/pyproject.toml services/api/pyproject.toml
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --package ai-ta-api --no-install-workspace

# Source second: cheap layer that changes on every code edit.
COPY services/api/src services/api/src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --package ai-ta-api

# ---------- stage 2: slim runtime ----------
FROM python:3.12-slim-bookworm
# Unprivileged user; nothing here needs root.
RUN useradd --create-home --uid 1000 app
WORKDIR /app
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/services/api/src /app/services/api/src
ENV PATH="/app/.venv/bin:$PATH" \
    APP_ENV=container
USER app
EXPOSE 8000
CMD ["uvicorn", "ai_ta_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
