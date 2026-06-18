#!/usr/bin/env bash
#
# Export the current NetBox dev database to dev-docker/seed/netbox-seed.sql.gz.
#
# The seed is auto-restored by Postgres on the next fresh build (e.g. after
# `docker compose ... down -v`), because dev-docker/seed/ is mounted into the
# container's /docker-entrypoint-initdb.d directory.
#
# Usage (from the repository root or from dev-docker/):
#   ./dev-docker/dump-seed.sh
#
set -euo pipefail

# Resolve paths relative to this script so it works from any cwd.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.yml"
SEED_FILE="${SCRIPT_DIR}/seed/netbox-seed.sql"

mkdir -p "${SCRIPT_DIR}/seed"

echo "Exporting NetBox database to ${SEED_FILE} ..."
docker compose -f "${COMPOSE_FILE}" exec -T postgres \
	pg_dump -U netbox -d netbox --no-owner --no-privileges \
	> "${SEED_FILE}"

echo "Done. Seed size: $(du -h "${SEED_FILE}" | cut -f1)"
