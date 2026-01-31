from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib import admin
from .models import SPDP_ActaDelegado, Regulacion

# -------------------------------
# SPDP_ActaDelegado PDFs
# -------------------------------

def delegado_pdf_link(obj):
    """PDF general DPD"""
    url = reverse('smartbusinesslaw:admin_delegado_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}" target="_blank"><span class="material-symbols-outlined">download</span> Descargar</a>')
delegado_pdf_link.short_description = "CERTIFICADO (DPD)"

def rat_pdf_link(obj):
    """PDF del Registro de Actividades de Tratamiento"""
    url = reverse('smartbusinesslaw:admin_rat_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}" target="_blank"><span class="material-symbols-outlined">download</span>Descarga</a>')
rat_pdf_link.short_description = "CERTIFICADO (RAT)"

def incidente_pdf_link(obj):
    """PDF de Incidentes y Mitigaciones"""
    url = reverse('smartbusinesslaw:admin_incidente_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}" target="_blank"><span class="material-symbols-outlined">download</span>Descarga</a>')
incidente_pdf_link.short_description = "CERTIFICADO (EIPD/DPIA)"



from django.utils import timezone
from django.urls import reverse
from django.utils.safestring import mark_safe


def VENCIMIENTO(obj):
    """
    PDF de Incidentes y Mitigaciones
    Muestra tiempo restante antes de expiración (días, horas, minutos)
    """
    url = reverse('smartbusinesslaw:admin_incidente_pdf', args=[obj.id])

    # ⏳ Cálculo del tiempo restante
    if obj.fecha_expiracion:
        now = timezone.now()
        delta = obj.fecha_expiracion - now

        if delta.total_seconds() > 0:
            dias = delta.days
            horas, remainder = divmod(delta.seconds, 3600)
            minutos = remainder // 60

            tiempo_restante = (
                f"{dias}d {horas}h {minutos}m"
            )
            estado = f"<small style='color:#2e7d32;'>⏳ {tiempo_restante}</small>"
        else:
            estado = "<small style='color:#c62828;'>⛔ EXPIRADO</small>"
    else:
        estado = "<small style='color:#757575;'>— sin fecha —</small>"

    return mark_safe(
        f"""
        {estado}
        """
    )


incidente_pdf_link.short_description = "CERTIFICADO EIPD / DPIA"


# -------------------------------
# Regulacion PDF
# -------------------------------

def regulacion_pdf_link(obj):
    """PDF de la regulación / base legal"""
    url = reverse('smartbusinesslaw:admin_regulacion_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}" target="_blank">Ver PDF</a>')
regulacion_pdf_link.short_description = "PDF"





# ===========================
# SCVS_Estatutos Admin
# ===========================
@admin.register(SCVS_Estatutos)
class SCVS_EstatutosAdmin(ModelAdmin):
    fieldsets = (
        ('Información General', {
            'fields': ('regulacion', 'nombre_empresa', 'fecha_aprobacion', 'notario'),
            'classes': ('unfold', 'tab-general'),
        }),
        ('Archivo', {
            'fields': ('archivo',),
            'classes': ('unfold', 'tab-archivo'),
        }),
    )
    list_display = ('nombre_empresa', 'fecha_aprobacion', 'notario', 'regulacion')
    list_filter = ('fecha_aprobacion', 'regulacion')
    unfold_fieldsets = True

# ===========================
# SPDP_ActaDelegado Admin
# ===========================
@admin.register(SPDP_ActaDelegado)
class SPDP_ActaDelegadoAdmin(ModelAdmin):

    fieldsets = (

        # ---------------------------------------------------
        # 1. DOCUMENTO DEL DELEGADO DE PROTECCIÓN DE DATOS
        # ---------------------------------------------------
        ('Documento del Delegado de Protección de Datos (DPD)', {
            'fields': (
                'regulacion',
                'nombre_delegado',
                'identificacion_delegado',
                'correo_delegado',
                'telefono_delegado',
                'fecha_nombramiento',
                'acto_designacion',
                'tipo_vinculacion',
                'funciones_delegado',
                'declaracion_independencia',
                'declaracion_confidencialidad',
       
            ),
            'classes': ('unfold', 'tab-dpd'),
        }),

        # ---------------------------------------------------
        # 2. REGISTRO DE ACTIVIDADES DE TRATAMIENTO (RAT)
        # ---------------------------------------------------
        ('Registro de Actividades de Tratamiento (RAT)', {
            'fields': (
                'rat_nombre_tratamiento',
                'rat_finalidad',
                'rat_base_legal',
                'rat_categoria_datos',
                'rat_categoria_titulares',
                'rat_categoria_destinatarios',
                'rat_responsable_tratamiento',
                'rat_titular_datos',
                'rat_plazo_conservacion',
                'rat_transferencias_internacionales',
                'rat_pais_transferencia',
                'rat_medidas_tecnicas',
                'rat_medidas_organizativas',
            ),
            'classes': ('unfold', 'tab-rat'),
        }),

        # ---------------------------------------------------
        # 3. REGISTRO DE INCIDENTES Y MITIGACIONES
        # ---------------------------------------------------
        ('Registro de Incidentes de Seguridad y Mitigación', {
            'fields': (
                'incidente_identificacion',
                'incidente_fecha_deteccion',
                'incidente_tipo',
                'incidente_descripcion',
                'incidente_datos_afectados',
                'incidente_titulares_afectados',
                'incidente_riesgo',
                'incidente_notificado_spdp',
                'incidente_fecha_notificacion',
                'incidente_medidas_mitigacion',
                'incidente_medidas_correctivas',
                'incidente_estado',
                'archivo_incidente',
            ),
            'classes': ('unfold', 'tab-incidentes'),
        }),

        # ---------------------------------------------------
        # 4. CONTROL Y OBSERVACIONES
        # ---------------------------------------------------
        ('Control y Observaciones', {
            'fields': (
                'observaciones',
                'fecha_creacion',
                'fecha_actualizacion',
            ),
            'classes': ('unfold', 'tab-control'),
        }),
    )

    # -------------------------
    # Listados
    # -------------------------
    list_display = (
        'nombre_delegado',
        'rat_titular_datos',
        VENCIMIENTO,
        delegado_pdf_link,       # Enlace PDF DPD
        rat_pdf_link,            # Enlace PDF RAT
        incidente_pdf_link, 
        'legalizado_spd',
    )

    list_editable = ['legalizado_spd']

    list_filter = (
        'fecha_nombramiento',
        'rat_transferencias_internacionales',
        'incidente_estado',
        'incidente_notificado_spdp',
        'regulacion',
    )

    search_fields = (
        'nombre_delegado',
        'rat_nombre_tratamiento',
        'incidente_identificacion',
    )

    readonly_fields = (
        'fecha_creacion',
        'fecha_actualizacion',
    )

    unfold_fieldsets = True


# ===========================
# SRI_RUC Admin
# ===========================
@admin.register(SRI_RUC)
class SRI_RUCAdmin(ModelAdmin):
    fieldsets = (
        ('Información RUC', {
            'fields': ('regulacion', 'ruc', 'fecha_emision'),
            'classes': ('unfold', 'tab-general'),
        }),
        ('Archivo', {
            'fields': ('archivo',),
            'classes': ('unfold', 'tab-archivo'),
        }),
    )
    list_display = ('ruc', 'fecha_emision', 'regulacion')
    list_filter = ('fecha_emision', 'regulacion')
    unfold_fieldsets = True

# ===========================
# MT_Contratos Admin
# ===========================
@admin.register(MT_Contratos)
class MT_ContratosAdmin(ModelAdmin):
    fieldsets = (
        ('Información del Contrato', {
            'fields': ('regulacion', 'empleado', 'fecha_inicio', 'fecha_fin', 'tipo_contrato'),
            'classes': ('unfold', 'tab-general'),
        }),
        ('Archivo', {
            'fields': ('archivo',),
            'classes': ('unfold', 'tab-archivo'),
        }),
    )
    list_display = ('empleado', 'tipo_contrato', 'fecha_inicio', 'fecha_fin', 'regulacion')
    list_filter = ('tipo_contrato', 'fecha_inicio', 'regulacion')
    unfold_fieldsets = True

# ===========================
# IESS_Aportes Admin
# ===========================
@admin.register(IESS_Aportes)
class IESS_AportesAdmin(ModelAdmin):
    fieldsets = (
        ('Información Aporte', {
            'fields': ('regulacion', 'empleado', 'periodo', 'monto', 'fecha_pago'),
            'classes': ('unfold', 'tab-general'),
        }),
        ('Archivo', {
            'fields': ('archivo',),
            'classes': ('unfold', 'tab-archivo'),
        }),
    )
    list_display = ('empleado', 'periodo', 'monto', 'fecha_pago', 'regulacion')
    list_filter = ('periodo', 'regulacion')
    unfold_fieldsets = True
