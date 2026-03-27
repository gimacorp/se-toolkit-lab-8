# Multi-stage build for nanobot gateway
# Uses uv for dependency management

ARG REGISTRY_PREFIX_DOCKER_HUB

# ---
# Stage 1: Build the application
# ---
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy workspace files (config.json, entrypoint.py, pyproject.toml)
COPY nanobot/ /app/nanobot/

# Copy mcp directory for lms-mcp editable install
COPY mcp/ /app/mcp/

# Copy nanobot-websocket-channel for webchat channel
COPY nanobot-websocket-channel/ /app/nanobot-websocket-channel/

# Sync dependencies and install editable packages
RUN --mount=type=cache,target=/root/.cache/uv \
    cd /app/nanobot && uv sync && \
    cd /app/nanobot && uv pip install -e /app/mcp && \
    cd /app/nanobot && uv pip install -e /app/nanobot-websocket-channel

# ---
# Stage 2: Final runtime image
# ---
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

RUN groupadd --system --gid 999 nonroot \
    && useradd --system --uid 999 --gid 999 --create-home --shell /bin/bash nonroot

WORKDIR /app/nanobot

# Copy the virtualenv from builder
COPY --from=builder --chown=nonroot:nonroot /app/nanobot/.venv /app/nanobot/.venv
COPY --from=builder --chown=nonroot:nonroot /app/nanobot /app/nanobot
COPY --from=builder --chown=nonroot:nonroot /app/mcp /app/mcp
COPY --from=builder --chown=nonroot:nonroot /app/nanobot-websocket-channel /app/nanobot-websocket-channel

# Ensure entrypoint is executable
RUN chmod +x /app/nanobot/entrypoint.py

USER nonroot

ENV PATH="/app/nanobot/.venv/bin:$PATH"

CMD ["python", "/app/nanobot/entrypoint.py"]
