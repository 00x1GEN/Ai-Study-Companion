#!/usr/bin/env sh
set -eu

# Explicit commands (pytest, alembic, shell, etc.) bypass the normal API startup flow.
if [ "$#" -gt 0 ]; then
  exec "$@"
fi

echo "[entrypoint] applying database migrations"
alembic upgrade head

echo "[entrypoint] loading idempotent seed data"
python -m app.seed

echo "[entrypoint] starting API"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
