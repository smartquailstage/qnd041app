import os
from django.core.wsgi import get_wsgi_application

# Obtener la variable de entorno DJANGO_SETTINGS_MODULE, si no está, se usará el valor predeterminado.
settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'qnd041app.settings.pro')

# Configurar la variable de entorno DJANGO_SETTINGS_MODULE si no está ya configurada.
os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

# Crear la aplicación WSGI
application = get_wsgi_application()
