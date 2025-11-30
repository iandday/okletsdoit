FROM python:3.14-slim-trixie AS development
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=okletsdoit.settings \
    PATH="/app/.venv/bin:$PATH" 

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    python3-dev \
    libffi-dev \
    postgresql-client-17 \
    libpq5 \
    libsqlite3-0 \
    libpam-modules \
    libpam-runtime \
    curl \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create user
RUN groupadd -r django && useradd -r -g django -s /bin/false django

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files and install
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --group dev 

RUN mkdir -p /app/app
COPY app/ /app/app

# Set up entrypoint
COPY --chown=django:django ./docker/docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

USER django

EXPOSE 8000

# Health check using django-health-check endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD /app/.venv/bin/python manage.py  health_check

WORKDIR /app/app  
ENTRYPOINT ["../docker-entrypoint.sh"]

# Build stage
FROM python:3.14-slim-trixie AS prod-builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_CACHE_DIR=/tmp/uv-cache

# Install build dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    python3-dev \
    libffi-dev \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files and install
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache 

# Copy source code
COPY app/ .

FROM python:3.14-slim-trixie AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=okletsdoit.settings \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    postgresql-client-17 \
    libpq5 \
    libsqlite3-0 \
    libpam-modules \
    libpam-runtime \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create user
RUN groupadd -r django && useradd -r -g django -s /bin/false django

WORKDIR /app

# Copy only what's needed from builder
COPY --from=prod-builder --chown=django:django /app/.venv /app/.venv
COPY --from=prod-builder --chown=django:django /app /app

# Set up entrypoint
COPY --chown=django:django ./docker/docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

USER django

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]