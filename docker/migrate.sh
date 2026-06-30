#!/bin/sh

set -e

echo "====================================="
echo " Iniciando migraciones"
echo "====================================="

sh docker/wait-for-db.sh

echo ""
echo "Ejecutando Alembic..."

alembic upgrade head

echo ""
echo "Ejecutando Seed..."

python3 -m app.seeds.seed

echo ""
echo "Migraciones finalizadas."