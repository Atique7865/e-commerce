# =============================================================================
# Dockerfile — TalentHeart Limited
# Multi-stage build:
#   builder  — installs Python deps
#   runtime  — lean production image
# =============================================================================

# ---- Stage 1: dependency builder -------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# System libs needed to compile psycopg2 and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        libjpeg-dev \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---- Stage 2: runtime image ------------------------------------------------
FROM python:3.11-slim AS runtime

# Metadata
LABEL maintainer="TalentHeart Engineering <dev@talentheart.com>"
LABEL org.opencontainers.image.title="TalentHeart Limited"
LABEL org.opencontainers.image.description="Digital Agency Web Application"

# Prevent .pyc files and enable stdout/stderr logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=talentheart.settings

WORKDIR /app

# Runtime shared libraries only (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        libjpeg62-turbo \
        wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy project source
COPY . .

# Create a non-root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser \
 && mkdir -p /app/staticfiles /app/media \
 && chown -R appuser:appgroup /app

USER appuser

# Collect static files at build time (WhiteNoise serves them)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Use the entrypoint script which runs migrations then starts gunicorn
ENTRYPOINT ["sh", "docker/entrypoint.sh"]
