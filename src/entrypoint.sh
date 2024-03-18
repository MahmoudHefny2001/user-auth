#!/bin/sh

# Apply database migrations then create superuser with credentials {
# Full Name: Mahmoud Hefny
# Email: hefny4@gmail.com
# Password: MA7MOUD7EFNY.
# }

python3 manage.py makemigrations
python manage.py migrate



# Start the application
gunicorn core.wsgi:application --bind 0.0.0.0:8000
