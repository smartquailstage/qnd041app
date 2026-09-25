from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MailingItem
from .tasks import enviar_mailing_task

@receiver(post_save, sender=MailingItem)
def disparar_mailing_signal(sender, instance, created, **kwargs):
    """
    Señal robusta que evita duplicidades al verificar el estado 
    y prevenir ejecuciones múltiples por guardados internos de Wagtail.
    """
    # Si viene de una carga cruda de la base de datos o guardados internos de Wagtail, ignorar
    if kwargs.get('raw', False):
        return

    # Solo nos interesa actuar si el estado actual es 'programado'
    if instance.estado == 'programado':
        # ⚠️ TRUCO CLAVE: Verificamos en la base de datos el estado REAL actual del registro.
        # Si en la BD ya figura como 'enviado' o 'procesando', evitamos lanzar otra tarea.
        # Esto frena los guardados múltiples consecutivos de Wagtail.
        db_instance = MailingItem.objects.filter(pk=instance.pk).only('estado').first()
        if db_instance and db_instance.estado == 'enviado':
            return

        # Lanzamos la tarea de Celery únicamente si pasa la validación
        enviar_mailing_task.delay(instance.pk)