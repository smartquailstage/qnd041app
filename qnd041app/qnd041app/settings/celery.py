from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Establece el módulo de configuración de Django para Celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qnd031app.settings.stage')

# Crea una instancia de Celery.
app = Celery('qnd031app')

# Configura Celery utilizando la configuración de Django.
# La opción 'namespace' especifica que las configuraciones de Celery deben estar bajo el prefijo CELERY en el archivo de configuración de Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carga los módulos de tareas de todas las aplicaciones registradas en Django.
# Esto permite que Celery descubra y registre las tareas en cada aplicación de Django automáticamente.
app.autodiscover_tasks()

# Un ejemplo de cómo se podría configurar un backend de resultados y un broker si fuera necesario:
app.conf.update(
     broker_url='pyamqp://guest:guest@localhost//',
     result_backend='django-db',
     broker_connection_retry_on_startup = True
 )

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


