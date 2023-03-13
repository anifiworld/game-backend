#!/bin/bash
# APP_PORT=${PORT:-8080}
# SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"toonbcc@gmail.com"}
# SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-"toontoon"}

# Collect static files
# echo "Collect static files"
# python manage.py collectstatic --noinput


# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# echo "Create Superuser"
# python manage.py createsuperuser --email $SUPERUSER_EMAIL --username $SUPERUSER_USERNAME --noinput || true


# Start server
echo "Starting server"
gunicorn --worker-tmp-dir /dev/shm app.wsgi:application --bind "0.0.0.0:${PORT:-8080}"