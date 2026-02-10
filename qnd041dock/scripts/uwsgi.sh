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
SUPERUSER_NAME=${DJANGO_SUPERUSER_NAME:-"C.O.T: Mauricio Silva"}
SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD}

# =============================
# Migraciones
# =============================
echo "Generando migraciones si faltan..."
python3 manage.py makemigrations --noinput || true

echo "Aplicando migraciones..."
python3 manage.py migrate --noinput

# =============================
# Crear superusuario si no existe
# =============================
echo "Creando superusuario si no existe..."
# Intentamos crear superusuario solo si no existe
python3 manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="$SUPERUSER_EMAIL").exists():
    User.objects.create_superuser(
        username="$SUPERUSER_NAME",
        email="$SUPERUSER_EMAIL",
        password="$SUPERUSER_PASSWORD"
    )
END

# =============================
# Recolectar archivos estáticos
# =============================
echo "Recolectando archivos estáticos..."
python3 manage.py collectstatic --noinput

# =============================
# Arrancar Celery en segundo plano (opcional)
# =============================
#echo "Iniciando Celery worker..."
#celery -A $NODE_NAME worker -l info &

# =============================
# Arrancar uWSGI (bloqueante)
# =============================
echo "Iniciando uWSGI..."
uwsgi --http :$APP_PORT --master --enable-threads --module $NODE_NAME.wsgi --ini uwsgi_pro.ini
