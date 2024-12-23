# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

# Instalar build dependencies y pandas del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    wget \
    python3-dev \
    python3-numpy \
    python3-pandas \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*
    
# Install the project into `/app`
WORKDIR /app

# Forzar el uso de Python 3.10
ENV PYTHON=/usr/local/bin/python3.10
ENV UV_PYTHON=/usr/local/bin/python3.10
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Run the Python service
CMD ["uv", "run", "run.py"]