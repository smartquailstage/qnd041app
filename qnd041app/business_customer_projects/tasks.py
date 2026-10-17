from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import BusinessProcess

from .models import BusinessSystemProject
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



@shared_task
def send_process_completed_email_task(process_id):
    """
    Tarea asíncrona que se ejecuta cuando un proceso de negocio alcanza el 100%.
    Envía un correo de notificación formal al cliente/usuario responsable.
    """
    try:
        process = BusinessProcess.objects.get(id=process_id)
        
        # Determinar el destinatario (ajusta según la relación de tu modelo, 
        # por ejemplo si el proyecto pertenece a un usuario o cliente)
        # recipient_email = process.project.client.email if process.project.client else None
        
        # Si prefieres enviarlo al desarrollador asignado o a un correo predeterminado de prueba:
        recipient_email = process.assigned_developer.email if process.assigned_developer and process.assigned_developer.email else None
        
        if not recipient_email:
            print(f"No hay un correo destinatario válido para el proceso ID {process_id}")
            return

        subject = f"¡Proceso completado al 100%!: {process.name}"
        
        context = {
            "process": process,
            "project": process.project,
        }

        try:
            html_content = render_to_string("emails/new_project_user.html", context)
            text_content = strip_tags(html_content)
        except Exception:
            text_content = f"El proceso {process.name} del proyecto {process.project.name} ha alcanzado el 100% de desarrollo."
            html_content = f"<div style='font-family: Arial;'><h2>{subject}</h2><p>{text_content}</p></div>"

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        return f"Correo de finalización enviado exitosamente para el proceso: {process.name}"

    except BusinessProcess.DoesNotExist:
        print(f"El proceso con ID {process_id} no fue encontrado.")
    except Exception as exc:
        print(f"Error al enviar el correo de proceso completado: {exc}")





@shared_task
def send_project_completed_email_task(project_id):
    """
    Tarea asíncrona que se ejecuta cuando un BusinessSystemProject alcanza el 100%.
    Envía un correo de notificación formal al cliente/usuario responsable.
    """
    try:
        project = BusinessSystemProject.objects.get(id=project_id)
        
        # Determinar el destinatario basado en la relación con el cliente o usuario
        recipient_email = project.client.email if project.client and project.client.email else None
        
        if not recipient_email:
            print(f"No hay un correo destinatario válido para el proyecto ID {project_id}")
            return

        subject = f"¡Proyecto completado al 100%!: {project.name}"
        
        context = {
            "project": project,
        }

        try:
            html_content = render_to_string("emails/new_project_user.html", context)
            text_content = strip_tags(html_content)
        except Exception:
            text_content = f"El proyecto {project.name} ha alcanzado el 100% de desarrollo e implementación."
            html_content = f"<div style='font-family: Arial;'><h2>{subject}</h2><p>{text_content}</p></div>"

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        return f"Correo de finalización de proyecto enviado exitosamente para: {project.name}"

    except BusinessSystemProject.DoesNotExist:
        print(f"El proyecto con ID {project_id} no fue encontrado.")
    except Exception as exc:
        print(f"Error al enviar el correo de proyecto completado: {exc}")