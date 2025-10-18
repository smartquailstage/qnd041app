# business/signals.py

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import BusinessSystemProject
from .tasks import notify_crew_members


@receiver(m2m_changed, sender=BusinessSystemProject.crew_members.through)
def notify_on_crew_assignment(sender, instance, action, pk_set, **kwargs):
    if action == "post_add" and pk_set:
        notify_crew_members(instance)
