# usuarios/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mensaje,ValoracionTerapia
from .tasks import enviar_correo_async, enviar_whatsapp_async, enviar_correo_valoracion_async
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags

from .models import Cita
from datetime import timedelta



@receiver(post_save, sender=Cita)
def crear_citas_recurrentes(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.tipo_cita != 'terapeutica':
        return

    if not instance.dias_recurrentes or not instance.fecha_fin:
        return

    dias = instance.dias_recurrentes.lower().split(",")
    dias = [dia.strip() for dia in dias]
    fecha_actual = instance.fecha
    fecha_fin = instance.fecha_fin

    dias_map = {
        "lunes": 0,
        "martes": 1,
        "miercoles": 2,
        "miércoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sabado": 5,
        "sábado": 5,
        "domingo": 6,
    }

    dias_numeros = [dias_map[dia] for dia in dias if dia in dias_map]

    fecha_iter = fecha_actual + timedelta(days=1)
    while fecha_iter <= fecha_fin:
        if fecha_iter.weekday() in dias_numeros:
            conflicto_terapeuta = Cita.objects.filter(
                profile_terapeuta=instance.profile_terapeuta,
                fecha=fecha_iter,
                hora=instance.hora,
            ).exists()

            conflicto_paciente = Cita.objects.filter(
                profile=instance.profile,
                fecha=fecha_iter,
                hora=instance.hora,
            ).exists()

            if not conflicto_terapeuta and not conflicto_paciente:
                Cita.objects.create(
                    sucursal=instance.sucursal,
                    tipo_cita=instance.tipo_cita,
                    creador=instance.creador,
                    destinatario=instance.destinatario,
                    profile=instance.profile,
                    profile_terapeuta=instance.profile_terapeuta,
                    nombre_paciente=instance.nombre_paciente,
                    fecha=fecha_iter,
                    hora=instance.hora,
                    motivo=instance.motivo,
                    notas=instance.notas,
                    pendiente=instance.pendiente,
                    confirmada=False,
                    cancelada=False,
                )
        fecha_iter += timedelta(days=1)


@receiver(post_save, sender=Mensaje)
def manejar_mensaje(sender, instance, created, **kwargs):
    if not created:
        return

    asunto = instance.asunto
    cuerpo = strip_tags(instance.cuerpo or "")
    emisor_username = instance.emisor.user.username if instance.emisor and instance.emisor.user else "Administrador"

    # 🎯 Casos dirigidos al receptor (paciente)
    if asunto in ["Consulta", "Solicitud de pago vencido", "Informativo"]:
        receptor = instance.receptor
        if receptor:
            telefono = str(receptor.telefono) if receptor.telefono else None
            email = receptor.email if receptor.email else None

            if asunto == "Solicitud de pago vencido":
                if email:
                    enviar_correo_async.delay(emisor_username, email, asunto, cuerpo)
                if telefono:
                    enviar_whatsapp_async.delay(telefono, f"⚠️ Solicitud de pago pendiente:\n{cuerpo}")

            elif asunto == "Consulta":
                if telefono:
                    enviar_whatsapp_async.delay(telefono, f"❓ Consulta médica:\n{cuerpo}")

            elif asunto == "Informativo":
                if telefono:
                    enviar_whatsapp_async.delay(telefono, f"📢 Mensaje informativo:\n{cuerpo}")

    # 🧠 Casos dirigidos al terapeuta
    elif asunto == "Terapéutico":
        terapeuta = instance.perfil_terapeuta
        if terapeuta and terapeuta.user:
            telefono = str(terapeuta.telefono) if terapeuta.telefono else None
            email = terapeuta.user.email if terapeuta.user.email else None

            if email:
                enviar_correo_async.delay(emisor_username, email, asunto, cuerpo)
            if telefono:
                enviar_whatsapp_async.delay(telefono, f"📘 Tarea terapéutica:\n{cuerpo}")

    # 🏛️ Casos administrativos
    elif asunto in [
        "Solicitud de Certificado Médico",
        "Reclamo del servicio Médico",
        "Cancelación del servicio Médico"
    ]:
        administrativo = instance.perfil_administrativo
        if administrativo and administrativo.user:
            telefono = str(administrativo.telefono) if administrativo.telefono else None
            email = administrativo.user.email if administrativo.user.email else None

            if email:
                enviar_correo_async.delay(emisor_username, email, asunto, cuerpo)
            if telefono:
                enviar_whatsapp_async.delay(telefono, f"📑 Notificación administrativa:\n{cuerpo}")

    # 🏫 Casos institucionales (extensible)
    elif instance.institucion_a_cargo and instance.institucion_a_cargo.usuario:
        institucion = instance.institucion_a_cargo
        telefono = str(institucion.telefono) if institucion.telefono else None
        email = institucion.usuario.email if institucion.usuario.email else None

        if email:
            enviar_correo_async.delay(emisor_username, email, asunto, cuerpo)
        if telefono:
            enviar_whatsapp_async.delay(telefono, f"🏛️ Mensaje institucional:\n{cuerpo}")



@receiver(post_save, sender=ValoracionTerapia)
def notificar_valoracion(sender, instance, created, **kwargs):
    if not created:
        return

    institucion = instance.institucion
    correo_destino = institucion.mail_institucion_general if institucion else None

    if not correo_destino:
        return  # No enviar correo si la institución no tiene un email

    asunto = f"Nueva Valoración Terapéutica - {instance.nombre}"

    archivo_link = ""
    if instance.archivo_adjunto:
        archivo_url = instance.archivo_adjunto.url
        archivo_link = f"{settings.SITE_DOMAIN}{archivo_url}"

    cuerpo = f"""
    Estimado equipo de {institucion.nombre},

    Se ha registrado una nueva valoración terapéutica asociada a su institución.

    🧑 Paciente:
    - Nombre: {instance.nombre}
    - Fecha de Nacimiento: {instance.fecha_nacimiento}
    - Edad: {instance.edad}
    - Servicio: {instance.servicio}
    - Fecha de Valoración: {instance.fecha_valoracion}
    - Diagnóstico: {instance.diagnostico or 'No ingresado'}
    - Recibe Asesoría: {'Sí' if instance.recibe_asesoria else 'No'}

    📎 Observaciones:
    {instance.observaciones or 'Sin observaciones'}

    {"📥 Archivo Adjunto: " + archivo_link if archivo_link else "No se adjuntó archivo."}

    Este es un mensaje automático generado por el sistema Meddes.

    Atentamente,
    Equipo Meddes@
    """

    enviar_correo_valoracion_async.delay(asunto, cuerpo, correo_destino)

