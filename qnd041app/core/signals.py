from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import SocialAutomationPost
from core.tasks import send_post_to_n8n

@receiver(post_save, sender=SocialAutomationPost)
def trigger_n8n_on_snippet_save(sender, instance, created, **kwargs):
    # Solo si es nuevo o pendiente
    if instance.status == "pending":
        send_post_to_n8n.delay(instance.id)