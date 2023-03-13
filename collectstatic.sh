#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Upgrate pip"
pip install pip --upgrade

echo "Install Poetry"
pip install poetry

echo "Export requirements"
poetry export -f requirements.txt --without-hashes --output requirements.txt

echo "Install requirements"
pip install -r requirements.txt

echo "Collect static files"
python manage.py collectstatic --no-input