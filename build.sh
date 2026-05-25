#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py findstatic css/styles.css --verbosity 0

python manage.py collectstatic --noinput

python manage.py migrate
