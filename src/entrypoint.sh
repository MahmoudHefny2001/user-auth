#!/bin/sh

python3 manage.py createsuperuser --email hefny4 --password MA7MOUDEEFNY.

# Start the application
gunicorn core.wsgi:application --bind 0.0.0.0:8000
