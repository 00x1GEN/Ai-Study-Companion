#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: Docker is required" >&2
  exit 2
fi

cp -n .env.example .env || true

echo "[1/9] Docker Compose validation"
docker compose config >/dev/null

echo "[2/9] Clean stack"
docker compose down -v --remove-orphans || true

echo "[3/9] Build and start"
docker compose up --build -d

echo "[4/9] Wait for API health"
for i in $(seq 1 60); do
  if curl -fsS http://localhost:8000/health >/dev/null; then break; fi
  sleep 2
  if [ "$i" -eq 60 ]; then docker compose logs; exit 1; fi
done

echo "[5/9] Migration status"
docker compose exec -T backend alembic current

echo "[6/9] Backend tests"
docker compose exec -T backend pytest -q

echo "[7/9] Seed/login/API smoke"
TOKEN=$(curl -fsS -X POST http://localhost:8000/api/v1/auth/login -H 'Content-Type: application/json' -d '{"email":"student@aspira.test","password":"password123"}' | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')
curl -fsS http://localhost:8000/api/v1/courses -H "Authorization: Bearer $TOKEN" >/dev/null
curl -fsS http://localhost:8000/api/v1/progress -H "Authorization: Bearer $TOKEN" >/dev/null

echo "[8/9] Flutter checks"
if command -v flutter >/dev/null 2>&1; then
  (cd mobile && flutter pub get && flutter analyze && flutter test)
else
  echo "WARNING: Flutter SDK not installed; mobile checks skipped."
fi

echo "[9/9] Container logs / health summary"
docker compose ps
docker compose logs --no-color --tail=80 backend

echo "RC1.1 host smoke completed."
