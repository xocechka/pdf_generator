# === Stage 1: Build dependencies ===

# Allow switching builder image
ARG BASE_BUILDER_IMAGE=python:3.12-alpine
ARG BASE_FINAL_IMAGE=python:3.12-alpine

FROM ${BASE_BUILDER_IMAGE} AS builder

# Build args
ARG ALPINE_MIRROR=https://dl-cdn.alpinelinux.org/alpine
ARG PYPI_REGISTRY=https://pypi.org/simple

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Configure Alpine repository dynamically
RUN echo "${ALPINE_MIRROR}/edge/community" >> /etc/apk/repositories

# Install build dependencies
RUN apk --no-cache add \
    build-base \
    gcc \
    git \
    libc-dev \
    libffi-dev \
    cairo-dev \
    pango-dev \
    gdk-pixbuf-dev \
    libxml2-dev \
    libxslt-dev \
    && python -m venv /venv \
    && /venv/bin/pip install --upgrade pip --index-url ${PYPI_REGISTRY}

# Install Python dependencies inside virtualenv
WORKDIR /app
COPY ./src/requirements.txt /app/
RUN /venv/bin/pip install -r requirements.txt --index-url ${PYPI_REGISTRY}

# === Stage 2: Final Image ===

# Allow switching final runtime image
FROM ${BASE_FINAL_IMAGE}

# Reuse Alpine mirror
ARG ALPINE_MIRROR
RUN echo "${ALPINE_MIRROR}/edge/community" >> /etc/apk/repositories

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install runtime dependencies
RUN apk --no-cache add \
    git \
    py3-cffi \
    curl \
    cairo \
    pango \
    gdk-pixbuf \
    libxml2 \
    libxslt \
    msttcorefonts-installer \
    ttf-dejavu \
    && update-ms-fonts && fc-cache -f \
    && apk del msttcorefonts-installer

# Copy virtual environment from builder stage
COPY --from=builder /venv /venv

# Copy application code
WORKDIR /app
COPY ./src/ ./src
COPY ./entrypoint.sh ./

# Ensure entrypoint.sh is executable
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Use virtual environment
ENV PATH="/venv/bin:$PATH"

# Set entrypoint
ENTRYPOINT ["sh", "./entrypoint.sh"]
