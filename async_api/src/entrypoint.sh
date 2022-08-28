#!/bin/sh
echo "Waiting for redis..."

    while ! nc -z $REDIS_HOST $REDIS_PORT; do
      sleep 1
    done

    echo "Redis started"


echo "Waiting for elastic..."

    while ! nc -z $ES_HOST $ES_PORT; do
      sleep 1
    done

    echo "Elastic started"

exec "$@"