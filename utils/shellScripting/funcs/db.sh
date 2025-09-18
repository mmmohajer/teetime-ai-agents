makeBackupOfDb() {
    echo "$PG_PASSWORD"
    local backupFileName=$(readData "What is backup filename  (without.sql)?")
    local addr="db_backups/$backupFileName.sql"
    docker exec -e PGPASSWORD=$PG_PASSWORD app-db-1 pg_dump $PG_DB_NAME -U $PG_USER > $addr
    echo "Backup file is ready"
}

restoreDb() {
    local restoreFileName=$(readData "What is restore filename (without.sql)?")
    local addr="db_backups/$restoreFileName.sql"
    docker exec -e PGPASSWORD=$PG_PASSWORD app-db-1 psql -U $PG_USER -d $PG_DB_NAME -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
    docker exec -e PGPASSWORD=$PG_PASSWORD app-db-1 psql -U $PG_USER -d $PG_DB_NAME -f $addr
    echo "DB succsessfully restored"
}