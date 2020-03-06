#!/bin/sh
set -e

until PGPASSWORD=$PG_DB_PASS psql -h $PG_DB_HOST -U $PG_DB_USER $PG_DB_NAME -c '\l'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - continuing"

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
fi

exec "$@"
