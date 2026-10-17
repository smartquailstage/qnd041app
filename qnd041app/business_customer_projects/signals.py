from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Noticia, NoticiaMetricas
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BusinessSystemProject
from .tasks import send_new_project_notifications
from django.db.models.signals import pre_save, post_save
from .models import BusinessSystemProject  # O BusinessProcess según corresponda
from .tasks import send_project_completed_email_task
from django.db.models.signals import m2m_changed


@receiver(post_save, sender=Noticia)
def crear_metricas_noticia(sender, instance, created, **kwargs):
    if created:
        NoticiaMetricas.objects.create(noticia=instance)




@receiver(post_save, sender=BusinessSystemProject)
def business_project_created(sender, instance, created, **kwargs):

    if created:
        send_new_project_notifications.delay(instance.id)



@receiver(m2m_changed, sender=BusinessSystemProject.crew_members.through)
def crew_members_added(sender, instance, action, **kwargs):

    if action == "post_add":

        send_new_project_notifications.delay(instance.id)




@receiver(pre_save, sender=BusinessSystemProject)
def track_old_progress(sender, instance, **kwargs):
    """
    Guarda temporalmente el progreso anterior antes de actualizar el registro en la BD.
    """
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance._old_progress = old_instance.progress
        except sender.DoesNotExist:
            instance._old_progress = 0
    else:
        instance._old_progress = 0

@receiver(post_save, sender=BusinessSystemProject)
def check_project_completion_signal(sender, instance, created, **kwargs):
    """
    Dispara la tarea de Celery si el progreso acaba de llegar al 100%.
    """
    old_progress = getattr(instance, '_old_progress', 0)
    
    # Si antes era menor a 100 y ahora es >= 100, lanzamos el correo asíncrono
    if old_progress < 100 and instance.progress >= 100:
        send_project_completed_email_task.delay(instance.id)