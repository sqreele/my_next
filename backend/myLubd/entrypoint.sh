#!/bin/sh

# Wait for postgres
while ! nc -z $SQL_HOST $SQL_PORT; do
    echo "Waiting for postgres..."
    sleep 1
done

echo "PostgreSQL started"

python src/manage.py migrate
python src/manage.py collectstatic --no-input
python src/manage.py runserver 0.0.0.0:8000

exec "$@"
