# An example using multi-stage image builds to create a final image without uv.

# First, build the application in the `/app` directory.
# See `Dockerfile` for details.
#FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim AS builder

FROM python:3.10.12-slim AS builder

#ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Instalar uv primero
RUN pip install uv

# Luego el resto de los comandos
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Segunda etapa
FROM python:3.10.12-slim

WORKDIR /app

# Copiar la aplicación desde el builder
COPY --from=builder --chown=app:app /app /app

# Crear usuario no-root
RUN groupadd -r app && useradd -r -g app app

# Configurar PYTHONPATH
ENV PYTHONPATH=/app

# Poner ejecutables en el path
ENV PATH="/app/.venv/bin:$PATH"

# Cambiar a usuario no-root
USER app

# Ejecutar la aplicación FastAPI por defecto
CMD ["python", "/app/run.py"]
