#!/bin/bash

# Get the container ID for the DB container
DB_CONTAINER_ID=$(docker ps --filter "name=db" -q)

# Check if the DB container ID is not empty
if [ ! -z "$DB_CONTAINER_ID" ]; then
    # Backup the database
    docker exec $DB_CONTAINER_ID pg_dump DB_NAME -U DB_USER > /var/www/app/db_backups/db_backup_$(date +%Y-%m-%d_%H-%M-%S).sql
    
    # Delete old database backups
    find /var/www/app/db_backups -type f -mtime +15 -delete
    find /var/www/app/db_backups -type d -empty -delete
else
    echo "Error: DB Container not found."
fi