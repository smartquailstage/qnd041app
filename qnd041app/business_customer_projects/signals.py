from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Noticia, NoticiaMetricas
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BusinessSystemProject
from .tasks import send_new_project_notifications


@receiver(post_save, sender=Noticia)
def crear_metricas_noticia(sender, instance, created, **kwargs):
    if created:
        NoticiaMetricas.objects.create(noticia=instance)




@receiver(post_save, sender=BusinessSystemProject)
def business_project_created(sender, instance, created, **kwargs):

    if created:
        send_new_project_notifications.delay(instance.id)


from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import BusinessSystemProject
from .tasks import send_new_project_notifications


@receiver(m2m_changed, sender=BusinessSystemProject.crew_members.through)
def crew_members_added(sender, instance, action, **kwargs):

    if action == "post_add":

        send_new_project_notifications.delay(instance.id)