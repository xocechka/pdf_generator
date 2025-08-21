#!/bin/bash

# Set app directory
cd ./src || exit

# Apply migrations
python3 manage.py migrate --noinput;
python3 manage.py createcachetable;

# Static files
python3 manage.py collectstatic --noinput;

# Check environment and run appropriate command
if [ "$DJANGO_DEBUG" = "True" ]; then
    # For development environment
    python3 manage.py runserver 0.0.0.0:8000 --settings config.settings
else
    # For production environment
    python3 -m gunicorn -c config/gunicorn_config.py config.wsgi:application;
fi
