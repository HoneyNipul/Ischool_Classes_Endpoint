#!/bin/bash

echo "Running Migrations"
python3 /var/webapp/manage.py migrate

echo "Collecting Static Assets"
python3 /var/webapp/manage.py collectstatic --noinput

/usr/local/bin/uwsgi --ini /etc/uwsgi/uwsgi.ini