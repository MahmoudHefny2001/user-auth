#!/bin/sh


python3 manage.py makemigrations
python manage.py migrate



# Start the application
gunicorn server.wsgi:application --bind 0.0.0.0:8000
