# business/signals.py

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import BusinessSystemProject
from .tasks import notify_crew_members


@receiver(m2m_changed, sender=BusinessSystemProject.crew_members.through)
def notify_on_crew_assignment(sender, instance, action, pk_set, **kwargs):
    if action == "post_add" and pk_set:
        notify_crew_members(instance)






from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.models import Site

def notify_crew_members(project):
    subject = f"Nuevo proyecto asignado: {project.name}"

    # Obtener URL completa del proyecto
    current_site = Site.objects.get_current()
    domain = current_site.domain  # Por ejemplo: smartquail.com
    project_url = f"https://{domain}{project.get_absolute_url()}"

    # 🔹 Correo personalizado para cada miembro
    for member in project.crew_members.all():
        if member.email:
            personalized_message = f"""
Hola {member.full_name},

Has sido asignado al nuevo proyecto: "{project.name}".

Descripción del proyecto:
{project.description}

👉 Para más información, visita: {project_url}

Saludos,
Equipo SmartQuail
"""
            send_mail(
                subject,
                personalized_message,
                settings.DEFAULT_FROM_EMAIL,
                [member.email],
                fail_silently=False,
            )

    # 🔹 Correo general al correo del proyecto
    if project.email:
        general_message = f"""
Hola equipo,

Se ha creado un nuevo proyecto: "{project.name}".

Descripción:
{project.description}

Miembros asignados:
{", ".join([m.full_name for m in project.crew_members.all()])}

👉 Ver proyecto en: {project_url}

Fecha de creación: {project.created_at.strftime('%d/%m/%Y %H:%M')}

Este mensaje fue enviado automáticamente por SmartQuail.
"""
        send_mail(
            f"[SmartQuail] Proyecto creado: {project.name}",
            general_message,
            settings.DEFAULT_FROM_EMAIL,
            [project.email],
            fail_silently=False,
        )
