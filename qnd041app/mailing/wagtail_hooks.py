from django.urls import path, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from wagtail import hooks
from .models import MailingItem

# 1. Crear una vista backend para procesar el envío del correo cuando se presione el botón
def enviar_mailing_view(request, pk):
    mailing = get_object_or_404(MailingItem, pk=pk)
    
    try:
        # AQUÍ INTEGRAS TU LÓGICA DE ENVÍO DE CORREO (ej. Django send_mail o celery)
        # send_mail(mailing.titulo, mailing.contenido, 'tu-correo@domain.com', [destinatario])
        
        # Actualizamos el estado a enviado
        mailing.estado = 'enviado'
        mailing.save()
        
        messages.success(request, f"¡El mailing '{mailing.titulo}' ha sido enviado con éxito!")
    except Exception as e:
        messages.error(request, f"Error al enviar el mailing: {str(e)}")
        
    # Redirigir de vuelta al listado de snippets de MailingItem
    return redirect('wagtailsnippets_tu_app_mailingitem:list') # Reemplaza 'tu_app' por el nombre real de tu app en minúsculas

# 2. Registrar la URL para la acción del botón
@hooks.register('register_admin_urls')
def register_enviar_url():
    return [
        path('mailing/enviar/<int:pk>/', enviar_mailing_view, name='enviar_mailing_admin'),
    ]


from wagtail.snippets import widgets as wagtailsnippets_widgets


@hooks.register('register_snippet_listing_buttons')
def snippet_listing_buttons(snippet, user, next_url=None):
    if isinstance(snippet, MailingItem):
        # 1. Botón de Previsualización (Abre en una pestaña nueva)
        preview_url = reverse('mailing:previsualizar_mailing', args=[snippet.pk])
        yield wagtailsnippets_widgets.SnippetListingButton(
            '👁️ Previsualizar',
            preview_url,
            attrs={'aria-label': f'Previsualizar {snippet.titulo}', 'class': 'button button-small button-secondary', 'target': '_blank'},
            priority=5
        )

        # 2. Botón de Enviar (Solo si no ha sido enviado)
        if snippet.estado != 'enviado':
            enviar_url = reverse('mailing:enviar_mailing_admin', args=[snippet.pk])
            yield wagtailsnippets_widgets.SnippetListingButton(
                '🚀 Enviar Ahora',
                enviar_url,
                attrs={'aria-label': f'Enviar {snippet.titulo}', 'class': 'button button-small button-secondary'},
                priority=10
            )