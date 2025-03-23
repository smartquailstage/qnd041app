
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el módulo predeterminado de Django para 'celery' programáticamente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qnd41app.settings.pro')

app = Celery('qnd41app')

# Carga las configuraciones de Celery desde los archivos de configuración de Django
app.config_from_object('django.conf:qnd41app.settings.pro', namespace='CELERY')

# Carga tareas de todos los módulos de tareas en Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')