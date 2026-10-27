#!/usr/bin/env bash
# Render build script (the same steps as buildCommand in render.yaml)
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input

# Auto-create the admin login (set DJANGO_SUPERUSER_* env vars on Render). Safe to re-run.
python manage.py createsuperuser --no-input || true
