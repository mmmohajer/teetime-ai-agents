#!/bin/bash

CLIENT_CONTAINER_ID=$(docker ps --filter "name=client" -q | head -n 1)
echo "Selected Client Container ID: $CLIENT_CONTAINER_ID"

if [ ! -z "$CLIENT_CONTAINER_ID" ]; then
    echo "Running sitemap generation in client container..."

    docker exec "$CLIENT_CONTAINER_ID" npm run generate-sitemap
    docker exec "$CLIENT_CONTAINER_ID" npm run generate:video-sitemap
    
    for FILE in $(docker exec "$CLIENT_CONTAINER_ID" sh -c 'ls /usr/src/app/public/sitemap*.xml' 2>/dev/null); do
        docker cp "$CLIENT_CONTAINER_ID:$FILE" /var/www/app/volume_data/to_be_served/
        echo "Copied $FILE to /var/www/app/volume_data/to_be_served/"
    done

    if [ $? -eq 0 ]; then
        echo "All sitemap files successfully copied to to_be_served folder."
    else
        echo "Error: No sitemap files found or copied."
    fi
else
    echo "Error: Client container not found."
fi