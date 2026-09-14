from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MailingItem
from .tasks import enviar_mailing_task  # Importa tu tarea de Celery creada anteriormente

@receiver(post_save, sender=MailingItem)
def disparar_mailing_signal(sender, instance, created, **kwargs):
    """
    Señal que detecta cuando un MailingItem es guardado y su estado 
    cambia a 'programado' (o listo para enviar).
    """
    # Si el estado es programado, lanzamos la tarea de Celery en segundo plano
    if instance.estado == 'programado':
        # Llamamos a Celery usando .delay() para que corra de manera asíncrona
        enviar_mailing_task.delay(instance.pk)
        
        # Opcional: Si quieres que pase a 'enviado' o a otro estado intermedio 
        # para que la señal no se dispare en bucle al guardar dentro de la misma tarea:
        # (Nota: es recomendable manejar el cambio a 'enviado' dentro de la propia task).