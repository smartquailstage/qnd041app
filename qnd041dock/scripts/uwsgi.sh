#!/bin/sh
set -e

NODE_NAME="qnd041app"
APP_PORT=${PORT:-9000}
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"support@smartquail.io"}
SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-"changeme"}

# Migraciones
echo "Aplicando migraciones..."
python3 manage.py migrate --settings=$NODE_NAME.settings.pro --noinput


# Realiza las migraciones de la base de datos (sin necesidad de intervención del usuario)
echo "Realizando migraciones..."
python3 manage.py migrate --settings=$NODE_NAME.settings.pro --noinput

# Crea el superusuario si no existe. Si ya existe, no causa un error
echo "Creando superusuario si no existe..."
python3 manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true

# Recolectar estáticos
echo "Recolectando archivos estáticos..."
python3 manage.py collectstatic --noinput

# Iniciar uWSGI
echo "Iniciando uWSGI..."
uwsgi --http :$APP_PORT --master --enable-threads --module $NODE_NAME.wsgi --ini uwsgi_pro.ini
