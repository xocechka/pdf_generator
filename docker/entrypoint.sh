#!/bin/bash

# Set app directory
cd ./src || exit

# Apply migrations
python3 manage.py migrate --noinput;
python3 manage.py createcachetable;

# Static files
python3 manage.py collectstatic --noinput;

python3 manage.py runserver 0.0.0.0:8000;
