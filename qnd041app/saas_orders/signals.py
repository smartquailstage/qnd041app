from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SaaSOrder
from .tasks import send_order_email

@receiver(post_save, sender=SaaSOrder)
def send_email_on_paid(sender, instance, created, **kwargs):
    if instance.paid and not instance.email_sent:
        # Llamar la tarea de Celery
        send_order_email.delay(instance.id)
