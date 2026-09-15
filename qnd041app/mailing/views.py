from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from .models import MailingItem
from .tasks import enviar_mailing_task


@staff_member_required
def enviar_mailing_view(request, pk):
    mailing = get_object_or_404(MailingItem, pk=pk)

    # BLOQUEO DE SEGURIDAD: Si ya fue enviado o programado, no hacer nada
    if mailing.estado == 'enviado':
        messages.warning(request, f"Este mailing ya fue enviado.")
        return redirect(request.META.get('HTTP_REFERER', reverse('wagtailsnippets:index')))

    try:
        # 1. Cambiamos el estado a 'enviado' PRIMERO para bloquear cualquier doble clic
        mailing.estado = 'enviado'
        mailing.save(update_fields=['estado'])

        # 2. Lanzamos la tarea a Celery una sola vez
        enviar_mailing_task.delay(mailing.pk)

        messages.success(request, f"¡Correo enviado con éxito!")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")

    return redirect(request.META.get('HTTP_REFERER', reverse('wagtailsnippets:index')))

@staff_member_required
def previsualizar_mailing_view(request, pk):
    """Vista protegida para administradores que permite previsualizar

    el diseño HTML exacto del mailing antes de ser enviado.
    """
    mailing = get_object_or_404(MailingItem, pk=pk)

    context = {
        "user": mailing.user,
        "mailing": mailing,
        "contenido": mailing.contenido,
        "tipo_mailing": mailing.get_tipo_mailing_display(),
        "idioma": mailing.idioma,
    }

    try:
        html_content = render_to_string(
            "emails/mailing/mailing_email.html", context
        )
    except Exception:
        html_content = (
            f"<div style='font-family: Arial, sans-serif; padding: 20px; max-width: 600px; margin: auto;'>"
            f"<h2 style='color: #2c3e50;'>{mailing.titulo}</h2>"
            f"<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>"
            f"<p style='color: #555; line-height: 1.6;'>{mailing.contenido.replace(chr(10), '<br>')}</p>"
            f"<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>"
            f"<p style='font-size: 12px; color: #999;'>Idioma: {mailing.get_idioma_display()} | Tipo: {mailing.get_tipo_mailing_display()}</p>"
            f"</div>"
        )

    return HttpResponse(html_content)