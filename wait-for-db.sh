#!/bin/bash

set -e

until PGPASSWORD=postgres psql -h "db" -U "postgres" -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

# Передаем управление команде, указанной в параметрах
exec "$@"