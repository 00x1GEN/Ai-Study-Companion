#!/usr/bin/env sh
set -eu
mkdir -p backups
STAMP=$(date +%Y%m%d_%H%M%S)
docker compose exec -T db sh -lc 'pg_dump --clean --if-exists --no-owner -U "$POSTGRES_USER" "$POSTGRES_DB"' | gzip > "backups/db_${STAMP}.sql.gz"
echo "Backup created: backups/db_${STAMP}.sql.gz"
