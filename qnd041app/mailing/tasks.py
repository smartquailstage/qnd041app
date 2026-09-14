from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import MailingItem


@shared_task
def enviar_mailing_task(mailing_id):
    """
    Envía un mailing de SmartQuail en segundo plano utilizando Celery.
    """
    try:
        mailing = MailingItem.objects.get(pk=mailing_id)
    except MailingItem.DoesNotExist:
        return "Mailing no encontrado"

    # Evitar reenvíos accidentales si ya fue marcado como enviado
    if mailing.estado == "enviado":
        return f"El mailing '{mailing.titulo}' ya fue enviado anteriormente."

    # Obtener el correo del CustomUser relacionado
    to_email = mailing.user.email
    if not to_email:
        return f"El usuario {mailing.user.get_full_name()} no tiene un correo válido."

    # Configurar datos del correo
    subject = mailing.titulo
    from_email = settings.DEFAULT_FROM_EMAIL

    # Contexto para las plantillas de correo (puedes estructurarlas por idioma si lo deseas)
    context = {
        "user": mailing.user,
        "mailing": mailing,
        "contenido": mailing.contenido,
        "tipo_mailing": mailing.get_tipo_mailing_display(),
        "idioma": mailing.idioma,
    }

    try:
        # Intentar renderizar plantillas personalizadas (ej. soporte multi-idioma o general)
        text_content = render_to_string(
            "emails/mailing/mailing_email.txt", context
        )
        html_content = render_to_string(
            "emails/mailing/mailing_email.html", context
        )
    except Exception:
        # Respaldo si no existen las plantillas físicas en el proyecto
        text_content = mailing.contenido
        html_content = (
            f"<div style='font-family: Arial, sans-serif;'>"
            f"<h2>{mailing.titulo}</h2>"
            f"<p>{mailing.contenido.replace(chr(10), '<br>')}</p>"
            f"</div>"
        )

    # Construir y enviar el correo con soporte HTML y Texto plano
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    # Actualizar el estado del MailingItem a 'enviado' automáticamente
    mailing.estado = "enviado"
    mailing.save(update_fields=["estado"])

    return (
        f"Mailing '{mailing.titulo}' ({mailing.get_idioma_display()}) "
        f"enviado exitosamente a {to_email}"
    )