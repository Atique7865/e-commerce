#!/bin/sh
# =============================================================================
# docker/entrypoint.sh
# Container startup script — wait for services, migrate, then serve
# =============================================================================
set -e

echo "==> Waiting for PostgreSQL..."
wait-for-it "${DB_HOST:-db}:${DB_PORT:-5432}" --timeout=60 --strict -- echo "   PostgreSQL is up."

echo "==> Waiting for Redis..."
wait-for-it "${REDIS_HOST:-redis}:${REDIS_PORT:-6379}" --timeout=30 --strict -- echo "   Redis is up."

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Seeding default services (idempotent)..."
python manage.py seed_services

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Starting Gunicorn..."
exec gunicorn talentheart.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-4}" \
    --worker-class sync \
    --worker-tmp-dir /dev/shm \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
