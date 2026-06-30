#!/bin/sh

echo "Esperando que MySQL esté disponible..."

until python3 - <<EOF
import os
import pymysql

try:
    pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    print("MySQL disponible")
except Exception:
    raise SystemExit(1)
EOF
do
    echo "MySQL aún no está listo..."
    sleep 2
done

echo "MySQL listo."