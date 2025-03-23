#!/bin/sh

# Configuración para que el script falle en caso de error
set -e

# Mostrar información del sistema (si neofetch está disponible, si no, se elimina o reemplaza por una salida simple)
if command -v screenfetch > /dev/null 2>&1; then
    screenfetch --ascii qnode_art.txt
else
    echo "screenfetch no está instalado, omitiendo la visualización ASCII."
fi

# Variables de configuración
SETTINGS_MODULE="qnd041app.settings.pro"
NODE_NAME="qnd041app"
DJANGO_SETTINGS_MODULE="qnd041app.settings.pro"
APP_PORT=${PORT:-9000}  # Asegúrate de que esta variable esté configurada en tu entorno Kubernetes
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"support@smartquail.io"}

# Realiza las migraciones de la base de datos (sin necesidad de intervención del usuario)
echo "Realizando migraciones..."
python3 manage.py migrate --settings=$NODE_NAME.settings.pro --noinput

# Crea el superusuario si no existe. Si ya existe, no causa un error
echo "Creando superusuario si no existe..."
python3 manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true

# Recolecta los archivos estáticos de Django (sin necesidad de intervención del usuario)
echo "Recolectando archivos estáticos..."
python3 manage.py collectstatic --settings=$NODE_NAME.settings.pro --noinput


uwsgi --http :9000  --master  --enable-threads --module $NODE_NAME.wsgi  --ini uwsgi_pro.ini

# Opcional: Gunicorn (descomentado si lo necesitas en lugar de uWSGI)
# gunicorn --worker-tmp-dir /dev/shm --bind "0.0.0.0:${APP_PORT}" qnode0_app.wsgi:application
