#!/bin/bash

until nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
    echo "$(date) - waiting for postgresql..."
    sleep 1
done


python manage.py createsuperuser --noinput
python manage.py runserver "${GATEWAY_HOST}":"${GATEWAY_PORT}"