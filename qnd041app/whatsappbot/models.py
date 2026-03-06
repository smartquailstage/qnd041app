# myapp/models.py

from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel

@register_snippet
class Conversacion(models.Model):
    telefono = models.CharField(max_length=20)
    mensaje_usuario = models.TextField()
    respuesta_bot = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.telefono} @ {self.timestamp}"
