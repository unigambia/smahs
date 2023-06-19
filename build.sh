#!/usr/bin/env bash
# exit on error
set -o errexit
pip install -r requirements.txt
poetry lock --no-update
poetry install
python manage.py collectstatic --no-input
python manage.py migrate
