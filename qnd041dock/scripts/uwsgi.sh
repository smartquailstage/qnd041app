#!/bin/sh

set -e

# Mostrar ASCII opcional
if command -v screenfetch > /dev/null 2>&1; then
    screenfetch --ascii qnode_art.txt
else
    echo "screenfetch no está instalado, omitiendo la visualización ASCII."
fi

# Variables
SETTINGS_MODULE="qnd041app.settings.pro"
NODE_NAME="qnd041app"
DJANGO_SETTINGS_MODULE="qnd041app.settings.pro"
APP_PORT=${PORT:-9000}
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"support@smartquail.io"}

# Migraciones
echo "Realizando migraciones..."
python3 manage.py migrate --settings=$NODE_NAME.settings.pro --noinput

# Crear superusuario
echo "Creando superusuario si no existe..."
python3 manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python3 manage.py collectstatic --settings=$NODE_NAME.settings.pro --noinput

# 🚀 Arrancar Celery en segundo plano
echo "Iniciando Celery worker..."
celery -A $NODE_NAME worker -l info &  # el & lo ejecuta en segundo plano

# ⬇️ Arrancar uWSGI (bloqueante)
echo "Iniciando uWSGI..."
uwsgi --http :9000 --master --enable-threads --module $NODE_NAME.wsgi --ini uwsgi_pro.ini
