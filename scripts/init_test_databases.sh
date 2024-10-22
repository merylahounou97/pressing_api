#!/bin/bash
set -e

# Nom de la base de données
DATABASE="test"

echo $DATABASE
echo $POSTGRES_USER
echo $POSTGRES_DB
echo "on est dans le test"

# Crée la base de données
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE $DATABASE;
EOSQL
