# -*- coding: utf-8 -*-
# usuarios/tasks.py
from celery import shared_task
from django.core.mail import send_mail,BadHeaderError,EmailMultiAlternatives
import requests
from django.conf import settings
from twilio.rest import Client
from django.core.mail.message import EmailMessage
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from email.header import Header
from email.utils import formataddr
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.template.loader import render_to_string


from django.utils.html import strip_tags
#from django.core.mail.backends.smtp import EmailBackend
import logging

logger = logging.getLogger(__name__)


from twilio.rest import Client


@shared_task
def enviar_correo_recuperacion(user_id, domain):
    """
    Envía un correo de restablecimiento de contraseña en segundo plano.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return "Usuario no encontrado"

    # Generar token y URL
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f"{domain}{reverse('usuarios:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

    # Construir correo
    subject = 'Restablezca su contraseña - SmartQuail, Inc.'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    text_content = render_to_string('emails/password_reset/password_reset_email.txt', {
        'user': user,
        'reset_url': reset_url
    })
    html_content = render_to_string('emails/password_reset/password_reset_email.html', {
        'user': user,
        'reset_url': reset_url
    })

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    return f"Correo de restablecimiento enviado a {user.email}"


@shared_task
def enviar_sms_recuperacion(user_id, domain):
    """
    Envía un SMS con el enlace de restablecimiento de contraseña usando Twilio.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return "Usuario no encontrado"

    # Generar token y URL
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f"{domain}{reverse('usuarios:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

    # Renderizar plantilla SMS
    sms_body = render_to_string('sms/password_reset.txt', {
        'user': user,
        'reset_url': reset_url
    }).strip()

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            to=str(user.telefono),
            from_=settings.TWILIO_FROM_NUMBER,
            body=sms_body
        )
    except Exception as e:
        return f"⚠️ Error al enviar SMS: {e}"

    return f"SMS enviado a {user.telefono}"



@shared_task
def enviar_correo_activacion(user_id, domain):
    """
    Envía un correo de activación de cuenta en segundo plano.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return "Usuario no encontrado"

    # 🔑 Generar token y UID
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # 🌐 Construir URL de activación completa
    activation_url = f"{domain}{reverse('usuarios:activar_cuenta', kwargs={'uidb64': uid, 'token': token})}"

    # 💬 Enlace de WhatsApp (opcional)
    whatsapp_link = f"https://wa.me/593963521262?text=Hola%20SmartQuail,%20quiero%20asistencia%20para%20activar%20mi%20cuenta%20({user.email})"

    # 📧 Contenido del correo
    subject = "🔐 Activa tu cuenta en SmartQuail, Inc."
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    text_content = render_to_string('sms/activation/account_activation_email.txt', {
        'user': user,
        'activation_url': activation_url,
        'whatsapp_link': whatsapp_link,
    })

    html_content = render_to_string('emails/activation/account_activation_email.html', {
        'user': user,
        'activation_url': activation_url,
        'whatsapp_link': whatsapp_link,
    })

    # ✉️ Enviar
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    return f"Correo de activación enviado a {user.email}"





@shared_task
def enviar_correo_login(user_id, fecha_hora, user_ip):
    """
    Envía un correo electrónico de notificación cuando el usuario inicia sesión.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return "Usuario no encontrado"

    subject = "🔐 Nuevo inicio de sesión detectado - SmartQuail, Inc."
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    text_content = render_to_string('emails/login_notification/login_notification_email.txt', {
        'user': user,
        'fecha_hora': fecha_hora,
        'user_ip': user_ip,
    })

    html_content = render_to_string('emails/login_notification/login_notification_email.html', {
        'user': user,
        'fecha_hora': fecha_hora,
        'user_ip': user_ip,
    })

    email_message = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email_message.attach_alternative(html_content, "text/html")
    email_message.send(fail_silently=True)

    return f"Correo enviado a {user.email}"


@shared_task(bind=True, max_retries=3, default_retry_delay=60)  # 3 intentos, 60s entre cada uno
def enviar_correo_async(self, emisor, receptor_email, asunto, cuerpo_html):
    try:
        cuerpo_texto = "Este es un mensaje alternativo en texto plano."

        asunto = Header(asunto, 'utf-8').encode()
        emisor = formataddr((str(Header(emisor, 'utf-8')), settings.DEFAULT_FROM_EMAIL))

        email = EmailMultiAlternatives(
            subject=asunto,
            body=cuerpo_texto,
            from_email=emisor,
            to=[receptor_email]
        )
        email.attach_alternative(cuerpo_html, "text/html")
        email.encoding = 'utf-8'

        email.send()
        logger.info("📧 Correo enviado exitosamente a %s", receptor_email)

    except Exception as e:
        logger.error("❌ Error al enviar correo a %s: %s", receptor_email, str(e))
        raise self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)  # 3 intentos, 30s entre cada uno
def enviar_whatsapp_async(self, telefono, mensaje):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=mensaje,
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{telefono}",
        )

        logger.info(f"✅ WhatsApp enviado a {telefono}: SID={message.sid}")

    except Exception as e:
        logger.error(f"❌ Error enviando WhatsApp a {telefono}: {e}")
        raise self.retry(exc=e)

@shared_task
def enviar_correo_valoracion_async(asunto, cuerpo, destinatario):
    send_mail(
        subject=asunto,
        message=cuerpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[destinatario],
        fail_silently=False,
    )
