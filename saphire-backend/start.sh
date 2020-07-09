#!/bin/bash

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="saphire", user="saphire", password="saphire", host="saphire")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
    >$2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

python manage.py migrate
python manage.py runserver 