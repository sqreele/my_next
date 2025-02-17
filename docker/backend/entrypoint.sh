#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"

python manage.py migrate
python manage.py collectstatic --no-input --clear

exec gunicorn myLubd.wsgi:application --bind 0.0.0.0:8000 --workers 3
