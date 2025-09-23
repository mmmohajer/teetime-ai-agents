#!/bin/sh

./wait-for db:5432

python manage.py collectstatic --noinput

python manage.py migrate --noinput

uwsgi --socket :8000 --workers 4 --threads 2 --master --enable-threads --module config.wsgi