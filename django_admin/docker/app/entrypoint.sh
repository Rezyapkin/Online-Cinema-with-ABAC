#!/bin/sh
python3 manage.py collectstatic --no-input
uwsgi --strict --ini uwsgi.ini
