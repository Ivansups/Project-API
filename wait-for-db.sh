#!/bin/bash
until nc -z -v -w30 db 5432; do
  echo "Waiting for main database to start..."
  sleep 1
done

until nc -z -v -w30 db_test 5432; do
  echo "Waiting for test database to start..."
  sleep 1
done

echo "Databases are ready!"
exec "$@"