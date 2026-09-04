#!/usr/bin/env sh
set -eu
FILE=${1:?Usage: restore.sh backups/file.sql.gz}
gunzip -c "$FILE" | docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" "$POSTGRES_DB"'
