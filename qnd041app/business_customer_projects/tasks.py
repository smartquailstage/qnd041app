from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import BusinessSystemProject


@shared_task
def send_new_project_notifications(project_id):

    try:
        project = BusinessSystemProject.objects.select_related(
            "user"
        ).prefetch_related(
            "crew_members"
        ).get(id=project_id)

    except BusinessSystemProject.DoesNotExist:
        return

    # =====================================================
    # EMAIL AL USUARIO LOGUEADO
    # =====================================================

    if project.user.email:

        user_subject = f"Proyecto creado correctamente: {project.name}"

        user_context = {
            "project": project,
            "user": project.user,
        }

        user_html = render_to_string(
            "emails/new_project_user.html",
            user_context
        )

        user_email = EmailMultiAlternatives(
            subject=user_subject,
            body=user_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[project.user.email]
        )

        user_email.attach_alternative(user_html, "text/html")
        user_email.send()


    # =====================================================
    # EMAILS DEL EQUIPO ASIGNADO (crew_members)
    # =====================================================

    crew_emails = list(
        project.crew_members.filter(
            is_active=True
        ).exclude(
            email=""
        ).values_list("email", flat=True)
    )

    # Evitar envío vacío
    if not crew_emails:
        return

    crew_subject = f"Nuevo proyecto asignado: {project.name}"

    crew_context = {
        "project": project,
        "user": project.user,
    }

    crew_html = render_to_string(
        "emails/new_project_crew.html",
        crew_context
    )

    crew_email = EmailMultiAlternatives(
        subject=crew_subject,
        body=crew_html,
        from_email=settings.DEFAULT_FROM_EMAIL,

        # 👇 recomendado para privacidad
        bcc=crew_emails
    )

    crew_email.attach_alternative(crew_html, "text/html")
    crew_email.send()