from __future__ import absolute_import, unicode_literals

# Esto asegura que las tareas de Celery se carguen cuando Django inicie.
# Importa la instancia Celery para que esté disponible en todo el proyecto.
from .celery import app as celery_app

# Esto hace que `celery_app` sea accesible en el módulo `qnd41app`.
__all__ = ('celery_app',)