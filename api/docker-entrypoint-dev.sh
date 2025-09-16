#!/bin/sh

./wait-for pgbouncer:6432 -- echo "PgBouncer is up!"

python manage.py collectstatic --noinput

python manage.py migrate

python manage.py runserver 0.0.0.0:8000