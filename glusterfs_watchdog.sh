#!/bin/bash

GLUSTER_MOUNT="/var/www/app"
DB_SERVICE="app_db"

while true; do
    # Check if GlusterFS is mounted
    if ! mountpoint -q "$GLUSTER_MOUNT"; then
        echo "$(date) - GlusterFS not mounted! Waiting for recovery..." | tee -a /var/log/glusterfs_watchdog.log
        while ! mountpoint -q "$GLUSTER_MOUNT"; do
            sleep 5  # Wait for GlusterFS to recover
        done
        echo "$(date) - GlusterFS is back! Restarting database service..." | tee -a /var/log/glusterfs_watchdog.log
        docker service update --force $(docker stack ls --format "{{.Name}}")_${DB_SERVICE}
    fi
    sleep 10
done
