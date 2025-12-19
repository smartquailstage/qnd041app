from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Noticia, NoticiaMetricas


@receiver(post_save, sender=Noticia)
def crear_metricas_noticia(sender, instance, created, **kwargs):
    if created:
        NoticiaMetricas.objects.create(noticia=instance)
