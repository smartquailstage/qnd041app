from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SaaSOrder
from .tasks import send_order_email

@receiver(post_save, sender=SaaSOrder)
def send_email_on_paid(sender, instance, created, **kwargs):
    if instance.paid and not instance.email_sent:
        # Llamar la tarea de Celery
        send_order_email.delay(instance.id)

# saas_orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SaaSOrder
from .tasks import send_payment_and_contracts_email_task

@receiver(post_save, sender=SaaSOrder)
def trigger_payment_email(sender, instance: SaaSOrder, **kwargs):
    """
    Si el pago ha sido forzado y no se ha enviado el email,
    se llama la task de Celery.
    """
    if instance.force_paid and instance.paid and not instance.email_sent:
        send_payment_and_contracts_email_task.delay(instance.id)
