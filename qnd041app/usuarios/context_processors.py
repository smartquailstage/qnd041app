from datetime import timedelta, date
from django.utils import timezone
from django.db.models import Count
from .models import pagos, tareas, Cita, Mensaje, Profile,  InformesTerapeuticos, AdministrativeProfile
from django.db.models import Q
from collections import defaultdict
from datetime import datetime
from django.utils.timezone import localtime, is_naive, make_aware
from django.db.models import FileField, ImageField
from django.shortcuts import get_object_or_404



def ultima_cita(request):
    """
    Procesador de contexto que obtiene la primera cita pendiente del usuario autenticado,
    filtrando por su perfil, sin lanzar errores si no existe.
    """
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile is None:
            return {'ultima_cita': None}

        # Obtener la primera cita pendiente (no confirmada ni cancelada)
        ultima_cita = (
            Cita.objects
            .filter(profile=profile, pendiente=True, confirmada=False, cancelada=False)
            .order_by('fecha', 'hora')
            .first()
        )

        return {'ultima_cita': ultima_cita}

    return {}


def ultima_tarea(request):
    """
    Obtener la última tarea usando profile, sin error si no existe el profile.
    """
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()  # devuelve None si no existe
        if profile is None:
            return {'ultima_tarea': None}
        ultima_tarea = tareas.objects.filter(profile=profile).order_by('-fecha_envio', '-fecha_entrega').first()
        return {'ultima_tarea': ultima_tarea}
    return {}


def citas_context(request):
    if request.user.is_authenticated:
        citas = Cita.objects.filter(destinatario=request.user).select_related('creador', 'destinatario').order_by('-fecha')[:20]

        agenda = defaultdict(lambda: defaultdict(list))
        fechas_unicas = set()
        horas_unicas = set()

        for cita in citas:
            if not cita.fecha:
                continue

            fecha = cita.fecha
            if is_naive(fecha):
                fecha = make_aware(fecha)

            fecha_local = localtime(fecha)
            dia_str = fecha_local.strftime("%Y-%m-%d")
            hora = fecha_local.strftime("%H:00")

            if fecha_local.weekday() >= 5:
                continue

            if not (9 <= fecha_local.hour <= 22):
                continue

            creador = cita.creador
            destinatario = cita.destinatario

            creador_nombre = (
                creador.get_full_name() if creador and hasattr(creador, 'get_full_name')
                else getattr(creador, 'username', 'Sin creador')
            )

            destinatario_nombre = (
                destinatario.get_full_name() if destinatario and hasattr(destinatario, 'get_full_name')
                else getattr(destinatario, 'username', 'Sin destinatario')
            )

            agenda[dia_str][hora].append({
                "id": cita.id,
                "motivo": cita.motivo or "Sin motivo",
                "creador": creador_nombre,
                "destinatario": destinatario_nombre,
                "estado": cita.estado,  # usa la propiedad
                "tipo_cita": cita.get_tipo_cita_display() if cita.tipo_cita else "Sin tipo"
            })

            fechas_unicas.add(dia_str)
            horas_unicas.add(hora)

        dias_date = [datetime.strptime(d, "%Y-%m-%d").date() for d in fechas_unicas]

        return {
            'agenda': agenda,
            'dias': sorted(dias_date),
            'horas': sorted(horas_unicas),
            'dias_str_map': {datetime.strptime(d, "%Y-%m-%d").date(): d for d in fechas_unicas}
        }

    return {}







def user_profile_data(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile  # o Profile.objects.get(user=request.user)
            return {
                'profile_photo': profile.photo.url if profile.photo else None,
                'name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        except:
            return {
                'profile_photo': None,
                'name': request.user.first_name,
                'last_name': request.user.last_name,
            }
    return {}


def mensajes_leidos_processor(request):
    mensajes_leidos = []
    if request.user.is_authenticated:
        try:
            perfil = Profile.objects.get(user=request.user)
            mensajes_leidos = Mensaje.objects.filter(
                receptor=perfil,
                leido=True
            ).exclude(emisor__user=request.user).order_by('-fecha_envio')
        except Profile.DoesNotExist:
            # Si el perfil no existe, devolvemos lista vacía
            mensajes_leidos = []

    return {
        'mensajes_recibidos': mensajes_leidos
    }


def mensajes_nuevos_processor(request):
    count = 0
    mensajes = []
    conteo_por_emisor = []

    if request.user.is_authenticated:
        hoy = date.today()
        desde = hoy - timedelta(days=7)

        try:
            perfil_admin = AdministrativeProfile.objects.get(user=request.user)

            mensajes_queryset = Mensaje.objects.filter(
                perfil_administrativo=perfil_admin,
                leido=False,
                fecha_envio__date__gte=desde
            ).order_by('-fecha_envio')

            count = mensajes_queryset.count()
            mensajes = mensajes_queryset[:6]

            conteo_por_emisor = (
                mensajes_queryset
                .values(
                    'emisor__id',
                    'emisor__user__username',
                )
                .annotate(total=Count('id'))
                .order_by('-total')
            )
        except AdministrativeProfile.DoesNotExist:
            pass

    return {
        'mensajes_nuevos': count,
        'mensajes_recientes': mensajes,
        'conteo_por_emisor': conteo_por_emisor
    }




def datos_panel_usuario(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user

    # Obtener el perfil asociado
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = None

    # Estado de pago
    try:
        ultimo_pago = pagos.objects.filter(profile__user=user).latest('created_at')
        if ultimo_pago.al_dia:
            estado_de_pago = "Al día"
        elif ultimo_pago.pendiente:
            estado_de_pago = "Pendiente"
        elif ultimo_pago.vencido:
            estado_de_pago = "Vencido"
        else:
            estado_de_pago = "Sin estado"
    except pagos.DoesNotExist:
        estado_de_pago = "No disponible"

    # Cantidad de mensajes recibidos — ahora filtrando por perfil, no por usuario
    if profile:
        cantidad_mensajes_recibidos = Mensaje.objects.filter(receptor=profile).count()
    else:
        cantidad_mensajes_recibidos = 0

    # Tareas realizadas por el paciente
    cantidad_terapias_realizadas = tareas.objects.filter(profile__user=user, tarea_realizada=True).count()

    # Citas confirmadas para el usuario
    if profile:
        citas_realizadas = Cita.objects.filter(profile=profile, confirmada=True).count()
    else:
        citas_realizadas = 0

    # Determinar estado general de la terapia desde el modelo Profile
    estado_terapia = "No definido"
    if profile:
        if profile.es_en_terapia:
            estado_terapia = "En terapia"
        elif profile.es_retirado:
            estado_terapia = "Retirado"
        elif profile.es_pausa:
            estado_terapia = "En pausa"
        elif profile.es_alta:
            estado_terapia = "Alta"

    return {
        'estado_de_pago': estado_de_pago,
        'cantidad_mensajes_recibidos': cantidad_mensajes_recibidos,
        'cantidad_terapias_realizadas': cantidad_terapias_realizadas,
        'citas_realizadas': citas_realizadas,
        'estado_terapia': estado_terapia,
    }



def citas_context(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return {}  # No se incluye nada si no hay perfil

        citas = Cita.objects.filter(profile=profile)

        return {
            'citas_todas': citas,
            'citas_confirmadas_count': citas.filter(confirmada=True).count(),
            'citas_pendientes_count': citas.filter(pendiente=True, confirmada=False, cancelada=False).count(),
            'citas_canceladas_count': citas.filter(cancelada=True).count(),
            'proximas_citas': citas.filter(fecha__gte=timezone.now()).order_by('fecha')[:5]
        }

    return {}


def tareas_context(request):
    if request.user.is_authenticated:
        # Tareas asignadas al usuario
        tareas_nuevas_qs = tareas.objects.filter(
            profile__user=request.user,
            actividad_realizada=False
        ).order_by('-fecha_envio')

        tareas_count = tareas_nuevas_qs.count()
        tareas_detalle = tareas_nuevas_qs[:5]  # Para usar en notificaciones o sidebar

        # Estadísticas adicionales
        actividades_nuevas = tareas.objects.filter(
            profile__user=request.user,
            envio_tarea=True,
            actividad_realizada=False
        ).count()

        actividades_realizadas = tareas.objects.filter(
            profile__user=request.user,
            envio_tarea=True,
            actividad_realizada=True
        ).count()

        tareas_sin_alta = tareas.objects.filter(
            profile__user=request.user,
            actividad_realizada=False
        ).count()

        tareas_con_alta = tareas.objects.filter(
            profile__user=request.user,
            actividad_realizada=True
        ).count()

        return {
            'tareas_nuevas_count': tareas_count,
            'tareas_detalle': tareas_detalle,
            'actividades_nuevas': actividades_nuevas,
            'actividades_realizadas': actividades_realizadas,
            'tareas_nuevas': tareas_sin_alta,
            'tareas_con_alta': tareas_con_alta,
        }

    return {}


def pagos_context(request):
    if request.user.is_authenticated:
        pagos_pendientes = pagos.objects.filter(profile__user=request.user, pendiente=True)
        pagos_vencidos = pagos.objects.filter(profile__user=request.user, vencido=True)

        total_pendientes = pagos_pendientes.count()
        total_vencidos = pagos_vencidos.count()
        total_pagos_nuevos = total_pendientes + total_vencidos

        return {
            'pagos_pendientes_notif': pagos_pendientes,
            'pagos_vencidos_notif': pagos_vencidos,
            'total_pendientes': total_pendientes,
            'total_vencidos': total_vencidos,
            'total_pagos_nuevos': total_pagos_nuevos,
        }
    return {}





def get_upload_fields(profile_instance):
    upload_fields = {}

    # Archivos del modelo Profile (campos FileField / ImageField)
    for field in profile_instance._meta.get_fields():
        if isinstance(field, (FileField, ImageField)):
            value = getattr(profile_instance, field.name)
            if value and hasattr(value, 'url'):
                label = field.verbose_name or field.name.replace('_', ' ').capitalize()
                upload_fields[label] = value.url

    # Archivos del modelo relacionado InformesTerapeuticos
    for informe in profile_instance.archivos_adjuntos.all().order_by('-fecha_creado'):
        upload_fields[f"🗂 {informe.titulo}"] = informe.archivo.url if informe.archivo else None

    return upload_fields

def profile_uploads_context(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.filter(user=request.user)
        if not profiles.exists():
            return {}

        profile = profiles.first()
        uploads = get_upload_fields(profile)
        if uploads:
            return {'upload_fields': uploads}
    return {}
