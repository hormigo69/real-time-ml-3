# Base layer
FROM python:3.12-slim-bookworm

# Instalar dependencias de compilación y librdkafka específica
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalar librdkafka desde el código fuente
RUN curl -L https://github.com/edenhill/librdkafka/archive/refs/tags/v2.4.0.tar.gz | tar xzf - \
    && cd librdkafka-2.4.0 \
    && ./configure \
    && make \
    && make install \
    && cd .. \
    && rm -rf librdkafka-2.4.0 \
    && ldconfig

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

# Run our service
CMD ["uv", "run", "run.py"]