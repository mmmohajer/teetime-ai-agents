#!/bin/bash

echo "Reloading Nginx replicas..."

# Loop through all running app_nginx replicas and reload Nginx
for container in $(docker ps --filter "name=nginx" --format "{{.ID}}"); do
    echo "Reloading Nginx in container $container..."
    docker exec $container nginx -s reload
    if [ $? -eq 0 ]; then
        echo "Reloaded Nginx successfully in container $container."
    else
        echo "Failed to reload Nginx in container $container."
    fi
done