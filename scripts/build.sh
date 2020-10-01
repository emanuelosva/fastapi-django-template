#!/bin/sh -c

docker-compose -f docker-compose.dev.yml up --build -d
docker-compose run app python3 manage.py makemigrations
docker-compose run app python3 manage.py migrate
docker-compose down