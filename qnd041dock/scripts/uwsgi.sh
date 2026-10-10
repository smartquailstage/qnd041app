#!/bin/sh
set -e

NODE_NAME="qnd041app"
APP_PORT=${PORT:-9000}
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"support@smartquail.io"}
SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-"changeme"}

# 1. Aplicar migraciones (una sola vez)
echo "Aplicando migraciones..."
python3 manage.py migrate --settings=$NODE_NAME.settings.pro --noinput

# 2. Crear el superusuario si no existe
echo "Verificando superusuario..."
python3 manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true

# 3. Recolectar archivos estáticos (comentado si prefieres hacerlo en el build, o descoméntalo si es necesario)
echo "Recolectando archivos estáticos..."
python3 manage.py collectstatic --noinput --settings=$NODE_NAME.settings.pro

# 4. Iniciar uWSGI limpiamente usando solo el archivo .ini
echo "Iniciando uWSGI..."
exec uwsgi --ini uwsgi_pro.ini