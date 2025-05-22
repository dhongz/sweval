# Build stage
FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install curl using Alpine's package manager
# RUN apk add --no-cache curl

# Copy just the dependency files first (for better layer caching)
COPY pyproject.toml uv.lock .

# Copy the rest of your application code
COPY . .

# Create and install into a virtual environment
RUN uv sync

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"