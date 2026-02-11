from django.utils.timezone import now
from usuarios.models import Perfil_Terapeuta
from usuarios.models import prospecion_administrativa
from usuarios.models import Profile
from usuarios.models import Cita, pagos
from usuarios.models import ValoracionTerapia
from usuarios.models import tareas
from usuarios.models import AsistenciaTerapeuta
from django.utils import timezone
from usuarios.models import Mensaje
from usuarios.models import Prospeccion
from smartbusinessanalytics_id.models import EstadoFinanciero




def badge_callback_meddes(request):
    try:
        total = Prospeccion.objects.count()
        return f"{total}"
    except Exception:
        return "0"

def badge_callback_notificaciones(request):
    try:
                # Filtramos los registros conciliados
        registros_conciliados = EstadoFinanciero.objects.filter(conciliado=True).order_by('id')

        # Contamos la cantidad de registros conciliados
        total_registros = registros_conciliados.count()

        # Obtenemos el valor de total_efectivo_bancos del último registro
        ultimo_total_efectivo = registros_conciliados.last().total_efectivo_bancos if total_registros > 0 else 0

        asistencias = {
            "Analisis": total_registros,
            "Total Efectivo Bancos": ultimo_total_efectivo
        }

        resumen = " | ".join(f"{value}" for key, value in asistencias.items())
        return f"{resumen}"

    except Exception:
        return "0"


from django.utils import timezone
from smartbusinessanalytics_id.models import MovimientoFinanciero

def badge_callback_ingresos_egresos(request):
    try:
        hoy = timezone.now().date()

        # Contamos movimientos de hoy
        total_ingresos = MovimientoFinanciero.objects.filter(
            es_ingreso=True,
            fecha_devengo=hoy
        ).count()

        total_egresos = MovimientoFinanciero.objects.filter(
            es_egreso=True,
            fecha_devengo=hoy
        ).count()

        # Diccionario de resultados
        resultados = {
            "Ingresos Hoy": total_ingresos,
            "Egresos Hoy": total_egresos,
        }

        # Formateamos la salida
        resumen = " | ".join(f"{key}: {value}" for key, value in resultados.items())
        return resumen

    except Exception as e:
        # Opcional: loggear el error
        return "0"


from django.utils import timezone

def badge_callback_analisis(request):
    try:
        # Fecha actual
        hoy = timezone.now().date()

        # Obtenemos el último registro conciliado del día de hoy
        ultimo_registro = EstadoFinanciero.objects.filter(
            conciliado=True,
            fecha_inicio=hoy
        ).order_by('fecha_inicio').last()

        # Valor de ingresos del último registro
        total_ingresos_ultimo = (
            float(ultimo_registro.total_ingresos.amount)
            if ultimo_registro and ultimo_registro.total_ingresos
            else 0.0
        )

        # Construimos el diccionario de resultados
        asistencias = {
            "Total Ingresos Último Registro Hoy": total_ingresos_ultimo,
        }

        resumen = " | ".join(f"{value} USD$" for key, value in asistencias.items())
        return resumen

    except Exception as e:
        # Opcional: loggear el error
        return "0"



def badge_callback_asistencias(request):
    try:
        asistencias = {
            "No asistirán": AsistenciaTerapeuta.objects.filter(no_asistire=True).count(),
            "Confirmaron asistencia": AsistenciaTerapeuta.objects.filter(asistire=True).count(),
            
        }

        return " | ".join(f"{value}" for key, value in asistencias.items())

    except Exception:
        return "0"


def badge_callback_tareas(request):
    try:
        conteos = {
            "Asistencia": tareas.objects.filter(asistire=True).count(),
            "Actividad realizada": tareas.objects.filter(actividad_realizada=True).count(),
            "Tarea realizada": tareas.objects.filter(tarea_realizada=True).count(),
        }

        return " | ".join(f"{value}" for key, value in conteos.items())

    except Exception as e:
        return "0"


def badge_callback_valoracion(request):
    try:
        valoraciones = {
            "Convenio": ValoracionTerapia.objects.filter(recibe_asesoria=True).count(),
            "Particular": ValoracionTerapia.objects.filter(proceso_terapia=True).count(),
           
        }

        return " | ".join(f"{value}" for key, value in valoraciones.items())

    except Exception:
        return "0"



def badge_callback_pagos(request):
    try:
        pagos_estado = {
            "vencidos": pagos.objects.filter(vencido=True).count(),
            "pendientes": pagos.objects.filter(pendiente=True).count(),
            "al_dia": pagos.objects.filter(al_dia=True).count(),
            
        }

        return " | ".join(str(value) for value in pagos_estado.values())

    except Exception:
        return "0"



def badge_callback_citas(request):
    try:
        citas = {
            "pendientes": Cita.objects.filter(pendiente=True).count(),
            "canceladas": Cita.objects.filter(cancelada=True).count(),
            "confirmadas": Cita.objects.filter(confirmada=True).count(),
        }

        return " | ".join(str(value) for value in citas.values())

    except Exception:
        return "0"


def badge_callback_terapeutico(request):
        try:
            estados = {
                "Retirado": Profile.objects.filter(es_retirado=True).count(),
                "En Terapia": Profile.objects.filter(es_en_terapia=True).count(),
                "Pausa": Profile.objects.filter(es_pausa=True).count(),
                "Alta": Profile.objects.filter(es_alta=True).count(),
                
            }

            return " | ".join(f"{value}" for key, value in estados.items())

        except Exception:
            return "0"


def badge_callback_prospeccion(request):
    try:
        estados = {
           # "PC": prospecion_administrativa.objects.filter(es_por_contactar=True).count(),
           # "CT": prospecion_administrativa.objects.filter(es_contactado=True).count(),
            "CIT": prospecion_administrativa.objects.filter(es_en_cita=True).count(),
          #  "CNV": prospecion_administrativa.objects.filter(es_convenio_firmado=True).count(),
          #  "CAP": prospecion_administrativa.objects.filter(es_capacitacion=True).count(),
            "VAL": prospecion_administrativa.objects.filter(es_valoracion=True).count(),
           # "TER": prospecion_administrativa.objects.filter(es_en_terapia=True).count(),
          #  "REJ": prospecion_administrativa.objects.filter(es_rechazado=True).count(),
            "FIN": prospecion_administrativa.objects.filter(es_finalizado=True).count(),
           # "INA": prospecion_administrativa.objects.filter(es_inactivo=True).count(),
        }

        # Formato visual compacto
        return " | ".join(f"{value}" for key, value in estados.items())

    except Exception:
        return "0"


        

def badge_color_callback(request):
    try:
        count = Perfil_Terapeuta.objects.filter(activo=True).count()
        if count == 0:
            return "custom-green-success"
        elif count < 2:
            return "custom-green-success"
        else:
            return "custom-green-success"
    except:
        return "custom-green-success"

def badge_callback(request):
    activos = Perfil_Terapeuta.objects.filter(activo=True).count()
    servicio_domicilio = Perfil_Terapeuta.objects.filter(servicio_domicilio=True).count()
    servicio_institucion = Perfil_Terapeuta.objects.filter(servicio_institucion=True).count()
    return f"{activos} | {servicio_domicilio} | {servicio_institucion}"



def dashboard_callback(request, context):
    context.update({
        "sample": "example"
    })
    return context


def environment_callback(request):
    return ["Producción", "danger"]