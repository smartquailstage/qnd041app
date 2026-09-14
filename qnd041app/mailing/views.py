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
    """Vista protegida que dispara la orden de envío y redirige

    de vuelta al listado del panel de Wagtail de forma segura.
    """
    mailing = get_object_or_404(MailingItem, pk=pk)

    if mailing.estado == "enviado":
        messages.warning(
            request,
            f"El mailing '{mailing.titulo}' ya fue enviado anteriormente.",
        )
    else:
        try:
            # Lanza la tarea de Celery en segundo plano
            enviar_mailing_task.delay(mailing.pk)

            # Actualiza el estado a programado
            mailing.estado = "programado"
            mailing.save(update_fields=["estado"])

            messages.success(
                request,
                f"¡Orden de envío procesada con éxito para '{mailing.titulo}'!",
            )
        except Exception as e:
            messages.error(
                request, f"Error al intentar enviar el mailing: {str(e)}"
            )

    # Redirección segura utilizando la página anterior o el índice general de snippets
    return redirect(
        request.META.get("HTTP_REFERER", reverse("wagtailsnippets:index"))
    )


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