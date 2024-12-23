# === Stage 1: Build dependencies ===

# Use an official Python runtime as a base image
FROM python:3.12-alpine AS builder

RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install build dependencies and necessary packages
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
    && /venv/bin/pip install --upgrade pip

# Create a virtual environment and install Python dependencies
WORKDIR /app
COPY ./src/requirements.txt /app/
RUN /venv/bin/pip install -r requirements.txt

# === Stage 2: Final Image ===

# Use a minimal image
FROM python:3.12-alpine

RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

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
    cairo \
    pango \
    gdk-pixbuf \
    libxml2 \
    libxslt \
    msttcorefonts-installer \
    ttf-dejavu \
    && update-ms-fonts && fc-cache -f \
    && apk del msttcorefonts-installer

# Copy virtual environment from the builder stage
COPY --from=builder /venv /venv

# Copy the rest of the application code
WORKDIR /app
COPY ./src/ ./src
COPY ./entrypoint.sh .

# Ensure entrypoint.sh is executable
RUN chmod +x /app/entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Set the entry point
ENTRYPOINT ["sh", "./entrypoint.sh"]

# Use the virtual environment for running the application
ENV PATH="/venv/bin:$PATH"
