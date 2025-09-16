#!/bin/bash

echo "Reloading Nginx replicas..."

docker compose -f /var/www/app/docker-compose-prod.yml exec nginx nginx -s reload
